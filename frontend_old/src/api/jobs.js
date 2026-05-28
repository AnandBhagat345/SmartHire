import axios from 'axios'

const API = import.meta.env.VITE_API_URL

// Create Job
export const createJob = async (data, token) => {

    const response = await axios.post(
        `${API}/jobs`,
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    return response.data
}


// Get All Jobs
export const getJobs = async (token) => {

    const response = await axios.get(
        `${API}/jobs`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    return response.data
}


// Update Job
export const updateJob = async (jobId, data, token) => {

    const response = await axios.put(
        `${API}/jobs/${jobId}`,
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    return response.data
}


// Delete Job
export const deleteJob = async (jobId, token) => {

    const response = await axios.delete(
        `${API}/jobs/${jobId}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    return response.data
}