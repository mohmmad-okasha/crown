<template>
    <div class="Available_hotelView">

        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>

        <!-- Rooms Monitor -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header  d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Available Hotel") }} </h6>
                </div>
                <div id="table" class="card-body">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-2"></div>

                                <div class="col-sm-2 m-1">
                                    <label class="col-form-label">{{ $t("Hotel") }}</label>
                                    <select class="form-control" placeholder="Hotel" v-model="hotel">
                                        <option v-for="h in this.hotels" :key="h" :value="h"> {{ h }}</option>
                                    </select>
                                </div>

                                <div class="col-sm-3 m-1">
                                    <label class="col-form-label">{{ $t("Date Range") }}</label>

                                    <div class="input-group mb-3">
                                        <div class="input-group-prepend">
                                            <button @click="show_date_range = true" class="btn btn-outline-secondary"
                                                type="button" id="button-addon1">
                                                <i class="fa-solid fa-calendar-days"></i></button>
                                        </div>
                                        <input :value="date_range" id="my-custom-editable-input" type="text"
                                            class="form-control" />
                                    </div>

                                    <date-picker v-model="date_range" :show="show_date_range" type="year-month" clearable
                                        locale="en" :auto-submit="true" color="#098290" input-format="MM/YYYY"
                                        format="MM/YYYY" display-format="jYYYY-jMM" custom-input="#my-custom-editable-input"
                                        @close="show_date_range = false" />

                                </div>


                                <div class="col-sm-2 m-1">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("Room Type") }}</label>

                                    <select id="room_type" class="form-control" placeholder="Room Type" v-model="room_type">
                                        <option value="SGL"> SGL</option>
                                        <option value="DBL"> DBL</option>
                                        <option value="TRPL"> TRPL</option>
                                        <option value="QAD"> QAD</option>
                                    </select>
                                </div>

                                <div class="col-sm-1 m-1">
                                    <label class="col-form-label">{{ $t("New") }}</label>

                                    <button @click="open_new()" class="form-control btn-outline-secondary">
                                        <i class="fa-solid fa-plus"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div id="monitor_table" class="table-responsive">
                        <table class="table-sm table ">
                            <thead class="sticky_header">
                                <tr class="header">
                                    <th>Room - Hotel</th>
                                    <th v-for="i in 31" :key="i" scope="col">{{ i }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="r in this.open_dates" :key="r.name">
                                    <td>
                                        <p>{{ r.categ + '/' + r.name + '  ' }}</p>
                                    </td>
                                    <td v-for="ii in 31" :key="ii" :id="r.name + '_' + ii.toString().padStart(2, '0')">
                                        <button v-for="d in r.dates" :key="d" v-show="ii == d.slice(0, 2)"
                                            :title="r.categ + '/' + r.name" type="button" class="btn btn-success"></button>
                                    </td>
                                    <br><br>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- modal -->
        <div class="modal  fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog ">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modal_label">{{ $t("Add booking") }}</h5>

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

                        <button type="button" title="save" @click="save_booking()" class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

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
//import block
import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import NavBar from '../components/parts/NavBar.vue';
import NewBooking from '../components/NewBooking.vue';
import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

// end of import block
export default {
    name: 'Available_hotelView',

    components: {
        NavBar,
        NewBooking,
        datePicker: VuePersianDatetimePicker,
        vSelect,
        Loading,
    },
    data() {
        //to get year + month auto on start
        function getYearMonth() {
            const today = new Date();
            const month = String(today.getMonth() + 1).padStart(2, '0'); // Add leading zero for single-digit months
            const year = today.getFullYear();
            return `${month}/${year}`;
        }

        return {
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
            is_range: true,
            print: false, //to print after save
            validate: false, //for check forms
            show_date_range: false,
            isLoading: false,
            fullPage: true,
            user_roles: "",
            test: [],
            date_range: getYearMonth(),
            all_range_dates: [],
            hotel: '',
            room_type: '',
            hotels: [],
            rooms: [],
            range: '',
            min_date: '',
            max_date: '',
            disable_dates: [],
            open_dates: [],//all dates for all room
            close_dates: [],//all dates for all room
            no_show_dates: [],

        }
    },
    async mounted() {

        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        await this.get_roles();
        if (this.user_roles[this.$route.path.substring(1)] == 0) {
            this.$router.back()
        }

        await this.get_hotels();
        await this.get_monitor();

        await this.filter_dates();//
        await this.create_closed();

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////

    },
    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/bookings/?search=" + data,
                }).then((response) => (this.booking_rows = response.data));
            } else {
                //this.get_booking_rows();
            }
        },
    },
    watch: {
        date_range: async function (newValue) {

            await this.get_monitor();
            // const currentDate = new Date(startDate);
            // this.all_range_dates = [];
            // while (currentDate <= endDate) {
            //     this.all_range_dates.push(currentDate.toLocaleDateString("en-GB"));
            //     currentDate.setDate(currentDate.getDate() + 1);
            // }
            await this.filter_dates();
            this.create_closed();

        },
        hotel: async function (newValue) {
            if (this.date_range.length > 0) {
                await this.get_monitor();
                await this.filter_dates();
                this.create_closed();
            }
        },
        room_type: async function (newValue) {
            if (this.date_range.length > 0) {
                await this.get_monitor();
                await this.filter_dates();
                this.create_closed();
            }
        },
        close_dates: function (newValue) {//to get all dates in the booked ranges
            newValue.forEach(item => {
                const datesArray = [];
                const ranges = item.dates.split(' / ');
                ranges.forEach(r => {
                    const minDateParts = r.split(',')[0].split('/');
                    const maxDateParts = r.split(',')[1].split('/');
                    const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                    const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);
                    const currentDate = new Date(startDate);
                    while (currentDate < endDate) {
                        datesArray.push(currentDate.toLocaleDateString("en-GB")); // Save each date within the range to the array
                        currentDate.setDate(currentDate.getDate() + 1);
                    }
                })
                item.dates = [...new Set(datesArray)]//remove dublicated dates from array
            })
        },
        no_show_dates: function (newValue) {//to get all dates in the booked ranges
            newValue.forEach(item => {
                const datesArray = [];
                const ranges = item.dates.split(' / ');
                ranges.forEach(r => {
                    const minDateParts = r.split(',')[0].split('/');
                    const maxDateParts = r.split(',')[1].split('/');
                    const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                    const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);
                    const currentDate = new Date(startDate);
                    while (currentDate <= endDate) { // <= only for no show dates
                        datesArray.push(currentDate.toLocaleDateString("en-GB")); // Save each date within the range to the array
                        currentDate.setDate(currentDate.getDate() + 1);
                    }
                })
                item.dates = [...new Set(datesArray)]//remove dublicated dates from array
            })
            // newValue.forEach(item => {
            //     const datesArray = [];
            //     const ranges = item.dates.split(' / ');
            //     ranges.forEach(r => {
            //         const minDateParts = r.split(',')[0].split('/');
            //         const maxDateParts = '';
            //         try {
            //             maxDateParts = r.split(',')[1].split('/');
            //         } catch (error) {}
            //         const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
            //         const endDate = startDate;
            //         if (maxDateParts) { endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]); }
            //         const currentDate = new Date(startDate);
            //         while (currentDate <= endDate) {
            //             datesArray.push(currentDate.toLocaleDateString("en-GB")); // Save each date within the range to the array
            //             currentDate.setDate(currentDate.getDate() + 1);
            //         }
            //     })
            //     item.dates = [...new Set(datesArray)]//remove dublicated dates from array
            // })
        },

        //new booking
        'this_row.hotel': async function (newValue) {
            this.this_row.room_id = '';
            await this.get_rooms();
            this.this_row.room_id = this.rooms[0];
        },

        'this_row.room_id': async function (newValue) {

            this.get_room_info(newValue);
            this.get_booked_dates();

        },
        range: async function (newValue) {
            const dateValues = newValue.split(",");
            this.min_date = dateValues[0];
            this.max_date = dateValues[1];
            this.this_row.out_date = this.this_row.dates[1];
            this.get_booked_dates()
        }
    },
    methods: {
        get_roles() {
            this.user_roles = this.$parent.user_roles;
        },

        filter_dates() {// remove any date out of selected range
            if (this.date_range) {
                let month = this.date_range.split('/')[0];
                let year = this.date_range.split('/')[1];
                //month = parseInt(month, 10).toString();//to remove 0 from month start with 0 like 05 , 09 

                // Filter out-of-range dates we loop in all dates 
                this.open_dates.forEach(item => {
                    item.dates = item.dates.filter(date => {
                        const parts = date.split('/');
                        return parts[2] == year && parts[1] == month;
                    });
                });

                this.close_dates.forEach(item => {
                    item.dates = item.dates.filter(date => {
                        const parts2 = date.split('/');
                        return parts2[2] == year && parts2[1] == month;
                    });
                    item.out_dates = item.out_dates.split(',');
                    item.out_dates = item.out_dates.filter(date => {
                        const parts3 = date.split('/');
                        return parts3[2] == year && parts3[1] == month;
                    });
                    item.out_dates = item.out_dates.toString();
                });

                this.no_show_dates.forEach(item => {
                    item.dates = item.dates.filter(date => {
                        const parts = date.split('/');
                        return parts[2] == year && parts[1] == month;
                    });
                });


            }
            // if (this.date_range.length > 0) {
            //     let min_date = this.date_range[0];
            //     let max_date = this.date_range[1];
            //     const minDateParts = min_date.split('/');
            //     const maxDateParts = max_date.split('/');
            //     const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
            //     const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

            //     // Filter out-of-range dates we loop in all dates 
            //     this.open_dates.forEach(item => {
            //         item.dates = item.dates.filter(date => {
            //             const parts = date.split('/');
            //             const cDate = new Date(parts[2], parts[1] - 1, parts[0]);
            //             return cDate >= startDate && cDate <= endDate;
            //         });
            //     });
            //     this.close_dates.forEach(item => {
            //         item.dates = item.dates.filter(date => {
            //             const parts2 = date.split('/');
            //             const cDate2 = new Date(parts2[2], parts2[1] - 1, parts2[0]);
            //             return cDate2 >= startDate && cDate2 <= endDate;
            //         });
            //     });
            // }

        },

        async create_closed() {
            //loop on close rooms dates and create button on monitoring table
            this.close_dates.forEach(item => {
                try {
                    item.dates.forEach(function (d) {// loop on all dates for all rooms
                        var div = document.getElementById(item.name + '_' + (d.slice(0, 2)));
                        var button = document.createElement("button");
                        button.className = "btn btn-danger";
                        button.title = item.name
                        div.appendChild(button);
                    });
                } catch (error) {
                }
            });

            //out_date two colors
            this.close_dates.forEach(o => {
                try {
                    o.out_dates = o.out_dates.split(','); // str to array of dates

                    o.out_dates.forEach(function (d) { // loop on all out_dates 

                        const [day, month, year] = d.split("/");
                        const date = new Date(`${month}/${day}/${year}`);
                        // Increment the date by one day
                        date.setDate(date.getDate());
                        // Format the incremented date to match the format in datesArray
                        const formattedDate = `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1).toString().padStart(2, "0")}/${date.getFullYear()}`;


                        // check if the next date of out date is booked then the out day will be booked 
                        if (!o.dates.includes(formattedDate)) {
                            var div = document.getElementById(o.name + '_' + (d.slice(0, 2)));// select target div by date day
                            div.innerHTML = ''; // remove any btn in this out_date day
                            var button = document.createElement("button");
                            button.className = "btn btn-danger tow_color";
                            div.appendChild(button);
                        }
                    });
                } catch (error) {
                }
            });

            //loop on no_show rooms dates and create button on monitoring table
            this.no_show_dates.forEach(n => {
                try {
                    //n.dates = n.dates.split(',') // text to array
                    n.dates.forEach(function (d) {// loop on all dates for all rooms
                        var div2 = document.getElementById(n.name + '_' + (d.slice(0, 2)));
                        var button2 = document.createElement("button");
                        div2.innerHTML = '';
                        button2.className = "btn btn-warning";
                        div2.appendChild(button2);
                    });
                } catch (error) {
                }
            });


            // this.close_dates.forEach(item => {
            //     try {
            //         item.dates.forEach(d => {// loop on all dates for all rooms
            //             var div = document.getElementById(item.name + '_' + (d.slice(0, 2)));
            //             var button = document.createElement("button");
            //             button.className = "btn btn-danger";
            //             div.appendChild(button);
            //         });
            //     } catch (error) {
            //     }
            // });
        },
        // page load **********************************
        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },
        async get_monitor() {
            this.isLoading = true;
            this.close_dates = [];
            this.open_dates = [];
            await this.get_open_rooms();
            await this.get_close_rooms();
            await this.get_no_show_rooms();
            for (let roomBooked of this.close_dates) {// to remove booked dates from open dates
                let roomBookedname = roomBooked.name;
                let roomBookedDates = roomBooked.dates;
                for (let room of this.open_dates) {
                    if (room.name === roomBookedname) {
                        room.dates = room.dates.filter(date => !roomBookedDates.includes(date));
                    }
                }
            };
            this.isLoading = false;
        },
        get_open_rooms() {

            return axios({
                method: "get",
                url: domain_url + "/backend/get_open_rooms/", params: { hotel: this.hotel, room_type: this.room_type, date_range: this.date_range },
            }).then((response) => (this.open_dates = response.data));

        },
        get_close_rooms() {

            return axios({
                method: "get",
                url: domain_url + "/backend/get_close_rooms/", params: { hotel: this.hotel, room_type: this.room_type, month: this.date_range, date_range: this.date_range },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.close_dates = response.data));

        },
        get_no_show_rooms() {

            return axios({
                method: "get",
                url: domain_url + "/backend/get_no_show_rooms/", params: { hotel: this.hotel, room_type: this.room_type, month: this.date_range },
            }).then((response) => {
                this.no_show_dates = response.data;

            });

        },
        // end page load *******************************
        // insert form *******************************
    
        get_rooms() {
            if (this.this_row.hotel)
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_rooms/", params: { hotel: this.this_row.hotel, persons: this.this_row.persons_number },
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
        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },
        closeModal() {
            this.add_mode = false; this.edit_mode = false;
            $('#addModal').modal('hide');
            this.clear_form();
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
        get_rooms() {
            if (this.this_row.hotel)
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_rooms/", params: { hotel: this.this_row.hotel },
                    //auth: { username: "admin", password: "123", },
                }).then((response) => (this.rooms = response.data));
        },
        get_room_info(value) {
            if (value && this.this_row.hotel)
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
                }).then((response) => {
                    if(response.data[0])
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
        closeModal() {
            this.add_mode = false; this.edit_mode = false;
            $('#addModal').modal('hide');
            this.clear_form();
        },
        open_new() {//open new booking modal
            this.this_row.hotel = this.hotel
            $('#addModal').modal('toggle');
        }

    },
}
</script>