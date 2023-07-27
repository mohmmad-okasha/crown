import Vue from "vue";
import VueRouter from "vue-router";
import UsersView from "../views/UsersView.vue";
import BookingsView from "../views/BookingsView.vue";
import Available_hotelView from "../views/Available_hotelView.vue";
import HotelsView from "../views/HotelsView.vue";
import Hotels_reportView from "../views/Hotels_reportView.vue";
import BackupsView from "../views/BackupsView.vue";
import LogsView from "../views/LogsView.vue";
import FlightsView from "../views/FlightsView.vue";
import DashboardView from "../views/DashboardView.vue";

//import HomeView from "../views/HomeView.vue";
//import About from "../views/AboutView.vue";
//import FlightsView from "../views/FlightsView.vue";
//import RoomsView from "../views/RoomsView.vue";
//import Hotel_roomsView from "../views/Hotel_roomsView.vue";
//import AccountsView from "../views/AccountsView.vue";
//import LoginView from "../views/LoginView.vue";

/* eslint-disable */
Vue.use(VueRouter);

const routes = [

  // {
  //   path: "/login",
  //   name: "login",
  //   component: LoginView,
  // },
  // {
  //   path: "/about",
  //   name: "about",
  //   component: About,
  //   meta: {
  //     requiresAuth: true, 
  //   },
  // },
  {
    path: "/flights",
    name: "FlightsView",
    component: FlightsView,
    meta: {
      requiresAuth: true, 
    },
  },
  // {
  //   path: "/rooms",
  //   name: "RoomsView",
  //   component: RoomsView,
  //   meta: {
  //     requiresAuth: true, 
  //   },
  // },
  // {
  //   path: "/Hotel_rooms",
  //   name: "Hotel_roomsView",
  //   component: Hotel_roomsView,
  //   meta: {
  //     requiresAuth: true, 
  //   },
  // },
  // {
  //   path: "/accounts",
  //   name: "AccountsView",
  //   component: AccountsView,
  //   meta: {
  //     requiresAuth: true, 
  //   },
  // },
  // {
  //   path: "/test",
  //   name: "test",
  //   component: () =>
  //     import("../components/TestCom.vue"),
  // },



  {
    path: "/",
    name: "DashboardView",
    component: DashboardView,
    meta: {
      requiresAuth: true, // add this meta field to routes that require authentication
    },
  },

  {
    path: "/backups",
    name: "BackupsView",
    component: BackupsView,
    meta: {
      requiresAuth: true, // add this meta field to routes that require authentication
    },
  },
  {
    path: "/logs",
    name: "LogsView",
    component: LogsView,
    meta: {
      requiresAuth: true, // add this meta field to routes that require authentication
    },
  },
  
  {
    path: "/users",
    name: "UsersView",
    component: UsersView,
    meta: {
      requiresAuth: true, 
    },
  },

  {
    path: "/bookings",
    name: "BookingsView",
    component: BookingsView,
    meta: {
      requiresAuth: true, 
    },
  },
  {
    path: "/available_hotel",
    name: "Available_hotelView",
    component: Available_hotelView,
    meta: {
      requiresAuth: true, 
    },
  },

  {
    path: "/hotels",
    name: "HotelsView",
    component: HotelsView,
    meta: {
      requiresAuth: true, 
    },
  },
  {
    path: "/hotels_report",
    name: "Hotels_reportView",
    component: Hotels_reportView,
    meta: {
      requiresAuth: true, 
    },
  },

  {
    path: "/dashboard",
    name: "DashboardView",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },

];

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes,
});


// to check use is logged in before each rout
router.beforeEach((to, from, next) => {
  if (to.matched.some((route) => route.meta.requiresAuth)) {
    const token = localStorage.getItem('access_token')
    if (!token) {
      // if access token is not found, redirect to login page
      next({ name: 'login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router;
