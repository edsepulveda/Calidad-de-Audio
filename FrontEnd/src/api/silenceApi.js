import axios from 'axios'


const silenceApi = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    headers: { 'Content-Type': 'application/json' } 
})


export default silenceApi