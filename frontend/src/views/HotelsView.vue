<template>
    <div class="HotelsView">

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

        <!-- Table Card -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Hotels Table") }} </h6>
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
                                        <th scope="col">{{ $t("Name") }}</th>
                                        <th scope="col">{{ $t("Country") }}</th>
                                        <th scope="col">{{ $t("City") }}</th>
                                        <th scope="col">{{ $t("Area") }}</th>
                                        <th scope="col">{{ $t("Rate") }}</th>
                                        <th scope="col">{{ $t("Allotment") }}</th>
                                        <th scope="col">{{ $t("Notes") }}</th>
                                        <th scope="col">{{ $t("User") }}</th>
                                        <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="r in this.hotels_rows" :key="r.hotel_id"
                                        @click="row_click(r.id)" @click.right="row_click(r.id)" @dblclick="open_edit_modal"
                                        role="button" :class="{ 'selected': r.id === active_index }">
                                        <th scope="row" id="id">{{ r.id }}</th>
                                        <td>{{ $t(r.name) }}</td>
                                        <td>{{ $t(r.country) }}</td>
                                        <td>{{ $t(r.city) }}</td>
                                        <td>{{ $t(r.area) }}</td>
                                        <td>{{ $t(r.rate) }}</td>
                                        <td>{{ $t(r.allotment) }}</td>
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
                                                    <a class="dropdown-item" @click="delete_hotel(hotel.id)">
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
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add hotel") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit hotel") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>

                            <div class="row">

                                <div class="form-group col-md">
                                    <label for="name"> {{ $t("name") }}</label>
                                    <input id="name" v-model="hotel.name"
                                        :class="{ 'is-invalid': !this.hotel.name && this.validate, 'is-valid': this.hotel.name && this.validate }"
                                        type="text" class="form-control">
                                    <div v-if="!this.hotel.name && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter The name") }}
                                    </div>
                                </div>

                                <div class="form-group col-md">
                                    <label for="country"> {{ $t("country") }}</label>
                                    <select id="country" v-model="hotel.country"
                                        :class="{ 'is-invalid': !this.hotel.country && this.validate, 'is-valid': this.hotel.country && this.validate }"
                                        type="text" class="form-control">
                                        <option v-for="country in countries" :value="country.name.common"
                                            :key="country.name.common">
                                            {{ country.name.common }}
                                        </option>
                                    </select>
                                    <div v-if="!this.hotel.country && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter The country") }}
                                    </div>
                                </div>

                                <div class="form-group col-md">
                                    <label for="city"> {{ $t("city") }}</label>
                                    <input id="city" v-model="hotel.city"
                                        :class="{ 'is-invalid': !this.hotel.city && this.validate, 'is-valid': this.hotel.city && this.validate }"
                                        type="text" class="form-control">

                                    <div v-if="!this.hotel.city && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter The city") }}
                                    </div>
                                </div>


                                <div class="form-group col-md">
                                    <label for="area"> {{ $t("area") }}</label>
                                    <input id="area" v-model="hotel.area"
                                        :class="{ 'is-invalid': !this.hotel.area && this.validate, 'is-valid': this.hotel.name && this.validate }"
                                        type="text" class="form-control">
                                    <div v-if="!this.hotel.area && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter The area") }}
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md">
                                    <label for="rate">{{ $t("rate") }}</label>
                                    <select id="rate" v-model="hotel.rate" type="text" class="form-control"
                                        :class="{ 'is-invalid': !this.hotel.rate && this.validate, 'is-valid': this.hotel.rate && this.validate }">
                                        <option :value="$t('5 Star')">{{ $t("5 Star") }} </option>
                                        <option :value="$t('4 Star')">{{ $t("4 Star") }} </option>
                                        <option :value="$t('3 Star')">{{ $t("3 Star") }} </option>
                                        <option :value="$t('2 Star')">{{ $t("2 Star") }} </option>
                                        <option :value="$t('1 Star')">{{ $t("1 Star") }} </option>
                                    </select>
                                    <div v-if="!this.hotel.rate && this.validate" class="invalid-feedback hidden">
                                        {{ $t("Please Select the rate") }}
                                    </div>
                                </div>

                                <div class="form-group col-md">
                                    <label for="allotment"> {{ $t("allotment") }}</label>
                                    <input type="number" min="1" value="1" class="form-control" v-model="hotel.allotment"
                                        id="allotment">
                                </div>

                                <div class="form-group col-md-6">
                                    <label for="hotel_notes"> {{ $t("Notes") }}</label>
                                    <textarea class="form-control" v-model="hotel.notes" id="hotel_notes"
                                        rows="1"></textarea>
                                </div>
                            </div>

                            <div v-if="this.hotel.allotment > 0" class="card form-group">
                                <h4 class="card-header">
                                    {{ $t("Rooms") }}
                                </h4>

                                <div class="card-body">
                                    <div v-for="i in parseInt(hotel.allotment)" :key="i">
                                        <div class="card">
                                            <div class="card-header">
                                                {{ $t("Room") + ' ' + i }}
                                            </div>
                                            <div class="card-body">

                                                <input hidden type="text" v-model="hotel.room[i - 1].hotel">
                                                <input hidden type="text" v-model="hotel.room[i - 1].room_id">
                                                <input hidden type="text" v-model="hotel.room[i - 1].user">
                                                <div class="row">

                                                    <div class="form-group col-md">
                                                        <label for="room_type">{{ $t("Room Type") }}</label>
                                                        <select v-model="hotel.room[i - 1].room_type" type="text"
                                                            class="form-control"
                                                            :class="{ 'is-invalid': !hotel.room[i - 1].room_type && validate, 'is-valid': hotel.room[i - 1].room_type && validate }">
                                                            <option :value="$t('SGL')">{{ $t("SGL") }} </option>
                                                            <option :value="$t('DBL')">{{ $t("DBL") }} </option>
                                                            <option :value="$t('TRPL')">{{ $t("TRPL") }} </option>
                                                            <option :value="$t('QAD')">{{ $t("QAD") }} </option>
                                                        </select>
                                                        <div v-if="!hotel.room[i - 1].room_type && validate"
                                                            class="invalid-feedback hidden">
                                                            {{ $t("Please Select the room type") }}
                                                        </div>
                                                    </div>

                                                    <div class="form-group col-md">
                                                        <label for="room_categ">{{ $t("Room Category") }}</label>
                                                        <input v-model="hotel.room[i - 1].room_categ" type="text"
                                                            class="form-control"
                                                            :class="{ 'is-invalid': !hotel.room[i - 1].room_categ && validate, 'is-valid': hotel.room[i - 1].room_categ && validate }">
                                                        <div v-if="!hotel.room[i - 1].room_categ && validate"
                                                            class="invalid-feedback hidden">
                                                            {{ $t("Please Input Room Category") }}
                                                        </div>
                                                    </div>

                                                    <div class="form-group col-md">
                                                        <label for="meals">{{ $t("Meals") }}</label>
                                                        <select v-model="hotel.room[i - 1].meals" type="text"
                                                            class="form-control"
                                                            :class="{ 'is-invalid': !hotel.room[i - 1].meals && validate, 'is-valid': hotel.room[i - 1].meals && validate }">
                                                            <option :value="$t('B.B')">{{ $t("B.B") }} </option>
                                                            <option :value="$t('H.B')">{{ $t("H.B") }} </option>
                                                            <option :value="$t('F.B')">{{ $t("F.B") }} </option>
                                                            <option :value="$t('ALL')">{{ $t("ALL") }} </option>
                                                            <option :value="$t('ULALL')">{{ $t("ULALL") }} </option>
                                                        </select>
                                                        <div v-if="!hotel.room[i - 1].meals && validate"
                                                            class="invalid-feedback hidden">
                                                            {{ $t("Please Select Meals") }}
                                                        </div>
                                                    </div>

                                                </div>

                                                <div class="row">

                                                    <div class="form-group col-md">
                                                        <label for="cutomer_notes"> {{ $t("Date Range") }}</label>

                                                        <date-picker v-model="hotel.room[i - 1].range" range clearable
                                                            :auto-submit="true" color="#098290" input-format="DD/MM/YYYY"
                                                            format="DD/MM/YYYY" locale="en" />

                                                    </div>

                                                    <div class="form-group col-md">
                                                        <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                                        <textarea class="form-control" v-model="hotel.room[i - 1].notes"
                                                            id="cutomer_notes" rows="1"></textarea>
                                                    </div>

                                                </div>
                                            </div>
                                        </div>
                                        <br>
                                    </div>
                                </div>

                            </div>
                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_hotel()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_hotel(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_hotel(active_index)"
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
    name: 'HotelsView',
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker
    },

    data() {
        return {
            saving: false,
            validate: false, //for check forms
            base_url: window.location.origin + '/media/hotels/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            //////////////////////////
            countries: [],
            selectedCountry: '',
            cities: [],
            hotels_rows: [],
            hotel: {
                name: "",
                country: "",
                city: "",
                area: "",
                rate: "",
                allotment: 0,
                notes: "",
                user: "",
                room: [{
                    hotel: "",
                    room_id: "",
                    room_categ: "",
                    room_type: "",
                    meals: "",
                    persons: 0,
                    range: [],
                    range_dates: [],
                    notes: "",
                    user: "",
                }],
            },

            edit_mode: false,
            max_id: 0,
            max_room_id: 0,
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
        // get user name to save in any record
        this.hotel.user = localStorage.getItem('user_name')

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////

        await this.get_Hotels();
        await this.get_max_room_id();
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
                this.get_Hotels();
            }
        },
    },

    watch: {
        'hotel.allotment'(newValue) {
            //to + - rooms count
            if (newValue > this.hotel.room.length) {
                const numberOfRoomsToAdd = newValue - this.hotel.room.length;
                for (let i = 0; i < numberOfRoomsToAdd; i++) {
                    this.hotel.room.push({
                        // initialize new room data
                    });
                }
            } else if (newValue < this.hotel.room.length) {
                const numberOfRoomsToRemove = this.hotel.room.length - newValue;
                this.hotel.room.splice(newValue, numberOfRoomsToRemove);
            }

            // if (newValue > 0 && newValue > hotel.room.length) {

            //    hotel.room.push({
            //         hotel: "",
            //         room_id: "",
            //         room_categ: "",
            //         room_type: "",
            //         meals: "",
            //         persons: 0,
            //         range: [],
            //         notes: "",
            //         user: ""
            //     });
            // }
            // else if (newValue > 0 && newValue < hotel.room.length) {
            //     hotel.room.pop();
            // }
        },
        'hotel.country'() {
            this.getCities();
        }
    },

    methods: {
        get_Hotels() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/hotels/')
                .then((response) => (this.hotels_rows = response.data))
                .catch(err => { alert(err) });
        },

        getCities() {
            const apiKey = '02b73423a39d9b8cac6e6d534b3f1268'; // Replace with your OpenWeatherMap API key

            axios.get('https://api.openweathermap.org/data/2.5/find', {
                params: {
                    q: this.hotel.country,
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
                    //this.hotel.range = this.hotel.range.toString();

                    this.get_persons();
                    // save hotel info
                    var response = await fetch(domain_url + "/backend/hotels/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.hotel),
                    });

                    if (!response.ok) {
                        // handle the error
                        var errorMessage = "Error: " + response.status + " " + response.statusText;
                        swal(errorMessage, { icon: 'error' });
                    } else {
                        // Request was successful
                        //save all rooms
                        await this.get_max_id();
                        for (const [i, element] of this.hotel.room.entries()) {
                            element.hotel = this.max_id;
                            element.user = this.hotel.user;
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
                            alert(this.max_room_id);
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
            this.hotel.room.forEach((element) => {
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
                    this.hotel.range = this.hotel.range.toString();

                    var response = await fetch(domain_url + "/backend/hotels/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.hotel),
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
                        this.max_id = this.hotel.id
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
            }).then((response) => (this.hotel = response.data[0]));
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

        get_hotel_type(value) {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_hotel_type/?hotel_id=" + value,
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.hotel.hotel_type = response.data[0]));
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add hotel');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            //$('#modal_label').html('Edit hotel');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            this.active_index = index; //to change row color
            await this.get_hotel(index);

            this.hotel.range = this.hotel.range.split(",");// convert text to array
        },

        clear_form() {
            this.hotel.name = '';
            this.hotel.country = '';
            this.hotel.city = '';
            this.hotel.area = '';
            this.hotel.rate = '';
            this.hotel.allotment = 0;
            this.hotel.notes = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.hotel.name &&
                this.hotel.country &&
                this.hotel.rate
            ) {
                return true
            } else {
                return false
            }
        },

    },
}
</script>
