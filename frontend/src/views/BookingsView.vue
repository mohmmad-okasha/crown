<template>
    <div class="BookingsView">
        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_booking(this_row.id)">
                    <i class="fa fa-trash"></i>
                    {{ $t("Delete") }}
                </li>
                <li class="ltr dropdown-item" @click="open_edit_modal">
                    <i class="fa fa-pen-to-square"></i>
                    {{ $t("Edit") }}
                </li>
                <li class="dropdown-item" @click="PrintDiv('booking_data')">
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
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Bookings Table") }} </h6>
                    <div class="btn-group" role="group">
                        <button type="button" title="Print" class="btn" @click="PrintDiv('table')">
                            <i class="fa fa-print on-hover"></i>
                        </button>

                        <button type="button" title="Add" class="btn" @click="open_add_modal">
                            <i class="fa fa-plus on-hover"></i>
                        </button>

                    </div>


                </div>
                <!-- Card Body -->
                <div id="table" class="card-body">

                    <div class="d-flex ">

                        <nav>
                            <ul class="pagination pagination-sm">
                                <li class="page-item" :class="{ active: activeNav === 1 }" @click="activeNav = 1"><button
                                        class="page-link">{{ $t("last week") }}</button></li>
                                <li class="page-item" :class="{ active: activeNav === 2 }" @click="activeNav = 2"><button
                                        class="page-link">{{ $t("last month") }}</button></li>
                                <li class="page-item" :class="{ active: activeNav === 3 }" @click="activeNav = 3"><button
                                        class="page-link">{{ $t("last year") }}</button></li>
                                <li class="page-item" @click="activeNav = null">
                                    <input type="text" class="custom-input form-control form-control-sm" placeholder="Custome Date Range"
                                        aria-label="Range">
                                    <date-picker v-model="searchRange" :range="true" clearable locale="en"
                                        :auto-submit="true" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY"
                                        display-format="DD/MM/YYYY" custom-input=".custom-input" />
                                </li>
                            </ul>
                        </nav>

                        <div class="col-sm-3 m-1">

                        </div>

                    </div>
                    <div class="card-header cnter" style="display: none;" id="head_txt"></div>
                    <form class="site-form-table">
                        <div id="main_table" class="table-responsive">
                            <table class="table table-hover">
                                <thead class="sticky_header">
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">{{ $t("Booking on") }}</th>
                                        <th scope="col">{{ $t("Names") }}</th>
                                        <th scope="col">{{ $t("Number") }}</th>
                                        <th scope="col">{{ $t("Hotel") }}</th>
                                        <th scope="col">{{ $t("Duration") }}</th>
                                        <th scope="col">{{ $t("Room ID") }}</th>
                                        <th scope="col">{{ $t("Room Type") }}</th>
                                        <th scope="col">{{ $t("Status") }}</th>
                                        <th scope="col">{{ $t("Notes") }}</th>
                                        <th scope="col">{{ $t("User") }}</th>
                                        <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="booking in this.booking_rows"
                                        :key="booking.id" @click="row_click(booking.id)"
                                        @click.right="row_click(booking.id)" @dblclick="open_edit_modal" role="button"
                                        :class="{ 'selected': booking.id === active_index }">
                                        <th scope="row" id="id">{{ booking.id }}</th>
                                        <td>{{ formatDate(booking.book_date) }}</td>
                                        <td>{{ $t(booking.persons_names + ' , ' + booking.kids_names) }}</td>
                                        <td>{{ $t(booking.persons_number + booking.kids_number) }}</td>
                                        <td>{{ $t(booking.hotel) }}</td>
                                        <td>{{ $t(booking.dates) }}</td>
                                        <td>{{ $t(booking.room_id) }}</td>
                                        <td>{{ $t(booking.room_type) }}</td>
                                        <td>{{ $t(booking.status) }}</td>
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
                                                    <a class="dropdown-item" @click="PrintDiv('booking_data')">
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
                                <input id="book_date" v-model="this_row.book_date" type="datetime-local"
                                    :class="{ 'is-invalid': !this.this_row.book_date && this.validate, 'is-valid': this.this_row.book_date && this.validate }"
                                    class="form-control">
                                <div v-if="!this.this_row.book_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select The Date") }}
                                </div>
                            </div>

                            <div class="row g-3 form-group">


                                <div class="form-group col-sm-7">
                                    <label for="hotel">{{ $t("Hotel") }}</label>
                                    <v-select id="hotel" v-model="this_row.hotel" :options="hotels"
                                        :class="{ 'is-invalid': !this_row.hotel && validate, 'is-valid': this_row.hotel && validate }" />

                                    <div v-if="!this_row.hotel && validate" class="invalid-feedback hidden">
                                        {{ $t("Please Select hotel") }}
                                    </div>
                                </div>

                                <div class="form-group col-sm-3">
                                    <label for="room_id">{{ $t("Room ID") }}</label>
                                    <select id="room_id" v-model="this_row.room_id" type="text" class="form-control"
                                        :class="{ 'is-invalid': !this.this_row.room_id && this.validate, 'is-valid': this.this_row.room_id && this.validate }">
                                        <option v-for="room in rooms" v-bind:value="room" :key="room">{{
                                            room }}</option>
                                    </select>
                                    <div v-if="!this.this_row.room_id && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Select room_id") }}
                                    </div>
                                </div>

                                <div class="form-group col-sm-2">
                                    <label for="room_type">{{ $t("Type") }}</label>
                                    <input readonly id="room_type" v-model="this_row.room_type" type="text"
                                        class="form-control">
                                </div>
                            </div>


                            <label v-show="this.this_row.room_id" for="dates">{{ $t("Select Date") }}</label>
                            <div v-show="this.this_row.room_id" class="form-group card" id="dates" style="width: 100%;">
                                <div class="card-body">
                                    <date-picker v-model="this_row.dates" :min="min_date" :max="max_date"
                                        :disable="disable_dates" :range="is_range" clearable locale="en" inline
                                        :auto-submit="false" custom-input="none" color="#098290" input-format="DD/MM/YYYY"
                                        format="DD/MM/YYYY" />
                                </div>

                                <input readonly id="dates" v-model="this_row.dates" type="text"
                                    :class="{ 'is-invalid': !this.this_row.dates && this.validate, 'is-valid': this.this_row.dates && this.validate }"
                                    class="form-control">
                                <div v-if="!this.this_row.dates && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select The Date") }}
                                </div>
                            </div>

                            <div class="card form-group">
                                <div class="card-header">
                                    {{ $t("Guests") }}
                                </div>
                                <div class="card-body">

                                    <div class="row g-3 form-group">
                                        <div class="col">
                                            <label for="Adults"> {{ $t("Adults") }}</label>
                                            <input id="Adults" v-model="this_row.persons_number" min="1" max="15"
                                                :class="{ 'is-invalid': !this.this_row.persons_number && this.validate, 'is-valid': this.this_row.persons_number && this.validate }"
                                                type="number" class="form-control">
                                            <div v-if="!this.this_row.persons_number && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Number of Persons") }}
                                            </div>
                                        </div>
                                        <div class="col">
                                            <label for="Children"> {{ $t("Children") }}</label>
                                            <input id="Children" v-model="this_row.kids_number" min="0" max="10"
                                                :class="{ 'is-invalid': this.this_row.kids_number < 0 && this.validate, 'is-valid': this.this_row.kids_number && this.validate }"
                                                type="number" class="form-control">
                                            <div v-if="this.this_row.kids_number < 0 && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Number of Kids") }}
                                            </div>
                                        </div>
                                    </div>

                                    <div v-if="this_row.persons_number > 0">
                                        <div v-for=" i in parseInt(this_row.persons_number)" :key="i" class="form-group">
                                            <label>{{ $t("Adult Name ") + i }}</label>
                                            <input v-model="this_row.persons_names[i - 1]" type="text" class="form-control"
                                                :class="{ 'is-invalid': !this_row.persons_names[i - 1] && validate, 'is-valid': this_row.persons_names[i - 1] && validate }">
                                            <div v-if="!this_row.persons_names[i - 1] && validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Name of Person") + i }}
                                            </div>
                                        </div>
                                    </div>

                                    <div v-if="this_row.kids_number > 0">
                                        <div v-for=" i in parseInt(this_row.kids_number)" :key="i" class="form-group">
                                            <div class="row">
                                                <div class="col">
                                                    <label>{{ $t("Children Name ") + i }}</label>
                                                    <input v-model="this_row.kids_names[i - 1]" type="text"
                                                        class="form-control"
                                                        :class="{ 'is-invalid': !this_row.kids_names[i - 1] && validate, 'is-valid': this_row.kids_names[i - 1] && validate }">
                                                    <div v-if="!this_row.kids_names[i - 1] && validate"
                                                        class="invalid-feedback hidden">
                                                        {{ $t("Please Enter Children Name") + i }}
                                                    </div>
                                                </div>
                                                <div class="col">
                                                    <label>{{ $t("Children Age ") + i }}</label>
                                                    <input v-model="this_row.kids_ages[i - 1]" type="number"
                                                        class="form-control"
                                                        :class="{ 'is-invalid': !this_row.kids_ages[i - 1] && validate, 'is-valid': this_row.kids_ages[i - 1] && validate }">
                                                    <div v-if="!this_row.kids_ages[i - 1] && validate"
                                                        class="invalid-feedback hidden">
                                                        {{ $t("Please Enter Children Age") + i }}
                                                    </div>
                                                </div>

                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>

                            <div class="form-group">
                                <label for="status">{{ $t("Status") }}</label>
                                <select id="status" v-model="this_row.status" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.this_row.status && this.validate, 'is-valid': this.this_row.status && this.validate }">
                                    <option selected :value="$t('Booked')">{{ $t("Booked") }} </option>
                                    <option :value="$t('No Show')">{{ $t("No Show") }} </option>

                                </select>
                                <div v-if="!this.this_row.status && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select the status") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                <textarea class="form-control" v-model="this_row.notes" id="cutomer_notes"
                                    rows="1"></textarea>
                            </div>
                            <div class="form-check">
                                <input v-model="print" class="form-check-input" type="checkbox" value=""
                                    id="flexCheckChecked" checked>
                                <label class="form-check-label" for="flexCheckChecked">
                                    Print
                                </label>
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

        <!-- to get search value from navbar -->
        <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>

        <!-- Data Card -->
        <div v-show="this.this_row.persons_names.length > 0" class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Details") }} </h6>
                    <div class="dropdown no-arrow">
                    </div>
                </div>
                <div id="booking_data" class="card-body">
                    <h1>Booking #{{ this.this_row.id }}</h1>
                    <p><b>Booking Date:</b> {{ this.this_row.book_date }} <b>User:</b> {{ this.this_row.user }}</p>

                    <div class="container text-center">
                        <div class="row">
                            <div class="col">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Persons Name</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(person, index) in this.this_row.persons_names" :key="index">
                                            <td>{{ person }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="col">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Kids Name</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(kids, index) in this.this_row.kids_names" :key="index">
                                            <td>{{ kids }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="col">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Kids Age</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(age, index) in this.this_row.kids_ages" :key="index">
                                            <td>{{ age }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Hotel:</b> {{ this.this_row.hotel }}</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Room:</b> {{ this.this_row.room_id }}</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Room Type:</b> {{ this.this_row.room_type }}</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Status:</b> {{ this.this_row.status }}</label>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Date Range:</b> {{ 'From :' + this.this_row.dates[0] +
                                        ' To :' +
                                        this.this_row.dates[1] }}</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="col-auto">
                                    <label class="col-form-label"><b>Notes:</b> {{ this.this_row.notes }}</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" title="print" @click="PrintDiv('booking_data')"
                            class="btn btn-primary on-hover-sm no_print">
                            <i class="fa fa-print"></i></button>
                    </div>
                </div>
            </div>
        </div>


        <div>

        </div>


    </div>
</template>

<script>
/* eslint-disable */

// import block
import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import NavBar from '../components/parts/NavBar.vue';
import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import Loading from 'vue-loading-overlay';

import 'vue-loading-overlay/dist/vue-loading.css';

// end of import block

export default {
    name: 'BookingsView',

    /////////////////////
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker,
        vSelect,
        Loading,
    },

    ////////////////////

    data() {
        return {
            activeNav: 1, //last week or last month....
            isLoading: false,
            fullPage: true,
            is_range: true,
            max_id: '',
            user_roles: "",
            print: false, //to print after save
            validate: false, //for check forms
            active_index: null,//current id
            edit_mode: false,//edit form open
            add_mode: false,//add form open
            booking_rows: [],//all rows
            rooms: [],//used in new & update form
            hotels: [],//used in new & update form
            range: '',
            searchRange: '',
            booked_dates: [],
            all_booked_dates: [],//all dates in booked_dates ranges for selected room
            all_rooms_booked_dates: [],//all dates in booked_dates ranges for all room
            all_rooms_dates: [],//all dates for all room
            min_date: '',
            max_date: '',
            disable_dates: [],
            room_id_id: '',
            //////
            this_row: {
                book_date: new Date().toISOString().slice(0, 16),
                hotel: "",
                room_id: "",
                room_type: "",
                dates: "",
                out_date: "",
                all_dates: "",
                guests: "",
                status: "",
                notes: "",
                persons_number: 1,
                persons_names: [],
                kids_number: '',
                kids_names: [],
                kids_ages: [],
                user: "",
            },
            //////

            //////contex menu
            isContextMenuActive: false,
            menuStyle: {
                display: 'none',
                top: 0,
                left: 0
            }///////////

        }
    },

    ////////////////////
    watch: {
        'this_row.hotel': async function (newValue) {
            if (this.edit_mode || this.add_mode) {
                this.this_row.room_id = '';
                await this.get_rooms();
                this.this_row.room_id = this.rooms[0];
            }
        },
        'this_row.room_id': function (newValue) {
            if (this.edit_mode || this.add_mode) {
                this.get_room_info(newValue);
                this.get_booked_dates();
            }
        },
        range: async function (newValue) {
            const dateValues = newValue.split(",");
            this.min_date = dateValues[0];
            this.max_date = dateValues[1];
            this.this_row.out_date = this.this_row.dates[1];
            this.get_booked_dates()
        },
        activeNav: async function (newValue) {
            this.isLoading = true
            if(newValue)
                this.searchRange=''
            return my_api.get(`/backend/bookings/?range=${this.activeNav}`)
                .then((response) => (this.booking_rows = response.data, this.isLoading = false))
                .catch(err => { alert(err) });
        },
        searchRange: async function (newValue) {
            this.isLoading = true
            return my_api.get(`/backend/bookings/?searchRange=${this.searchRange}`)
                .then((response) => (this.booking_rows = response.data, this.isLoading = false))
                .catch(err => { alert(err) });
        }
    },

    ////////////////////

    async mounted() {
        this.isLoading = true;
        this.this_row.user = localStorage.getItem('user_name'); //to get logged in user name

        //get roles
        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        await this.get_roles();
        if (this.user_roles[this.$route.path.substring(1)] == 0) {
            this.$router.back()
        }

        await this.get_booking_rows();
        await this.get_hotels();

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////


        this.isLoading = false;
    },

    ////////////////////

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/bookings/?search=" + data,
                }).then((response) => (this.booking_rows = response.data));
            } else {
                this.get_booking_rows();
            }
        },
    },

    ////////////////////

    methods: {

        formatDate(date) {
            const formattedDate = new Date(date);
            const day = String(formattedDate.getDate()).padStart(2, '0');
            const month = String(formattedDate.getMonth() + 1).padStart(2, '0');
            const year = formattedDate.getFullYear();
            const hours = String(formattedDate.getHours()).padStart(2, '0');
            const minutes = String(formattedDate.getMinutes()).padStart(2, '0');

            return `${day}/${month}/${year} ${hours}:${minutes}`;
        },

        async get_roles() {
            return my_api.get('backend/get_roles/?user_name=' + this.this_row.user, { auth: { username: "admin", password: "123", } })
                .then((response) => (this.user_roles = response.data))
                .catch(err => { });
        },

        // page load **********************************

        get_booking_rows() {
            // we using return first of the function for 'await' 
            return my_api.get(`/backend/bookings/?range=${this.activeNav}`)
                .then((response) => (this.booking_rows = response.data))
                .catch(err => { alert(err) });
        },

        async get_booking(id) {
            try {
                const response = await axios.get(`${domain_url}/backend/bookings/?id=${id}`);
                this.this_row = response.data[0];
            } catch (error) {
                console.error("Error fetching booking:", error);
                // Handle the error gracefully (e.g., display an error message to the user)
            }
        },

        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },

        get_open_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_open_rooms/",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.all_rooms_dates = response.data));
        },

        // end page load *******************************


        // insert form *******************************

        get_rooms() {
            if (this.this_row.hotel)
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_rooms/", params: { hotel: this.this_row.hotel },
                    //auth: { username: "admin", password: "123", },
                }).then((response) => (this.rooms = response.data));
        },

        get_room_info(value) {
            if (value && this.this_row.hotel) {
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_room_info/", params: { room_id: value, hotel: this.this_row.hotel },
                    //auth: { username: "admin", password: "123", },
                }).then((response) => (this.this_row.room_type = response.data.type, this.room_id_id = response.data.id, this.range = response.data.range));
            }
        },

        async get_booked_dates() {
            if (this.this_row.room_id && this.this_row.hotel) {
                this.booked_dates = [];
                await axios({
                    method: "get", url: domain_url + "/backend/get_booked_dates/", params: { room_id: this.this_row.room_id, hotel: this.this_row.hotel },
                }).then((response) => {
                    if (response.data[0])
                        this.booked_dates = response.data[0].split(', ')
                })

                this.all_booked_dates = [];
                this.disable_dates = [];

                //get all dates in the range
                this.booked_dates.forEach((element) => {
                    const minDateParts = element.split(',')[0].split('/');
                    const maxDateParts = element.split(',')[1].split('/');

                    const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                    const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);
                    const currentDate = new Date(startDate);

                    currentDate.setDate(currentDate.getDate() + 1);//to skip in_date from booking dates list

                    while (currentDate < endDate) {
                        this.all_booked_dates.push(currentDate.toLocaleDateString("en-GB"));
                        currentDate.setDate(currentDate.getDate() + 1);
                    }
                });
                //copy all dates from all_booked_dates to disable_dates
                this.all_booked_dates.forEach(element => this.disable_dates.push(element));
            }
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

        // end insert form *******************************


        // for modals *******************************

        open_add_modal() {
            this.edit_mode = false;
            this.add_mode = true;
            this.clear_form();
            this.this_row.book_date = new Date().toISOString().slice(0, 16);

            $('#addModal').modal('toggle');
        },

        async open_edit_modal() {
            if (this.user_roles.hotels) {

                this.edit_mode = true;
                this.add_mode = false;

                // remove this booked dates from disable_dates to enable edit booked dates
                this.this_row.all_dates = [];

                if (this.this_row.dates.length < 2) {
                    this.this_row.dates.push(this.this_row.dates[0]);
                } else {
                    await this.get_booked_dates(); // to disable other booked dates 
                }
                const minDateParts = this.this_row.dates[0].split('/');
                const maxDateParts = this.this_row.dates[1].split('/');
                const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

                const currentDate = new Date(startDate);
                while (currentDate <= endDate) {
                    this.this_row.all_dates.push(currentDate.toLocaleDateString("en-GB"));
                    currentDate.setDate(currentDate.getDate() + 1);
                }
                this.disable_dates = this.disable_dates.filter((el) => !this.this_row.all_dates.includes(el));
                //////////////////////////////////////////////
                await this.get_rooms();
                $('#addModal').modal('toggle');
            }
        },

        clear_form() {
            this.this_row.persons_names = [];
            this.this_row.kids_names = [];
            this.this_row.persons_number = 1;
            this.this_row.kids_number = '';
            this.this_row.hotel = '';
            this.this_row.dates = '';
            this.this_row.room_id = '';
            this.this_row.room_type = '';
            this.this_row.status = '';
            this.this_row.notes = '';
            this.enable_dates = [];
            this.disable_dates = [];
            this.validate = false;
        },

        closeModal() {
            this.add_mode = false; this.edit_mode = false;
            $('#addModal').modal('hide');
            this.clear_form();
        },

        // end for modals ***************************

        async save_booking() {
            this.isLoading = true;
            try {
                if (this.check_form()) {
                    if (this.print) {
                        this.PrintDiv('booking_data');
                    }
                    // save out date
                    if (this.this_row.dates.length > 1) {
                        this.this_row.out_date = this.this_row.dates[1];
                    } else {
                        this.this_row.dates.push(this.this_row.dates[0]);
                    }
                    this.this_row.dates = this.this_row.dates.toString();
                    if (!this.this_row.kids_number) { this.this_row.kids_number = 0; }
                    this.this_row.persons_names = this.this_row.persons_names.join(',');
                    this.this_row.kids_names = this.this_row.kids_names.join(',');
                    this.this_row.kids_ages = this.this_row.kids_ages.join(',');
                    var response = await fetch(domain_url + "/backend/bookings/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.this_row),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 1500, });

                    await this.get_max_id();

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add booking :' + this.max_id, time: new Date() })


                    window.location.reload();

                    this.get_booking_rows();

                    this.closeModal();
                }
            } catch (error) { console.error(); }
            this.isLoading = false;
        },

        async delete_booking(id) {
            if (this.user_roles.hotels) {
                this.isLoading = true;
                try {
                    const willDelete = await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, });

                    if (willDelete) {
                        await my_api.delete(`/backend/bookings/${id}/`);
                        swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });

                        //save log
                        axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'delete booking :' + id, time: new Date() })


                        this.get_booking_rows();
                        this.closeModal();
                    }
                } catch (error) {
                    console.error("Error deleting booking:", error);
                }
                this.isLoading = false;
            }
        },

        async update_booking(id) {
            this.isLoading = true;
            try {
                if (this.check_form()) {
                    if (this.print) {
                        await this.PrintDiv('booking_data');
                    }
                    // save out date
                    if (this.this_row.dates.length > 1) {
                        this.this_row.out_date = this.this_row.dates[1];
                    } else {
                        this.this_row.dates.push(this.this_row.dates[0]);
                    }
                    // convert the dates array to string to save it in db
                    this.this_row.dates = this.this_row.dates.toString();
                    this.this_row.persons_names = this.this_row.persons_names.join(',');
                    this.this_row.kids_names = this.this_row.kids_names.join(',');
                    this.this_row.kids_ages = this.this_row.kids_ages.join(',');
                    var response = await fetch(domain_url + "/backend/bookings/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.this_row),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'update booking :' + id, time: new Date() })

                    //this.max_id = this.this_row.id
                    this.get_booking_rows();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }
            this.isLoading = false;
        },

        async row_click(index) {
            await this.get_booking(index);//get this row data
            this.this_row.dates = Array.from(this.this_row.dates.split(","));
            this.this_row.persons_names = Array.from(this.this_row.persons_names.split(","));
            this.this_row.kids_names = Array.from(this.this_row.kids_names.split(","));
            this.this_row.kids_ages = Array.from(this.this_row.kids_ages.split(","));
            this.get_room_info(this.this_row.room_id);
            //await this.get_room_info(this.this_row.room_id);
            //await this.findMinMaxDate();
            this.active_index = index; //to change row color
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.this_row.book_date &&
                this.this_row.persons_number &&
                this.this_row.persons_names &&
                //this.this_row.kids_number >0 &&
                this.this_row.hotel &&
                this.this_row.dates &&
                this.this_row.room_id &&
                this.this_row.room_type &&
                this.this_row.status
            ) {
                return true
            } else {
                return false
            }
        },

        async get_max_id() {
            try {
                const response = await axios.get(`${domain_url}/backend/get_max_id/?table_name=Bookings`);
                this.max_id = response.data.data.id__max;
            } catch (error) {
                console.error("Error fetching max ID:", error);
            }
        },


        // context menu ***************************

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

        // end context menu ***************************

    },

}

</script>
