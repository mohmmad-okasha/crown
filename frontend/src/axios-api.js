import axios from 'axios';
var currentURL = window.location.protocol + "//" + window.location.hostname + ":8000" + window.location.pathname;
const domain_url = currentURL;
 
//13.51.198.229
//127.0.0.1
const my_api = axios.create({
    baseURL: domain_url,
    timeout: 2500
});





export { my_api, domain_url }