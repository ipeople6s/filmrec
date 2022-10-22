<template>
  <div>
    <div class="background">
      <div class="shape"></div>
      <div class="shape"></div>
    </div>
    <transition name="el-zoom-in-center">
      <form v-if="isLogin">
        <h3>Login</h3>

        <label for="username" style="text-align: left">Username</label>
        <input
          type="text"
          placeholder=""
          id="username"
          v-model="username"
        />

        <label for="password" style="text-align: left">Password</label>
        <input
          type="password"
          placeholder=""
          id="password"
          v-model="password"
        />

        <button @click="login" style="color: white">Login</button>
        <div style="margin-top: 10px; color: gray;" @click="isLogin=false">New user? Start here.</div>
      </form>
    </transition>
    <transition name="el-zoom-in-center">
      <form v-if="!isLogin">
        <h3>Regist</h3>

        <label for="username" style="text-align: left">Username</label>
        <input
          type="text"
          placeholder=""
          id="username"
          v-model="username"
        />

        <label for="password" style="text-align: left">Password</label>
        <input
          type="password"
          placeholder=""
          id="password"
          v-model="password"
        />

        <button @click="regist" style="color: white">Regist</button>
        <div style="margin-top: 10px; color: gray;" @click="isLogin=true">Login</div>
      </form>
    </transition>
  </div>
</template>

<script>
import api from "../api";
import router from "@/router/index";
import { cookies } from "@/api/utils";

export default {
  name: "Login",
  components: {},
  data: () => ({
    role: "0",
    username: "",
    password: "",
    isLogin: true
  }),
  activated() {
  },
  methods: {
    async login() {
      if (this.username === undefined || this.username === "") {
        this.$notify({
          type: "warning",
          title: "Tips",
          message: "Please input your username",
        });
        return;
      }
      if (this.password === undefined || this.password === "") {
        this.$notify({
          type: "warning",
          title: "Tips",
          message: "Please input your password",
        });
        return;
      }

      var resp = await api.user.LOGIN({
        username: this.username,
        password: this.password,
      });
      cookies.set("token", resp);
      cookies.set("role", this.role);
      console.log(resp);

      this.$notify({
        type: "success",
        title: "Tip",
        message: "Login success",
      });
      // if (this.role == "1") {
      //   this.thisVideo.srcObject.getTracks()[0].stop();
      router.push("board");
      // } else {
      //   this.thisVideo.srcObject.getTracks()[0].stop();
      //   router.push("admin");
      //   router.push("upload");
      // }
    },
    flip() {
      this.isLogin = false
    }
  },
};
</script>

<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  background-color: #080710;
  margin: 0px;
}
.background {
  width: 430px;
  height: 520px;
  position: absolute;
  transform: translate(-50%, -50%);
  left: 50%;
  top: 50%;
}
.background .shape {
  height: 200px;
  width: 200px;
  position: absolute;
  border-radius: 50%;
}
.shape:first-child {
  background: linear-gradient(#1845ad, #23a2f6);
  left: -80px;
  top: -80px;
}
.shape:last-child {
  background: linear-gradient(to right, #ff512f, #f09819);
  right: -30px;
  bottom: -80px;
}
form {
  height: 400px;
  width: 380px;
  background-color: rgba(255, 255, 255, 0.13);
  position: absolute;
  transform: translate(-50%, -50%);
  top: 50%;
  left: 50%;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(224, 224, 224, 0.1);
  box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
  padding: 50px 35px;
}
form * {
  font-family: "Poppins", sans-serif;
  color: #000;
  letter-spacing: 0.5px;
  outline: none;
  border: none;
}
form h3 {
  font-size: 32px;
  font-weight: 500;
  line-height: 42px;
  text-align: center;
}
label {
  display: block;
  margin-top: 30px;
  font-size: 16px;
  font-weight: 500;
}
input {
  display: block;
  height: 50px;
  width: 100%;
  background-color: rgba(77, 76, 76, 0.07);
  border-radius: 3px;
  padding: 0 10px;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 300;
}
::placeholder {
  color: #101010;
}
button {
  margin-top: 50px;
  width: 100%;
  background-color: #1e7cd1;
  color: #080710;
  padding: 15px 0;
  font-size: 18px;
  font-weight: 600;
  border-radius: 5px;
  cursor: pointer;
}
.social {
  margin-top: 30px;
  display: flex;
}
.social div {
  background: red;
  width: 150px;
  border-radius: 3px;
  padding: 5px 10px 10px 5px;
  background-color: rgba(255, 255, 255, 0.27);
  color: #eaf0fb;
  text-align: center;
}
.social div:hover {
  background-color: rgba(255, 255, 255, 0.47);
}
.social .fb {
  margin-left: 25px;
}
.social i {
  margin-right: 4px;
}
</style>
