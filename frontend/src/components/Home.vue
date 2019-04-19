<template>
<div>
    <section class="hero is-light is-bold">
        <div class="hero-body">
            <div class="container">
            <h1 class="title">
                Biomass Feedstock Logistics
            </h1>
            <h2 class="subtitle">
                Virginia Tech
            </h2>
            <router-link class="button is-link" to="/s-bfls">Decision Support Tool</router-link>
            <router-link class="button is-link" to="/methodology">Methodolgy</router-link>
            <a class="button is-link" href="https://github.com/fzsun/BFL-web/tree/master">GitHub</a>
            </div>
        </div>
    </section>
    <div class="about">
        <div class="title is-4">Development Team</div>
        <About></About>
    </div>
</div>
</template>
<script>
import About from './About'

export default {
    components: {
        'About': About
    }
}
</script>
<style>
.about {
    margin: 2rem;
}

.title {
    text-align: center;
}

.textLeft {
    text-align: left;
}

.hero-body .button {
    width: 11rem;
    height: 3rem;
    margin: .25rem .5rem;
}
</style>