<template>
  <div id="app" style="width: 100vw; height: 100vh; margin: 0px;">
    <el-main style="width: 100%; height: 100%; margin: 0px; padding: 0px;">
      <keep-alive>
        <router-view />
      </keep-alive>
    </el-main>
  </div>
</template>

<script>

export default {
  name: "App",
  components: {
  },
  computed: {
  },
  methods: {
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
