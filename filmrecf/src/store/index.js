import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from "vuex/dist/logger";
// import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

var files = require.context("./modules", true, /\.js$/);
const modules = {};

files.keys().forEach(key => {
  modules[key.replace(/(\.\/|\.js)/g, "")] = files(key).default;
});

export default new Vuex.Store({
  modules,
  plugins: [createLogger()]
  // plugins: [createPersistedState()]
});