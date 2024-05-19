<template>
    <div class="">

        <form>
            <div class="form-group">
                <label for="book_date">{{ $t("Booking Date") }}</label>
                <input id="book_date" v-model="this_row.book_date" type="datetime-local"
                    :class="{ 'is-invalid': !this.this_row.book_date && this.validate, 'is-valid': this.this_row.book_date && this.validate }"
                    class="form-control">
                <div v-if="!this.this_row.book_date && this.validate" class="invalid-feedback hidden">
                    {{ $t("Please Select The Date") }}
                </div>
            </div>

            <div class="row g-3 form-group">


                <div class="form-group col-sm-7">
                    <label for="hotel">{{ $t("Hotel") }}</label>
                    <v-select id="hotel" v-model="this_row.hotel" :options="hotels" 
                        :class="{ 'is-invalid': !this_row.hotel && validate, 'is-valid': this_row.hotel && validate }" />

                    <div v-if="!this_row.hotel && validate" class="invalid-feedback hidden">
                        {{ $t("Please Select hotel") }}
                    </div>
                </div>

                <div class="form-group col-sm-3">
                    <label for="room_id">{{ $t("Room ID") }}</label>
                    <select id="room_id" v-model="this_row.room_id" type="text" class="form-control"
                        :class="{ 'is-invalid': !this.this_row.room_id && this.validate, 'is-valid': this.this_row.room_id && this.validate }">
                        <option v-for="room in rooms" v-bind:value="room" :key="room">{{
                            room }}</option>
                    </select>
                    <div v-if="!this.this_row.room_id && this.validate" class="invalid-feedback hidden">
                        {{ $t("Please Select room_id") }}
                    </div>
                </div>

                <div class="form-group col-sm-2">
                    <label for="room_type">{{ $t("Type") }}</label>
                    <input readonly id="room_type" v-model="this_row.room_type" type="text" class="form-control">
                </div>
            </div>


            <label v-show="this.this_row.room_id" for="dates">{{ $t("Select Date") }}</label>
            <div v-show="this.this_row.room_id" class="form-group card" id="dates" style="width: 100%;">
                <div class="card-body">
                    <date-picker v-model="this_row.dates" :min="min_date" :max="max_date" :disable="disable_dates"
                        :range="is_range" clearable locale="en" inline :auto-submit="false" custom-input="none"
                        color="#098290" input-format="DD/MM/YYYY" format="DD/MM/YYYY" />
                </div>

                <input readonly id="dates" v-model="this_row.dates" type="text"
                    :class="{ 'is-invalid': !this.this_row.dates && this.validate, 'is-valid': this.this_row.dates && this.validate }"
                    class="form-control">
                <div v-if="!this.this_row.dates && this.validate" class="invalid-feedback hidden">
                    {{ $t("Please Select The Date") }}
                </div>
            </div>

            <div class="card form-group">
                <div class="card-header">
                    {{ $t("Guests") }}
                </div>
                <div class="card-body">

                    <div class="row g-3 form-group">
                        <div class="col">
                            <label for="Adults"> {{ $t("Adults") }}</label>
                            <input id="Adults" v-model="this_row.persons_number" min="1" max="15"
                                :class="{ 'is-invalid': !this.this_row.persons_number && this.validate, 'is-valid': this.this_row.persons_number && this.validate }"
                                type="number" class="form-control">
                            <div v-if="!this.this_row.persons_number && this.validate" class="invalid-feedback hidden">
                                {{ $t("Please Enter The Number of Persons") }}
                            </div>
                        </div>
                        <div class="col">
                            <label for="Children"> {{ $t("Children") }}</label>
                            <input id="Children" v-model="this_row.kids_number" min="0" max="10"
                                :class="{ 'is-invalid': this.this_row.kids_number < 0 && this.validate, 'is-valid': this.this_row.kids_number && this.validate }"
                                type="number" class="form-control">
                            <div v-if="this.this_row.kids_number < 0 && this.validate" class="invalid-feedback hidden">
                                {{ $t("Please Enter The Number of Kids") }}
                            </div>
                        </div>
                    </div>

                    <div v-if="this_row.persons_number > 0">
                        <div v-for=" i in parseInt(this_row.persons_number)" :key="i" class="form-group">
                            <label>{{ $t("Adult Name ") + i }}</label>
                            <input v-model="this_row.persons_names[i - 1]" type="text" class="form-control"
                                :class="{ 'is-invalid': !this_row.persons_names[i - 1] && validate, 'is-valid': this_row.persons_names[i - 1] && validate }">
                            <div v-if="!this_row.persons_names[i - 1] && validate" class="invalid-feedback hidden">
                                {{ $t("Please Enter The Name of Person") + i }}
                            </div>
                        </div>
                    </div>

                    <div v-if="this_row.kids_number > 0">
                        <div v-for=" i in parseInt(this_row.kids_number)" :key="i" class="form-group">
                            <div class="row">
                                <div class="col">
                                    <label>{{ $t("Children Name ") + i }}</label>
                                    <input v-model="this_row.kids_names[i - 1]" type="text" class="form-control"
                                        :class="{ 'is-invalid': !this_row.kids_names[i - 1] && validate, 'is-valid': this_row.kids_names[i - 1] && validate }">
                                    <div v-if="!this_row.kids_names[i - 1] && validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter Children Name") + i }}
                                    </div>
                                </div>
                                <div class="col">
                                    <label>{{ $t("Children Age ") + i }}</label>
                                    <input v-model="this_row.kids_ages[i - 1]" type="number" class="form-control"
                                        :class="{ 'is-invalid': !this_row.kids_ages[i - 1] && validate, 'is-valid': this_row.kids_ages[i - 1] && validate }">
                                    <div v-if="!this_row.kids_ages[i - 1] && validate" class="invalid-feedback hidden">
                                        {{ $t("Please Enter Children Age") + i }}
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <div class="form-group">
                <label for="status">{{ $t("Status") }}</label>
                <select id="status" v-model="this_row.status" type="text" class="form-control"
                    :class="{ 'is-invalid': !this.this_row.status && this.validate, 'is-valid': this.this_row.status && this.validate }">
                    <option selected :value="$t('Booked')">{{ $t("Booked") }} </option>
                    <option :value="$t('No Show')">{{ $t("No Show") }} </option>

                </select>
                <div v-if="!this.this_row.status && this.validate" class="invalid-feedback hidden">
                    {{ $t("Please Select the status") }}
                </div>
            </div>

            <div class="form-group ">
                <label for="cutomer_notes"> {{ $t("Notes") }}</label>
                <textarea class="form-control" v-model="this_row.notes" id="cutomer_notes" rows="1"></textarea>
            </div>
            <div class="form-check">
                <input v-model="print" class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
                <label class="form-check-label" for="flexCheckChecked">
                    Print
                </label>
            </div>
        </form>


        <div class="modal-footer">

            <button type="button" id="closeModal" title="close" class="btn btn-secondary on-hover-sm"
                @click="this.closeModal">
                <i class="fa fa-xmark"></i>
            </button>

            <button type="button" title="save" @click="save_booking()"
                class="btn btn-primary on-hover-sm">
                <i class="fa fa-floppy-disk"></i></button>

        </div>

    </div>
