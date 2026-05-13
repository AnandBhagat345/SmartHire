import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { analyzeResume, getHistory } from '../api/resume'
import { getJobs } from '../api/jobs'
import Navbar from '../components/Navbar'

export default function Dashboard() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [jobs, setJobs] = useState([])
  const [error, setError] = useState('')

  const { token, logout } = useAuth()
  const navigate = useNavigate()

  // Page load pe data fetch karo
  useEffect(() => {
    fetchHistory()
    fetchJobs()
  }, [])

  const fetchHistory = async () => {
    try {
      const data = await getHistory(token)
      setHistory(data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchJobs = async () => {
    try {
      const data = await getJobs(token)
      setJobs(data)
    } catch (err) {
      console.error(err)
    }
  }

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!file) return setError('Upload the PDF!')
    
    setLoading(true)
    setError('')
    
    try {
      const data = await analyzeResume(file, jobDescription, token)
      setResult(data)
      fetchHistory() // Refresh history 
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong!')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
  <div className="min-h-screen bg-slate-100">
    
    {/* Navbar */}
    <Navbar />

    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">

      {/* Welcome */}
      <h2 className="text-2xl font-bold text-slate-700">
        Welcome back! 👋
      </h2>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-4">
        
        <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-200 text-center">
          <p className="text-sm text-slate-500">Total Analyses</p>
          <p className="text-3xl font-bold text-blue-600 mt-1">{history.length}</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-200 text-center">
          <p className="text-sm text-slate-500">Jobs Tracked</p>
          <p className="text-3xl font-bold text-indigo-600 mt-1">{jobs.length}</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-200 text-center">
          <p className="text-sm text-slate-500">Latest ATS Score</p>
          <p className="text-3xl font-bold text-cyan-600 mt-1">
            {history.length > 0 ? `${history[0].ats_score}%` : 'N/A'}
          </p>
        </div>

      </div>

      {/* Analyze Section */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
        
        <h3 className="text-lg font-semibold text-slate-700 mb-4">
          📄 Analyze New Resume
        </h3>

        {error && (
          <div className="bg-red-100 border border-red-300 text-red-600 text-sm rounded-lg px-4 py-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleAnalyze} className="space-y-4">

          {/* PDF Upload */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Upload Resume (PDF)
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm"
            />
          </div>

          {/* Job Description */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Job Description
            </label>
            <textarea
              placeholder="Paste job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={5}
              className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition disabled:opacity-50"
          >
            {loading ? 'Analyzing... ⏳' : '🔍 Analyze Resume'}
          </button>

        </form>
      </div>

      {/* Result Section */}
      {result && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200 space-y-4">
          
          <h3 className="text-lg font-semibold text-slate-700">
            📊 Analysis Result
          </h3>

          {/* ATS Score */}
          <div className="text-center">
            <p className="text-sm text-slate-500">ATS Score</p>
            <p className="text-5xl font-extrabold text-blue-600 mt-1">
              {result.ats_score}%
            </p>
          </div>

          {/* Missing Keywords */}
          <div>
            <p className="text-sm font-semibold text-slate-700 mb-2">Missing Keywords:</p>
            <div className="flex flex-wrap gap-2">
              {result.missing_keywords.map((kw, i) => (
                <span key={i} className="bg-red-100 text-red-600 text-xs px-3 py-1 rounded-full">
                  {kw}
                </span>
              ))}
            </div>
          </div>

          {/* ATS Feedback */}
          <div>
            <p className="text-sm font-semibold text-slate-700 mb-1">ATS Feedback:</p>
            <p className="text-sm text-slate-600">{result.ats_feedback}</p>
          </div>

          {/* Recruiter Feedback */}
          <div>
            <p className="text-sm font-semibold text-slate-700 mb-1">Recruiter Feedback:</p>
            <p className="text-sm text-slate-600">{result.recruiter_feedback}</p>
          </div>

          {/* Suggestions */}
          <div>
            <p className="text-sm font-semibold text-slate-700 mb-2">Suggestions:</p>
            <ul className="space-y-1">
              {result.suggestions.map((s, i) => (
                <li key={i} className="text-sm text-slate-600 flex gap-2">
                  <span>✅</span> {s}
                </li>
              ))}
            </ul>
          </div>

        </div>
      )}

      {/* History Section */}
      {history.length > 0 && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          
          <h3 className="text-lg font-semibold text-slate-700 mb-4">
            📋 Recent Analyses
          </h3>

          <div className="space-y-3">
            {history.map((item, i) => (
              <div key={i} className="flex items-center justify-between border border-slate-100 rounded-lg px-4 py-3">
                <div>
                  <p className="text-sm font-medium text-slate-700">
                    {item.job_description?.slice(0, 50)}...
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    {new Date(item.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className="text-2xl font-bold text-blue-600">
                  {item.ats_score}%
                </span>
              </div>
            ))}
          </div>

        </div>
      )}

    </div>
  </div>
)
}