<template>
  <body>
    <div id="map"></div>
    <form id="refineryForm">
        <label>Refinery Location</label>
        <input id="latInput" type="number" placeholder="Lat">
        <input id="lngInput" type="number" placeholder="Lng">
        <input type="button" onclick="formSubmit()" value="Submit">
    </form>
  </body>  
</template>

<script>
export default {
  name: 'hello',
  data() {
    return {
      msg: 'Hello world'
    }},
  methods: {
      getMap(){
        console.log("map: ", google.maps)
        this.map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 61, lng: -149},
        zoom: 4
        })
      }
  },
  mounted: function() {
      this.getMap();
  }
};
</script>

<style>
#map {
    height: 500px;
    width: 75%;
}
</style>
