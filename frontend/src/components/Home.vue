<template>
<div>
    <section class="hero  is-light is-bold">
    <div class="hero-body">
        <div class="container">
        <h1 class="title">
            Biomass Feedstock Logistics
        </h1>
        <h2 class="subtitle">
            Some introduction about team. 
        </h2>
        <a class="button is-primary" href="/team/">View More</a>
        </div>
    </div>
    </section>

    <div class="columns">

    <div class="column is-4">
        <div class="card">
        <div class="card-image">
            <figure class="image is-3by2">
            <img src="%% url_for('static', filename='images/s-bfls.jpg')%%" alt="Placeholder image">
            </figure>
        </div>
        <div class="card-content">
            <p class="title">Sorghum BFLS</p>
            <p>A decision support tool for optimal design of sorghum biomass feedstock supply chains.</p>
        </div>
        <div class="card-content is-bottom">
            <router-link class="button is-primary is-fullwidth" :to="{ name: 'S_BFLS'}">View</router-link>
        </div>
        </div>
    </div>

    </div>
</div>
</template> 