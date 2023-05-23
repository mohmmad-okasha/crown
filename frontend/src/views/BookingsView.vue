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
                                    <th>Room - Hotel</th>
                                    <th v-for="i in 31" :key="i" scope="col">{{ i }}</th>
                                </tr>
                            </thead>
                            <tbody>

                                <tr v-for="r in this.all_rooms_booked_dates" :key="r.name">
                                    <td>{{ r.name }}</td>
                                    <td v-for="ii in 31" :key="ii">
                                        <button v-for="d in r.dates" :key="d" v-show="ii == d.slice(0, 2)" :title="r.name"
                                            type="button" class="btn btn-danger"></button>
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
                                        <th scope="col">{{ $t("Dook Date") }}</th>
                                        <th scope="col">{{ $t("Guest") }}</th>
                                        <th scope="col">{{ $t("Hotel") }}</th>
                                        <th scope="col">{{ $t("Dates") }}</th>
                                        <th scope="col">{{ $t("Room ID") }}</th>
                                        <th scope="col">{{ $t("Room Type") }}</th>
                                        <th scope="col">{{ $t("Status") }}</th>
                                        <th scope="col">{{ $t("Guests") }}</th>
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
                                        <td>{{ booking.book_date }}</td>
                                        <td>{{ $t(booking.guest_name) }}</td>
                                        <td>{{ $t(booking.hotel) }}</td>
                                        <td>{{ $t(booking.dates) }}</td>
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

                            <div class="card form-group">
                                <div class="card-header">
                                    {{ $t("Guests") }}
                                </div>
                                <div class="card-body">

                                    <div class="row g-3 form-group">
                                        <div class="col">
                                            <label for="guests"> {{ $t("Number of Persons") }}</label>
                                            <input id="guests" v-model="this_row.persons_number" min="0" max="10"
                                                :class="{ 'is-invalid': !this.this_row.persons_number && this.validate, 'is-valid': this.this_row.persons_number && this.validate }"
                                                type="number" class="form-control">
                                            <div v-if="!this.this_row.persons_number && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Number of Persons") }}
                                            </div>
                                        </div>
                                        <div class="col">
                                            <label for="guests"> {{ $t("Number of Kids") }}</label>
                                            <input id="guests" v-model="this_row.kids_number" min="0" max="10"
                                                :class="{ 'is-invalid': !this.this_row.kids_number && this.validate, 'is-valid': this.this_row.kids_number && this.validate }"
                                                type="number" class="form-control">
                                            <div v-if="!this.this_row.kids_number && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Number of Persons") }}
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="this_row.persons_number > 0">
                                        <div v-for=" i in parseInt(this_row.persons_number)" :key="i" class="form-group">
                                            <label>{{ $t("Person Name ") + i }}</label>
                                            <input v-model="this_row.persons_names[i - 1]" type="text" class="form-control"
                                            :class="{ 'is-invalid': !this_row.persons_names[i-1] && validate, 'is-valid': this_row.persons_names[i-1] && validate }"
                                            >
                                            <div v-if="!this_row.persons_names[i - 1] && validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Name of Person") + i }}
                                            </div>
                                        </div>
                                    </div>

                                    <div v-if="this_row.kids_number > 0">
                                        <div v-for=" i in parseInt(this_row.kids_number)" :key="i" class="form-group">
                                            <label>{{ $t("Person Name ") + i }}</label>
                                            <input v-model="this_row.kids_names[i - 1]" type="text" class="form-control"
                                            :class="{ 'is-invalid': !this_row.kids_names[i-1] && validate, 'is-valid': this_row.kids_names[i-1] && validate }"
                                            >
                                            <div v-if="!this_row.kids_names[i - 1] && validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Enter The Name of Kids") + i }}
                                            </div>
                                        </div>
                                    </div>


                                </div>
                            </div>

                            <div class="form-group">
                                <label for="hotel">{{ $t("Hotel") }}</label>
                                <v-select id="hotel" v-model="this_row.hotel" :options="hotels"
                                    :class="{ 'is-invalid': !this_row.hotel && validate, 'is-valid': this_row.hotel && validate }" />

                                <div v-if="!this_row.hotel && validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select hotel") }}
                                </div>
                            </div>

                            <div class="form-group">
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

                            <div class="form-group">
                                <label for="room_type">{{ $t("Room Type") }}</label>
                                <input readonly id="room_type" v-model="this_row.room_type" type="text"
                                    class="form-control">
                            </div>

                            <label v-show="this.this_row.room_id" for="dates">{{ $t("Select Date") }}</label>
                            <div v-show="this.this_row.room_id" class="form-group card" id="dates" style="width: 100%;">
                                <div class="card-body">
                                    <date-picker v-model="this_row.dates" :min="min_date" :max="max_date"
                                        :disable="disable_dates" range clearable locale="en" inline :auto-submit="true"
                                        custom-input="none" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY" />
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
// end of import block

