<template>
    <div class="Hotels_reportView">
        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_hotel(hotel.id)">
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

        <!-- Search Card -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Search") }} </h6>
                </div>
                <!-- Card Body -->
                <div class="card-body">
                    <div class="row">
                        <div class="col-sm-3"></div>
                        <div class="col-sm-3 m-1">
                            <label for="hotel">{{ $t("Hotel") }}</label>
                            <v-select id="hotel" v-model="hotel" :options="hotels" />
                        </div>

                        <div class="col-sm-3 m-1">
                            <label for="range">{{ $t("Select Range") }}</label>
                            <input type="text" class="form-control date_input">
                            <date-picker v-model="range" range clearable locale="en" :auto-submit="true"
                                custom-input=".date_input" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY" />
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- Report Card -->
        <div v-show="data.hotel_name" class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Report") }} </h6>
                </div>
                <!-- Card Body -->
                <div class="card-body" ref="exportContent">
                    <div class="row">
                        <div class="col">
                            <h1>{{ this.data.hotel_name }} Hotel </h1>
                            <p><b>Range:</b> {{ this.data.from_date }} to : {{ this.data.to_date }} </p>
                            <div id="books_table" class="table-responsive">
                                <table class="table table-hover">
                                    <thead class="sticky_header">
                                        <tr>
                                            <th scope="col">#</th>
                                            <th scope="col">{{ $t("Names") }}</th>
                                            <th scope="col">{{ $t("Gustes") }}</th>
                                            <th scope="col">{{ $t("Range") }}</th>
                                            <th scope="col">{{ $t("Room ID") }}</th>
                                            <th scope="col">{{ $t("Room Type") }}</th>
                                            <th scope="col">{{ $t("Room Categ") }}</th>
                                            <th scope="col">{{ $t("Meals") }}</th>
                                            <th scope="col">{{ $t("Notes") }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="booking in this.bookings" :key="booking.id">
                                            <th scope="row" id="id">{{ booking.id }}</th>
                                            <td>{{ $t(booking.persons_names + ' , ' + booking.kids_names) }}</td>
                                            <td>{{ $t(booking.persons_number + booking.kids_number) }}</td>
                                            <td>{{ $t(booking.dates) }}</td>
                                            <td>{{ $t(booking.room_id) }}</td>
                                            <td>{{ $t(booking.room_type) }}</td>
                                            <td>{{ $t(booking.room_categ) }}</td>
                                            <td>{{ $t(booking.meals) }}</td>
                                            <td>{{ $t(booking.notes) }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <br>
                            <hr>
                            <p class="text-right"><b>User:</b> {{ this.data.user }}</p>

                        </div>
                    </div>
                </div>


                <div class="card-footer text-muted" v-show="this.bookings.length">
                    <button type="button" class="btn btn-primary m-1" @click="exportToWord"> <i
                            class="fa-solid fa-file-word"></i></button>
                    <button type="button" class="btn btn-primary m-1" @click="exportToExcel"> <i
                            class="fa-solid fa-file-excel"></i></button>
                </div>

            </div>
        </div>

        <!-- to get search value from navbar -->
        <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>




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
import XLSX from 'xlsx/dist/xlsx.full.min';
import { saveAs } from 'file-saver';

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

import vSelect from 'vue-select';

export default {
    name: 'Hotels_reportView',
    components: {
        NavBar,
        vSelect,
        datePicker: VuePersianDatetimePicker,
        Loading,
    },

    data() {
        return {
            isLoading: false,
            fullPage: true,

            validate: false,
            user_roles: "",
            hotel: "",
            range: "",
            hotels: [],
            rooms: [],
            bookings: [],
            data: {
                hotel_name: "",
                room: "",
                from_date: "",
                to_date: "",
                names: "",
                meals: "",
                notes: "",
                user: ""
            },

            //////////////////////////
            isContextMenuActive: false,
            menuStyle: {
                display: 'none',
                top: 0,
                left: 0
            }
        }
    },

    async mounted() {
        this.isLoading = true;
        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        await this.get_roles();
        if (this.user_roles[this.$route.path.substring(1)] == 0) {
            this.$router.back()
        }

        // get user name to save in any record
        this.data.user = localStorage.getItem('user_name')

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////

        await this.get_hotels();



        //await this.get_report();

        //get all countrys names
        axios.get('https://restcountries.com/v3/all')
            .then(response => {
                this.countries = response.data.sort((a, b) => {
                    const nameA = a.name.common.toUpperCase();
                    const nameB = b.name.common.toUpperCase();
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }
                    return 0;
                });
            })
            .catch(error => {
                console.log(error);
            });

            this.isLoading = false;
    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/hotels/?search=" + data,
                }).then((response) => (this.Hotels = response.data));
            } else {
                //this.get_report();
            }
        },
    },

    watch: {
        hotel() {
            this.get_report()
        },
        range() {
            this.get_report()
        },
        bookings(newValue) {//send selected values to hotel array
            this.data.hotel_name = this.hotel
            this.data.from_date = this.range[0]
            this.data.to_date = this.range[1]

        }
    },

    methods: {
        get_roles() {
            this.user_roles = this.$parent.user_roles;
        },

        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },

        get_rooms(hotel_id) {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/rooms/?hotel_id=' + hotel_id)
                .then((response) => (this.rooms = response.data))
                .catch(err => { alert(err) });
        },

        get_report() {
            this.isLoading = true;
            // we using return first of the function for 'await' 
            return my_api.get('/backend/booking_report/?hotel=' + this.hotel + '&from_date=' + this.range[0] + '&to_date=' + this.range[1])
                .then((response) => (
                    this.bookings = response.data,
                    this.isLoading = false,
                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'get report for:' +  this.hotel +' from :'+this.range[0] + ' to :' + this.range[1], time: new Date() })
                ))
                .catch(err => { alert(err) });

            
        },

        exportToExcel() {
            this.isLoading = true;
            const wb = XLSX.utils.table_to_book(document.querySelector('#books_table'));
            XLSX.writeFile(wb, this.hotel + ' on ' + this.range + '.xlsx');
            this.isLoading = false;
        },

        exportToWord() {
            this.isLoading = true;
            // Generate the Word content (replace with your own logic)
            const divContent = this.$refs.exportContent.innerHTML;
            const wordContent = `<html><body>${divContent}</body></html>`;

            // Convert the content to a Blob
            const blob = new Blob([wordContent], { type: 'application/msword' });

            // Save the Blob as a Word file
            saveAs(blob, this.hotel + ' on ' + this.range + '.doc');
            this.isLoading = false;
        },

        getCities() {
            const apiKey = '02b73423a39d9b8cac6e6d534b3f1268'; // Replace with your OpenWeatherMap API key

            axios.get('https://api.openweathermap.org/data/2.5/find', {
                params: {
                    q: this.data.country,
                    type: 'like',
                    sort: 'population',
                    cnt: 10,
                    appid: apiKey
                }
            })
                .then(response => {
                    this.cities = response.data.list.map(city => city.name);
                })
                .catch(error => {
                    console.log(error);
                });
        },

        async save_hotel() {
            try {
                if (this.check_form()) {
                    this.saving = true;

                    // convert the range array to string to save it in db
                    //this.data.range = this.data.range.toString();

                    this.get_persons();
                    // save hotel info
                    var response = await fetch(domain_url + "/backend/hotels/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.data),
                    });

                    if (!response.ok) {
                        // handle the error
                        var errorMessage = "Error: " + response.status + " " + response.statusText;
                        swal(errorMessage, { icon: 'error' });
                    } else {
                        // Request was successful
                        //save all rooms
                        await this.get_max_id();
                        for (const [i, element] of this.data.room.entries()) {
                            element.hotel = this.max_id;
                            element.user = this.data.user;
                            element.room_id = 'room_' + (parseInt(i) + 1);
                            element.range = element.range.toString();
                            await fetch(domain_url + "/backend/rooms/", {
                                method: "post",
                                body: JSON.stringify(element),
                                headers: {
                                    'Content-Type': 'application/json;charset=UTF-8'
                                }
                            });
                            await this.get_max_room_id();

                            // save all room dates to db
                            element.range = element.range.split(","); // str to array
                            let min_date = element.range[0];
                            let max_date = element.range[1];
                            const minDateParts = min_date.split('/');
                            const maxDateParts = max_date.split('/');
                            const startDate = new Date(minDateParts[2], minDateParts[1] - 1, minDateParts[0]);
                            const endDate = new Date(maxDateParts[2], maxDateParts[1] - 1, maxDateParts[0]);

                            const currentDate = new Date(startDate);
                            element.range_dates = [];
                            while (currentDate <= endDate) {
                                element.range_dates.push(currentDate.toLocaleDateString("en-GB"));
                                currentDate.setDate(currentDate.getDate() + 1);
                            }
                            element.range_dates.forEach((element_range) => {
                                fetch(domain_url + "/backend/room_dates/", {
                                    method: "post",
                                    body: JSON.stringify({ 'room_id': this.max_room_id, 'date': element_range }),
                                    headers: {
                                        'Content-Type': 'application/json;charset=UTF-8'
                                    }
                                });
                            });
                        };

                        swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                        this.get_Hotels();
                        await this.get_max_id();
                        this.closeModal();
                    }
                    this.saving = false;

                }
            } catch (error) { console.error(); }
        },

        get_persons() {
            this.data.room.forEach((element) => {
                switch (element.room_type) {
                    case 'SGL':
                        element.persons = 1;
                        break;
                    case 'DBL':
                        element.persons = 2;
                        break;
                    case 'TRPL':
                        element.persons = 3;
                        break;
                    case 'QAD':
                        element.persons = 4;
                        break;
                }
            });


        },

        async update_hotel(id) {
            try {
                if (this.check_form()) {
                    // convert the dates array to string to save it in db
                    this.data.range = this.data.range.toString();

                    var response = await fetch(domain_url + "/backend/hotels/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.data),
                    });

                    if (!response.ok) {
                        // handle the error
                        var errorMessage = "Error: " + response.status + " " + response.statusText;
                        swal(errorMessage, { icon: 'error' });
                    } else {
                        // Request was successful

                        //delete old dates and save the new
                        this.range_dates.forEach((element) => {
                            fetch(domain_url + "/backend/hotel_dates/", {
                                method: "post",
                                body: JSON.stringify({ 'hotel_id': this.max_id, 'date': element }),
                                headers: {
                                    'Content-Type': 'application/json;charset=UTF-8'
                                }
                            });
                        });


                        swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                        this.max_id = this.data.id
                        this.get_Hotels();
                        this.closeModal();
                        this.edit_mode = false;
                    }
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_hotel(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            var response = await fetch(domain_url + '/backend/hotels/' + id + '/', {
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
                                this.clear_form();
                                await this.get_Hotels();
                                this.closeModal();
                            }

                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_hotel(id) {

            return axios({
                method: "get",
                url: domain_url + "/backend/hotels/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.selected_hotel = response.data[0]));

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

        PrintDiv(id) {
            var divToPrint = document.getElementById(id);
            var popupWin = window.open('', '_blank', 'width=100000,height=10000');
            document.getElementById('head_txt').style.display = "block";
            document.getElementById('head_txt').innerHTML = this.$t("Hotels");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Hotels",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        get_max_room_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Rooms",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_room_id = response.data.data.id__max));
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add hotel');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            this.data.room.forEach(element => {
                element.range = element.range.split(',');
            });
            //$('#modal_label').html('Edit hotel');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        close_details_Modal() {
            $('#detailsModal').modal('hide');
        },

        async row_click(index) {
            this.active_index = index; //to change row color

            await this.get_hotel(index);
            await this.get_rooms(index);
            return true
            //this.data.range = this.data.range.split(",");// convert text to array

        },

        clear_form() {
            this.data.name = '';
            this.data.country = '';
            this.data.city = '';
            this.data.area = '';
            this.data.rate = '';
            this.data.allotment = 0;
            this.data.notes = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.data.name &&
                this.data.country &&
                this.data.rate
            ) {
                return true
            } else {
                return false
            }
        },

    },
}
</script>
