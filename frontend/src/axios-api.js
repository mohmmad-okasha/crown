import axios from 'axios';

const domain_url = 'https://7840-16-16-199-164.ngrok-free.app';

const my_api = axios.create({
    baseURL: domain_url,
    timeout: 1000
});



export { my_api, domain_url }