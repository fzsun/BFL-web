<template>
<div>
    <section class="hero is-light is-bold">
        <div class="hero-body">
            <div class="container">
            <h1 class="title">
                Biomass Feedstock Logistics
            </h1>
            <h2 class="subtitle">
                Some introduction about team.
            </h2>
            <router-link class="button is-primary" to="/about">View More</router-link>
            </div>
        </div>
    </section>

    <div class="section columns">

    <div class="column is-4">
        <div class="card">
        <div class="card-image">
            <figure class="image is-3by2">
            <img src="../assets/images/s-bfls.jpg" alt="Placeholder image">
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
