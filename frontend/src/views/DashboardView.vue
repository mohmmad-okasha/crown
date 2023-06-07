<template>
    <div class="row" id="page-top">
        <div v-for="button in buttons" :key="button.id" v-show="button.show && user_roles[button.url]" class="col-xl-3 col-md-6 mb-4 on-hover-sm"
            role="button">
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

    </div>
</template>

<script>
/* eslint-disable */

import axios from 'axios';
import { my_api, domain_url } from "../axios-api";
import NavBar from '../components/parts/NavBar.vue'

export default {

    name: "dashboard",

    components: {
        NavBar,
    },

    data() {
        return {
            buttons: [],
            user_roles: ''

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
        await this.get_dashboard_buttons();
        await new Promise(resolve => setTimeout(resolve, 500)); // wait
        this.get_roles();
    },

    methods: {
        get_dashboard_buttons() {
            return my_api.get('/backend/dashboard_buttons/')
                .then((response) => (this.buttons = response.data))
                .catch(err => { alert(err) });
        },
        get_roles() {
            this.user_roles = this.$parent.user_roles;
        }

    },
}

</script>
