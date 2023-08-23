<template>
  <div class="sidebar">
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="">
        <div class="sidebar-brand-icon">
          <i class="bi bi-activity"></i>
        </div>
        <div class="sidebar-brand-text mx-3"><img src="static/img/logo_white.png" width="80%"></div>
      </a>
      <!-- Divider -->
      <hr class="sidebar-divider my-0" />
      <!-- Nav Item - Dashboard -->
      <li class="nav-item active">
        <router-link tag="a" aria-controls="collapseTwo" aria-expanded="true" class="nav-link collapsed" to="/dashboard">
          <i class="fas fa-fw fa-tachometer-alt"></i>
          <span>{{ $t("Dashboard") }}</span>
        </router-link>
      </li>
      <!-- Divider -->
      <hr class="sidebar-divider" />
      <!-- Heading -->
      <!-- <div class="sidebar-heading">{{ $t("Booking") }}</div> -->

      <!-- Booking Menu -->
      <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#booking_menu" aria-expanded="true"
          aria-controls="booking_menu">
          <i class="fas fa fa-hotel"></i>
          <span>{{ $t("Booking") }}</span>
        </a>
        <div id="booking_menu" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <router-link v-if="this.$parent.user_roles['hotels']" tag="a" class="collapse-item" to="/hotels"> {{
              $t("Hotels") }} </router-link>
            <router-link v-if="this.$parent.user_roles['bookings']" tag="a" class="collapse-item" to="/bookings"> {{
              $t("Bookings") }} </router-link>
            <router-link v-if="this.$parent.user_roles['available_hotel']" tag="a" class="collapse-item"
              to="/available_hotel"> {{ $t("Available Hotels") }} </router-link>
            <router-link v-if="this.$parent.user_roles['hotels_report']" tag="a" class="collapse-item"
              to="/hotels_report"> {{ $t("Hotels Report") }} </router-link>
          </div>
        </div>
      </li>

      <!-- flights Menu -->
      <li class="nav-item" v-if="this.$parent.user_roles['flights']">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#flights_menu" aria-expanded="true"
          aria-controls="flights_menu">
          <i class="fas fa fa-plane"></i>
          <span>{{ $t("Flights") }}</span>
        </a>
        <div id="flights_menu" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <router-link v-if="this.$parent.user_roles['flights']" tag="a" class="collapse-item" to="/flights"> {{
              $t("Flights") }} </router-link>
            <router-link v-if="this.$parent.user_roles['flight_bookings']" tag="a" class="collapse-item" to="/flight_bookings"> {{
              $t("Flight Bookings") }} </router-link>
          </div>
        </div>
      </li>

      <!-- system Menu -->
      <li class="nav-item" v-if="this.$parent.user_roles['backups']">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#admin_menu" aria-expanded="true"
          aria-controls="admin_menu">
          <i class="fas fa fa-toolbox"></i>
          <span>{{ $t("Admin") }}</span>
        </a>
        <div id="admin_menu" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <router-link v-if="this.$parent.user_roles['backups']" tag="a" class="collapse-item" to="/backups"> {{
              $t("Backups") }} </router-link>

            <router-link v-if="this.$parent.user_roles['logs']" tag="a" class="collapse-item" to="/logs"> {{
              $t("Logs") }} </router-link>
          </div>
        </div>

      </li>

      <!-- <li class="nav-item">
        <router-link tag="a" aria-controls="collapseTwo" aria-expanded="true" class="nav-link collapsed" to="/flights">
          <i class="fa fa-plane"></i>
          <span>{{ $t("Flights") }}</span>
        </router-link>
      </li> -->
      <!-- Hotels Menu -->
      <!-- <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#hotels_menu" aria-expanded="true"
          aria-controls="hotels_menu">
          <i class="fas fa fa-hotel"></i>
          <span>{{ $t("Hotels") }}</span>
        </a>
        <div id="hotels_menu" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
          </div>
        </div>
      </li> -->
      <!-- Trips Menu -->
      <!-- <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#trips_menu" aria-expanded="true"
          aria-controls="trips_menu">
          <i class="fa fa-arrows-split-up-and-left"></i>
          <span>{{ $t("Trips") }}</span>
        </a>
        <div id="trips_menu" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
          </div>
        </div>
      </li> -->
      <!-- Nav Item - Persons Collapse Menu -->
      <!-- <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseUtilities"
          aria-expanded="true" aria-controls="collapseUtilities">
          <i class="fas fa fa-users"></i>
          <span>{{ $t("Persons") }}</span>
        </a>
        <div id="collapseUtilities" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <router-link tag="a" class="collapse-item" to="/customers"> {{ $t("Customers") }} </router-link>
            <router-link tag="a" class="collapse-item" to="/users"> {{ $t("Users") }} </router-link>
            <router-link tag="a" class="collapse-item" to="/employees"> {{ $t("Employees") }} </router-link>
            <a class="collapse-item" href="utilities-border.html">{{ $t("Borders") }}</a>
            <a class="collapse-item" href="utilities-animation.html">{{ $t("Animations") }}</a>
            <a class="collapse-item" href="utilities-other.html">{{ $t("Other") }}</a>
          </div>
        </div>
      </li> -->
      <!-- Divider -->
      <hr class="sidebar-divider" />
      <!-- Heading -->
      <!-- <div class="sidebar-heading">{{ $t("Addons") }}</div> -->
      <!-- Nav Item - Pages Collapse Menu -->
      <!-- <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapsePages" aria-expanded="true"
          aria-controls="collapsePages">
          <i class="fas fa-fw fa-folder"></i>
          <span>{{ $t("Pages") }}</span>
        </a>
        <div id="collapsePages" class="collapse" aria-labelledby="headingPages" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <h6 class="collapse-header">Login Screens:</h6>
            <a class="collapse-item" href="login.html">Login</a>
            <a class="collapse-item" href="register.html">Register</a>
            <a class="collapse-item" href="forgot-password.html">Forgot Password</a>
            <div class="collapse-divider"></div>
            <h6 class="collapse-header">Other Pages:</h6>
            <a class="collapse-item" href="404.html">404 Page</a>
            <a class="collapse-item" href="blank.html">Blank Page</a>
          </div>
        </div>
      </li> -->
      <!-- Nav Item - Charts -->
      <!-- <li class="nav-item">
        <a class="nav-link" href="charts.html">
          <i class="fas fa-fw fa-chart-area"></i>
          <span>Charts</span></a>
      </li> -->
      <!-- Nav Item - Tables -->
      <!-- <li class="nav-item">
        <a class="nav-link" href="tables.html">
          <i class="fas fa-fw fa-table"></i>
          <span>Tables</span></a>
      </li> -->
      <!-- Divider -->
      <!-- <hr class="sidebar-divider d-none d-md-block" /> -->
      <!-- Sidebar Toggler (Sidebar) -->
      <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
      </div>
    </ul>
  </div>
</template>
<script>
export default {
  name: "SideBar",
  data() {
    return {
      user_name: '',
      user_roles: ''
    }
  },
  async mounted() {
    this.user_name = localStorage.getItem('user_name');

    await new Promise(resolve => setTimeout(resolve, 500)); // wait
    this.get_roles();

  },

  methods: {
    get_roles() {
      this.user_roles = this.$parent.user_roles;
    }
  }
};
</script>
