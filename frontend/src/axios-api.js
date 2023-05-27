import axios from 'axios';

const domain_url = 'http://13.50.110.227:8000';
//13.50.110.227
const my_api = axios.create({
    baseURL: domain_url,
    timeout: 1000
});



export { my_api, domain_url }