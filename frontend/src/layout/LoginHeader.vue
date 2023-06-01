<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
      <div class="navbar-brand"> <img src="../assets/img/logo.png"> </div>
      <div href="#" class="navbar-brand"> My Money Manager </div>
      <ul class="navbar-nav ml-lg-auto">
        <li class="nav-item">
          <a href="#">
            <router-link to="/accounting" class="nav-link">Accounting</router-link>
          </a>
        </li>
        <li class="nav-item">
          <a href="#">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </a>
        </li>
        <li class="nav-item dropdown">
          <a href="#" class="nav-link" @click="logoutNow()">
            Logout
          </a>
        </li>
      </ul>
    </base-nav>
  </header>
</template>
<script>
  import BaseNav from "@/components/BaseNav";
  import utils from "@/api/utils";
  export default {
    components: {
      BaseNav
    },
    methods: {
      // This function handles the logout process for a user.
      logoutNow() {
        utils.logout({
          userId: Number(window.sessionStorage.getItem('userId'))
        }).then((res) => {
          console.log(res)
          if (res.data.success) {
            sessionStorage.clear();
            this.$router.push({
              path: 'login'
            })
            this.$message({
              message: 'successfully logout!',
              type: 'success'
            })
          }
        })
      }
    }
  };
</script>
<style>

</style>
