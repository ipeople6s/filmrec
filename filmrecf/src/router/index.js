import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import("../views/Login.vue")
  },
  {
    path: "/",
    name: "board",
    component: () => import ("../views/Board.vue")
  },
  {
    path: "/board",
    name: "board",
    component: () => import ("../views/Board.vue")
  },
]

const router = new VueRouter({
  routes
})

export default router