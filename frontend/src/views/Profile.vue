<template>
  <div class="profile-page">
    <section class="overall"></section>
    <div class="shape shape-style-1 shape-primary shape-skew alpha-4"></div>
    <div class="container ct-example-row" id="main-container">
      <!-- <div class="container"> -->
      <div class="col d-flex justify-content-center" id="profile-section">
        <card shadow class="card-profile mt--300" no-body id="main-card">
          <br />
          <div class="row">
            <div class="col">
              <h1 class="display-4" id="titles">Profile</h1>
              <br />
              <!-- main profile section -->
              <card shadow class="main-profile">
                <div class="profile"><img class="rounded-circle" :src="profilePic" alt="Profile picture" />
                  <!-- default image from https://icons8.com/icon/set/profile/color  -->
                  <button class="btn btn-info">Change image</button>
                  <input type="file" style="display: none" ref="fileInput" accept="image/*" id="customFile" /></div>
                <h5>Username: </h5>
                {{ username }}
                <h5>Email: </h5>
                {{ email }}
              </card>
            </div>
            <!-- budget section -->
            <div class="col">
              <h1 class="display-4" id="titles">Budget</h1>
              <br />
              <card shadow class="main-profile">
                <base-button block type="primary" class="btn btn-info" id="add-budget" @click="addBudget = true">
                  Set your monthly budget
                </base-button>
                <div class="budget">
                  <h5>
                    Your monthly budget is:
                  </h5>
                  <br>
                  <base-alert id="funds" type="secondary">{{ displayBudget + budget}} </base-alert>
                  <br>
                  <br>
                </div>
                <!-- Modals -->
                <Modal :show.sync="addBudget" body-classes="p-0" modal-classes="modal-dialog-centered modal-sm">
                  <card type="secondary" shadow header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0">
                    <form role="form">
                      <base-input alternative class="mb-3" placeholder="Please enter your budget" addon-left-icon="ni ni-money-coinss" v-model="budgetAmount">
                      </base-input>
                      <div class="text-center">
                        <base-button type="default" class="my-4" @click="updateBudget()">Set budget</base-button>
                      </div>
                    </form>
                  </card>
                </Modal>
                <!-- Expenses and budget -->
                <h5>
                  Current month's total expenses:
                </h5>
                <div class="profile-budget">
                  <base-alert type="secondary">£{{totalExpenses}}</base-alert>
                  <!-- <base-alert id="check-spend" :type="alertType">{{ amount }}</base-alert> -->
                </div>
                <base-alert type="warning" icon="ni ni-bell-55" dismissible v-if="overBudget">
                  <span slot="text"><strong>Warning!</strong> Your total expenses are over your budget!</span>
                </base-alert>
              </card>
            </div>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
  import Modal from "@/components/Modal.vue";
  import profilePicture from "../assets/img/profile-pic.png";
  import utils from "@/api/utils";
  export default {
    components: {
      Modal,
    },
    data() {
      return {
        addBudget: false,
        budget: 0,
        budgetAmount: '',
        profilePic: profilePicture,
        totalExpenses: 0,
        alertType: 'secondary',
        displayBudget: '£',
        username: '',
        email: '',
        userId: window.sessionStorage.getItem('userId'),
        overBudget: false
      }
    },
    mounted() {
      this.getUserInfo()
    },
    methods: {
      getUserInfo() {
        let user = JSON.parse(window.sessionStorage.getItem('user'))
        console.log(user)
        this.username = user.username
        this.email = user.email
        utils.getSummary({
          userId: this.userId
        }).then((res) => {
          console.log(res)
          debugger
          if (res.data.success) {
            this.totalExpenses = res.data.result.total_expense
            // this.budget = 200
            this.budget = res.data.result.budget
            if (this.budget !== 0 && this.totalExpenses > this.budget) {
              this.overBudget = true
            }
          }
        })
      },
      updateBudget() {
        // 
        // this.budget = Number(this.budgetAmount)
        // if (this.budget !== 0 && (0.9 * this.totalExpenses) >= this.budget){
        //       this.overBudget = true
        //     }
        
        utils.setBudget({
          userId: this.userId,
          setBudget: Number(this.budgetAmount)
        }).then((res) => {
          debugger
          console.log(res)
          if (res.data.success) {
            this.$message({
              message: res.data.success,
              type: 'success'
            })
            // this.budget = Number(this.budgetAmount)
            this.getUserInfo()

          }
        })
        this.addBudget = false;
      },
    }
    
  };
</script>
<style scoped>
  .overall {
    background-image: url("../assets/img/bg-test.png");
    padding-bottom: 600px;
    margin-bottom: 5%;
    height: 200px;
    background-position: center;
    /* Center the image */
    background-repeat: no-repeat;
    /* Do not repeat the image */
    background-size: cover;
    /* Resize the background image to cover the entire container */
  }
  #main-card {
    /* height: 700px; */
    height: 70%;
    width: 1200px;
    margin: 0, auto;
    float: none;
    padding: 20px;
    max-width: 100%;
  }
  .main-profile {
    /* height: 100%; */
    padding: 10px;
    margin: 20px;
    max-width: 100%;
  }
  .col {
    display: table-cell;
  }
  .rounded-circle {
    border: 20px;
    padding: 20px;
  }
  #customFile {
    margin: 0px;
    text-align: center;
  }
  #titles {
    margin-left: 20px;
  }
  .display-3,
  .display-4 {
    text-align: center;
    margin-bottom: 0px;
  }
  /* .alert, . {
    width: 350px;
    margin: auto;
    text-align: center;
  } */
  .profile-page .card-profile {
    margin-top: -550px;
  }
  #funds {
    /* display: inline; */
    margin-right: 20px;
  }
  .profile-budget {
    /* margin: 20px,20px;
     */
    display: flex;
    border: 20px;
    column-gap: 10px;
    margin: 20px;
  }
  #add-budget {
    margin: 5px 5px 30px 5px;
  }
  #check-spend {
    text-align: center;
  }
</style>
