import axios from 'axios';

const domain_url = 'http://13.48.31.82:8000';

const my_api = axios.create({
    baseURL: domain_url,
    timeout: 1000
});



export { my_api, domain_url }