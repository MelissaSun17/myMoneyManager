<template>
    <footer class="footer has-cards">

        <div class="container">
            <div class="row row-grid align-items-center my-md">
                <div class="col-lg-8">
                    <h3 class="text-primary font-weight-light mb-2" id ="fmessage">Thank you for Using My Money Manager!</h3>
                </div>
            </div>
            <hr>
            <router-link class="nav-link" to="/About" >About Us</router-link>
        </div>
    </footer>
</template>
<script>
export default {
  name: 'app-footer',
  data() {
    return {
    }
  }
};
</script>
<style>
</style>
