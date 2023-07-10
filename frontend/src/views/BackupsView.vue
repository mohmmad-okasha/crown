<template>
    <div class="backupsView">
        <loading :active.sync="isLoading" :can-cancel="false" :is-full-page="fullPage"></loading>

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>

                <a class="dropdown-item" @click="restore_backup(active_index)">
                    <i class="fa fa-arrow-right-arrow-left"></i>
                    {{ $t("Restore") }}
                </a>
                <a class="dropdown-item" @click="delete_backup(active_index)">
                    <i class="fa fa-trash"></i>
                    {{ $t("Delete") }}
                </a>
            </ul>
        </div>

        <!-- Table Card -->
        <div class="col-xl-12 center">
            <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Backups Table") }} </h6>
                    <div class="dropdown no-arrow">

                        <div class="btn-group" role="group">
                            <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                <i class="fa fa-bars on-hover"></i>
                            </button>
                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1" x-placement="bottom-start"
                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">

                                <a class="dropdown-item hand-mouse" @click="save_backup()">
                                    <i class="fa fa-download"></i>
                                    {{ $t("Save Backup") }}
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
                            <table id="mytable" class="table table-hover">
                                <thead>
                                    <tr>
                                        <th scope="col">{{ $t("Name") }}</th>
                                        <th scope="col">{{ $t("Time") }}</th>
                                        <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr @contextmenu="showContextMenu" v-for="r in this.backups_rows" :key="r.name"
                                        @click="row_click(r.name)" @click.right="row_click(r.name)" role="button"
                                        :class="{ 'selected': r.name === active_index }">
                                        <td>{{ $t(r.name) }}</td>
                                        <td>{{ $t(r.time) }}</td>

                                        <td class="no_print">

                                            <div class="btn-group" role="group">
                                                <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                                    <i class="fa fa-gear on-hover"></i>
                                                </button>
                                                <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                    x-placement="bottom-start"
                                                    style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                    <a class="dropdown-item" @click="restore_backup(r.name)">
                                                        <i class="fa fa-arrow-right-arrow-left"></i>
                                                        {{ $t("Restore") }}
                                                    </a>
                                                    <a class="dropdown-item" @click="delete_backup(r.name)">
                                                        <i class="fa fa-trash"></i>
                                                        {{ $t("Delete") }}
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
import XLSX from 'xlsx/dist/xlsx.full.min';

export default {
    name: 'backupsView',
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
            base_url: window.location.origin + '/media/backups/',//for images 
            active_index: null,//current id
            //////////////////////////
            backups_rows: [],

            user_roles: '',
            max_id: 0,
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

        //to remove modal background on auto vue js reload
        const elements = document.getElementsByClassName("modal-backdrop fade show");
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }////

        await this.get_backups();

        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        await this.get_roles();
        if (this.user_roles[this.$route.path.substring(1)] == 0) {
            this.$router.back()
        }

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
                    url: domain_url + "/backend/backups/?search=" + data,
                }).then((response) => (this.backups = response.data));
            } else {
                this.get_backups();
            }
        },
    },


    methods: {
        get_roles() {
            this.user_roles = this.$parent.user_roles;
        },

        get_backups() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/get_backup_files/')
                .then((response) => (this.backups_rows = response.data.data))
                .catch(err => { alert(err) });
        },


        async save_backup() {
            this.isLoading = true;

            try {
                my_api.get('/backend/save_backup/')
                    .then(swal(this.$t("Saved!"), { buttons: false, icon: "success", timer: 2000, }))
                    .catch(err => { swal(err, { icon: 'error' }) });

            } catch (error) { console.error(); }
            await this.get_backups()
            this.isLoading = false;

        },

        async restore_backup(backup_name) {
            await swal({ title: this.$t("Are you sure to restore "+backup_name+" backup?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                .then(async (willrestore) => {
                    if (willrestore) {
                        this.isLoading = true;

                        await this.save_backup();

                        try {
                            my_api.get('/backend/restore_backup/?backup_name=' + backup_name)
                                .then(swal(this.$t("Restored!"), { buttons: false, icon: "success", timer: 2000, }))
                                .catch(err => { swal(err, { icon: 'error' }) });

                        } catch (error) { console.error(); }
                        await this.get_backups()
                        this.isLoading = false;
                    }
                });

        },


        async delete_backup(backup_name) {
            this.isLoading = true;
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            var response = await fetch(domain_url + '/backend/remove_backup_file/?backup_name=' + backup_name, {
                                method: "get",
                                headers: { "Content-Type": "application/json", },
                            });
                            if (!response.ok) {
                                // handle the error
                                var errorMessage = "Error: " + response.status + " " + response.statusText;
                                swal(errorMessage, { icon: 'error' });
                            } else {
                                // Request was successful
                                swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                                await this.get_backups();
                            }

                        }
                    });
            } catch (error) { console.error(); }
            this.isLoading = false;
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
            document.getElementById('head_txt').innerHTML = this.$t("backups");
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

            await this.get_backup(index);
            await this.get_rooms(index);
            return true
            //this.backup.range = this.backup.range.split(",");// convert text to array

        },

    },
}
</script>
