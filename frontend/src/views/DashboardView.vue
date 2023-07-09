<template>
    <div class="row" id="page-top">

        <!-- loading  -->
        <loading :active.sync="isLoading" :can-cancel="true" :on-cancel="onCancel" :is-full-page="fullPage"></loading>

        <div v-for="button in buttons" :key="button.id" v-show="button.show && user_roles[button.url]"
            class="col-xl-3 col-md-6 mb-4 on-hover-sm" role="button">
            <div :class="button.color" class="card shadow h-100 py-2">
                <router-link tag="div" class="card-body" :to="'/' + button.url">

                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class=" font-weight-bold text-primary text-uppercase mb-1">
                                {{ $t(button.title) }}</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"></div>
                        </div>
                        <div class="col-auto">
                            <i :class="button.icon" class="fa-2x text-gray-300"></i>
                        </div>
                    </div>

                </router-link>
            </div>
        </div>
        <!-- to get search value from navbar -->
        <input :value="this.$parent.$refs.NavBar.search" v-bind:on-change="search" hidden>
        
        <!-- <div>
            <div v-for="message in messages" :key="message.timestamp">
                <strong>{{ message.sender }}</strong>: {{ message.message }}
            </div>
            <input v-model="newMessage" placeholder="Type your message">
            <button @click="sendMessage">Send</button>
        </div> -->

    </div>
</template>

<script>
/* eslint-disable */

import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import NavBar from '../components/parts/NavBar.vue'

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {

    name: "dashboard",

    components: {
        NavBar,
        Loading,
    },

    data() {
        return {
            isLoading: false,
            fullPage: true,

            buttons: [],
            user_roles: '',

            messages: [],
            newMessage: ''
        }
    },
    computed: {

        search() {
            let data = this.$parent.$refs.NavBar.search
            if (data && data.trim()) { // data.trim() to check data not spaces only
                return axios({
                    method: "get",
                    url: domain_url + "/backend/dashboard_buttons/?search=" + data,
                }).then((response) => (this.buttons = response.data));
            } else {
                this.get_dashboard_buttons();
            }
        },
    },
    async mounted() {
        this.isLoading = true;


        //this.fetchMessages();


        //my_api.get('backend/create_backup/');
        await this.get_dashboard_buttons();
        await this.get_user_name_id();
        await this.get_roles();
        this.isLoading = false;
    },

    methods: {

        get_dashboard_buttons() {
            return my_api.get('/backend/dashboard_buttons/')
                .then((response) => (this.buttons = response.data))
                .catch(err => { alert(err) });
        },
        get_user_name_id() {
            return axios({
                method: "get",
                url: domain_url + "/backend/get_user_name_id/?username=" + this.$parent.user_name,
                //auth: { username: "admin", password: "123", },
            }).then((response) => (this.user_name_id = response.data.data));
        },
        async get_roles() {
            return my_api.get('backend/get_roles/?user_id=' + this.user_name_id, { auth: { username: "admin", password: "123", } })
                .then((response) => (this.user_roles = response.data))
                .catch(err => { alert(err) });
        },

        fetchMessages() {
            const receiverId = 1; // Set the receiver ID dynamically
            axios.get(`/backend/get-messages/?receiver_id=${receiverId}`)
                .then(response => {
                    this.messages = response.data.messages;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        sendMessage() {
            const receiverId = 1; // Set the receiver ID dynamically
            axios.post('/backend/send-message/', {
                receiver_id: receiverId,
                message: this.newMessage
            })
                .then(response => {
                    if (response.data.status === 'success') {
                        this.newMessage = '';
                        this.fetchMessages();
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }

    },
}

</script>
