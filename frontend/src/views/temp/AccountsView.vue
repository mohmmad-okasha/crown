<template>
    <!-- &nbsp; -->
    <div class="AccountsView">

        <!-- context-menu -->
        <div id="context-menu" class="context-menu" :style="menuStyle">
            <ul>
                <li class="dropdown-item" @click="delete_account(account.id)">
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
                    <h6 class="m-0 font-weight-bold text-primary">{{ $t("Accounts Table") }} </h6>
                    <div class="dropdown no-arrow">

                        <div class="btn-group" role="group">
                            <button id="btnGroupVerticalDrop1" type="button" class="btn dropdown-toggle"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                <i class="fa fa-bars on-hover"></i>
                            </button>
                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1" x-placement="bottom-start"
                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                <a class="dropdown-item" @click="open_add_modal">
                                    <i class="fa fa-plus"></i>
                                    {{ $t("Add") }}
                                </a>
                                <a class="dropdown-item" @click="PrintDiv('table')">
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
                                    <th scope="col">{{ $t("Parent") }}</th>
                                    <th scope="col">{{ $t("Name") }}</th>
                                    <th scope="col">{{ $t("Debit") }}</th>
                                    <th scope="col">{{ $t("Credit") }}</th>
                                    <th scope="col">{{ $t("User") }}</th>
                                    <th scope="col" class="no_print">{{ $t("Actions") }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr @contextmenu="showContextMenu" v-for="account in this.accounts" :key="account.id"
                                    @click="row_click(account.id)" @click.right="row_click(account.id)"
                                    @dblclick="open_edit_modal" role="button"
                                    :class="{ 'selected': account.id === active_index }">
                                    <th scope="row" id="id">{{ account.id }}</th>
                                    <td>{{ $t(account.parent) }}</td>
                                    <td>{{ $t(account.name) }}</td>
                                    <td>{{ $t(account.debit) }}</td>
                                    <td>{{ $t(account.credit) }}</td>
                                    <td>{{ $t(account.user) }}</td>

                                    <td class="no_print">
                                        <div class="btn-group" role="group">
                                            <button @click.right="alert('1')" id="btnGroupVerticalDrop1" type="button"
                                                class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true"
                                                aria-expanded="true">
                                                <i class="fa fa-gear on-hover"></i>
                                            </button>
                                            <div class="dropdown-menu" aria-labelledby="btnGroupVerticalDrop1"
                                                x-placement="bottom-start"
                                                style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 37px, 0px);">
                                                <a class="dropdown-item" @click="delete_account(account.id)">
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

        <!-- to get search value from navbar -->
        <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>

        <!-- modal -->
        <div class="modal fade" id="addModal" data-backdrop="static" data-keyboard="false" tabindex="-1"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 v-if="!this.edit_mode" class="modal-title" id="modal_label">{{ $t("Add Account") }}</h5>
                        <h5 v-if="this.edit_mode" class="modal-title" id="modal_label">{{ $t("Edit Account") }}</h5>
                        <button type="button" class="close on-hover" @click="this.closeModal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">

                        <form>
                            <div class="form-group">
                                <label for="account_name">{{ $t("Name") }}</label>
                                <input id="account_name" v-model="account.name" type="text"
                                    :class="{ 'is-invalid': !this.account.name && this.validate, 'is-valid': this.account.name && this.validate }"
                                    class="form-control">
                                <div v-if="!this.account.name && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Enter The Account Name") }}
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="Parent">{{ $t("Parent") }}</label>
                                <select id="Parent" v-model="account.parent" type="text" class="form-control"
                                    :class="{ 'is-invalid': !this.account.parent && this.validate, 'is-valid': this.account.parent && this.validate }">
                                    <option selected :value="$t('Account')">{{ $t("Account") }}</option>
                                    <option :value="$t('Supplier')">{{ $t("Supplier") }}</option>
                                </select>
                                <div v-if="!this.account.parent && this.validate" class="invalid-feedback hidden">
                                    {{ $t("Please Select The Parent") }}
                                </div>
                            </div>
                        </form>

                    </div>
                    <div class="modal-footer">

                        <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                            @click="this.closeModal">
                            <i class="fa fa-xmark"></i>
                        </button>

                        <button v-if="!edit_mode" type="button" title="save" @click="save_account()"
                            class="btn btn-primary on-hover-sm">
                            <i class="fa fa-floppy-disk"></i></button>

                        <button v-if="edit_mode" type="button" title="delete" @click="delete_account(active_index)"
                            class="btn btn-danger on-hover-sm"> <i class="fa fa-trash"></i> </button>

                        <button v-if="edit_mode" type="button" title="save" @click="update_account(active_index)"
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

