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
        <!-- <div class="shape shape-style-1 shape-primary">
            <span class="span-150"></span>
            <span class="span-50"></span>
            <span class="span-50"></span>
            <span class="span-75"></span>
            <span class="span-100"></span>
            <span class="span-75"></span>
            <span class="span-50"></span>
            <span class="span-100"></span>
            <span class="span-50"></span>
            <span class="span-100"></span>
        </div> -->
        <div class="container pt-lg-md">
            <div class="row justify-content-center">
                <div class="col-lg-5">
                    <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                        <!-- <template>
                            <div class="text-muted text-center mb-3">
                                <small>Sign in with</small>
                            </div>
                            <div class="btn-wrapper text-center">
                                <base-button type="neutral">
                                    <img slot="icon" src="../assets/img/github.svg">
                                    Github
                                </base-button>

                                <base-button type="neutral">
                                    <img slot="icon" src="../assets/img/google.svg">
                                    Google
                                </base-button>
                            </div>
                        </template> -->
                        <template>
                            <div class="text-center text-muted mb-4">
                                <h6>Sign in with email and password</h6>
                            </div>
                            <form role="form">
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
                                <base-checkbox>
                                    Remember me
                                </base-checkbox>
                                <div class="text-center">
                                    <base-button type="primary" class="my-4" @click="jump()">Sign In</base-button>
                                    <base-button type="primary" class="my-4" @click="visitor()">View as a visitor</base-button>
                                </div>
                            </form>
                        </template>
                    </card>
                    <!-- <div class="row mt-3">
                        <div class="col-6">
                            <a href="#" class="text-light">
                                <small></small>
                            </a>
                        </div>
                        <div class="col-6 text-right">
                            <a href="#" class="text-light">
                                <small><router-link to="/register" >Create an account</router-link></small>
                            </a>
                        </div>
                    </div> -->
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import utils from '@/api/utils';
export default {
  data() {
    return {
      userInfo: {
        email: '',
        password: ''
      }
    };
  },
  methods: {
    visitor(){
      this.$router.push({ path: 'visitor' })
    }, 
    jump() {
      utils.login(this.userInfo).then((res) =>{
        debugger
        if (res.status == 200){
          if (res.data.success){
            
            console.log(res.data)
            let result = JSON.parse(res.data.result)
            console.log(result)
            window.sessionStorage.setItem('user', JSON.stringify(result[0].fields))
            window.sessionStorage.setItem('userId', result[0].pk)
            this.$router.push({ path: 'accounting' })
            this.$message({
              message: 'successfully logged in!',
              type: 'success'
          })
          } else {
            this.$message("Sorry, your password or email is incorrect, or you may not be registered!")
          }
        }
      })
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
