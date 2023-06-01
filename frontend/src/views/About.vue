<template>
  <div class="profile-page">
    <section class="overall">
      <div class="col d-flex justify-content-center" id="info">
        <h1>My Money Manager:</h1>
        <img class="rounded-circle" :src="rightArrow" alt="right arrow">
        <h1>Track your expenses</h1>
        <img class="rounded-circle" :src="rightArrow" alt="right arrow">
        <h1>Visualise your spending</h1>
        <img class="rounded-circle" :src="rightArrow" alt="right arrow">
        <h1>Gain control over your finances!</h1>
      </div>
      <div class="row">
        <card shadow class="card-profile mt--100" no-body id="main-card">
          <div class="about">
            <!-- Need to change the text below -->
            <p>
              Manage your finances with My Money Manager.<br> As a user of My Money Manager, you can add expenses and set an overall monthly budget.<br> Create an account and start managing your expenses today!
            </p>
          </div>
        </card>
      </div>
    </section>
    <div class="shape shape-style-1 shape-primary shape-skew alpha-4"></div>
    <br />
    <!-- </card> -->
  </div>
  <!-- </div> -->
  <!-- </div> -->
</template>
<script>
  // import Modal from "@/components/Modal.vue";
  import rightArrow from "../assets/img/right-arrow.png";
  export default {
    components: {},
    data() {
      return {
        rightArrow: rightArrow,
      }
    },
  };
</script>
<style scoped>
h1{
  color: white
  
}
  #profile-section {
    gap: 30px;
  }
  .overall {
    padding-bottom: 600px;
    margin-bottom: 10%;
    height: 200px;
  }
  #main-card {
    /* height: 700px; */
    height: 50%;
    width: 500px;
    padding: 20px;
    max-width: 100%;
    margin: auto;
  }
  .col {
    display: table-cell;
  }
  .row {
    margin-top: 300px;
  }
  .about {
    margin: 0px;
  }
  .rounded-circle {
    border: 20px;
    padding: 20px;
    width: 100px;
    height: 100px;
  }
  #titles {
    margin-left: 20px;
  }
  .display-3,
  .display-4 {
    text-align: center;
    margin-bottom: 0px;
  }
  .profile-page {
    background-image: url("../assets/img/bg-test.png");
    height: 800px;
    background-position: center;
    /* Center the image */
    background-repeat: no-repeat;
    /* Do not repeat the image */
    background-size: cover;
    /* Resize the background image to cover the entire container */
  }
  .profile-page .card-profile {
    margin-top: -550px;
  }
  #funds {
    /* display: inline; */
    margin-right: 20px;
  }
  #info {
    margin: auto;
    padding-top: 200px;
    justify-content: center;
  }
  p {
    padding: 10px;
    text-align: center;
    /* font-size: larger; */
  }
</style>
  