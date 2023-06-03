var BASE_URL = '';

if (process.env.NODE_ENV=='development'){
    BASE_URL = 'www.testurl.com/';
}

export const API_URL = BASE_URL;