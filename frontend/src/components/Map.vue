<template>
  <body class="wrapper">
    <div class="mapDescription">
        <div class="is-size-4 floatLeft">Create Network</div>
        <div class="floatLeft is-size-5">Click map to place <b>{{name}}</b></div>
        <div class="control is-size-5">
            <label class="container">Refinery
                <input
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="Refinery"
                >
                <span class="checkmark"></span>
            </label>
            <label class="container">Farm
                <input 
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="Farm"
                >
                <span class="checkmark"></span>
            </label>
            <label class="container">SSL
                <input 
                    v-model="name" 
                    type="radio" 
                    name="radio" 
                    value="SSL"
                >
                <span class="checkmark"></span>
            </label>
        </div>
        <!-- <form id="refineryFormLatLong">
            <label>Location</label>
            <input id="farmnameLatLon" type="text" placeholder="Farm">
            <input id="latInput" type="number" placeholder="Lat">
            <input id="lonInput" type="number" placeholder="Lng">
            <a href="#" v-on:click="latlon">SUBMIT</a>
        </form> -->
        <form id="refineryFormAddress" class="is-size-5 paddingRight">
            <br>
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
                <button v-if="this.name != refinery" class="button is-info">Add</button>
                <button class="button is-primary" v-on:click="submitAddress">Submit</button>
            </span>
        </form>
    </div>
    <div id="map" class="map"></div>
    <form id="getLocations">
        <a href="#" v-on:click="locations">Print Locations</a>
    </form>
    <button v-on:click="addRoutes" class="button">Add Route</button>
    <p id="locations"></p>
  </body>
</template>

<script>
import axios from 'axios'

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
                ref.placeMarker(event.latLng, typeName);
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
                    label: name,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                    }
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
                    label: name,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                    }
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
                    label: name,
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
                    }
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
            // var address = document.getElementById("address").value;
            // var farmname = document.getElementById("farmnameAddress").value;
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
                ref.placeMarker(
                    new google.maps.LatLng(address_lat, address_lng),
                    addressName);
            });
        },

        //Print Locations to website
        locations() {
            var locations = "Locations: </br>";
            var k;
            for(k = 0; k < this.farmsCounter; k++) {
                if (this.farms[k] != null) {
                    locations = locations +
                                this.farms[k].name + ": " +
                                this.farms[k].latitude + " -- " +
                                this.farms[k].longitude + "</br>";
                }
            }
            locations = locations + "SSL Locations: </br>";
            for(k = 0; k < this.sslCounter; k++) {
                if (this.ssls[k] != null) {
                    locations = locations +
                                this.ssls[k].name + ": " +
                                this.ssls[k].latitude + " -- " +
                                this.ssls[k].longitude + "</br>";
                }
            }
			locations = locations + "Refinery: </br>";
			if (this.refinery != null) {
				locations = locations +
              	            this.refinery.name + ": " +
                            this.refinery.latitude + " -- " +
                            this.refinery.longitude + "</br>";
			}
            document.getElementById("locations").innerHTML = locations;
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
            console.log("child", mapInfo)
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

        flightPath.setMap(this.map)
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
    height: 400px;
    width: 100%;
}

.map {
    grid-area: map;
}

.mapDescription {
    grid-area: mapDescription;
}

.wrapper {
    display: grid;
    grid-template-columns: 1fr 2fr;
    grid-template-rows: auto;
    grid-template-areas: "mapDescription map"
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
