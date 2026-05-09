import axios from 'axios'

const API = import.meta.env.VITE_API_URL

// Analyze Resume
export const analyzeResume = async (file, jobDescription, token) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('job_description', jobDescription)
    
    const response = await axios.post(`${API}/resume/analyze`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`  // token bheja
        }
    })
    return response.data
}

// Get History
export const getHistory = async (token) => {
    const response = await axios.get(
        `${API}/resume/history`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    return response.data
}