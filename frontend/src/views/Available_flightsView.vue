<template>
    <div class="Available_flightsView">

        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>

        <!-- Flights Monitor -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Available Flights") }} </h6>
                </div>
                <div id="table" class="card-body">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-2"></div>

                                <div class="col-sm-2 m-1">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("From City") }}</label>
                                    <select class="form-control" placeholder="From City" v-model="citys">
                                        <option v-for="c in this.citys" :key="c" :value="c"> {{ c }}</option>
                                    </select>
                                </div>

                                <div class="col-sm-2 m-1">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("To City") }}</label>
                                    <select class="form-control" placeholder="To City" v-model="citys">
                                        <option v-for="c in this.citys" :key="c" :value="c"> {{ c }}</option>
                                    </select>
                                </div>

                                <div class="col-sm-3 m-1">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("Date Range") }}</label>
                                    <input type="text" class="custom-input form-control" placeholder="Range"
                                        aria-label="Range">
                                    <date-picker v-model="date_range" type="year-month" clearable locale="en"
                                        :auto-submit="true" color="#098290" input-format="MM/YYYY" format="MM/YYYY"
                                        display-format="jYYYY-jMM" custom-input=".custom-input" />
                                </div>


                                <div class="col-sm-2 m-1">
                                    <label class="col-form-label">{{ $t("Seats") }}</label>

                                    <input type="number" class="custom-input form-control" placeholder="Seats"
                                        aria-label="Seats">
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div id="monitor_table" class="table-responsive">
                        <table class="table-sm table ">
                            <thead class="sticky_header">
                                <tr>
                                    <th>Flights</th>
                                    <th v-for="i in 31" :key="i" scope="col">{{ i }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="r in this.open_dates" :key="r.name">
                                    <td>
                                        <p>{{ r.categ + '/' + r.name }}</p>
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

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

// end of import block
export default {
    name: 'Available_flightsView',
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
            isLoading: false,
            fullPage: true,

            user_roles: "",
            test: [],
            date_range: [],
            all_range_dates: [],
            flights: '',
            room_type: '',
            flights: [],
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

        await this.get_flights();
        await this.get_monitor();
        await this.create_closed();
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
        flights: async function (newValue) {
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
 
        }
    },
    ////////////////////

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

        },

        // page load **********************************
        get_flights() {
            return my_api.get('/backend/get_flights/')
                .then((response) => (this.flights = response.data))
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
                url: domain_url + "/backend/get_open_rooms/", params: { flights: this.flights, room_type: this.room_type },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.open_dates = response.data));

        },
        get_close_rooms() {

            return axios({
                method: "get",
                url: domain_url + "/backend/get_close_rooms/", params: { flights: this.flights, room_type: this.room_type, month: this.date_range },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.close_dates = response.data));

        },
        get_no_show_rooms() {

            return axios({
                method: "get",
                url: domain_url + "/backend/get_no_show_rooms/", params: { flights: this.flights, room_type: this.room_type, month: this.date_range },
            }).then((response) => {
                this.no_show_dates = response.data;

            });

        },
        // end page load *******************************
        // insert form *******************************
        get_rooms() {
            if (this.this_row.flights)
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_rooms/", params: { flights: this.this_row.flights, persons: this.this_row.persons_number },
                    //auth: { username: "admin", password: "123", },
                }).then((response) => (this.rooms = response.data));
        },
        get_room_info(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_info/", params: { room_id: value, flights: this.this_row.flights },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.this_row.room_type = response.data.type, this.room_id_id = response.data.id, this.range = response.data.range));
        },
        // end insert form *******************************
    },
}
</script>