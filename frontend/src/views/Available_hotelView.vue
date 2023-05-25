<template>
    <div class="Available_hotelView">


        <!-- Rooms Monitor -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Available Hotel") }} </h6>

                    <div class="col-auto">
                        <label for="inputPassword6" class="col-form-label">{{ $t("Date Range") }}</label>
                    </div>
                    <div class="col-auto">
                        <input type="text" class="custom-input form-control" placeholder="Range" aria-label="Range">
                        <date-picker v-model="range" range clearable locale="en" :auto-submit="true" color="#098290"
                            input-format="DD/MM/YYYY" format="DD/MM/YYYY" display-format="jYYYY-jMM-jDD"
                            custom-input=".custom-input" />
                    </div>
                    <div class="col-auto">
                        <label for="inputPassword6" class="col-form-label">{{ $t("Hotel") }}</label>
                    </div>
                    <div class="col-auto">
                        <select id="hotel" value="test" class="form-control" placeholder="Hotel" v-model="hotel">
                            <option v-for="h in this.hotels" :value="h"> {{ h }}</option>
                        </select>
                    </div>
                    <div class="col-auto">
                        <label for="inputPassword6" class="col-form-label">{{ $t("Room Type") }}</label>
                    </div>
                    <div class="col-auto">
                        <select id="room_type" class="form-control" placeholder="Room Type" v-model="room_type">
                                    <option value="Single"> {{ $t("Single") }}</option>
                                    <option value="Double"> {{ $t("Double") }}</option>
                                    <option value="Triple"> {{ $t("Triple") }}</option>
                                </select>
                    </div>

     


                </div>

                <div id="table" class="card-body">
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
            range: '',
            hotel: '',
            room_type: '',

            hotels: [],
            booked_dates: [],//all dates in booked_dates ranges for all room
            open_dates: [],//all dates for all room

        }
    },



    async mounted() {
        await this.get_hotels();
        await this.get_monitor();

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////


        //loop on open rooms dates and create button on monitoring table
        this.booked_dates.forEach(item => {
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

        // page load **********************************

        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },

        async get_monitor() {

            await this.get_open_rooms();

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

                const existingEntry = this.booked_dates.find(entry => entry.name === item.room_id + ' - ' + item.hotel);

                if (existingEntry) {
                    existingEntry.dates = existingEntry.dates.concat(datesArray);
                } else {
                    this.booked_dates.push({
                        name: item.room_id + ' - ' + item.hotel,
                        dates: datesArray
                    });
                }


            });


            for (let roomBooked of this.booked_dates) {
                let roomBookedId = roomBooked.room_id;
                let roomBookedHotel = roomBooked.hotel;
                let roomBookedDates = roomBooked.dates;

                for (let room of this.open_dates) {
                    if (room.room_id === roomBookedId && room.hotel === roomBookedHotel) {
                        room.dates = room.dates.filter(date => !roomBookedDates.includes(date));
                    }
                }
            }


        },

        get_booking_rows() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/bookings/')
                .then((response) => (this.booking_rows = response.data))
                .catch(err => { alert(err) });
        },

        get_open_rooms() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_open_rooms/",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.open_dates = response.data));
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


    },

}

</script>
