import Vue from "vue";
import Router from "vue-router";
import AppHeader from "./layout/AppHeader";
import LoginHeader from "./layout/LoginHeader";
import AppFooter from "./layout/AppFooter";
import Accounting from "./views/Accounting.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Profile from "./views/Profile.vue";
import About from "./views/About.vue";
import Visitor from "./views/Visitor.vue";

Vue.use(Router);

export default new Router({
  linkExactActiveClass: "active",
  routes: [
    {
      path: "/",
      name: "",
      components: {
        header: AppHeader,
        default: Register,
        footer: AppFooter
      }
    },
    {
      path: "/visitor",
      name: "visitor",
      components: {
        header: AppHeader,
        default: Visitor,
        footer: AppFooter
      }
    },
    {
      path: "/accounting",
      name: "accounting",
      components: {
        header: LoginHeader,
        default: Accounting,
        footer: AppFooter
      }
    },
    {
      path: "/login",
      name: "login",
      components: {
        header: AppHeader,
        default: Login,
        footer: AppFooter
      }
    },
    {
      path: "/register",
      name: "register",
      components: {
        header: AppHeader,
        default: Register,
        footer: AppFooter
      }
    },
    {
      path: "/profile",
      name: "profile",
      components: {
        header: LoginHeader,
        default: Profile,
        footer: AppFooter
      }
    },
    {
      path: "/about",
       name: "about",
       components:  {
        header: AppHeader,
        default: About,
        footer: AppFooter
       }
      }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
