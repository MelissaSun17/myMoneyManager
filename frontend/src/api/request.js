// // import axios from 'axios'
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)



export default {
postJson(url, data) {
  return new Promise((resolve, reject) => {
    Vue.axios.post(url, data).then(resp => {
      if (resp.data.code === 200) {
        resolve(resp.data.mainData);
      }
      resolve(resp)
    }).catch(function (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
      }
      console.log(error.config);
      reject(error);
    });
  });
},


getJson(url, data) {
  return new Promise((resolve, reject) => {
    // console.log(url, data)
    // const token = Cookies.get('token');
    // console.log("token: ", token);

    // this.$axios.get(newUrl, {
    //   data,
    //   headers: token && token !== undefined && token != 'undefined' ?
    //     {
    //       'Content-Type': 'application/json; charset=UTF-8',
    //       'Authorization': token,
    //     } : {}
    // }
    // ).then(resp => {
    //   if (resp.data.code === 200) {
    //     resolve(resp.data.mainData);
    //   } else {
    //     Message("not able to connect api: " + resp.data.message);
    //   }
    //   resolve(resp)
    // }, err => {
    //   if (err.message) {
    //     console.log("getJson error:", err);
    //   } else {
    //     console.log("getJson error");
    //   }
    //   Message.error("Retry later")
    //   reject(err)
    // })
    // Vue.axios.get(url, {data, headers: { 'Content-Type': 'application/x-www-from-urlencoded'}}).then((resp) => {
    Vue.axios.get(url, data).then((resp) => {
      
      if (resp.data.code === 200) {
        resolve(resp.data.mainData);
      } 
      resolve(resp)
    }).catch(function (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
      }
      console.log(error.config);
      reject(error);
    });
  });
}
}


// export function request(config) {
//   // 1.创建axios的实例
//   const instance = axios.create({
//     baseURL:"/api",
//     timeout: 5000,
//   })
//     // 2.1.请求拦截的作用
//   instance.interceptors.request.use(config => {
//     return config
//   }, err => {
//     console.log(err);
//   })
//   // 2.2.响应拦截
//   instance.interceptors.response.use(res => {
//     return res.data
//   }, err => {
//     console.log(err);
//   })
//   // 3.发送真正的网络请求
//   return instance(config)
// }

