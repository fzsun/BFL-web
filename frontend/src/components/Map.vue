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
            geocoder: null
    }},
    methods: {
        //Initial retrieval of map
        getMap(){
            console.log("map: ", google.maps)
            this.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 61, lng: -149},
            zoom: 4
            })
            this.geocoder = new google.maps.Geocoder();
        },

        //Add points to map
        addPushpin(){
            var ref = this;
            google.maps.event.addListener(this.map, 'click', function(event) {
                 var farmname = prompt("Farm Name", "Farm");
                 ref.placeMarker(event.latLng, farmname);
            });
        },
        placeMarker(location, farmname) {
            var marker = new google.maps.Marker({
                position: location,
                map: this.map,
                title: farmname
            });
            this.farms[this.farmsCounter] = {name: farmname,
                                             latitude: location.lat(),
                                             longitude: location.lng()}
            this.farmsCounter = this.farmsCounter + 1;
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
//            var address = document.getElementById("address").value;
//            main.get('geocode?q=' + address).then(response =>  console.log(response.data));
        },


        //Get Locations
        locations : function(){
            var locations = "Locations: </br>";
            var k;
            for(k = 0; k < this.farmsCounter; k++) {
                locations = locations +
                            this.farms[k].name + ": " +
                            this.farms[k].latitude + " -- " +
                            this.farms[k].longitude + "</br>";
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
