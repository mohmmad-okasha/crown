<template>
  <div class="UsersView">

    <!-- context-menu -->
    <div id="context-menu" class="context-menu" :style="menuStyle">
      <ul>
        <li class="dropdown-item" @click="delete_user(user.id)">
          <i class="fa fa-trash"></i>
          {{ $t("Delete") }}
        </li>
        <li class="ltr dropdown-item" @click="open_edit_modal">
          <i class="fa fa-pen-to-square"></i>
          {{ $t("Edit") }}
        </li>
        <li class="dropdown-item">
          <i class="fa fa-print"></i>
          {{ $t("Print") }}
        </li>
      </ul>
    </div>

    <!-- Table Card -->
    <div class="col-xl-12 center">
      <div class="card shadow mb-4">
        <!-- Card Header - Dropdown -->
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">{{ $t("Users Table") }} </h6>
          <div class="dropdown no-arrow">

            <div class="btn-group" role="group">
              <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle" data-toggle="dropdown"
                aria-haspopup="true" aria-expanded="true">
                <i class="fa fa-bars on-hover"></i>
              </button>
              <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1" x-placement="bottom-start"
                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                <a class="dropdown-item hand-mouse" @click="open_add_modal">
                  <i class="fa fa-plus"></i>
                  {{ $t("Add") }}
                </a>
                <a class="dropdown-item hand-mouse" @click="PrintDiv('table')">
                  <i class="fa fa-print"></i>
                  {{ $t("Print") }}
                </a>
              </div>
            </div>

          </div>
        </div>
        <!-- Card Body -->
        <div id="table" class="card-body">
          <div class="card-header cnter" style="display: none;" id="head_txt"></div>
          <form class="site-form-table">
            <div class="table-responsive">
              <table id="mytable" class="table table-hover">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">{{ $t("First Name") }}</th>
                    <th scope="col">{{ $t("Last Name") }}</th>
                    <th scope="col">{{ $t("User Name") }}</th>
                    <th scope="col">{{ $t("Email") }}</th>
                    <th scope="col">{{ $t("Created On") }}</th>
                    <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr @contextmenu="showContextMenu" v-for="r in this.users" :key="r.id" @click="row_click(r.id)"
                    @click.right="row_click(r.id)" role="button" :class="{ 'selected': r.id === active_index }">
                    <th scope="row" id="id">{{ r.id }}</th>
                    <td>{{ $t(r.first_name) }}</td>
                    <td>{{ $t(r.last_name) }}</td>
                    <td>{{ $t(r.username) }}</td>
                    <td>{{ $t(r.email) }}</td>
                    <td>{{ r.date_joined.substring(0, 10) }}</td>

                    <td class="no_print">

                      <div class="btn-group" role="group">
                        <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                          data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                          <i class="fa fa-gear on-hover"></i>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1" x-placement="bottom-start"
                          style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                          <a class="dropdown-item" @click="delete_user(user.id)">
                            <i class="fa fa-trash"></i>
                            {{ $t("Delete") }}
                          </a>
                          <a class="dropdown-item" @click="open_edit_modal">
                            <i class="fa fa-pen-to-square"></i>
                            {{ $t("Edit") }}
                          </a>
                          <a class="dropdown-item">
                            <i class="fa fa-print"></i>
                            {{ $t("Print") }}
                          </a>
                        </div>

                      </div>

                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- to get id of selected record -->
            <input hidden type="text" v-model="active_index" id="row_id" />
          </form>
        </div>
      </div>
    </div>

    <!-- to get search value from navbar -->
    <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>

    <!-- modal -->
    <div class="modal  fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
      aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add User") }}</h5>
            <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit User") }}</h5>
            <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form>

              <div class="form-group col-md">
                <label for="first_name"> {{ $t("First Name") }}</label>
                <input id="first_name" v-model="user.first_name"
                  :class="{ 'is-invalid': !this.user.first_name && this.validate, 'is-valid': this.user.first_name && this.validate }"
                  type="text" class="form-control">
                <div v-if="!this.user.first_name && this.validate" class="invalid-feedback hidden">
                  {{ $t("Please Enter The first_name") }}
                </div>
              </div>

              <div class="form-group col-md">
                <label for="last_name"> {{ $t("Last Name") }}</label>
                <input id="last_name" v-model="user.last_name"
                  :class="{ 'is-invalid': !this.user.last_name && this.validate, 'is-valid': this.user.last_name && this.validate }"
                  type="text" class="form-control">
                <div v-if="!this.user.last_name && this.validate" class="invalid-feedback hidden">
                  {{ $t("Please Enter The last_name") }}
                </div>
              </div>

              <div class="form-group col-md">
                <label for="username"> {{ $t("User Name") }}</label>
                <input id="username" v-model="user.username"
                  :class="{ 'is-invalid': !this.user.username && this.validate, 'is-valid': this.user.username && this.validate }"
                  type="text" class="form-control">
                <div v-if="!this.user.username && this.validate" class="invalid-feedback hidden">
                  {{ $t("Please Enter The username") }}
                </div>
              </div>

              <div class="form-group col-md">
                <label for="email"> {{ $t("Email") }}</label>
                <input id="city" v-model="user.email"
                  :class="{ 'is-invalid': !this.user.email && this.validate, 'is-valid': this.user.email && this.validate }"
                  type="text" class="form-control">

                <div v-if="!this.user.email && this.validate" class="invalid-feedback hidden">
                  {{ $t("Please Enter The Email") }}
                </div>
              </div>

              <div class="form-group col-md">
                <label for="password"> {{ $t("Password") }}</label>
                <input id="password" v-model="user.password"
                  :class="{ 'is-invalid': !(this.user.password == this.user.password2) && this.validate, 'is-valid': (this.user.password == this.user.password2) && this.validate }"
                  type="password" class="form-control">

                <div v-if="!(this.user.password == this.user.password2) && this.validate" class="invalid-feedback hidden">
                  {{ $t("Password not match") }}
                </div>
              </div>

              <div class="form-group col-md">
                <label for="password2"> {{ $t("Confirm Password") }}</label>
                <input id="password2" v-model="user.password2"
                  :class="{ 'is-invalid': !(this.user.password == this.user.password2) && this.validate, 'is-valid': (this.user.password == this.user.password2) && this.validate }"
                  type="password" class="form-control">

                <div v-if="!(this.user.password == this.user.password2) && this.validate" class="invalid-feedback hidden">
                  {{ $t("Password not match") }}
                </div>
              </div>

              <!-- Roles -->
              <div class="card m-1">
                <div class="card-header">
                  {{ $t('Roles') }}
                </div>
                <div class="card-body ">
                  <div class="form-group row center">
                    <div v-for="(value, role) in user.roles" :key="role">
                      <label  class="col-auto" v-if="role != 'id' && role != 'user_name'">
                        <input  type="checkbox" :value="value" :checked="checkboxValues[role]"
                          @change="updateUserRole(role, $event.target.checked)">
                        {{ role }}
                      </label>
                    </div>
                  </div>
                  <!-- <div class="form-row center">
                    <div class="form-group col-md-6">
                      <label for="no_list">{{ $t('Disabled') }}</label>
                      <select v-if="!this.edit_mode" name="no_list" id="no_list" class="form-control input-medium"
                        multiple size="10">
                        <option v-for="d in disabled_roles" @dblclick="add_role(b)" :key="d" :value="d">{{ d }}</option>
                      </select>

                      <select v-if="this.edit_mode" name="no_list" id="no_list" class="form-control input-medium" multiple
                        size="10">
                        <option v-for="d in disabled_roles" @dblclick="add_role(b)" :key="d" :value="d">{{ d }}</option>
                      </select>

                      <button @click="add_role()" type="button" class="btn-sm btn btn-success btn-circle mt-3"
                        :title="$t('Enable')"><i class="fas fa-angle-right"></i></button>
                      <button @click="add_all_role()" type="button" class="btn-sm btn btn-success btn-circle mt-3"
                        :title="$t('Enable All')"><i class="fas fa-angle-double-right"></i></button>
                    </div>
                    <div class="form-group col-md-6">
                      <label for="ok_list">{{ $t('Enabled') }}</label>
                      <select v-if="!this.edit_mode" name="ok_list" id="ok_list" class="form-control input-medium"
                        multiple size="10">
                        <option v-for="a in this.all_roles" :key="a" :value="a">{{ a }}</option>
                      </select>
                      <select v-if="this.edit_mode" name="ok_list" id="ok_list" class="form-control input-medium" multiple
                        size="10">
                        <option v-for="e in enabled_roles" @dblclick="remove_role(e)" :key="e" :value="e">{{ e }}</option>
                      </select>
                      <button @click="remove_role()" type="button" class="btn-sm btn btn-danger btn-circle mt-3"
                        :title="$t('Disable')"><i class="fas fa-angle-left"></i></button>
                      <button @click="remove_all_role()" type="button" class="btn-sm btn btn-danger btn-circle mt-3"
                        :title="$t('Disable All')"><i class="fas fa-angle-double-left"></i></button>
                    </div>



                  </div> -->
                </div>
              </div>

            </form>

          </div>
          <div class="modal-footer">

            <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
              @click="this.closeModal">
              <i class="fa fa-xmark"></i>
            </button>

            <button v-if="!edit_mode" type="button" title="save" @click="save_user()" class="btn btn-primary on-hover-sm">
              <i class="fa fa-floppy-disk"></i></button>

            <button v-if="edit_mode" type="button" title="delete" @click="delete_user(active_index)"
              class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

            <button v-if="edit_mode" type="button" title="save" @click="update_user(active_index)"
              class="btn btn-primary on-hover-sm"> <i class="fa fa-floppy-disk"></i> </button>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
