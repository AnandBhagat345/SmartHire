import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../api/auth'
import { Link } from 'react-router-dom'


export default function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      // API calling
      const data = await register(name,email, password)
      
      // Dashboard 
      navigate('/')
      
    } catch (err) {
      
setError(err.response?.data?.detail || "Something went wrong!")
    } finally {
      setLoading(false)
    }
  }

 return (
  <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4">
    
    <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-slate-200">

      {/* Heading */}
        <div className="text-center mb-8 overflow-hidden">

        {/* Main Brand */}
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 via-cyan-500 to-indigo-600 bg-clip-text text-transparent tracking-wide">
            SmartHire 🚀
        </h1>

        {/* Animated Line */}
        <div className="relative mt-3 h-6 overflow-hidden">

            <p className="absolute whitespace-nowrap text-sm font-medium text-slate-500 animate-marquee">
            AI Resume Analyzer • ATS Score • Recruiter Insights • Job Tracker • Smart Career Tools
            </p>

        </div>

        </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-300 text-red-600 text-sm rounded-lg px-4 py-3 mb-4">
          {error}
        </div>
      )}

      {/* Login Form */}
      <form onSubmit={handleSubmit} className="space-y-5">

        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Name
          </label>
        
        
          <input
            type="text"
            placeholder="Enter your Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Email */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Email
          </label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Password */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 transition-colors duration-200 text-white py-3 rounded-lg font-medium disabled:opacity-50"
        >
          {loading ? 'Registering in...' : 'Register'}
        </button>

      </form>

      {/* Footer */}
      <p className="text-center text-sm text-slate-500 mt-6">
        Already have an account?{" "}
        <Link
          to="/"
          className="text-blue-600 hover:text-blue-700 font-medium"
        >
          Login
        </Link>
      </p>

    </div>
  </div>
)
}