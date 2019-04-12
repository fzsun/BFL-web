<template>
  <body class="wrapper">
    <div v-if="showing_options" class="mapDescription">
        <div class="is-size-4 floatLeft">1. Create Network</div><br><br>
        <div class="is-size-5 floatLeft ">Click map to place <b>{{name}}</b></div>
        <div class="control is-size-5">
            <label class="container" style="color: red">Refinery
                <input
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="Refinery"
                >
                <span class="checkmark"></span>
            </label>
            <label class="container" style="color: green">Farm
                <input 
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="Farm"
                >
                <span class="checkmark"></span>
            </label>
            <label class="container" style="color: blue">SSL
                <input 
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="SSL"
                >
                <span class="checkmark"></span>
            </label>
        </div>
        <form id="refineryFormAddress" class="is-size-5 paddingRight addressInput" @submit.prevent="submitAddress()">
            <div class="floatLeft is-size-5">Or enter address</div>
            <input 
                class="input"
                v-model="addressName" 
                type="text" 
                placeholder="Location Name"
            >
            <input 
                class="input"
                v-model="address" 
                type="text" 
                placeholder="Address"
            >
            <span class="floatRight">
                <button class="button is-primary" v-on:click="submitAddress">Add Pin</button>
            </span>
        </form>
    </div>
    <div v-else class="costChart">
		<pie-chart prefix="$" :data="chart_data" width="48%" style="float: left; display:inline"></pie-chart>
        <div class="list is-hoverable" width="40%" style="float: right; display:inline;">
          <p class="list-item">Farm to SSL Cost: ${{chart_info['farm_ssl_trans_cost']}}</p>
          <p class="list-item">SSL to Refinery Cost: ${{chart_info['ssl_ref_trans_cost']}}</p>
          <p class="list-item">Farm Holding Cost: ${{chart_info['farm_holding_cost']}}</p>
          <p class="list-item">SSL Holding Cost: ${{chart_info['ssl_holding_cost']}}</p>
          <p class="list-item">Local Ownership Cost: ${{chart_info['local_ownership']}}</p>
          <p class="list-item">Operation Cost: ${{chart_info['operation_cost']}}</p>
          <p class="list-item is-active">Total Cost: ${{chart_info['total_cost']}}</p>
        </div>
    </div>
    <div id="map" class="map"></div>
  </body>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js'

