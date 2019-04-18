<template>
<div class="columns">

  <div class="column is-3" v-for="team_member in team_members" :key="team_member.name">
    <div class="card">
      <div class="card-image">
        <figure class="image is-1by1">
          <img v-bind:src="team_member.img"/>
        </figure>
      </div>
      <div class="card-content">
        <a class="title is-5" href="https://www.ise.vt.edu/people/faculty/sarin.html">{{ team_member.name}}</a>
      </div>
    </div>
  </div>

</div>
</template>

<script>
/* eslint-disable */
export default {
    data() {
        return {
            team_members: [
                {name: "Dr. Sarin", img: "'../assets/images/subhash-sarin-w.jpg'"},
                {name: "Fangshou", img: "https://picsum.photos/200/300/?random"},
                {name: "Nate", img: "https://picsum.photos/200/300/?random"},
                {name: "Hannah", img: "https://picsum.photos/200/300/?random"},
                {name: "Robert", img: "https://picsum.photos/200/300/?random"},
            ]}
    }
}
</script>

<style>

</style>