import { my_api, domain_url } from "../axios-api";
import axios from "axios";
/* eslint-disable */
export default {
  name: "users",
  data() {
    return {
      checkboxValues: {},
      all_roles: [],
      validate: false,
      edit_mode: false,
      active_index: '',
      max_user_id: 0,
      role_id: 0,
      users: [],


      user: {
        id: "",
        first_name: "",
        last_name: "",
        username: "",
        password: "",
        password2: "",
        email: "",
        date_joined: "",
        roles: [],
        roles_list: [],
      },
      //////////////////////////
      isContextMenuActive: false,
      menuStyle: {
        display: 'none',
        top: 0,
        left: 0
      }
    };
  },
  watch: {

  },
  computed: {
    // Computed property to determine whether each checkbox should be checked or not
    checkedRoles() {
      const checkedRoles = {};
      for (const role in this.user.roles) {
        checkedRoles[role] = this.user.roles[role] === 1;
      }
      return checkedRoles;
    },

    search() {
      let data = this.$parent.$refs.NavBar.search
      if (data && data.trim()) { // data.trim() to check data not spaces only
        return axios({
          method: "get",
          url: domain_url + "/backend/hotels/?search=" + data,
        }).then((response) => (this.Hotels = response.data));
      } else {
        this.get_users();
      }
    },


  },
  created() {

  },

  async mounted() {

    await this.get_users();
    await this.get_all_roles();
  },
  methods: {
    get_max_user_id() {
      return axios({
        method: "get",
        url: domain_url + "/backend/get_max_id/?table_name=User",
        //auth: { username: "admin", password: "123", },
      }).then((response) => (this.max_user_id = response.data.data.id__max));
    },

    async save_user() {
      try {
        if (this.check_form()) {
          this.saving = true;

          // save roles to array
          // this.user.roles_list = [];
          // var list_box = document.getElementById("ok_list");
          // for (var i = 0; i < list_box.length; i++) {
          //   this.user.roles_list.push(list_box.options[i].value);
          // }

          var response = await fetch(domain_url + "/backend/users/", {
            method: "post",
            headers: { "Content-Type": "application/json", },
            body: JSON.stringify(this.user),
          }); 

          await this.get_max_user_id();

          this.user.roles["user_name"] = this.max_user_id;
          var response2 = await fetch(domain_url + "/backend/roles/", {
            method: "post",
            headers: { "Content-Type": "application/json", },
            body: JSON.stringify(this.user.roles),
          });

          if (!response.ok || !response2.ok) {
            // handle the error
            var errorMessage = "Error: " + response.status + " " + response.statusText;
            swal(errorMessage, { icon: 'error' });
          } else {
            // Request was successful

            swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
            this.get_users();
            this.closeModal();
          }

          this.saving = false;

        }
      } catch (error) { console.error(); }
    },

    async delete_user(id) {
      try {
        await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
          .then(async (willDelete) => {
            if (willDelete) {
              var response = await fetch(domain_url + '/backend/users/?id=' + id, {
                method: "delete",
                headers: { "Content-Type": "application/json", },
              });
              if (!response.ok) {
                // handle the error
                var errorMessage = "Error: " + response.status + " " + response.statusText;
                swal(errorMessage, { icon: 'error' });
              } else {
                // Request was successful
                swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 1500, });
                this.clear_form();
                await this.get_users();
                this.closeModal();
              }

            }
          });
      } catch (error) { console.error(); }
    },

    update_user(id) {
      try {
        if (this.check_form()) {
          axios
            .patch(`/backend/users/`, { id: id, new_data: this.user })
            .then(response => {
              swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
              var response2 = fetch(domain_url + "/backend/roles/" + this.role_id + "/", {
                method: "PUT",
                headers: { "Content-Type": "application/json", },
                body: JSON.stringify(this.user.roles),
              });
              this.get_users();
              this.closeModal();
              this.edit_mode = false;
            })
            .catch(error => {
              console.error();
              var errorMessage = "Error: " + error;
              swal(errorMessage, { icon: 'error' });
            });
        }
      } catch (error) {
        console.error();
      }
    },

    async update_user1(id) {
      try {
        if (this.check_form()) {
          var response = await fetch(domain_url + "/backend/users/", { id: id, new_data: this.user }, {
            method: "PUT",
            headers: { "Content-Type": "application/json", },
            body: JSON.stringify(this.user),
          });

          if (!response.ok) {
            // handle the error
            var errorMessage = "Error: " + response.status + " " + response.statusText;
            swal(errorMessage, { icon: 'error' });
          } else {
            // Request was successful


            swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
            this.get_users();
            this.closeModal();
            this.edit_mode = false;
          }
        }
      } catch (error) {
        console.error();
      }

    },


    async get_users() {
      return my_api.get('backend/users/', { auth: { username: "admin", password: "123", } })
        .then((response) => (this.users = response.data))
        .catch(err => { alert(err) });
    },
    async get_roles() {
      return my_api.get('backend/get_roles/?user_id=' + this.user.id, { auth: { username: "admin", password: "123", } })
        .then((response) => (this.user.roles = response.data))
        .catch(err => { alert(err) });
    },
    async get_role_id() {
      return my_api.get('backend/get_role_id/?user_name_id=' + this.user.id, { auth: { username: "admin", password: "123", } })
        .then((response) => (this.role_id = response.data.role_id))
        .catch(err => { alert(err) });
    },
    async get_all_roles() {
      return my_api.get('backend/get_all_roles/', { auth: { username: "admin", password: "123", } })
        .then((response) => (this.all_roles = response.data))
        .catch(err => { alert(err) });
    },

    // Object.keys(response.data)

    showContextMenu(event) {
      event.preventDefault();
      this.isContextMenuActive = true;
      this.menuStyle.top = `${event.clientY}px`;
      this.menuStyle.left = `${event.clientX}px`;
      this.menuStyle.display = 'block';
      // Add a click listener to the window object to hide the context menu
      window.addEventListener('click', this.hideContextMenu);
    },

    hideContextMenu() {
      this.isContextMenuActive = false;
      this.menuStyle.display = 'none';
      // Remove the click listener from the window object
      window.removeEventListener('click', this.hideContextMenu);
    },

    async open_add_modal() {
      await this.get_max_user_id();
      this.edit_mode = false;
      //$('#modal_label').html('Add user');
      this.clear_form();

      this.user.roles = this.all_roles; //create boxs
      // Set the values for checkboxes based on user.roles
      for (const role in this.user.roles) {
        this.$set(this.checkboxValues, role, this.user.roles[role] === 1);
      }


      $('#addModal').modal('toggle');
    },

    updateUserRole(role, checked) {
      this.user.roles[role] = checked ? 1 : 0;
    },

    async open_edit_modal() {
      this.edit_mode = true;

      // Set the values for checkboxes based on user.roles
      for (const role in this.user.roles) {
        this.$set(this.checkboxValues, role, this.user.roles[role] === 1);
      }

      $('#addModal').modal('toggle');
    },

    closeModal() {
      $('#addModal').modal('hide');
      this.clear_form();
    },

    clear_form() {
      this.user.first_name = '';
      this.user.last_name = '';
      this.user.username = '';
      this.user.email = '';
      this.user.password = '';
      this.user.password2 = '';

      this.validate = false;
    },

    async get_user(id) {

      return axios({
        method: "get",
        url: domain_url + "/backend/users/?id=" + id,
        auth: { username: "admin", password: "123", },
      }).then((response) => (this.user = response.data[0]));

    },

    async row_click(index) {
      this.active_index = index; //to change row color
      await this.get_user(index);
      await this.get_roles();
      await this.get_role_id();
      return true
    },

    check_form() {
      this.validate = true; //to change inputs color 'red/green'

      if (
        this.user.username &&
        this.user.email &&
        this.user.password === this.user.password2
      ) {
        return true
      } else {
        return false
      }
    },

  },
};
</script>
