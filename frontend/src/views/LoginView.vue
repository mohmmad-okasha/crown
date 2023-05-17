<template>
    <div >
      <!-- <section class="vh-100" style="background-color: var(--primary);">
        <div class="container py-5 h-100">
          <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-12 col-md-8 col-lg-6 col-xl-5">
              <div class="card shadow-2-strong" style="border-radius: 1rem;">
                <div class="card-body p-5 text-center">

                  <h3 class="mb-5">Sign in</h3>
                  <form @submit.prevent="loginUser">
                    <div class="form-outline mb-4">
                      <label class="form-label" for="typeEmailX-2">User Name</label>
                      <input type="text" v-model="username" required class="form-control form-control-lg" />
                    </div>

                    <div class="form-outline mb-4">
                      <label class="form-label" for="typePasswordX-2">Password</label>
                      <input type="password" v-model="password" required class="form-control form-control-lg" />
                    </div>

                    <button class="btn btn-primary btn-lg btn-block" type="submit">Login</button>
                  </form>

                </div>
              </div>
            </div>
          </div>
        </div>
      </section> -->
    </div>
</template>

<!-- <script>
import axios from 'axios'
import { domain_url } from "../axios-api";

export default {
  data() {
    return {
      username: '',
      password: '',
      token:'',
    }
  },
  methods: {
    async loginUser() {
      const data = { username: this.username, password: this.password }

      try {

        const response = await axios.post(domain_url + '/backend/login/', data)
        this.token = response.data.access
        localStorage.setItem('access_token', this.token)
        
        // redirect to dashboard or homepage after successful login
        this.$router.push('dashboard') 

      } catch (error) {
        console.log(error)
      }
    },

  },
}
</script> -->
