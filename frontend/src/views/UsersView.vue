<template>
  <div class="users">
    <h1>This is an users page</h1>
    {{ this.users }}
    <input v-model="test.a" type="text" />
    <input v-model="test.b" type="text" />
    <button @click="save_user()">save</button>
  </div>
</template>

<script>
/* eslint-disable */

import axios from "axios";
/* eslint-disable */
export default {
  name: "users",
  data() {
    return {
      users: [],
      test: {
        a: "",
        b: "",
      },
    };
  },
  async mounted() {
    this.get_users();
  },
  methods: {
    async save_user() {
      var response = await fetch(
        "http://127.0.0.1:8000/users/api/users_router/",
        {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.test),
        }
      );
      this.users.push(await response.json());
    },

    get_users() {
      // var response= await fetch("http://127.0.0.1:8000/users/api/users_router/");
      // this.users= await response.json();

      axios({
        method: "get",
        url: "http://127.0.0.1:8000/users/api/users_router/",
        auth: {
          username: "admin",
          password: "123",
        },
      }).then((response) => (this.users = response.data));
    },
  },
};
</script>
