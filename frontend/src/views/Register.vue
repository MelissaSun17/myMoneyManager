<template>
    <section class="section section-shaped section-lg my-0" style="padding-bottom: 400px;">
        <div class="shape shape-style-0 shape-primary">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="container pt-lg-md">
            <div class="row justify-content-center">
                <div class="col-lg-5">
                    <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                        <template>
                            <div class="text-center text-muted mb-4">
                                <h6>Sign up with email and password</h6>
                            </div>
                            <form role="form">
                                <base-input alternative
                                            class="mb-3"
                                            placeholder="Name"
                                            addon-left-icon="ni ni-hat-3"
                                            v-model="userInfo.username">
                                </base-input>
                                <base-input alternative
                                            class="mb-3"
                                            placeholder="Email"
                                            addon-left-icon="ni ni-email-83"
                                            v-model="userInfo.email">
                                </base-input>
                                <base-input alternative
                                            type="password"
                                            placeholder="Password"
                                            addon-left-icon="ni ni-lock-circle-open"
                                            v-model="userInfo.password">
                                </base-input>
                                <base-input alternative
                                            type="password"
                                            placeholder="Confirm Password, please enter again"
                                            addon-left-icon="ni ni-lock-circle-open"
                                            v-model="userInfo.confirm_password">
                                </base-input>
                                <div class="text-center">
                                    <base-button type="primary" class="my-4" @click="jump()">Create account</base-button>
                                    <base-button type="primary" class="my-4" @click="visitor()">View as a visitor</base-button>
                                </div>
                            </form>
                        </template>
                    </card>
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import utils from '@/api/utils'
export default {
  
  data() {
    return {
      jumpTo: true,
      userInfo: {
        username:'',
        email: '',
        password: '',
        confirm_password: ''

      }
    };
  },
  methods: {
    visitor(){
      this.$router.push({ path: 'visitor' })
    }, 
    jump() {
      utils.register(this.userInfo).then((res) =>{
        debugger
        console.log(res)
        if (res.data == "Success"){
          this.$message({
              message: 'successfully registered!!',
              type: 'success'
          })
        } else {
          this.$message({
              showClose: true,
              message: 'failed to register',
              type: 'error'
          })
        }
      })
      if (this.jumpTo){
          this.$router.push({ path: 'login' })
      }
    }
  }
};
</script>
<style>
body, html {
  height: 100%;
}
.section{
  background-image: url('../assets/img/accounting.jpg');
  height: 100%;
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  background-size: cover; /* Resize the background image to cover the entire container */
}
</style>