export default {
    name: 'BookingsView',

    /////////////////////
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker,
        vSelect
    },

    ////////////////////

    data() {
        return {
            validate: false, //for check forms
            active_index: null,//current id
            edit_mode: false,//edit form open
            add_mode: false,//add form open
            booking_rows: [],//all rows
            rooms: [],//used in new & update form
            hotels: [],//used in new & update form
            range: '',
            booked_dates: [],
            all_booked_dates: [],//all dates in booked_dates ranges for selected room
            all_rooms_booked_dates: [],//all dates in booked_dates ranges for all room
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
                all_dates: "",
                guests: "",
                status: "",
                notes: "",
                persons_number: 0,
                persons_names: [],
                kids_number: 0,
                kids_names: [],
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
        'this_row.hotel': function (newValue) {
            if (this.edit_mode || this.add_mode) {
                this.get_rooms()
            }
        },
        'this_row.persons_number': function (newValue) {
            if (this.edit_mode || this.add_mode) {
                this.get_rooms()
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
            this.get_booked_dates()
        },
    },

    ////////////////////

    async mounted() {
        this.this_row.user = localStorage.getItem('user_name'); //to get logged in user name
        await this.get_booking_rows();
        await this.get_hotels();
        await this.get_monitor();

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////
    },

    ////////////////////

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/bookings/?search=" + data,
                }).then((response) => (this.this_row = response.data));
            } else {
                this.get_booking_rows();
            }
        },
    },

    ////////////////////

    methods: {

        // page load **********************************

        get_booking_rows() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/bookings/')
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

        async get_monitor() {

            //get all booked dates for all rooms
            this.booking_rows.forEach(item => {
                const minDateParts = item.dates.split(',')[0].split('/');
                const maxDateParts = item.dates.split(',')[1].split('/');
                const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

                const currentDate = new Date(startDate);
                const datesArray = [];

                while (currentDate < endDate) {
                    datesArray.push(currentDate.toLocaleDateString("en-GB")); // Save each date within the range to the array
                    currentDate.setDate(currentDate.getDate() + 1);
                }

                const existingEntry = this.all_rooms_booked_dates.find(entry => entry.name === item.room_id + ' - ' + item.hotel);

                if (existingEntry) {
                    existingEntry.dates = existingEntry.dates.concat(datesArray);
                } else {
                    this.all_rooms_booked_dates.push({
                        name: item.room_id + ' - ' + item.hotel,
                        dates: datesArray
                    });
                }
            });



        },

        // end page load *******************************


        // insert form *******************************

        get_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_rooms/", params: { hotel: this.this_row.hotel, persons: this.this_row.persons_number },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.rooms = response.data));
        },

        get_room_info(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_info/", params: { room_id: value, hotel: this.this_row.hotel },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.this_row.room_type = response.data.type, this.room_id_id = response.data.id, this.range = response.data.range));
        },

        async get_booked_dates() {
            if (this.this_row.room_id && this.this_row.hotel) {
                this.booked_dates = [];
                await axios({
                    method: "get", url: domain_url + "/backend/get_booked_dates/", params: { room_id: this.this_row.room_id, hotel: this.this_row.hotel },
                }).then((response) => (this.booked_dates = response.data[0].split(', ')));

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
            }
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
            this.edit_mode = true;
            this.add_mode = false;

            await this.get_booked_dates(); // to disable other booked dates 

            // remove this booked dates from disable_dates to enable edit booked dates
            this.this_row.all_dates = [];
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

            $('#addModal').modal('toggle');
        },

        clear_form() {
            this.this_row.persons_names = [];
            this.this_row.kids_names = [];
            this.this_row.persons_number = '';
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
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.this_row.dates = this.this_row.dates.toString();
                    this.this_row.persons_names = this.this_row.persons_names.join(',');
                    this.this_row.kids_names = this.this_row.kids_names.join(',');
                    alert(this.this_row.persons_names)
                    var response = await fetch(domain_url + "/backend/bookings/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.this_row),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                    this.get_booking_rows();
                    this.get_max_id();
                    this.closeModal();
                }
            } catch (error) { console.error(); }
        },

        async delete_booking(id) {
            try {
                const willDelete = await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, });

                if (willDelete) {
                    await my_api.delete(`/backend/bookings/${id}/`);
                    swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                    this.get_booking_rows();
                    this.closeModal();
                }
            } catch (error) {
                console.error("Error deleting booking:", error);
            }
        },

        async update_booking(id) {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.this_row.dates = this.this_row.dates.toString();
                    var response = await fetch(domain_url + "/backend/bookings/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.this_row),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                    //this.max_id = this.this_row.id
                    this.get_booking_rows();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }

        },

        async row_click(index) {
            await this.get_booking(index);//get this row data
            this.this_row.dates = Array.from(this.this_row.dates.split(","));
            this.this_row.persons_names = Array.from(this.this_row.persons_names.split(","));
            this.this_row.kids_names = Array.from(this.this_row.kids_names.split(","));
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
                this.this_row.kids_number &&
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
