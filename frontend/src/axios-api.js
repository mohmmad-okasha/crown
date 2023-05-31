import axios from 'axios';

const domain_url = 'http://13.51.198.229:8000';

//127.0.0.1
const my_api = axios.create({
    baseURL: domain_url,
    timeout: 1000
});



export { my_api, domain_url }