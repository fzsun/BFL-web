<template>
  <body>
    <div id="map"></div>
    <p id="choice">Current choice: Farm</p>
    <form id="changeType">
        <a href="#" v-on:click="farm_or_ssl">CHANGE</a>
    </form>
    </br>
    </br>
    <form id="refineryFormLatLong">
        <label>Location</label>
        <input id="farmnameLatLon" type="text" placeholder="Farm">
        <input id="latInput" type="number" placeholder="Lat">
        <input id="lonInput" type="number" placeholder="Lng">
        <a href="#" v-on:click="latlon">SUBMIT</a>
    </form>
    </br>
    </br>
    <form id="refineryFormAddress">
        <label>Location</label>
        <input id="farmnameAddress" type="text" placeholder="Farm">
        <input id="address" type="text" placeholder="Address">
        <a href="#" v-on:click="address">SUBMIT</a>
    </form>
    </br>
    </br>
    <form id="getLocations">
        <a href="#" v-on:click="locations">Print Locations</a>
    </form>
    <p id="locations"></p>
  </body>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Map',
    data() {
        return {
            //0 = farm, 1 = ssl, 2 = refinery
            type: 0,
			      name: 'Farm',
            msg: 'BFL Map',
            refinery: null,
            refineryMarker: null,
            farmsCounter: 0,
            sslCounter: 0,
            farms: [],
            ssls: [],
            farmMarkers: [],
            sslMarkers: []
    }},
    methods: {
        farm_or_ssl : function() {
            this.type = (this.type + 1) % 3;

			if (this.type == 2) this.name = "Refinery"
            else if (this.type == 1) this.name = "SSL";
            else this.name = "Farm";

			document.getElementById("choice").innerHTML = "Current choice: " + this.name;
            document.getElementById("farmnameLatLon").placeholder = this.name;
            document.getElementById("farmnameAddress").placeholder = this.name;
        },

        //Initial retrieval of map
        getMap(){
            this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 37.22904237824045, lng: -80.41982042804534},
            zoom: 16
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
			if (this.type == 2) {
				if (this.refinery != null) {
					this.refineryMarker.setMap(null);
				}
				var marker = new google.maps.Marker({
                    position: location,
                    map: this.map,
                    title: name,
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
            } else if (this.type == 1) {
                var marker = new google.maps.Marker({
                    position: location,
                    map: this.map,
                    title: name,
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
                    title: name,
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
        latlon : function(){
            var lat = document.getElementById("latInput").value;
            var lon = document.getElementById("lonInput").value;
            var farmname = document.getElementById("farmnameLatLon").value;
            var myLatlng = new google.maps.LatLng(lat, lon);
            this.placeMarker(myLatlng, farmname);
        },
        address : function() {
            var address = document.getElementById("address").value;
            var farmname = document.getElementById("farmnameAddress").value;
            var url = 'https://api.geocod.io/v1.3/geocode?' +
                      'q=' + address +
                      '&api_key=' + '57cf5c27cf057777f7fd555f33f3b56d77f5da5';

            var result = axios
                .get(url)
                .then(response => {
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
                    farmname);
            });
        },

        //Print Locations to website
        locations : function() {
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
        submitLocations : function() {
            var filteredFarm = this.farms.filter(function (el) {
                return el != null;
            });
            var filteredSSL = this.ssls.filter(function (el) {
                return el != null;
            });

            if (this.refinery == null) return "Refinery Missing";

            var mapInfo = {};
            mapInfo.refinery_location =
              [this.refinery.latitude, this.refinery.longitude];
            mapInfo.mode = "coordintates";
            mapInfo.Coord_f = {};
            mapInfo.Coord_s = {};
            var k;
            for (k = 0; k < filteredFarm.length; k++) {
              mapInfo.Coord_f[k] =
                [filteredFarm[k].latitude, filteredFarm[k].longitude];
            }
            for (k = 0; k < filteredSSL.length; k++) {
              mapInfo.Coord_s[k] =
                [filteredSSL[k].latitude, filteredSSL[k].longitude];
            }
            return mapInfo;
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
    height: 500px;
    width: 75%;
}
</style>