</template>

<script>
/* eslint-disable */
import vSelect from 'vue-select';
import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
import axios from 'axios';
import { my_api,domain_url } from "../axios-api";

export default {
    name: 'NewBooking',
    components: {
        datePicker: VuePersianDatetimePicker,
        vSelect,
    },
    data() {
        return {
            edit_mode: false,
            is_range: true,
            print: false, //to print after save
            validate: false, //for check forms
            rooms: [],//used in new & update form
            hotels: [],//used in new & update form
            min_date: '',
            max_date: '',
            disable_dates: [],
            this_row: {
                book_date: new Date().toISOString().slice(0, 16),
                hotel: "",
                room_id: "",
                room_type: "",
                dates: "",
                out_date: "",
                all_dates: "",
                guests: "",
                status: "",
                notes: "",
                persons_number: 1,
                persons_names: [],
                kids_number: '',
                kids_names: [],
                kids_ages: [],
                user: "",
            },
        }
    },
    async mounted() {
        await this.get_hotels();
    },
    watch: {
        'this_row.hotel': async function (newValue) {
                this.this_row.room_id = '';
                await this.get_rooms();
                this.this_row.room_id = this.rooms[0];
        },
        'this_row.room_id': function (newValue) {
            
                this.get_room_info(newValue);
                this.get_booked_dates();
            
        },
        range: async function (newValue) {
            const dateValues = newValue.split(",");
            this.min_date = dateValues[0];
            this.max_date = dateValues[1];
            this.this_row.out_date = this.this_row.dates[1];
            this.get_booked_dates()
        }
    },

    methods: {
        async save_booking() {
            this.isLoading = true;
            try {
                if (this.check_form()) {
                    if (this.print) {
                        this.PrintDiv('booking_data');
                    }
                    // save out date
                    if (this.this_row.dates.length > 1) {
                        this.this_row.out_date = this.this_row.dates[1];
                    } else {
                        this.this_row.dates.push(this.this_row.dates[0]);
                    }
                    this.this_row.dates = this.this_row.dates.toString();
                    if (!this.this_row.kids_number) { this.this_row.kids_number = 0; }
                    this.this_row.persons_names = this.this_row.persons_names.join(',');
                    this.this_row.kids_names = this.this_row.kids_names.join(',');
                    this.this_row.kids_ages = this.this_row.kids_ages.join(',');
                    var response = await fetch(domain_url + "/backend/bookings/", {
                        method: "post",
                        headers: { "Content-Type": "application/json", },
                        body: JSON.stringify(this.this_row),
                    });

                    swal(this.$t("Added!"), { buttons: false, icon: "success", timer: 1500, });

                    await this.get_max_id();

                    //save log
                    axios.post(domain_url + '/backend/logs/', { user_name: this.$parent.user_name, log: 'add booking :' + this.max_id, time: new Date() })


                    window.location.reload();

                    this.get_booking_rows();
                    
                    this.closeModal();
                }
            } catch (error) { console.error(); }
            this.isLoading = false;
        },
        check_form() {
            this.validate = true; //to change inputs color 'red/green'

            if (
                this.this_row.book_date &&
                this.this_row.persons_number &&
                this.this_row.persons_names &&
                //this.this_row.kids_number >0 &&
                this.this_row.hotel &&
                this.this_row.dates &&
                this.this_row.room_id &&
                this.this_row.room_type &&
                this.this_row.status
            ) {
                return true
            } else {
                return false
            }
        },
        get_hotels() {
            return my_api.get('/backend/get_hotels/')
                .then((response) => (this.hotels = response.data))
                .catch(err => { alert(err) });
        },
        closeModal() {
            this.add_mode = false; this.edit_mode = false;
            $('#addModal').modal('hide');
            this.clear_form();
        },
        clear_form() {
            this.this_row.persons_names = [];
            this.this_row.kids_names = [];
            this.this_row.persons_number = 1;
            this.this_row.kids_number = '';
            this.this_row.hotel = '';
            this.this_row.dates = '';
            this.this_row.room_id = '';
            this.this_row.room_type = '';
            this.this_row.status = '';
            this.this_row.notes = '';
            this.enable_dates = [];
            this.disable_dates = [];
            this.validate = false;
        },
        get_rooms() {
            if (this.this_row.hotel)
                return axios({
                    method: "get",
                    url: domain_url + "/backend/get_rooms/", params: { hotel: this.this_row.hotel },
                    //auth: { username: "admin", password: "123", },
                }).then((response) => (this.rooms = response.data));
        },
        get_room_info(value) {
            if(value && this.this_row.hotel)
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

                    currentDate.setDate(currentDate.getDate() + 1);//to skip in_date from booking dates list

                    while (currentDate < endDate) {
                        this.all_booked_dates.push(currentDate.toLocaleDateString("en-GB"));
                        currentDate.setDate(currentDate.getDate() + 1);
                    }
                });
                //copy all dates from all_booked_dates to disable_dates
                this.all_booked_dates.forEach(element => this.disable_dates.push(element));
            }
        },
    }
}
</script>