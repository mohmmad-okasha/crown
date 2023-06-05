<template>
    <!-- &nbsp; -->
    <div class="Hotel_roomsView">

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_Hotel_room(Hotel_room.id)">
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
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Hotel_rooms Table") }} </h6>
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
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">{{ $t("Hotel") }}</th>
                                    <th scope="col">{{ $t("Rooms Count") }}</th>
                                    <th scope="col">{{ $t("Rooms Type") }}</th>
                                    <th scope="col">{{ $t("Notes") }}</th>
                                    <th scope="col">{{ $t("Status") }}</th>
                                    <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr @contextmenu="showContextMenu" v-for="Hotel_room in this.Hotel_rooms" :key="Hotel_room.id"
                                    @click="row_click(Hotel_room.id)" @click.right="row_click(Hotel_room.id)"
                                    @dblclick="open_edit_modal" role="button"
                                    :class="{ 'selected': Hotel_room.id === active_index }">
                                    <th scope="row" id="id">{{ Hotel_room.id }}</th>
                                    <td>{{ $t(Hotel_room.name) }}</td>
                                    <td>{{ $t(Hotel_room.rooms_count) }}</td>
                                    <td>{{ $t(Hotel_room.rooms_type) }}</td>
                                    <td>{{ $t(Hotel_room.notes) }}</td>
                                    <td>
                                        <img v-if="Hotel_room.count > 0 " width="30px" height="30px"
                                            src="https://img.icons8.com/color/2x/ok--v1">
                                        <img v-if="Hotel_room.count <= 0" width="30px" height="30px"
                                            src="https://img.icons8.com/color/2x/cancel--v1">
                                    </td>

                                    <td class="no_print">

                                        <div class="btn-group" role="group">
                                            <button id="btnGroupVerticalDrop1" type="button"
                                                class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true"
                                                aria-expanded="true">
                                                <i class="fa fa-gear on-hover"></i>
                                            </button>
                                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                x-placement="bottom-start"
                                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                <a class="dropdown-item" @click="delete_Hotel_room(Hotel_room.id)">
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
                        <!-- to get id of selected record -->
                        <input hidden type="text" v-model="active_index" id="row_id" />
                    </form>
                </div>
            </div>
        </div>

        <!-- to get search value from navbar -->
        <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>

        <!-- modal -->
        <div class="modal fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add Hotel_room") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit Hotel_room") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>
                            <div class="form-group">
                                <label for="Hotel_room_code">{{ $t("Code") }}</label>
                                <input id="Hotel_room_code" v-model="Hotel_room.code" type="text"
                                    :class="{ 'is-invalid': !this.Hotel_room.code && this.validate, 'is-valid': this.Hotel_room.code && this.validate }"
                                    class="form-control">
                                <div v-if="!this.Hotel_room.code && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The code") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="airline">{{ $t("Airline") }}</label>
                                <select id="airline" v-model="Hotel_room.airline" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.Hotel_room.airline && this.validate, 'is-valid': this.Hotel_room.airline && this.validate }">
                                    <option selected :value="$t('R1')">{{ $t("R1") }}</option>
                                    <option :value="$t('RJ')">{{ $t("RJ") }}</option>
                                </select>
                                <div v-if="!this.Hotel_room.airline && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select airline") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="from_airport">{{ $t("From Airport") }}</label>
                                <select id="from_airport" v-model="Hotel_room.from_airport" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.Hotel_room.from_airport && this.validate, 'is-valid': this.Hotel_room.from_airport && this.validate }">
                                    <option selected :value="$t('AMM')">{{ $t("AMM") }}</option>
                                    <option :value="$t('IST')">{{ $t("IST") }}</option>
                                    <option :value="$t('TZX')">{{ $t("TZX") }}</option>
                                </select>
                                <div v-if="!this.Hotel_room.from_airport && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select from airport") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="to_airport">{{ $t("To Airport") }}</label>
                                <select id="to_airport" v-model="Hotel_room.to_airport" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.Hotel_room.to_airport && this.validate, 'is-valid': this.Hotel_room.to_airport && this.validate }">
                                    <option selected :value="$t('AMM')">{{ $t("AMM") }}</option>
                                    <option :value="$t('IST')">{{ $t("IST") }}</option>
                                    <option :value="$t('TZX')">{{ $t("TZX") }}</option>
                                </select>
                                <div v-if="!this.Hotel_room.to_airport && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select to airport") }}
                                </div>
                            </div>

                            <div class="form-group mb-2">
                                <label for="departure_date">{{ $t("Departure date") }}</label>

                                <input id="departure_date" v-model="Hotel_room.departure_date" type="date"
                                    :class="{ 'is-invalid': !this.Hotel_room.departure_date && this.validate, 'is-valid': this.Hotel_room.departure_date && this.validate }"
                                    class="form-control">
                                <div v-if="!this.Hotel_room.type && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter departure_date") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="arrival_date"> {{ $t("Arrival date") }}</label>
                                <input id="arrival_date" v-model="Hotel_room.arrival_date"
                                    :class="{ 'is-invalid': !this.Hotel_room.arrival_date && this.validate, 'is-valid': this.Hotel_room.arrival_date && this.validate }"
                                    type="date" class="form-control">
                                <div v-if="!this.Hotel_room.arrival_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The arrival date") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="seats"> {{ $t("Seats") }}</label>
                                <input id="seats" v-model="Hotel_room.seats"
                                    :class="{ 'is-invalid': !this.Hotel_room.seats && this.validate, 'is-valid': this.Hotel_room.seats && this.validate }"
                                    type="number" class="form-control">
                                <div v-if="!this.Hotel_room.seats && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The seats") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="status">{{ $t("Status") }}</label>
                                <select id="status" v-model="Hotel_room.status" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.Hotel_room.status && this.validate, 'is-valid': this.Hotel_room.status && this.validate }">
                                    <option selected :value="$t('enable')">{{ $t("Enable") }} </option>
                                    <option :value="$t('disabled')">{{ $t("Disabled") }} </option>

                                </select>
                                <div v-if="!this.Hotel_room.status && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select the status") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                <textarea class="form-control" v-model="Hotel_room.notes" id="cutomer_notes"
                                    rows="1"></textarea>
                            </div>

                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_Hotel_room()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_Hotel_room(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_Hotel_room(active_index)"
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

export default {
    name: 'Hotel_roomsView',
    components: {
        NavBar,
    },

    data() {
        return {
            date:'',
            validate: false, //for check forms
            base_url: window.location.origin + '/media/Hotel_rooms/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            Hotel_rooms: [],
            Hotel_room: {
                code: "",
                airline: "",
                from_airport: "",
                to_airport: "",
                departure_date: "",
                arrival_date: "",
                seats: "",
                status: "",
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
        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////
        await this.get_Hotel_rooms();
    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/Hotel_rooms/?search=" + data,
                }).then((response) => (this.Hotel_rooms = response.data));
            } else {
                this.get_Hotel_rooms();
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
            document.getElementById('head_txt').innerHTML = this.$t("Hotel_rooms");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        onFileChange(e) {
            try {
                this.img_file = e.target.files[0];
                this.previewImage = URL.createObjectURL(this.img_file);
            } catch (err) {
                alert(err);
            }
        },

        uploadImage() {
            if (this.img_file) {
                let formData = new FormData()
                formData.append('image', this.img_file)
                return axios.post(domain_url + "/backend/upload_file/?file_name=/Hotel_rooms/" + this.max_id + '_' + this.Hotel_room.name + '.png', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    .then(response => {
                        // handle successful response
                    })
                    .catch(error => {
                        alert(error)
                    })
            }
        },

        remove_file(file_name) {
            return axios({
                method: "get",
                url: domain_url + "/backend/remove_file/?file_name=" + file_name,
                auth: { username: "admin", password: "123" },
            });
        },

        get_Hotel_rooms() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/Hotel_rooms/')
                .then((response) => (this.Hotel_rooms = response.data))
                .catch(err => { alert(err) });
        },

        async save_Hotel_room() {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/Hotel_rooms/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.Hotel_room),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                    this.get_Hotel_rooms();
                    await this.get_max_id();
                    await this.uploadImage();
                    this.closeModal();
                }
            } catch (error) { console.error(); }
        },

        async update_Hotel_room(id) {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/Hotel_rooms/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.Hotel_room),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                    this.max_id = this.Hotel_room.id
                    await this.uploadImage();
                    this.get_Hotel_rooms();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_Hotel_room(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/Hotel_rooms/' + id + '/')
                            this.remove_file('/Hotel_rooms/' + id + '_' + this.Hotel_room.name + '.png')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                            await this.get_Hotel_rooms(); this.closeModal();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_Hotel_room(id) {
            return axios({
                method: "get",
                url: domain_url + "/backend/Hotel_rooms/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.Hotel_room = response.data[0]));
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Hotel_rooms",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add Hotel_room');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            //$('#modal_label').html('Edit Hotel_room');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            this.active_index = index; //to change row color
            await this.get_Hotel_room(index);
        },

        clear_form() {
            this.Hotel_room.code = '';
            this.Hotel_room.airline = '';
            this.Hotel_room.from_airport = '';
            this.Hotel_room.to_airport = '';
            this.Hotel_room.departure_date = '';
            this.Hotel_room.arrival_date = '';
            this.Hotel_room.seats = '';
            this.Hotel_room.status = '';
            this.Hotel_room.notes = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.Hotel_room.code &&
                this.Hotel_room.airline &&
                this.Hotel_room.from_airport &&
                this.Hotel_room.to_airport &&
                this.Hotel_room.departure_date &&
                this.Hotel_room.arrival_date &&
                this.Hotel_room.seats &&
                this.Hotel_room.status
            ) {
                return true
            } else {
                return false
            }
        },

    },
}

</script>
