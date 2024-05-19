<template>
  <!-- <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/users">users</router-link>
    </nav>
    <router-view />
  </div> -->

  <div class="home" id="page-top"
    :style="{ '--primary': primary_color, '--back_color': back_color, '--primary_text': primary_text }">

    <!-- Login page -->
    <div v-if="!this.auth.logged_in">

      <section class="vh-100" style="background-color: var(--primary);">
        <div class="container py-5 h-100">
          <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-12 col-md-8 col-lg-6 col-xl-5">
              <div class="card shadow-2-strong" style="border-radius: 1rem;">
                <div class="card-body p-5 text-center">

                  <h3 class="mb-5">Sign in</h3>
                  <form @submit.prevent="loginUser">
                    <div class="form-outline mb-4">
                      <label class="form-label" for="typeEmailX-2">User Name</label>
                      <input type="text" v-model="user_name" required class="form-control form-control-lg"
                        :class="{ 'is-invalid': this.error }" />
                    </div>

                    <div class="form-outline mb-4">
                      <label class="form-label" for="typePasswordX-2">Password</label>
                      <input type="password" v-model="password" required class="form-control form-control-lg"
                        :class="{ 'is-invalid': this.error }" />

                    </div>

                    <div v-if="this.error" class="alert alert-danger" role="alert">
                      {{ $t("Login Error") }}
                    </div>

                    <button class="btn btn-primary btn-lg btn-block" type="submit">Login</button>
                  </form>

                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>

    <div v-if="this.auth.logged_in">

      <!-- Page Wrapper -->
      <div id="wrapper">
        <!-- Sidebar -->
        <SideBar />
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">
          <!-- Main Content -->
          <div id="content">
            <!-- navbar -->
            <NavBar ref="NavBar" />
            <!-- End of navbar -->

            <!-- Begin Page Content -->
            <div class="container-fluid">
              <!-- Content here -->
              <!-- <router-link to="/">Home</router-link>
            <router-link to="/test">About</router-link>
            <router-link to="/customers">Customers</router-link> -->
              <router-view :search="search" />
            </div>
            <!-- /.container-fluid -->
          </div>
          <!-- End of Main Content -->

          <!-- Footer -->
          <footer class="sticky-footer bg-white"></footer>
          <!-- End of Footer -->
        </div>
        <!-- End of Content Wrapper -->
      </div>
      <!-- End of Page Wrapper -->

      <!-- Scroll to Top Button-->
      <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
      </a>

      <!-- Logout Modal-->
      <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
              <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">×</span>
              </button>
            </div>
            <div class="modal-body">
              Select "Logout" below if you are ready to end your current session.
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" type="button" data-dismiss="modal">
                Cancel
              </button>
              <a class="btn btn-primary" @click="logout">Logout</a>
            </div>
          </div>
        </div>
      </div>

      <!-- settings modal -->
      <div class="modal fade" id="settings_modal" data-backdrop="static" data-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="modal_label">{{ $t("Settings") }}</h5>
              <button type="button" class="close" @click="this.close_settings_modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="row">
                  <div class="col-sm-4">
                    <div class="form-group mb-2">
                      <label for="lang">{{ $t("Language") }}</label>
                      <select id="lang" v-model="settings.lang" type="text" class="form-control">
                        <option selected :value="$t('ar')">{{ $t("Arabic") }}</option>
                        <option :value="$t('en')">{{ $t("English") }}</option>
                      </select>
                    </div>
                  </div>
                  <div class="col">
                    <div class="form-group">
                      <label for="dark_mode">{{ $t("Dark Mode") }}</label>
                      <select id="dark_mode" v-model="settings.dark_mode" type="text" class="form-control">
                        <option :value="true">{{ $t("On") }}</option>
                        <option :value="false">{{ $t("Off") }}</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div v-show="settings.dark_mode == false" class="row">
                  <div class="col">
                    <div class="form-group">
                      <label for="primary_color">{{ $t("Primary Color") }}</label>
                      <input type="color" v-model="settings.primary_color" class="form-control">
                    </div>
                  </div>
                  <div class="col">
                    <div class="form-group">
                      <label for="back_color">{{ $t("Back Color") }}</label>
                      <input type="color" v-model="settings.back_color" class="form-control">
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" id="closeModal" class="btn btn-secondary" @click="this.close_settings_modal">
                {{ $t("Cancel") }}
              </button>
              <button type="button" class="btn btn-primary" @click="this.save_settings">
                {{ $t("Save") }}</button>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
/* eslint-disable */
import moment from 'moment';
import axios from "axios";
import { my_api, domain_url } from "./axios-api";

