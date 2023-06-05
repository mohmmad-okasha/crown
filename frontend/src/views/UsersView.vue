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
                    <th scope="col">{{ $t("Admin") }}</th>
                    <th scope="col">{{ $t("Last Login") }}</th>
                    <th scope="col">{{ $t("Created On") }}</th>
                    <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr @contextmenu="showContextMenu" v-for="r in this.users" :key="r.id" @click="row_click(r.id)"
                    @click.right="row_click(r.id)" @dblclick="open_edit_modal" role="button"
                    :class="{ 'selected': r.id === active_index }">
                    <th scope="row" id="id">{{ r.id }}</th>
                    <td>{{ $t(r.first_name) }}</td>
                    <td>{{ $t(r.last_name) }}</td>
                    <td>{{ $t(r.username) }}</td>
                    <td>{{ $t(r.email) }}</td>
                    <td>{{ $t(r.is_superuser) }}</td>
                    <td>{{ r.last_login.substring(0, 10) }}</td>
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
    <!-- <div class="modal  fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
          aria-labelledby="staticBackdropLabel" aria-hidden="true">
          <div class="modal-dialog modal-xl">
              <div class="modal-content">
                  <div class="modal-header">
                      <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add user") }}</h5>
                      <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit user") }}</h5>
                      <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                      </button>
                  </div>
                  <div class="modal-body">

                      <form>

                          <div class="row">

                              <div class="form-group col-md">
                                  <label for="name"> {{ $t("name") }}</label>
                                  <input id="name" v-model="user.name"
                                      :class="{ 'is-invalid': !this.user.name && this.validate, 'is-valid': this.user.name && this.validate }"
                                      type="text" class="form-control">
                                  <div v-if="!this.user.name && this.validate" class="invalid-feedback hidden">
                                      {{ $t("Please Enter The name") }}
                                  </div>
                              </div>

                              <div class="form-group col-md">
                                  <label for="country"> {{ $t("country") }}</label>
                                  <select id="country" v-model="user.country"
                                      :class="{ 'is-invalid': !this.user.country && this.validate, 'is-valid': this.user.country && this.validate }"
                                      type="text" class="form-control">
                                      <option v-for="country in countries" :value="country.name.common"
                                          :key="country.name.common">
                                          {{ country.name.common }}
                                      </option>
                                  </select>
                                  <div v-if="!this.user.country && this.validate" class="invalid-feedback hidden">
                                      {{ $t("Please Enter The country") }}
                                  </div>
                              </div>

                              <div class="form-group col-md">
                                  <label for="city"> {{ $t("city") }}</label>
                                  <input id="city" v-model="user.city"
                                      :class="{ 'is-invalid': !this.user.city && this.validate, 'is-valid': this.user.city && this.validate }"
                                      type="text" class="form-control">

                                  <div v-if="!this.user.city && this.validate" class="invalid-feedback hidden">
                                      {{ $t("Please Enter The city") }}
                                  </div>
                              </div>


                              <div class="form-group col-md">
                                  <label for="area"> {{ $t("area") }}</label>
                                  <input id="area" v-model="user.area"
                                      :class="{ 'is-invalid': !this.user.area && this.validate, 'is-valid': this.user.name && this.validate }"
                                      type="text" class="form-control">
                                  <div v-if="!this.user.area && this.validate" class="invalid-feedback hidden">
                                      {{ $t("Please Enter The area") }}
                                  </div>
                              </div>
                          </div>

                          <div class="row">
                              <div class="form-group col-md">
                                  <label for="rate">{{ $t("rate") }}</label>
                                  <select id="rate" v-model="user.rate" type="text" class="form-control"
                                      :class="{ 'is-invalid': !this.user.rate && this.validate, 'is-valid': this.user.rate && this.validate }">
                                      <option :value="$t('5 Star')">{{ $t("5 Star") }} </option>
                                      <option :value="$t('4 Star')">{{ $t("4 Star") }} </option>
                                      <option :value="$t('3 Star')">{{ $t("3 Star") }} </option>
                                      <option :value="$t('2 Star')">{{ $t("2 Star") }} </option>
                                      <option :value="$t('1 Star')">{{ $t("1 Star") }} </option>
                                  </select>
                                  <div v-if="!this.user.rate && this.validate" class="invalid-feedback hidden">
                                      {{ $t("Please Select the rate") }}
                                  </div>
                              </div>

                              <div class="form-group col-md">
                                  <label for="allotment"> {{ $t("allotment") }}</label>
                                  <input type="number" min="1" value="1" class="form-control" v-model="user.allotment"
                                      id="allotment">
                              </div>

                              <div class="form-group col-md-6">
                                  <label for="user_notes"> {{ $t("Notes") }}</label>
                                  <textarea class="form-control" v-model="user.notes" id="user_notes"
                                      rows="1"></textarea>
                              </div>
                          </div>

                          <div v-if="this.user.allotment > 0" class="card form-group">
                              <h4 class="card-header">
                                  {{ $t("Rooms") }}
                              </h4>

                              <div class="card-body">
                                  <div v-for="i in parseInt(user.allotment)" :key="i">
                                      <div class="card">
                                          <div class="card-header">
                                              {{ $t("Room") + ' ' + i }}
                                          </div>
                                          <div class="card-body">

                                              <input hidden type="text" v-model="user.room[i - 1].user">
                                              <input hidden type="text" v-model="user.room[i - 1].room_id">
                                              <input hidden type="text" v-model="user.room[i - 1].user">
                                              <div class="row">

                                                  <div class="form-group col-md">
                                                      <label for="room_type">{{ $t("Room Type") }}</label>
                                                      <select v-model="user.room[i - 1].room_type" type="text"
                                                          class="form-control"
                                                          :class="{ 'is-invalid': !user.room[i - 1].room_type && validate, 'is-valid': user.room[i - 1].room_type && validate }">
                                                          <option :value="$t('SGL')">{{ $t("SGL") }} </option>
                                                          <option :value="$t('DBL')">{{ $t("DBL") }} </option>
                                                          <option :value="$t('TRPL')">{{ $t("TRPL") }} </option>
                                                          <option :value="$t('QAD')">{{ $t("QAD") }} </option>
                                                      </select>
                                                      <div v-if="!user.room[i - 1].room_type && validate"
                                                          class="invalid-feedback hidden">
                                                          {{ $t("Please Select the room type") }}
                                                      </div>
                                                  </div>

                                                  <div class="form-group col-md">
                                                      <label for="room_categ">{{ $t("Room Category") }}</label>
                                                      <input v-model="user.room[i - 1].room_categ" type="text"
                                                          class="form-control"
                                                          :class="{ 'is-invalid': !user.room[i - 1].room_categ && validate, 'is-valid': user.room[i - 1].room_categ && validate }">
                                                      <div v-if="!user.room[i - 1].room_categ && validate"
                                                          class="invalid-feedback hidden">
                                                          {{ $t("Please Input Room Category") }}
                                                      </div>
                                                  </div>

                                                  <div class="form-group col-md">
                                                      <label for="meals">{{ $t("Meals") }}</label>
                                                      <select v-model="user.room[i - 1].meals" type="text"
                                                          class="form-control"
                                                          :class="{ 'is-invalid': !user.room[i - 1].meals && validate, 'is-valid': user.room[i - 1].meals && validate }">
                                                          <option :value="$t('B.B')">{{ $t("B.B") }} </option>
                                                          <option :value="$t('H.B')">{{ $t("H.B") }} </option>
                                                          <option :value="$t('F.B')">{{ $t("F.B") }} </option>
                                                          <option :value="$t('ALL')">{{ $t("ALL") }} </option>
                                                          <option :value="$t('ULALL')">{{ $t("ULALL") }} </option>
                                                      </select>
                                                      <div v-if="!user.room[i - 1].meals && validate"
                                                          class="invalid-feedback hidden">
                                                          {{ $t("Please Select Meals") }}
                                                      </div>
                                                  </div>

                                              </div>

                                              <div class="row">

                                                  <div class="form-group col-md">
                                                      <label for="cutomer_notes"> {{ $t("Date Range") }}</label>

                                                      <date-picker v-model="user.room[i - 1].range" range clearable
                                                          :auto-submit="true" color="#098290" input-format="DD/MM/YYYY"
                                                          format="DD/MM/YYYY" locale="en" />

                                                  </div>

                                                  <div class="form-group col-md">
                                                      <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                                      <textarea class="form-control" v-model="user.room[i - 1].notes"
                                                          id="cutomer_notes" rows="1"></textarea>
                                                  </div>

                                              </div>
                                          </div>
                                      </div>
                                      <br>
                                  </div>
                              </div>

                          </div>
                      </form>

                  </div>
                  <div class="modal-footer">

                      <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                          @click="this.closeModal">
                          <i class="fa fa-xmark"></i>
                      </button>

                      <button v-if="!edit_mode" type="button" title="save" @click="save_user()"
                          class="btn btn-primary on-hover-sm">
                          <i class="fa fa-floppy-disk"></i></button>

                      <button v-if="edit_mode" type="button" title="delete" @click="delete_user(active_index)"
                          class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                      <button v-if="edit_mode" type="button" title="save" @click="update_user(active_index)"
                          class="btn btn-primary on-hover-sm"> <i class="fa fa-floppy-disk"></i> </button>

                  </div>
              </div>
          </div>
      </div> -->

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
      active_index:'',
      max_id:0,
      users: [],
      
      user: {
        id: "",
        first_name: "",
        last_name: "",
        username: "",
        email: "",
        is_superuser: "",
        last_login: "",
        date_joined: "",
        rols: [],
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
  async mounted() {
    this.get_users();
  },
  methods: {
    // async save_user() {
    //   var response = await fetch(
    //     "http://127.0.0.1:8000/users/api/users_router/",
    //     {
    //       method: "post",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(this.test),
    //     }
    //   );
    //   this.users.push(await response.json());
    // },

    get_users() {
      return my_api.get('backend/users/', { auth: { username: "admin", password: "123", } })
        .then((response) => (this.users = response.data))
        .catch(err => { alert(err) });
    },

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

    open_add_modal() {
      this.edit_mode = false;
      //$('#modal_label').html('Add user');
      this.clear_form();
      $('#addModal').modal('toggle');
    },

    open_edit_modal() {
      this.edit_mode = true;
      this.user.room.forEach(element => {
        element.range = element.range.split(',');
      });
      $('#addModal').modal('toggle');
    },

    closeModal() {
      $('#addModal').modal('hide');
      this.clear_form();
    },

    async row_click(index) {
      this.active_index = index; //to change row color
      await this.get_user(index);
      return true
    },

    clear_form() {
      this.user.first_name = '';
      this.user.last_name = '';
      this.user.username = '';
      this.user.email = '';
      this.user.is_superuser = '';
      this.user.last_login = '';
      this.user.date_joined = '';
      this.validate = false;
    },

    check_form() {
      this.validate = true; //to change inputs color 'red/green'

      if (
        this.user.username &&
        this.user.email &&
        this.user.is_superuser
      ) {
        return true
      } else {
        return false
      }
    },
  },
};
</script>
