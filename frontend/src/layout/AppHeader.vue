<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <div class="navbar-brand"> <img src="../assets/img/logo.png"> </div>
            <div href="#" class="navbar-brand"> My Money Manager </div>
            <ul class="navbar-nav navbar-nav-hover ml-auto">
              <base-button type="secondary"><router-link to="/login" >Login </router-link></base-button>
              <base-button type="secondary"><router-link to="/register" >Register</router-link></base-button>
              <base-button type="secondary"><router-link to="/about" >About </router-link></base-button>
            </ul>
        </base-nav>
    </header>
</template>
<script>
import BaseNav from "@/components/BaseNav";

export default {
  components: {
    BaseNav
  }
};
</script>
<style>
</style>
