<template>
<div>
  <!-- Navigation -->
  <nav class="navbar is-fixed-top is-primary">
    <div class="container">
      <div class="navbar-brand">
        <a class="navbar-item" href="/"><img src="/favicon.ico"></a>
        <span class="navbar-burger burger" data-target="navMenu">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
      <div id="navMenu" class="navbar-menu">
        <div class="navbar-end">
          <a href="/" class="navbar-item">Home</a>
          <a href="/team/" class="navbar-item">Team</a>
          <a href="/contact/" class="navbar-item">Contact</a>
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">Projects</a>
            <div class="navbar-dropdown is-boxed">
              <a class="navbar-item" href="/s-bfls/">Sorghum BFLS</a>
              <a class="navbar-item" href="/tsp/">TSP Example</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <div>
    <router-view></router-view>
  </div>

  <footer class="footer has-background-primary">
    <div class="content has-text-centered has-text-white">
      <p>Copyright &copy; VT BFL Team 2018</p>
    </div>
  </footer>
</div>


</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  padding-top: 60px;
}

.columns {
  flex-wrap: wrap;
}

.card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.is-bottom {
  margin-top: auto;
}
</style>