// @ is an alias to /src
import SideBar from "@/components/parts/SideBar.vue";
import NavBar from "@/components/parts/NavBar.vue";
export default {

  name: "HomeView",
  components: {
    SideBar,
    NavBar,
  },
  data() {
    return {

      error: false,
      settings: {
        dark_mode: '',
        lang: '',
        primary_color: '',
        back_color: '',
      },
      user_name: '',
      password:'',
      user_name_id: '',
      auth: {
        username: '',
        password: '',
        logged_in: localStorage.getItem('access_token'),
      },
      search: NavBar.search,
      primary_color: '',
      primary_text: '',
      back_color: '',
      user_roles: []
    }
  },
  async mounted() {
    this.user_name = localStorage.getItem('user_name')
    this.get_user_name_id();
    await this.get_settings();
    this.dark_mode();
    this.get_roles();
    this.set_lang();
  },
  methods: {
    async loginUser() {
      const data = { username: this.user_name, password: this.password }
      try {
        const response = await axios.post(domain_url + '/backend/login/', data)
        this.auth.logged_in = response.data.access
        this.auth.username = this.user_name

        localStorage.setItem('access_token', this.auth.logged_in)
        localStorage.setItem('token_time', new Date())
        localStorage.setItem('user_name', this.user_name)

        axios.post(domain_url + '/backend/logs/', {user_name: this.user_name, log: 'login',time: new Date()})

        window.location.reload();

        // redirect to dashboard or homepage after successful login
        this.error = false;
        this.$router.push('dashboard')

      } catch (error) {
        this.error = true;
        console.log(error);
      }
    },
    async logout() {
      //to remove modal background on auto vue js reload
      const elements = document.getElementsByClassName("modal-backdrop fade show");
      while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
      }////
      localStorage.setItem('access_token', '');
      localStorage.setItem('user_name', '');
      this.auth.logged_in = '';
    },
    save_backup() {
      return my_api.get('/backend/save_backup/')
        .then(localStorage.setItem('last_backup', new Date()))
        .catch(err => { alert(err) });
    },
    get_user_name_id() {
      if(this.user_name)
      return axios({
        method: "get",
        url: domain_url + "/backend/get_user_name_id/?username=" + this.user_name,
        //auth: { username: "admin", password: "123", },
      }).then((response) => (this.user_name_id = response.data.data));
    },
    async get_roles() {
      if(this.user_name_id)
      return my_api.get('backend/get_roles/?user_id=' + this.user_name_id, { auth: { username: "admin", password: "123", } })
        .then((response) => (this.user_roles = response.data))
        .catch(err => { });
    },
    dark_mode() {
      if (this.settings.dark_mode) {
        this.primary_color = '#242526';
        this.primary_text = '#fff';
        this.back_color = '#18191a';
      } else {
        this.primary_color = this.settings.primary_color;//'#6096B4'
        this.primary_text = this.settings.primary_color;
        this.back_color = this.settings.back_color;//'#f8f9fc';
      }
    },
    get_settings() {
      return my_api.get("/backend/settings/1")
        .then((response) => (
          this.settings.dark_mode = response.data['dark_mode'],
          this.settings.primary_color = response.data['primary_color'],
          this.settings.back_color = response.data['back_color'],
          this.settings.lang = response.data['lang']
        ));
    },
    async save_settings() {
      try {
        var response = await fetch(domain_url + "/backend/settings/1/", {
          method: "PUT",
          headers: { "Content-Type": "application/json", },
          body: JSON.stringify(this.settings),
        }
        );
        swal(this.$t("Saved"), { buttons: false, icon: "success", timer: 2000, });
        await this.get_settings();
        this.dark_mode();
        this.set_lang();
        this.close_settings_modal();
      } catch (error) {
        console.error();
      }

    },
    set_lang() {
      this.$i18n.locale = this.settings.lang;
    },
    open_settings_modal() {
      $('#settings_modal').modal('toggle');
    },
    close_settings_modal() {
      $('#settings_modal').modal('hide');
    },
  },
  beforeCreate() {
    //if mobile click sidebarToggleTop button
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
      $(document).ready(function () {
        $('#sidebarToggleTop').click();
      });
    }

    const token = localStorage.getItem('access_token')
    this.logged_in = token
    this.user_name = localStorage.getItem('user_name')

    var token_time = localStorage.getItem('token_time')
    const date1 = new Date(); // Set date1 to the current date and time
    const date2 = new Date(token_time); // Set date2 to the date specified by date2String

    const diffInMs = Math.abs(date2 - date1);
    const diffInMinutes = Math.floor((diffInMs / 1000) / 60);

    //auto logout
    if (diffInMinutes > 60) {
      localStorage.setItem('access_token', '');
      localStorage.setItem('token_time', 0)
    }


    //auto backup
    const last_backup = localStorage.getItem('last_backup')
    if (!last_backup) {
      my_api.get('/backend/save_backup/')
        .then(localStorage.setItem('last_backup', new Date()))
        .catch(err => { alert(err) });
    } else {

      const last_backup_date = new Date(last_backup);
      const backup_diffInMs = Math.abs(last_backup_date - date1);
      const backup_diffInMinutes = Math.floor((backup_diffInMs / 1000) / 60);
      if (backup_diffInMinutes > 800) {
        my_api.get('/backend/save_backup/')
          .then(localStorage.setItem('last_backup', new Date()))
          .catch(err => { alert(err) });
      }
      
    }




  },
};
</script>
