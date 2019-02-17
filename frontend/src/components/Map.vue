<template>
  <body>
    <!-- <div id="map"></div>
    <form id="refineryForm">
        <label>Refinery Location</label>
        <input id="latInput" type="number" placeholder="Lat">
        <input id="lngInput" type="number" placeholder="Lng">
        <input type="button" onclick="formSubmit()" value="Submit">
    </form>
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCsjUcVoOYO7m30tvBJlCl-MZrlHAECmkE&callback=initMap"
    type="text/javascript"></script> -->
    </body>  
</template>

<script>
import gmapsInit from '../utils/gmaps';

export default {
  name: 'App',
  async mounted() {
    try {
      const google = await gmapsInit();
      const geocoder = new google.maps.Geocoder();
      const map = new google.maps.Map(this.$el);

      geocoder.geocode({ address: 'Austria' }, (results, status) => {
        if (status !== 'OK' || !results[0]) {
          throw new Error(status);
        }

        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);
      });
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style>
/* #map {
    height: 500px;
    width: 75%;
} */
</style>
