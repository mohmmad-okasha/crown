<template>
    <div class="logsView">
        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>


        <!-- Table Card -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Logs Table") }} </h6>
                    
                    <div class="dropdown no-arrow">

                        <div class="btn-group" role="group">
                            <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                <i class="fa fa-bars on-hover"></i>
                            </button>
                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1" x-placement="bottom-start"
                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
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

                    <!-- search -->
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-2"></div>

                                <div class="col-sm-3 m-1">
                                    <label class="col-form-label">{{ $t("User") }}</label>
                                    <select class="form-control" placeholder="user" v-model="user" @change="filter_data()">
                                        <option v-for="u in this.users" :key="u" :value="u"> {{ u }}</option>
                                    </select>
                                </div>
                                
                                <div class="col-sm-4 m-1">
                                    <label class="col-form-label">{{ $t("Date Range") }}</label>
                                    <input type="text" class="custom-input form-control" placeholder="Range"
                                        aria-label="Range">
                                    <date-picker v-model="range" :range="true" clearable locale="en"
                                        :auto-submit="true" color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY"
                                        display-format="DD/MM/YYYY" custom-input=".custom-input" @change="filter_data()" />
                                </div>

                            </div>
                        </div>
                    </div>


                    <div class="card-header cnter" style="display: none;" id="head_txt"></div>
                    <form class="site-form-table">
                        <div class="table-responsive">
                            <table id="mytable" class="table table-hover">
                                <thead>
                                    <tr>
                                        <th scope="col">{{ $t("User Name") }}</th>
                                        <th scope="col">{{ $t("Log") }}</th>
                                        <th scope="col">{{ $t("Time") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="r in this.logs_rows" :key="r.name"
                                        @click="row_click(r.name)" @click.right="row_click(r.name)" role="button"
                                        :class="{ 'selected': r.name === active_index }">
                                        <td>{{ $t(r.user_name) }}</td>
                                        <td>{{ $t(r.log) }}</td>
                                        <td>{{ r.time | formatDate }}</td>
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


    </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import { my_api, domain_url } from "../axios-api";

import NavBar from '../components/parts/NavBar.vue'

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
import swal from 'sweetalert';

export default {
    name: 'logsView',
    components: {
        NavBar,
        datePicker: VuePersianDatetimePicker,
        Loading,
    },

    data() {
        return {
            isLoading: false,
            fullPage: true,
            user: '',
            range: [],
            users: [],
            active_index: null,//current id
            logs_rows: [],
            user_roles: '',
            max_id: 0,
        }
    },

    async mounted() {
        this.isLoading = true;
        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////
        
        await this.get_logs();
        this.get_users();

        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        await this.get_roles();
        if (this.user_roles[this.$route.path.substring(1)] == 0) {
            this.$router.back()
        }

        this.isLoading = false;
    },

    
    filters: {
        formatDate(value) {
            const date = new Date(value);
            const formattedDate = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`;
            return formattedDate;
        }
    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/logs/?search=" + data,
                }).then((response) => (this.logs = response.data));
            } else {
                this.get_logs();
            }
        },
    },


    methods: {
        filter_data() {
            
            if (this.user && this.range.length==0) {

                return axios({
                    method: "get",
                    url: domain_url + "/backend/logs/?user=" + this.user,
                }).then((response) => (this.logs_rows = response.data));
            } else if (this.range.length>1 && !this.user) {
                return axios({
                    method: "get",
                    url: domain_url + "/backend/logs/?range=" + this.range.toString(),
                }).then((response) => (this.logs_rows = response.data));
            } else if (this.range.length>1 && this.user) {
                return axios({
                    method: "get",
                    url: domain_url + "/backend/logs/?range=" + this.range.toString() +'&user='+this.user,
                }).then((response) => (this.logs_rows = response.data));
            } else {
                this.get_logs();
            }
        },

        get_roles() {
            this.user_roles = this.$parent.user_roles;
        },

        get_users() {
            return my_api.get('/backend/get_users/')
                .then((response) => (this.users = response.data))
                .catch(err => { alert(err) });
        },

        get_logs() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/logs/')
                .then((response) => (this.logs_rows = response.data))
                .catch(err => { alert(err) });
        },

        PrintDiv(id) {
            var divToPrint = document.getElementById(id);
            var popupWin = window.open('', '_blank', 'width=100000,height=10000');
            document.getElementById('head_txt').style.display = "block";
            document.getElementById('head_txt').innerHTML = this.$t("logs");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        async row_click(index) {
            this.active_index = index; //to change row color

            await this.get_log(index);
            await this.get_rooms(index);
            return true
            //this.log.range = this.log.range.split(",");// convert text to array

        },

    },
}
</script>
