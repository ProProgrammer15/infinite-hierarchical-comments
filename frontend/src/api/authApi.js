import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/users';

export const signup = async (payload) => {
    const response = await axios.post(`${API_BASE_URL}/signup`, payload);
    return response.data;
};

export const login = async (payload) => {
    const response = await axios.post(`${API_BASE_URL}/login`, payload);
    return response.data;
};
