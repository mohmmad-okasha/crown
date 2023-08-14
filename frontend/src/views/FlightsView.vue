<template>
    <!-- &nbsp; -->
    <div class="FlightsView">

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_flight(flight.id)">
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
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Flights Table") }} </h6>
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
                                    <th scope="col">{{ $t("Code") }}</th>
                                    <th scope="col">{{ $t("Airline") }}</th>
                                    <th scope="col">{{ $t("From airport") }}</th>
                                    <th scope="col">{{ $t("To airport") }}</th>
                                    <th scope="col">{{ $t("Departure date") }}</th>
                                    <th scope="col">{{ $t("Arrival date") }}</th>
                                    <th scope="col">{{ $t("Seats") }}</th>
                                    <th scope="col">{{ $t("Status") }}</th>
                                    <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr @contextmenu="showContextMenu" v-for="flight in this.flights" :key="flight.id"
                                    @click="row_click(flight.id)" @click.right="row_click(flight.id)"
                                    @dblclick="open_edit_modal" role="button"
                                    :class="{ 'selected': flight.id === active_index }">
                                    <th scope="row" id="id">{{ flight.id }}</th>
                                    <td>{{ $t(flight.code) }}</td>
                                    <td>{{ $t(flight.airline) }}</td>
                                    <td>{{ $t(flight.from_airport) }}</td>
                                    <td>{{ $t(flight.to_airport) }}</td>
                                    <td>{{ formatDate(flight.departure_date) }}</td>
                                    <td>{{ formatDate(flight.arrival_date) }}</td>
                                    <td>{{ $t(flight.seats) }}</td>
                                    <td>
                                        <img v-if="flight.status == 'enable'" width="30px" height="30px"
                                            src="https://img.icons8.com/color/2x/ok--v1">
                                        <img v-if="flight.status == 'disabled'" width="30px" height="30px"
                                            src="https://img.icons8.com/color/2x/cancel--v1">
                                    </td>

                                    <td class="no_print">

                                        <div class="btn-group" role="group">
                                            <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                                <i class="fa fa-gear on-hover"></i>
                                            </button>
                                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                x-placement="bottom-start"
                                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                <a class="dropdown-item" @click="delete_flight(flight.id)">
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
        <date-picker multiple type="datetime" compact-time v-model="date" />

        <!-- modal -->
        <div class="modal fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add Flight") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit Flight") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>
                            <div class="form-group">
                                <label for="flight_code">{{ $t("Code") }}</label>
                                <input id="flight_code" v-model="flight.code" type="text"
                                    :class="{ 'is-invalid': !this.flight.code && this.validate, 'is-valid': this.flight.code && this.validate }"
                                    class="form-control">
                                <div v-if="!this.flight.code && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The code") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="airline">{{ $t("Airline") }}</label>
                                <div class="container p-0">
                                    <div class="row">
                                        <div class="col col-11 pr-0">
                                            <v-select id="airline" v-model="flight.airline" :options="airlineOptions"
                                                :class="{ 'is-invalid': !this.flight.airline && this.validate, 'is-valid': this.flight.airline && this.validate }" />
                                            <div v-if="!this.flight.airline && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Select airline") }}
                                            </div>
                                        </div>
                                        <div class="col col-1 p-0">
                                            <button class="btn btn-light" type="button" data-toggle="collapse"
                                                data-target="#airline_collapse" aria-expanded="false"
                                                aria-controls="collapseExample">
                                                <i class="fa-solid fa-pen-to-square"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="collapse m-4" id="airline_collapse">
                                        <div class="card">
                                            <div class="card-header">
                                                Airlines
                                            </div>
                                            <div class="card-body">
                                                <div class="table-responsive-sm table-sm">
                                                    <table class="table">
                                                        <thead>
                                                            <tr>
                                                                <th scope="col">Code</th>
                                                                <th scope="col">Name EN</th>
                                                                <th scope="col">Name AR</th>
                                                                <th scope="col">City</th>
                                                                <th scope="col">Actions</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr v-for="a in this.airlines" :key="a.code">
                                                                <th>{{ a.code }}</th>
                                                                <th>{{ a.name_en }}</th>
                                                                <th>{{ a.name_ar }}</th>
                                                                <th>{{ a.city }}</th>
                                                                <th>
                                                                    <button @click="delete_airline(a.id)"
                                                                        class="btn btn-dangares" type="button"> <i
                                                                            class="fa-solid fa-trash"></i>
                                                                    </button>
                                                                </th>
                                                            </tr>
                                                        </tbody>

                                                    </table>
                                                    <hr>
                                                    <div class="center">
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airline.name_ar" type="text"
                                                                    placeholder="Name ar" class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airline.name_en" type="text"
                                                                    placeholder="Name en" class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airline.code" type="text" placeholder="Code"
                                                                    class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airline.city" type="text" placeholder="City"
                                                                    class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <button @click="save_airline()" class=" btn btn-light"
                                                            type="button">
                                                            <i class="fa-solid fa-plus"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                                <div class="text-center mt-4">
                                                    <a class="center" onclick="$('#airline_collapse').collapse('hide')"><i
                                                            class="fa-solid fa-chevron-up"></i></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="airport">{{ $t("From Airport") }}</label>
                                <div class="container p-0">
                                    <div class="row">
                                        <div class="col col-11 pr-0">
                                            <v-select id="from_airport" v-model="flight.from_airport"
                                                :options="airportOptions"
                                                :class="{ 'is-invalid': !this.flight.from_airport && this.validate, 'is-valid': this.flight.from_airport && this.validate }" />
                                            <div v-if="!this.flight.from_airport && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Select from airport") }}
                                            </div>
                                        </div>
                                        <div class="col col-1 p-0">
                                            <button class="btn btn-light" type="button" data-toggle="collapse"
                                                data-target="#from_airport_collapse" aria-expanded="false"
                                                aria-controls="collapseExample">
                                                <i class="fa-solid fa-pen-to-square"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="collapse m-4" id="from_airport_collapse">
                                        <div class="card">
                                            <div class="card-header">
                                                Airports
                                            </div>
                                            <div class="card-body">
                                                <div class="table-responsive-sm table-sm">
                                                    <table class="table">
                                                        <thead>
                                                            <tr>
                                                                <th scope="col">Code</th>
                                                                <th scope="col">Name EN</th>
                                                                <th scope="col">Name AR</th>
                                                                <th scope="col">City</th>
                                                                <th scope="col">Actions</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr v-for="a in this.airports" :key="a.code">
                                                                <th>{{ a.code }}</th>
                                                                <th>{{ a.name_en }}</th>
                                                                <th>{{ a.name_ar }}</th>
                                                                <th>{{ a.city }}</th>
                                                                <th>
                                                                    <button @click="delete_airport(a.id)"
                                                                        class="btn btn-dangares" type="button"> <i
                                                                            class="fa-solid fa-trash"></i>
                                                                    </button>
                                                                </th>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    <hr>
                                                    <div class="center">
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airport.name_ar" type="text"
                                                                    placeholder="Name ar" class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airport.name_en" type="text"
                                                                    placeholder="Name en" class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airport.code" type="text" placeholder="Code"
                                                                    class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airport.city" type="text" placeholder="City"
                                                                    class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <button @click="save_airport()" class=" btn btn-light"
                                                            type="button">
                                                            <i class="fa-solid fa-plus"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                                <div class="text-center mt-4">
                                                    <a class="center"
                                                        onclick="$('#from_airport_collapse').collapse('hide')"><i
                                                            class="fa-solid fa-chevron-up"></i></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="airport">{{ $t("To Airport") }}</label>
                                <div class="container p-0">
                                    <div class="row">
                                        <div class="col col-11 pr-0">
                                            <v-select id="to_airport" v-model="flight.to_airport" :options="airportOptions"
                                                :class="{ 'is-invalid': !this.flight.to_airport && this.validate, 'is-valid': this.flight.to_airport && this.validate }" />
                                            <div v-if="!this.flight.to_airport && this.validate"
                                                class="invalid-feedback hidden">
                                                {{ $t("Please Select to airport") }}
                                            </div>
                                        </div>
                                        <div class="col col-1 p-0">
                                            <button class="btn btn-light" type="button" data-toggle="collapse"
                                                data-target="#to_airport_collapse" aria-expanded="false"
                                                aria-controls="collapseExample">
                                                <i class="fa-solid fa-pen-to-square"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="collapse m-4" id="to_airport_collapse">
                                        <div class="card">
                                            <div class="card-header">
                                                Airports
                                            </div>
                                            <div class="card-body">
                                                <div class="table-responsive-sm table-sm">
                                                    <table class="table">
                                                        <thead>
                                                            <tr>
                                                                <th scope="col">Code</th>
                                                                <th scope="col">Name EN</th>
                                                                <th scope="col">Name AR</th>
                                                                <th scope="col">City</th>
                                                                <th scope="col">Actions</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr v-for="a in this.airports" :key="a.code">
                                                                <th>{{ a.code }}</th>
                                                                <th>{{ a.name_en }}</th>
                                                                <th>{{ a.name_ar }}</th>
                                                                <th>{{ a.city }}</th>
                                                                <th>
                                                                    <button @click="delete_airport(a.id)"
                                                                        class="btn btn-dangares" type="button"> <i
                                                                            class="fa-solid fa-trash"></i>
                                                                    </button>
                                                                </th>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    <hr>
                                                    <div class="center">
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airport.name_ar" type="text"
                                                                    placeholder="Name ar" class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airport.name_en" type="text"
                                                                    placeholder="Name en" class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <div class="row">
                                                            <div class="col-6">
                                                                <input v-model="airport.code" type="text" placeholder="Code"
                                                                    class="form-control">
                                                            </div>
                                                            <div class="col-6">
                                                                <input v-model="airport.city" type="text" placeholder="City"
                                                                    class="form-control">
                                                            </div>
                                                        </div>
                                                        <br>
                                                        <button @click="save_airport()" class=" btn btn-light"
                                                            type="button">
                                                            <i class="fa-solid fa-plus"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                                <div class="text-center mt-4">
                                                    <a class="center"
                                                        onclick="$('#to_airport_collapse').collapse('hide')"><i
                                                            class="fa-solid fa-chevron-up"></i></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group mb-2">
                                <label for="departure_date">{{ $t("Departure date") }}</label>
                                <!-- datetime-local -->
                                <input id="departure_date" v-model="flight.departure_date" type="datetime-local"
                                    :class="{ 'is-invalid': !this.flight.departure_date && this.validate, 'is-valid': this.flight.departure_date && this.validate }"
                                    class="form-control">

                                <div v-if="!this.flight.type && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter departure_date") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="arrival_date"> {{ $t("Arrival date") }}</label>
                                <input id="arrival_date" v-model="flight.arrival_date"
                                    :class="{ 'is-invalid': !this.flight.arrival_date && this.validate, 'is-valid': this.flight.arrival_date && this.validate }"
                                    type="datetime-local" class="form-control">
                                <div v-if="!this.flight.arrival_date && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The arrival date") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="seats"> {{ $t("Seats") }}</label>
                                <input id="seats" v-model="flight.seats"
                                    :class="{ 'is-invalid': !this.flight.seats && this.validate, 'is-valid': this.flight.seats && this.validate }"
                                    type="number" class="form-control">
                                <div v-if="!this.flight.seats && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The seats") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="status">{{ $t("Status") }}</label>
                                <select id="status" v-model="flight.status" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.flight.status && this.validate, 'is-valid': this.flight.status && this.validate }">
                                    <option selected :value="$t('enable')">{{ $t("Enable") }} </option>
                                    <option :value="$t('disabled')">{{ $t("Disabled") }} </option>
                                </select>
                                <div v-if="!this.flight.status && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select the status") }}
                                </div>
                            </div>

                            <div class="form-group ">
                                <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                                <textarea class="form-control" v-model="flight.notes" id="cutomer_notes"
                                    rows="1"></textarea>
                            </div>

                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_flight()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button type="button" title="save and add" @click="save_and_add()"
                            class="btn btn-success on-hover-sm">
                            <i class="fa fa-copy"></i>
                        </button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_flight(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_flight(active_index)"
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
import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import { lang, change_lang } from '../main';
import vSelect from 'vue-select';

import NavBar from '../components/parts/NavBar.vue'

export default {
    name: 'FlightsView',
    components: {
        NavBar,
        vSelect
    },

    data() {
        return {
            date: '',
            validate: false, //for check forms
            base_url: window.location.origin + '/media/flights/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            flights: [],
            airlines: [],
            airports: [],
            flight: {
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
            airline: {
                name_ar: '',
                name_en: '',
                code: '',
                city: ''
            },
            airport: {
                name_ar: '',
                name_en: '',
                code: '',
                city: ''
            },
            add_airline: '',
            add_airport: '',
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
        await this.get_flights();
        this.get_airlines();
        this.get_airports();

    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/flights/?search=" + data,
                }).then((response) => (this.flights = response.data));
            } else {
                this.get_flights();
            }
        },
        airlineOptions() {
            return this.airlines.map(airline => airline.code);
        },
        airportOptions() {
            return this.airports.map(airport => airport.code);
        },
        format_dates() {
            //this.flight.arrival_date = this.formatDate(this.flight.arrival_date);
            //this.flight.departure_date = this.formatDate(this.flight.departure_date);
        }
    },

    methods: {
        formatDate(date) {
            const formattedDate = new Date(date);
            const day = String(formattedDate.getDate()).padStart(2, '0');
            const month = String(formattedDate.getMonth() + 1).padStart(2, '0');
            const year = formattedDate.getFullYear();
            let hours = formattedDate.getHours();
            const minutes = String(formattedDate.getMinutes()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';

            // Convert hours to 12-hour format and add leading zeros
            hours = String((hours % 12) || 12).padStart(2, '0');

            return `${month}/${day}/${year} ${hours}:${minutes} ${ampm}`;
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
            document.getElementById('head_txt').innerHTML = this.$t("Flights");
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
                return axios.post(domain_url + "/backend/upload_file/?file_name=/flights/" + this.max_id + '_' + this.flight.name + '.png', formData, {
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

        get_flights() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/flights/')
                .then((response) => (this.flights = response.data))
                .catch(err => { alert(err) });
        },

        async save_flight() {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/flights/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.flight),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });

                    await this.get_max_id();

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add flight :' + this.max_id, time: new Date() })

                    this.get_flights();
                    this.closeModal();
                }
            } catch (error) { console.error(); }
        },

        async save_and_add() {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/flights/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.flight),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });

                    await this.get_max_id();

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add flight :' + this.max_id, time: new Date() })

                    this.get_flights();

                    this.validate = false;
                }
            } catch (error) { console.error(); }
        },

        async get_airlines() {
            return my_api.get('/backend/airlines/')
                .then((response) => (this.airlines = response.data))
                .catch(err => { alert(err) });
        },

        async save_airline() {
            try {
                var response = await fetch(domain_url + "/backend/airlines/", {
                    method: "post",
                    headers: { "Content-Type": "application/json", },
                    body: JSON.stringify(this.airline),
                });

                if (response.ok) {
                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                    $('#airline_collapse').collapse('hide');

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add airline :' + this.airline.name_en, time: new Date() })

                    await this.get_airlines();
                    this.add_airline = '';
                    this.flight.airline = airlineOptions[airlineOptions.length - 1]
                }
                else {
                    var data = await response.json();
                    swal(this.$t(JSON.stringify(data.name[0])), { buttons: false, icon: "error", timer: 5000, });

                }



            } catch (error) { console.error(); }
        },

        async delete_airline(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/airlines/' + id + '/')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });

                            //save log
                            axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'delete airline id:' + id, time: new Date() })

                            await this.get_airlines();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_airports() {
            return my_api.get('/backend/airports/')
                .then((response) => (this.airports = response.data))
                .catch(err => { alert(err) });
        },

        async save_airport() {
            try {
                var response = await fetch(domain_url + "/backend/airports/", {
                    method: "post",
                    headers: { "Content-Type": "application/json", },
                    body: JSON.stringify(this.airport),
                });

                if (response.ok) {
                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add airport :' + this.airport.name_en, time: new Date() })

                    $('#airports_collapse').collapse('hide');
                    $('#airports_collapse2').collapse('hide');
                    await this.get_airports();
                    this.add_airport = '';
                    this.flight.airport = airportOptions[airportOptions.length - 1]
                }
                else {
                    var data = await response.json();
                    swal(this.$t(JSON.stringify(data.name[0])), { buttons: false, icon: "error", timer: 5000, });

                }



            } catch (error) { console.error(); }
        },

        async delete_airport(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/airports/' + id + '/')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });

                            //save log
                            axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'delete airport id:' + id, time: new Date() })

                            await this.get_airports();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async update_flight(id) {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/flights/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.flight),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'update flight :' + id, time: new Date() })

                    this.max_id = this.flight.id
                    await this.uploadImage();
                    this.get_flights();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_flight(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/flights/' + id + '/')
                            this.remove_file('/flights/' + id + '_' + this.flight.name + '.png')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });

                            //save log
                            axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'delete flight :' + id, time: new Date() })

                            await this.get_flights(); this.closeModal();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_flight(id) {
            return axios({
                method: "get",
                url: domain_url + "/backend/flights/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.flight = response.data[0]));
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Flights",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add Flight');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            //$('#modal_label').html('Edit Flight');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            this.active_index = index; //to change row color
            await this.get_flight(index);
        },

        clear_form() {
            this.flight.code = '';
            this.flight.airline = '';
            this.flight.from_airport = '';
            this.flight.to_airport = '';
            this.flight.departure_date = '';
            this.flight.arrival_date = '';
            this.flight.seats = '';
            this.flight.status = '';
            this.flight.notes = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.flight.code &&
                this.flight.airline &&
                this.flight.from_airport &&
                this.flight.to_airport &&
                this.flight.departure_date &&
                this.flight.arrival_date &&
                this.flight.seats &&
                this.flight.status
            ) {
                return true
            } else {
                return false
            }
        },

    },
}

</script>
