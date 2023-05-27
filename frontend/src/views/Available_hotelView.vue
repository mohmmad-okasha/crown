<template>
    <div class="Available_hotelView">
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
                                <div class="col-auto">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("Date Range") }}</label>
                                </div>
                                <div class="col-3">
                                    <!-- <input type="text" class="custom-input form-control" placeholder="Range"
                                        aria-label="Range">
                                    <date-picker v-model="date_range" range clearable locale="en" :auto-submit="true"
                                        color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY"
                                        display-format="jYYYY-jMM-jDD" custom-input=".custom-input" /> -->
                                    <input type="text" class="custom-input form-control" placeholder="Range"
                                        aria-label="Range">
                                    <date-picker v-model="date_range" type="year-month" clearable locale="en"
                                        :auto-submit="true" color="#098290" input-format="MM/YYYY" format="MM/YYYY"
                                        display-format="jYYYY-jMM" custom-input=".custom-input" />
                                </div>
                                <div class="col-auto">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("Hotel") }}</label>
                                </div>
                                <div class="col-auto">
                                    <select class="form-control" placeholder="Hotel" v-model="hotel">
                                        <option v-for="h in this.hotels" :key="h" :value="h"> {{ h }}</option>
                                    </select>
                                </div>
                                <div class="col-auto">
                                    <label for="inputPassword6" class="col-form-label">{{ $t("Room Type") }}</label>
                                </div>
                                <div class="col-auto">
                                    <select id="room_type" class="form-control" placeholder="Room Type" v-model="room_type">
                                        <option selected value="Single"> {{ $t("Single") }}</option>
                                        <option value="Double"> {{ $t("Double") }}</option>
                                        <option value="Triple"> {{ $t("Triple") }}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div id="monitor_table" class="table-responsive">
                        <table class="table-sm table ">
                            <thead class="sticky_header">
                                <tr>
                                    <th>Room - Hotel</th>
                                    <th v-for="i in 31" :key="i" scope="col">{{ i }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="r in this.open_dates" :key="r.name">
                                    <td>{{ r.name }}</td>
                                    <td v-for="ii in 31" :key="ii" :id="r.name + '_' + ii.toString().padStart(2, '0')">
                                        <button v-for="d in r.dates" :key="d" v-show="ii == d.slice(0, 2)" :title="r.name"
                                            type="button" class="btn btn-success"></button>
                                    </td>
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
// end of import block
export default {
    name: 'Available_hotelView',
    /////////////////////
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker,
        vSelect
    },
    ////////////////////
    data() {
        return {
            test: [],
            date_range: [],
            all_range_dates: [],
            hotel: 'Hotel 1',
            room_type: '',
            hotels: [],
            open_dates: [],//all dates for all room
            close_dates: [],//all dates for all room
        }
    },
    async mounted() {
        await this.get_hotels();
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
        hotel: async function (newValue) {
            await this.get_monitor();
            await this.filter_dates();
            this.create_closed();
        },
        room_type: async function (newValue) {
            await this.get_monitor();
            await this.filter_dates();
            this.create_closed();
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
                item.dates = datesArray
            })
        }
    },
    ////////////////////

    methods: {

        filter_dates() {// remove any date out of selected range
            if (this.date_range) {
                let month = this.date_range.split('/')[0];
                let year = this.date_range.split('/')[1];
                month = parseInt(month, 10).toString();//to remove 0 from month start with 0 like 05 , 09 

                // Filter out-of-range dates we loop in all dates 
                this.open_dates.forEach(item => {
                    item.dates = item.dates.filter(date => {
                        const parts = date.split('/');
                        const cDate = new Date(parts[2], parts[1] , parts[0]);
                        return cDate.getFullYear() == year && cDate.getMonth() == month;
                    });
                });
                this.close_dates.forEach(item => {
                    item.dates = item.dates.filter(date => {
                        const parts2 = date.split('/');
                        const cDate2 = new Date(parts2[2], parts2[1] , parts2[0]);
                        return cDate2.getFullYear() == year && cDate2.getMonth() == month;
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

        create_closed() {
            //loop on open rooms dates and create button on monitoring table
            this.close_dates.forEach(item => {
                try {
                    item.dates.forEach(d => {// loop on all dates for all rooms
                        var div = document.getElementById(item.name + '_' + (d.slice(0, 2)));
                        var button = document.createElement("button");
                        button.className = "btn btn-danger";
                        div.appendChild(button);
                    });
                } catch (error) {
                }
            });
        },

        // page load **********************************
        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },
        async get_monitor() {
            this.close_dates = [];
            this.open_dates = [];
            await this.get_open_rooms();
            await this.get_close_rooms();
            for (let roomBooked of this.close_dates) {// to remove booked dates from open dates
                let roomBookedId = roomBooked.room_id;
                let roomBookedHotel = roomBooked.hotel;
                let roomBookedDates = roomBooked.dates;
                for (let room of this.open_dates) {
                    if (room.room_id === roomBookedId && room.hotel === roomBookedHotel) {
                        room.dates = room.dates.filter(date => !roomBookedDates.includes(date));
                    }
                }
            };
        },
        get_open_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_open_rooms/", params: { hotel: this.hotel, room_type: this.room_type },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.open_dates = response.data));
        },
        get_close_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_close_rooms/", params: { hotel: this.hotel, room_type: this.room_type },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.close_dates = response.data));
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
            return axios({
                method: "get",
                url: domain_url + "/backend/get_room_info/", params: { room_id: value, hotel: this.this_row.hotel },
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.this_row.room_type = response.data.type, this.room_id_id = response.data.id, this.range = response.data.range));
        },
        // end insert form *******************************
    },
}
</script>
