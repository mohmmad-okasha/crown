<template>
    <!-- &nbsp; -->
    <div class="RoomsView">

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_room(room.id)">
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
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Rooms Table") }} </h6>
                    <div class="dropdown no-arrow">

                        <div class="btn-group" role="group">
                            <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
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
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">{{ $t("hotel") }}</th>
                                        <th scope="col">{{ $t("room_id") }}</th>
                                        <th scope="col">{{ $t("room_type") }}</th>
                                        <th scope="col">{{ $t("dates") }}</th>
                                        <th scope="col">{{ $t("notes") }}</th>
                                        <th scope="col">{{ $t("User") }}</th>
                                        <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="r in this.Rooms" :key="r.room_id"
                                        @click="row_click(r.id)" @click.right="row_click(r.id)" @dblclick="open_edit_modal"
                                        role="button" :class="{ 'selected': r.id === active_index }">
                                        <th scope="row" id="id">{{ r.id }}</th>
                                        <td>{{ $t(r.hotel) }}</td>
                                        <td>{{ $t(r.room_id) }}</td>
                                        <td>{{ $t(r.room_type) }}</td>
                                        <td>{{ $t(r.dates.substr(0, 20)) }}</td>
                                        <td>{{ $t(r.notes) }}</td>
                                        <td>{{ $t(r.user) }}</td>

                                        <td class="no_print">

                                            <div class="btn-group" role="group">
                                                <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                                    <i class="fa fa-gear on-hover"></i>
                                                </button>
                                                <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                    x-placement="bottom-start"
                                                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                    <a class="dropdown-item" @click="delete_room(room.id)">
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
            <div class="modal-dialog ">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add room") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit room") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>


                            <div class="form-group ">
                                <label for="hotel"> {{ $t("hotel") }}</label>
                                <input id="hotel" v-model="room.hotel"
                                    :class="{ 'is-invalid': !this.room.hotel && this.validate, 'is-valid': this.room.hotel && this.validate }"
                                    type="text" class="form-control">
                                <div v-if="!this.room.hotel && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The hotel") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="room_id"> {{ $t("room_id") }}</label>
                                <input id="room_id" v-model="room.room_id"
                                    :class="{ 'is-invalid': !this.room.room_id && this.validate, 'is-valid': this.room.room_id && this.validate }"
                                    type="text" class="form-control">
                                <div v-if="!this.room.room_id && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The room_id") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="room_type">{{ $t("room_type") }}</label>
                                <select id="room_type" v-model="room.room_type" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.room.room_type && this.validate, 'is-valid': this.room.room_type && this.validate }">
                                    <option :value="$t('Single')">{{ $t("Single") }} </option>
                                    <option :value="$t('Double')">{{ $t("Double") }} </option>
                                </select>
                                <div v-if="!this.room.room_type && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select the room type") }}
                                </div>
                            </div>

                            <label for="dates">{{ $t("Select Date") }}</label>
                            <div class="form-group card" id="dates" style="width: 100%;">
                                <div class="card-body">
                                    <date-picker v-model="room.dates" multiple clearable inline :auto-submit="true"
                                        custom-input="none" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY"
                                        locale="en" />
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="room_notes"> {{ $t("Notes") }}</label>
                                <textarea class="form-control" v-model="room.notes" id="room_notes" rows="1"></textarea>
                            </div>

                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_room()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_room(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_room(active_index)"
                            class="btn btn-primary on-hover-sm"> <i class="fa fa-floppy-disk"></i> </button>

                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import { lang, change_lang } from '../main';

import NavBar from '../components/parts/NavBar.vue'

import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
import swal from 'sweetalert';

export default {
    name: 'RoomsView',
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker

    },

    data() {
        return {
            dateArray: [],
            validate: false, //for check forms
            base_url: window.location.origin + '/media/rooms/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            Rooms: [],
            hotels: [],
            room: {
                hotel: "",
                room_id: "",
                room_type: "",
                dates: [],
                notes: "",
                user: "",
            },
            edit_mode: false,
            max_id: 0,
            isContextMenuActive: false,
            menuStyle: {
                display: 'none',
                top: 0,
                left: 0
            }
        }
    },

    async mounted() {
        this.room.user = localStorage.getItem('user_name')

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////
        await this.get_Rooms();
        await this.get_hotels();
        //await this.get_room();

    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/rooms/?search=" + data,
                }).then((response) => (this.Rooms = response.data));
            } else {
                this.get_Rooms();
            }
        },
    },

    methods: {

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

        PrintDiv(id) {
            var divToPrint = document.getElementById(id);
            var popupWin = window.open('', '_blank', 'width=100000,height=10000');
            document.getElementById('head_txt').style.display = "block";
            document.getElementById('head_txt').innerHTML = this.$t("Rooms");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        get_Rooms() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/rooms/')
                .then((response) => (this.Rooms = response.data))
                .catch(err => { alert(err) });
        },

        get_hotels() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_hotels/",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.hotels = response.data[0]));
        },

        async save_room() {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.room.dates = this.room.dates.toString();
                    var response = await fetch(domain_url + "/backend/rooms/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.room),
                    });


                    if (!response.ok) {
                        // handle the error
                        var errorMessage = "Error: " + response.status + " " + response.statusText;
                        swal(errorMessage, { icon: 'error' });
                    } else {
                        // Request was successful
                        swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                        this.get_Rooms();
                        await this.get_max_id();
                        this.closeModal();
                    }





                }
            } catch (error) { console.error(); }
        },

        async update_room(id) {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.room.dates = this.room.dates.toString();

                    var response = await fetch(domain_url + "/backend/rooms/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.room),
                    });

                    if (!response.ok) {
                        // handle the error
                        var errorMessage = "Error: " + response.status + " " + response.statusText;
                        swal(errorMessage, { icon: 'error' });
                    } else {
                        // Request was successful
                        swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                        this.max_id = this.room.id
                        this.get_Rooms();
                        this.closeModal();
                        this.edit_mode = false;
                    }
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_room(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            var response = await fetch(domain_url + '/backend/rooms/' + id + '/', {
                                method: "delete",
                                headers: { "Content-Type": "application/json", },

                            });
                            if (!response.ok) {
                                // handle the error
                                var errorMessage = "Error: " + response.status + " " + response.statusText;
                                swal(errorMessage, { icon: 'error' });
                            } else {
                                // Request was successful
                                swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                                await this.get_Rooms(); this.closeModal();
                            }

                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_room(id) {
            return axios({
                method: "get",
                url: domain_url + "/backend/rooms/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.room = response.data[0]));
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Rooms",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        get_room_type(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_type/?room_id=" + value,
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.room.room_type = response.data[0]));
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add room');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            //$('#modal_label').html('Edit room');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            this.active_index = index; //to change row color
            await this.get_room(index);

            this.room.dates = this.room.dates.split(",");// convert text to array
        },

        clear_form() {
            this.room.hotel = '';
            this.room.room_id = '';
            this.room.room_type = '';
            this.room.dates = [];
            this.room.notes = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.room.hotel &&
                this.room.room_id &&
                this.room.room_type &&
                this.room.dates
            ) {
                return true
            } else {
                return false
            }
        },

    },
}
</script>
