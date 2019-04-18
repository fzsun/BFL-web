<template>
<div class="columns is-centered">

  <div class="column is-2" v-for="team_member in team_members" :key="team_member.name">
    <div class="card">
      <div class="card-image">
        <figure class="image is-1by1">
          <img v-bind:src="team_member.img">
        </figure>
      </div>
      <div class="media-content">
        <p class="name">{{team_member.name}}</p>
        <p class="contact">{{team_member.contact}}</p>
      </div>
      <div class="card-content"><p class="content">{{team_member.bio}}</p></div>
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
                {
                  name: "Dr. Subhash Sarin", 
                  img: "../static/subhash-sarin-w.jpg",
                  contact: "sarins@vt.edu",
                  bio: "Dr. Sarin earned his PhD from North Carolina State University in 1978 and continues to contribute to research in production scheduling, sequencing, applied mathematical programming, and in analyzing and designing algorithms for the operational control of manufacturing systems."
                },
                {
                  name: "Fangzhou Sun", 
                  img: "../static/F_Sun.jpg",
                  contact: "fangzhou@vt.edu",
                  bio: "Fagnzhou is a Ph.D. candidate in the Grado Department of Industrial and Systems Engineering at Virginia Tech under the supervision of Professor Subhash C. Sarin. His research interests are in the areas of operations research, supply chain management, and revenue management."
                },
                {
                  name: "Nathan Smith", 
                  img: "../static/nate-smith.jpg", 
                  contact: "nates3@vt.edu", 
                  bio: "Nate is a Industrial and Systems Engineering Major and Green Engineering Minor at Virginia Tech graduating class of 2020. He works as a part time researcher with VTTI doing data analytics experiments and data reduction."
                },
                {
                  name: "Ben Hadinger", 
                  img: "https://picsum.photos/200/300/?random",
                  contact: "bmh@vt.edu",
                  bio: "Ben is a Computer Science student at Virginia Tech, graduating class of 2020. He has worked for Parsons Federal and enjoys teaching people about AI's and good variable naming."
                },
                {
                  name: "Robert Shelton", 
                  img: "../static/robert.jpg",
                  contact: "robes98@vt.edu",
                  bio: "Robert is an Industrial & Systems Engineering student at Virginia Tech, part time web developer with Excella Consulting, and inventory manager for non-profit Micah's Backpack."
                },
            ]}
    }
}
</script>

<style>
.name {
  text-align: center;
  font-size: 24px;
}

.contact {
  text-align: center;
  font-size: 20px;
}

.card-content {
  position: relative;
  z-index: 1;
}

.content {
  position: relative;
  z-index: 4
}

</style>


