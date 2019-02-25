<template>
  <body>
    <div id="map"></div>
    <form id="refineryFormLatLong">
        <label>Refinery Location</label>
        <input id="farmnameLatLon" type="text" placeholder="Farm">
        <input id="latInput" type="number" placeholder="Lat">
        <input id="lonInput" type="number" placeholder="Lng">
        <a href="#" v-on:click="latlon">SUBMIT</a>
    </form>
    <form id="refineryFormAddress">
        <label>Refinery Location</label>
        <input id="farmnameLatLon" type="text" placeholder="Farm">
        <input id="address" type="text" placeholder="Address">
        <a href="#" v-on:click="address">SUBMIT</a>
    </form>
    <form id="getLocations">
        <a href="#" v-on:click="locations">SUBMIT</a>
    </form>
    <p id="locations"></p>
  </body>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Google Maps',
    data() {
        return {
            msg: 'BFL Map',
            centerLat: 0,
            centerLon: 0,
            farmsCounter: 0,
            farms: [],
            storages: [],
            markers: []
    }},
    methods: {
        //Initial retrieval of map
        getMap(){
            this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 61, lng: -149},
            zoom: 4
            })
        },

        //Add points to map
        addPushpin() {
            var ref = this;
            google.maps.event.addListener(this.map, 'click', function(event) {
                 var farmname = prompt("Farm Name", "Farm");
                 ref.placeMarker(event.latLng, farmname);
            });
        },

        placeMarker(location, farmname) {
            var ref = this;
            var marker = new google.maps.Marker({
                position: location,
                map: this.map,
                title: farmname
            });
            var id = this.farmsCounter;
            google.maps.event.addListener(marker, "rightclick", 
                function (point) { ref.delMarker(id) });

            this.markers[this.farmsCounter] = marker;
            this.farms[this.farmsCounter] = {name: farmname,
                                             latitude: location.lat(),
                                             longitude: location.lng()}
            this.farmsCounter = this.farmsCounter + 1;
        },

        delMarker(id) {
            var marker = this.markers[id]; 
            marker.setMap(null);
            this.farms[id] = null;
            this.markers[id] = null;
        },


        //Submit Forms for farm locations
        latlon : function(){
            var lat = document.getElementById("latInput").value;
            var lon = document.getElementById("lonInput").value;
            var farmname = document.getElementById("farmnameLatLon").value;
            var myLatlng = new google.maps.LatLng(lat, lon);
            this.placeMarker(myLatlng, farmname);
        },
        address : function(){
            var address = document.getElementById("address").value;
            var farmname = document.getElementById("farmnameLatLon").value;
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


        //Get Locations
        locations : function(){
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
            document.getElementById("locations").innerHTML = locations;
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
