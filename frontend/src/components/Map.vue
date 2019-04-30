<template>
  <body class="wrapper">
    <div v-if="showing_options" class="mapDescription">
        <div class="is-size-4 floatLeft">1. Create Network</div>
        <div class="is-size-5 floatLeft">Click map to place <b>{{name}}</b></div>
        <div class="field is-grouped nameButtons">
            <div class="control">
                <label class="button red">
                    Refinery
                    <input 
                        type="radio"
                        name="radio" 
                        v-model="name"
                        value="Refinery"
                    >
                </label>
            </div>
            <div class="control">
                <label class="button green">
                    Farm
                    <input 
                        type="radio"
                        name="radio" 
                        v-model="name"
                        value="Farm"
                    >
                </label>
            </div>
            <div class="control">
                <label class="button blue">
                    SSL
                    <input 
                        type="radio"
                        name="radio" 
                        v-model="name"
                        value="SSL"
                    >
                </label>
            </div>
        </div>
        <p class="max-width paddingLeft">
            Place refinery (red pin) as center of 2-layer hub 
            and spoke optimization model. Next place farm locations 
            (green pins). Finally, place potential satellite storage 
            locations (blue pins).
        </p>
        <br>
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
    }},
    props: ['mapInfo'],
    methods: {
        //Initial retrieval of map
        getMap() {
            this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 37.22904237824045, lng: -80.41982042804534},
            zoom: 8
            })
        },

        //Called when user clicks on map to add pin
        addPushpin() {
            var ref = this;
            google.maps.event.addListener(this.map, 'click', function(event) {
                var typeName = prompt(ref.name + " Name", this.name);
                if (typeName !== null) ref.placeMarker(event.latLng, typeName);
            });
        },

        //Place specific marker on map, given the location and name. Give different
        //colors and place in different arrays based on which location type it is
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

        //Delete marker from map and from it's corresponding array
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

        //Put address on map and in array when given a specific address for a location
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
            //This removes all the elements in the map that were deleted (became null)
            //The array has to act like this because if we simply remove elements
            //during deletion on the map, then all the references to each point will
            //be off by 1 element. Instead, we make that element null when removed,
            //and when we send to the backend, we create new arrays without the null elements.
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
        height: 250px;
    }
}

p {
    max-width: 24rem;
}

.clickInstruction {
    display: block;
}

.map {
    flex-grow: 2;
}

.mapDescription {
    grid-area: mapDescription;
    display: flex;
    flex-direction: column;
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

.paddingLeft {
    padding-left: 1rem;
}

.nameButtons input[type="radio"] {
    opacity: 0.0011;
    z-index: 100;
}
.nameButtons .button {
    padding-left: 1.5rem;
}

.red {
    color: red;
}

.blue {
    color: blue;
}

.green {
    color: green;
}
</style>