export default {
    name: 'AccountsView',
    components: {
        NavBar,
    },

    data() {
        return {
            validate: false, //for check forms
            base_url: window.location.origin + '/media/accounts/',//for images 
            previewImage: null,// to show selected image before save
            img_file: null,
            active_index: null,//current id
            accounts: [],
            account: {
                id: "",
                parent: "",
                name: "",
                debit: 0,
                credit: 0,
                user: "admin",
            },
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

        await this.get_accounts();
        this.teest();
    },

    computed: {
        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/accounts/?search=" + data,
                }).then((response) => (this.accounts = response.data));
            } else {
                this.get_accounts();
            }
        },
    },

    methods: {

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
            document.getElementById('head_txt').innerHTML = this.$t("Accounts");
            popupWin.document.write('<link href="static/css/sb-admin-2.min.css" rel="stylesheet">');
            popupWin.document.write('<link href="static/css/reports.css" rel="stylesheet">');
            popupWin.document.write('<style>body{background-color:white !important;}</style>');
            popupWin.document.write('<iframe src="static/parts/report_head.html" width="100%" height="200px" frameBorder="0"></iframe>');
            popupWin.document.write('<html><body onload="window.print()"> ' + divToPrint.innerHTML + '</html>');
            document.getElementById('head_txt').style.display = "none";
            popupWin.document.close();
        },

        get_accounts() {
            // we using return first of the function for 'await' 
            return my_api.get('/backend/accounts/')
                .then((response) => (this.accounts = response.data))
                .catch(err => { alert(err) });
        },

        async save_account() {
            try {
                this.account.debit=0
                this.account.credit=0
                this.account.user=0

                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/accounts/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.account),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 2000, });
                    this.get_accounts();
                    await this.get_max_id();
                    await this.uploadImage();
                    this.closeModal();
                }
            } catch (error) { console.error(); }
        },

        async update_account(id) {
            try {
                if (this.check_form()) {
                    var response = await fetch(domain_url + "/backend/accounts/" + id + "/", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.account),
                    }
                    );
                    swal(this.$t("Updated!"), { buttons: false, icon: "success", timer: 2000, });
                    this.max_id = this.account.id
                    await this.uploadImage();
                    this.get_accounts();
                    this.closeModal();
                    this.edit_mode = false;
                }
            } catch (error) {
                console.error();
            }

        },

        async delete_account(id) {
            try {
                await swal({ title: this.$t("Are you sure to delete?"), text: "", icon: "warning", buttons: true, dangerMode: true, })
                    .then(async (willDelete) => {
                        if (willDelete) {
                            await my_api.delete('/backend/accounts/' + id + '/')
                            swal(this.$t("Deleted!"), { buttons: false, icon: "success", timer: 2000, });
                            await this.get_accounts(); this.closeModal();
                        }
                    });
            } catch (error) { console.error(); }
        },

        async get_account(id) {
            return axios({
                method: "get",
                url: domain_url + "/backend/accounts/?id=" + id,
                auth: { username: "admin", password: "123", },
            }).then((response) => (this.account = response.data[0]));
        },

        get_max_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_max_id/?table_name=Accounts",
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.max_id = response.data.data.id__max));
        },

        teest() {
            return axios({
                method: "post",
                url: domain_url + "/backend/new_account/?parent=100&name=test",
                //auth: { username: "admin", password: "123", },
            });
        },

        open_add_modal() {
            this.edit_mode = false;
            //$('#modal_label').html('Add Account');
            this.clear_form();
            $('#addModal').modal('toggle');
        },

        open_edit_modal() {
            this.edit_mode = true;
            //$('#modal_label').html('Edit Account');
            $('#addModal').modal('toggle');
        },

        closeModal() {
            $('#addModal').modal('hide');
            this.clear_form();
        },

        async row_click(index) {
            this.active_index = index; //to change row color
            await this.get_account(index);
        },

        clear_form() {
            this.account.name = '';
            this.account.parent = '';
            this.account.debit = '';
            this.account.credit = '';
            this.account.user = '';
            this.account.id = '';
            this.validate = false;
        },

        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (this.account.name && this.account.parent ) {
                return true
            } else {
                return false
            }
        },

    },
}

</script>
