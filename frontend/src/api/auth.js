import axios from 'axios'

const API = import.meta.env.VITE_API_URL

// Register
export const register = async (name, email, password) => {
    const response = await axios.post(`${API}/auth/register`, {
    name: name,
    email: email,
    password: password
})
return response.data
}

// Login
export const login = async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const response = await axios.post(`${API}/auth/login`, formData)
    return response.data
}