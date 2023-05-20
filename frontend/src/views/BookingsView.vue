<template>
    <div class="BookingsView">

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_booking(booking.id)">
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

        <!-- Rooms Monitor -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Bookings Monitor") }} </h6>
                </div>
                <div id="table" class="card-body">
                    <div class="table-responsive">
                        <table class="table-sm table ">
                            <thead>
                                <tr>
                                    <th>Hotel/Room</th>
                                    <th v-for="i in 31" :key="i" scope="col">{{ i }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="r in this.booked_rooms" :key="r.room">
                                    <td>{{ r.room }}</td> <!-- room id + hotel -->
                                    <td v-for="ii in 31" :key="ii">
                                        <button v-for="d in r.dates.split(',')" :key="d" v-show="ii == d.slice(0, 2)"
                                            :title="r.room" type="button" class="btn btn-danger"></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Table Card -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Bookings Table") }} </h6>
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
                                        <th scope="col">{{ $t("book_date") }}</th>
                                        <th scope="col">{{ $t("guest_name") }}</th>
                                        <th scope="col">{{ $t("hotel") }}</th>
                                        <th scope="col">{{ $t("dates") }}</th>
                                        <th scope="col">{{ $t("room_id") }}</th>
                                        <th scope="col">{{ $t("room_type") }}</th>
                                        <th scope="col">{{ $t("status") }}</th>
                                        <th scope="col">{{ $t("guests") }}</th>
                                        <th scope="col">{{ $t("notes") }}</th>
                                        <th scope="col">{{ $t("user") }}</th>
                                        <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="booking in this.Bookings" :key="booking.id"
                                        @click="row_click(booking.id)" @click.right="row_click(booking.id)"
                                        @dblclick="open_edit_modal" role="button"
                                        :class="{ 'selected': booking.id === active_index }">
                                        <th scope="row" id="id">{{ booking.id }}</th>
                                        <td>{{ booking.book_date }}</td>
                                        <td>{{ $t(booking.guest_name) }}</td>
                                        <td>{{ $t(booking.hotel) }}</td>
                                        <td>{{ $t(booking.dates.substr(0, 20)) }}</td>
                                        <td>{{ $t(booking.room_id) }}</td>
                                        <td>{{ $t(booking.room_type) }}</td>
                                        <td>{{ $t(booking.status) }}</td>
                                        <td>{{ $t(booking.guests) }}</td>
                                        <td>{{ $t(booking.notes) }}</td>
                                        <td>{{ $t(booking.user) }}</td>

                                        <td class="no_print">

                                            <div class="btn-group" role="group">
                                                <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                                    <i class="fa fa-gear on-hover"></i>
                                                </button>
                                                <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                    x-placement="bottom-start"
                                                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                    <a class="dropdown-item" @click="delete_booking(booking.id)">
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
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add booking") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit booking") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>
                            <div class="form-group">
                                <label for="book_date">{{ $t("Booking Date") }}</label>
                                <input id="book_date" v-model="booking.book_date" type="datetime-local"
                                    :class="{ 'is-invalid': !this.booking.book_date && this.validate, 'is-valid': this.booking.book_date && this.validate }"
                                    class="form-control">
                                <div v-if="!this.booking.book_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select The Date") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="guest_name">{{ $t("guest name") }}</label>
                                <input id="guest_name" v-model="booking.guest_name" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.booking.guest_name && this.validate, 'is-valid': this.booking.guest_name && this.validate }">
                                <div v-if="!this.booking.guest_name && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select guest_name") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="hotel">{{ $t("Hotel") }}</label>
                                <v-select id="hotel" v-model="booking.hotel" v-on:change="get_rooms" :options="hotels"
                                    :class="{ 'is-invalid': !this.booking.hotel && this.validate, 'is-valid': this.booking.hotel && this.validate }" />

                                <div v-if="!this.booking.hotel && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select hotel") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="room_id">{{ $t("Room ID") }}</label>
                                <select id="airline" v-model="booking.room_id" v-on:change="get_room_type(booking.room_id)"
                                    type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.booking.room_id && this.validate, 'is-valid': this.booking.airline && this.validate }">
                                    <option v-for="room in rooms" v-bind:value="room.room_id" :key="room.room_id">{{
                                        room.room_id }}</option>
                                </select>
                                <div v-if="!this.booking.room_id && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select room_id") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="room_type">{{ $t("Room Type") }}</label>
                                <input readonly id="room_type" v-model="booking.room_type" type="text" class="form-control">
                            </div>

                            <label v-show="this.booking.room_id" for="dates">{{ $t("Select Date") }}</label>
                            <div v-show="this.booking.room_id" class="form-group card" id="dates" style="width: 100%;">
                                <div class="card-body">
                                    <date-picker v-model="booking.dates" :min="min_date" :max="max_date"
                                        :disable="disable_dates" range clearable locale="en" inline :auto-submit="true"
                                        custom-input="none" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY" />
                                </div>
                            </div>


                            <!-- 


                            <div class="form-group ">
                                <label for="check_in_date"> {{ $t("check_in_date") }}</label>
                                <input id="check_in_date" v-model="booking.check_in_date"
                                    :class="{ 'is-invalid': !this.booking.check_in_date && this.validate, 'is-valid': this.booking.arrival_date && this.validate }"
                                    type="date" class="form-control">
                                <div v-if="!this.booking.check_in_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The check_in_date") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="check_out_date"> {{ $t("check_out_date") }}</label>
                                <input id="check_out_date" v-model="booking.check_out_date"
                                    :class="{ 'is-invalid': !this.booking.check_out_date && this.validate, 'is-valid': this.booking.arrival_date && this.validate }"
                                    type="date" class="form-control">
                                <div v-if="!this.booking.check_out_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The check_out_date") }}
                                </div>
                            </div> -->

                            <div class="form-group ">
                                <label for="guests"> {{ $t("guests") }}</label>
                                <input id="guests" v-model="booking.guests"
                                    :class="{ 'is-invalid': !this.booking.guests && this.validate, 'is-valid': this.booking.guests && this.validate }"
                                    type="number" class="form-control">
                                <div v-if="!this.booking.guests && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The guests") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="status">{{ $t("Status") }}</label>
                                <select id="status" v-model="booking.status" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.booking.status && this.validate, 'is-valid': this.booking.status && this.validate }">
                                    <option selected :value="$t('Booked')">{{ $t("Booked") }} </option>
                                    <option :value="$t('No Show')">{{ $t("No Show") }} </option>

                                </select>
                                <div v-if="!this.booking.status && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select the status") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                <textarea class="form-control" v-model="booking.notes" id="cutomer_notes"
                                    rows="1"></textarea>
                            </div>

                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_booking()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_booking(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_booking(active_index)"
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

import vSelect from 'vue-select'

import 'vue-select/dist/vue-select.css';
export default {
    name: 'BookingsView',
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker,
        vSelect
    },

    data() {
        return {
            //date:'',
            user_name: '',
            validate: false, //for check forms
            base_url: window.location.origin + '/media/bookings/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            Bookings: [],
            rooms: [],
            hotels: [],
            dates: [],
            test: [],
            range_dates: [],
            enable_dates: [],
            disable_dates: [],
            booked_dates: [],
            all_booked_dates: [],
            // monitoring
            booked_rooms: [],
            pended_rooms: [],
            //
            min_date: '',
            max_date: '',
            booking: {
                book_date: new Date().toISOString().slice(0, 16),
                dates: "",
                all_dates: [],
                guest_name: "",
                hotel: "",
                room_id: "",
                room_type: "",
                status: "",
                guests: "",
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

    watch: {
        'booking.hotel': function (newValue) {
            this.get_rooms()
        },
        enable_dates: function (newValue) {
            this.findMinMaxDate()
        },
    },

    async mounted() {
        this.booking.user = localStorage.getItem('user_name')
        this.get_booked_rooms()
        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////
        await this.get_Bookings();
        await this.get_hotels();
        //await this.get_rooms();
    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/bookings/?search=" + data,
                }).then((response) => (this.Bookings = response.data));
            } else {
                this.get_Bookings();
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
            document.getElementById('head_txt').innerHTML = this.$t("Bookings");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        get_Bookings() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/bookings/')
                .then((response) => (this.Bookings = response.data))
                .catch(err => { alert(err) });
        },

        get_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_rooms/?hotel=" + this.booking.hotel,
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.rooms = response.data[0]));
        },

        get_hotels() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_hotels/",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.hotels = response.data));
        },

        async save_booking() {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.booking.dates = this.booking.dates.toString();
                    var response = await fetch(domain_url + "/backend/bookings/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.booking),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                    this.get_Bookings();
                    await this.get_max_id();
                    this.closeModal();
                }
            } catch (error) { console.error(); }
        },

        async update_booking(id) {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.booking.dates = this.booking.dates.toString();
                    var response = await fetch(domain_url + "/backend/bookings/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.booking),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                    this.max_id = this.booking.id
                    this.get_Bookings();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_booking(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/bookings/' + id + '/')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                            await this.get_Bookings(); this.closeModal();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_booking(id) {
            return axios({
                method: "get",
                url: domain_url + "/backend/bookings/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.booking = response.data[0]));
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Bookings",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        get_room_type(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_type/", params: { room_id: value, hotel: this.booking.hotel },
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.booking.room_type = response.data[0][0])).then(this.get_room_dates(value));
        },

        get_room_dates(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_dates/", params: { room_id: value, hotel: this.booking.hotel },
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.get_room_range(response.data[0])));
        },



        // for monitoring
        get_booked_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_booked_rooms/",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.booked_rooms = response.data.booked_rooms));
        },

        get_booked_dates() {
            if (this.booking.room_id && this.booking.hotel) {

                this.booked_dates = [];
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_booked_dates/", params: { room_id: this.booking.room_id, hotel: this.booking.hotel },
                    //auth: { username: "admin", password: "123", },
                    //}).then((response) => (this.booked_dates = response.data[0].replace(', ', ',').split(",")));
                }).then((response) => (this.booked_dates = response.data[0].split(', ')));
            }
        },

        findMinMaxDate() {
            //get min & max date , if one date set min=max to enable this range in datepiker
            this.min_date = this.booking.dates[0];
            this.max_date = this.booking.dates[1];
            if (!this.max_date) { this.max_date = this.min_date }
            this.filter_enabled_dates();
        },

        get_room_range(range) {
            //to get min & max for this room
            this.min_date = range.split(",")[0];
            this.max_date = range.split(",")[1];
            this.filter_enabled_dates();
        },

        async filter_enabled_dates() {
            // to get booked dates for this room and diable it
            try {
                await this.get_booked_dates();
            } catch (error) { }

            this.all_booked_dates = [];
            this.disable_dates = [];

            //get all dates in the range
            this.booked_dates.forEach((element) => {

                const minDateParts = element.split(',')[0].split('/');
                const maxDateParts = element.split(',')[1].split('/');
                const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

                const currentDate = new Date(startDate);
                while (currentDate < endDate) {
                    this.all_booked_dates.push(currentDate.toLocaleDateString("en-GB"));
                    currentDate.setDate(currentDate.getDate() + 1);
                }

            });

            //copy all dates from all_booked_dates to disable_dates
            this.all_booked_dates.forEach(element => this.disable_dates.push(element));

            // to enable edit booked dates
            if (this.edit_mode) {
                //get all dates in the range
                this.booking.all_dates = [];

                const minDateParts = this.booking.dates[0].split('/');
                const maxDateParts = this.booking.dates[1].split('/');
                const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

                const currentDate = new Date(startDate);
                while (currentDate <= endDate) {
                    this.booking.all_dates.push(currentDate.toLocaleDateString("en-GB"));
                    currentDate.setDate(currentDate.getDate() + 1);
                }

                this.disable_dates = this.disable_dates.filter((el) => !this.booking.all_dates.includes(el));
            }


        },



        findMinMaxDate_old() {

            let min = this.enable_dates[0];
            let max = this.enable_dates[0];
            for (let i = 0; i < this.enable_dates.length; i++) {
                if (this.enable_dates[i] > max) { max = this.enable_dates[i] }
                if (this.enable_dates[i] < min) { min = this.enable_dates[i] }
            }



            this.min_date = min;
            this.max_date = max;
            this.filter_enabled_dates();

        },
        async filter_enabled_dates_old() {
            // to get all dates in the range then push not needed dates to disabled_dates
            const minDateParts = this.min_date.split('/');
            const maxDateParts = this.max_date.split('/');
            const startDate = new Date(
                minDateParts[2],
                minDateParts[1] - 1,
                minDateParts[0]
            );
            const endDate = new Date(
                maxDateParts[2],
                maxDateParts[1] - 1,
                maxDateParts[0]
            );

            // to get booked dates for this room and diable it
            try {
                await this.get_booked_dates();
                this.booked_dates.sort();
            } catch (error) { }

            const currentDate = new Date(startDate);
            this.disable_dates = [];
            while (currentDate <= endDate) {
                if (this.enable_dates.includes(currentDate.toLocaleDateString("en-GB"))) { }
                else {
                    this.disable_dates.push(currentDate.toLocaleDateString("en-GB"));
                }
                if (this.booked_dates.length > 0 && this.booked_dates.includes(currentDate.toLocaleDateString("en-GB"))) {
                    this.disable_dates.push(currentDate.toLocaleDateString("en-GB"));
                }

                currentDate.setDate(currentDate.getDate() + 1);
            }


            // to enable edit booked dates
            if (this.edit_mode) {
                this.disable_dates = this.disable_dates.filter((el) => !this.booking.dates.includes(el));
            }



        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add booking');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            //return
            this.disable_dates = [];
            this.edit_mode = true;
            //$('#modal_label').html('Edit booking');
            $('#addModal').modal('toggle');

        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            await this.get_booking(index);


            //this.enable_dates = this.booking.dates;
            //this.enable_dates = this.enable_dates.split(",");// convert text to array then datepicker can read dates
            this.booking.dates = this.booking.dates.split(",");// 
            await this.get_room_type(this.booking.room_id);
            await this.findMinMaxDate();

            this.active_index = index; //to change row color
        },

        clear_form() {
            //this.booking.book_date = '';
            this.booking.guest_name = '';
            this.booking.hotel = '';
            this.booking.dates = '';
            this.booking.room_id = '';
            this.booking.room_type = '';
            this.booking.status = '';
            this.booking.guests = '';
            this.booking.notes = '';
            this.enable_dates = [];
            this.disable_dates = [];
            this.min_date = '';
            this.max_date = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.booking.book_date &&
                this.booking.guest_name &&
                this.booking.hotel &&
                this.booking.dates &&
                this.booking.room_id &&
                this.booking.room_type &&
                this.booking.status &&
                this.booking.guests
            ) {
                return true
            } else {
                return false
            }
        },

    },
}
</script>