Vue.use(VueChartkick, {adapter: Chart})
export default {
    data() {
        return {
		    name: 'Refinery',
            msg: 'BFL Map',
            refinery: null,
            refineryMarker: null,
            farmsCounter: 0,
            sslCounter: 0,
            farms: [],
            ssls: [],
            farmMarkers: [],
            sslMarkers: [],
            address: '',
            addressName: '',
            flight_paths: [],
            num_flight_paths: 0,
            showing_options: true,
            chart_data: [],
            chart_info: {},
    }},
    props: ['mapInfo'],
    methods: {
        //Initial retrieval of map
        getMap() {
            this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 37.22904237824045, lng: -80.41982042804534},
            zoom: 4
            })
        },

        //Add points to map
        addPushpin() {
            var ref = this;
            google.maps.event.addListener(this.map, 'click', function(event) {
                var typeName = prompt(ref.name + " Name", this.name);
                // console.log(event.latLng.lat(), event.latLng.lng(), typeName);
                if (typeName !== null) ref.placeMarker(event.latLng, typeName);
            });
        },

        placeMarker(location, locationname) {
            var ref = this;
			if (this.name == 'Refinery') {
				if (this.refinery != null) {
					this.refineryMarker.setMap(null);
				}
				var marker = new google.maps.Marker({
                    position: location,
                    map: this.map,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                    }
                });
                var info_window = new google.maps.InfoWindow({
                    content: locationname
                });
                google.maps.event.addListener(marker, "click", function(e) {
                    info_window.open(map, marker);
                });
				google.maps.event.addListener(marker, "rightclick",
                    function (point) { ref.delMarker(0, "refinery") });
				this.refinery = {name: locationname,
                                 latitude: location.lat(),
                                 longitude: location.lng()};
				this.refineryMarker = marker;
            } else if (this.name == "SSL") {
                var marker = new google.maps.Marker({
                    position: location,
                    map: this.map,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                    }
                });
                var info_window = new google.maps.InfoWindow({
                    content: locationname
                });
                google.maps.event.addListener(marker, "click", function(e) {
                    info_window.open(map, marker);
                });
                var id = this.sslCounter;
                google.maps.event.addListener(marker, "rightclick",
                    function (point) { ref.delMarker(id, "ssl") });

                this.sslMarkers[this.sslCounter] = marker;
                this.ssls[this.sslCounter] = {name: locationname,
                                             latitude: location.lat(),
                                             longitude: location.lng()};
                this.sslCounter = this.sslCounter + 1;
            } else {
                var marker = new google.maps.Marker({
                    position: location,
                    map: this.map,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
                    }
                });
                var info_window = new google.maps.InfoWindow({
                    content: locationname
                });
                google.maps.event.addListener(marker, "click", function(e) {
                    info_window.open(map, marker);
                });
                var id = this.farmsCounter;
                google.maps.event.addListener(marker, "rightclick",
                    function (point) { ref.delMarker(id, "farm") });

                this.farmMarkers[this.farmsCounter] = marker;
                this.farms[this.farmsCounter] = {name: locationname,
                                                 latitude: location.lat(),
                                                 longitude: location.lng()};
                this.farmsCounter = this.farmsCounter + 1;
            }
        },
        
        delMarker(id, type) {
			if (type == "refinery") {
				var marker = this.refineryMarker;
				marker.setMap(null);
				this.refinery = null;
				this.refineryMarker = null;
            } else if (type == "ssl") {
                var marker = this.sslMarkers[id];
                marker.setMap(null);
                this.ssls[id] = null;
                this.sslMarkers[id] = null;
            } else {
                var marker = this.farmMarkers[id];
                marker.setMap(null);
                this.farms[id] = null;
                this.farmMarkers[id] = null;
            }
        },

        //Submit Forms for farm locations (by lat,lng and by address)
        latlon(){
            var lat = document.getElementById("latInput").value;
            var lon = document.getElementById("lonInput").value;
            var farmname = document.getElementById("farmnameLatLon").value;
            var myLatlng = new google.maps.LatLng(lat, lon);
            this.placeMarker(myLatlng, farmname);
        },

        submitAddress() {
            var address = this.address;
            var addressName = this.addressName;
            console.log("address: ", this.address)
            var url = 'https://api.geocod.io/v1.3/geocode?' +
                      'q=' + address +
                      '&api_key=' + '57cf5c27cf057777f7fd555f33f3b56d77f5da5';

            var result = axios
                .get(url)
                .then(response => {
                    this.summary = response.data;
                    return response.data;
                })
                .catch(error => {
                    console.log(error);
                });
            var ref = this;
            result.then(data => {
                var address_lat = data.results[0].location.lat;
                var address_lng = data.results[0].location.lng;
                this.address = '';
                this.addressName = '';
                ref.placeMarker(
                    new google.maps.LatLng(address_lat, address_lng),
                    addressName);
            });
        },

        //Submit locations to background for optimization
        submitLocations() {
            var filteredFarm = this.farms.filter(function (el) {
                return el != null;
            });
            var filteredSSL = this.ssls.filter(function (el) {
                return el != null;
            });
            var mapInfo = {}
            if (this.refinery == null) return "Refinery Missing";

            mapInfo.refinery_location =
              [this.refinery.latitude, this.refinery.longitude];
            mapInfo.mode = "coordinates";
            mapInfo.Coord_f = {};
            mapInfo.Coord_s = {};
            var k;
            for (k = 0; k < filteredFarm.length; k++) {
              mapInfo.Coord_f[k] = {
                  "lat": filteredFarm[k].latitude,
                  "lng": filteredFarm[k].longitude
              }
            }
            for (k = 0; k < filteredSSL.length; k++) {
              mapInfo.Coord_s[k] = {
                  "lat": filteredSSL[k].latitude,
                  "lng": filteredSSL[k].longitude
              }
            }
            this.$emit('Emit stuff', mapInfo)
            return mapInfo;
        },
        addRoutes(routeCoordinates){
        var flightPath = new google.maps.Polyline({
          path: routeCoordinates,
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });
        
        flightPath.setMap(this.map);
        this.flight_paths[this.num_flight_paths++] = flightPath;
        },
        removeRoutes() {
            var i;
            for (i = 0; i < this.num_flight_paths; i++) {
                this.flight_paths[i].setMap(null);
            }
            this.flight_paths = [];
            this.num_flight_paths = 0;
        },

        show_results(data) {
            this.chart_info['farm_ssl_trans_cost'] = Math.round(data.tran_farms_ssl);
            this.chart_info['ssl_ref_trans_cost'] = Math.round(data.tran_ssl_refinery);
            this.chart_info['farm_holding_cost'] = Math.round(data.farm_inventory);
            this.chart_info['ssl_holding_cost'] = Math.round(data.ssl_inventory);
            this.chart_info['local_ownership'] = Math.round(data.loc_own);
            this.chart_info['operation_cost'] = Math.round(data.operation);
            this.chart_info['total_cost'] = Math.round(data.total_ub);

            this.chart_data[0] = ['farm to ssl', Math.round(data.tran_farms_ssl)];
            this.chart_data[1] = ['ssl to refinery', Math.round(data.tran_ssl_refinery)];
            this.chart_data[2] = ['farm holding', Math.round(data.farm_inventory)];
            this.chart_data[3] = ['ssl holding', Math.round(data.ssl_inventory)];
            this.chart_data[4] = ['local ownership', Math.round(data.loc_own)];
            this.chart_data[5] = ['operations', Math.round(data.operation)];
            this.showing_options = false;
        },
        hide_results() {
            this.chart_info = {};
            this.chart_data = [];
            this.showing_options = true;
        }


    },
    mounted: function() {
        this.getMap();
        this.addPushpin();
    }
};
</script>

<style>
#map {
    height: 25rem;
    width: 100%;
    max-width: 50rem;
}

.addressInput {
    max-width: 25rem;
    flex-grow: 1;
}

@media only screen and (max-width: 600) {
    #map {
        height: 300px;
    }
}

.clickInstruction {
    display: block;
}

.map {
    flex-grow: 2;
}

.mapDescription {
    grid-area: mapDescription;
}

.wrapper {
    display: flex;
    flex-wrap: wrap;
    flex-grow: 1;
}

.floatLeft {
    float: left;
}

.floatRight {
    float: right;
}

.paddingRight {
    padding-right: 1rem;
}
</style>
