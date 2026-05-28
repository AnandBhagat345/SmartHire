import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { analyzeResume, getHistory } from '../api/resume'
import { getJobs } from '../api/jobs'
import Navbar from '../components/Navbar'

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import ScoreCard from '../components/ScoreCard'
import SkillTags from '../components/SkillTags'
import { rewriteResume,  generateInterviewQuestions } from '../api/resume'

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

  const [rewriting, setRewriting] = useState(false)
  const [rewrittenText, setRewrittenText] = useState(null)
  const [resumeText, setResumeText] = useState('')

  const [questions, setQuestions] = useState(null)
const [loadingQuestions, setLoadingQuestions] = useState(false)

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

  const handleRewrite = async () => {
    if (!result) return
    setRewriting(true)
    try {
        const data = await rewriteResume(
            result.resume_text,  
            jobDescription,
            token
        )
        setRewrittenText(data.rewritten_text)
    } catch (err) {
        setError(err.response?.data?.detail || 'Something went wrong!')
    } finally {
        setRewriting(false)
    }
}



const handleInterviewPrep = async () => {
    if (!result) return
    setLoadingQuestions(true)
    try {
        const data = await generateInterviewQuestions(
            result.resume_text,
            jobDescription,
            token
        )
        setQuestions(data)
    } catch (err) {
        setError(err.response?.data?.detail || 'Something went wrong!')
    } finally {
        setLoadingQuestions(false)
    }
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

      {result && (
  <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200 space-y-6">
    
    <h3 className="text-lg font-semibold text-slate-700">
      📊 Analysis Result
    </h3>

    {/* Score Card */}
    <ScoreCard score={result.ats_score} />

    {/* Missing Keywords */}
    <SkillTags keywords={result.missing_keywords} />

    {/* ATS Feedback */}
    <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
      <p className="text-sm font-semibold text-slate-700 mb-2">
        🤖 ATS Feedback
      </p>
      <p className="text-sm text-slate-600">{result.ats_feedback}</p>
    </div>

    {/* Recruiter Feedback */}
    <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
      <p className="text-sm font-semibold text-slate-700 mb-2">
        👔 Recruiter Feedback
      </p>
      <p className="text-sm text-slate-600">{result.recruiter_feedback}</p>
    </div>

    {/* Suggestions */}
    <div>
      <p className="text-sm font-semibold text-slate-700 mb-3">
        💡 Suggestions
      </p>
      <ul className="space-y-2">
        {result.suggestions.map((s, i) => (
          <li key={i} className="flex gap-2 text-sm text-slate-600 bg-blue-50 px-4 py-2 rounded-lg border border-blue-100">
            <span>✅</span> {s}
          </li>
        ))}
      </ul>
    </div>

    {/* Rewrite Button */}
    <button
      onClick={handleRewrite}
      disabled={rewriting}
      className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:opacity-90 text-white py-3 rounded-lg font-medium transition disabled:opacity-50"
    >
      {rewriting ? 'Polishing Resume... ✨⏳' : '✨ Polish My Resume'}
    </button>

    <button
        onClick={handleInterviewPrep}
        disabled={loadingQuestions}
        className="w-full bg-gradient-to-r from-violet-600 to-purple-600 hover:opacity-90 text-white py-3 rounded-lg font-medium transition disabled:opacity-50"
    >
        {loadingQuestions ? 'Generating Questions... 🎤⏳' : '🎤 Generate Interview Questions'}
    </button>

    {/* Interview Questions */}
{questions && (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200 space-y-6">
        
        <h3 className="text-lg font-semibold text-slate-700">
            🎯 Interview Preparation
        </h3>

        {/* Technical */}
        <div>
            <h4 className="text-sm font-bold text-blue-600 mb-3 flex items-center gap-2">
                💻 Technical Questions ({questions.technical.length})
            </h4>
            <ul className="space-y-2">
                {questions.technical.map((q, i) => (
                    <li key={i} className="bg-blue-50 border border-blue-100 rounded-lg px-4 py-3 text-sm text-slate-700">
                        <span className="font-bold text-blue-500">Q{i+1}.</span> {q}
                    </li>
                ))}
            </ul>
        </div>

        {/* HR */}
        <div>
            <h4 className="text-sm font-bold text-green-600 mb-3 flex items-center gap-2">
                👔 HR Questions ({questions.hr.length})
            </h4>
            <ul className="space-y-2">
                {questions.hr.map((q, i) => (
                    <li key={i} className="bg-green-50 border border-green-100 rounded-lg px-4 py-3 text-sm text-slate-700">
                        <span className="font-bold text-green-500">Q{i+1}.</span> {q}
                    </li>
                ))}
            </ul>
        </div>

        {/* Resume Based */}
        <div>
            <h4 className="text-sm font-bold text-purple-600 mb-3 flex items-center gap-2">
                📄 Resume-Based Questions ({questions.resume_based.length})
            </h4>
            <ul className="space-y-2">
                {questions.resume_based.map((q, i) => (
                    <li key={i} className="bg-purple-50 border border-purple-100 rounded-lg px-4 py-3 text-sm text-slate-700">
                        <span className="font-bold text-purple-500">Q{i+1}.</span> {q}
                    </li>
                ))}
            </ul>
        </div>

        {/* Copy All Button */}
        <button
            onClick={() => {
                const all = [
                    '💻 TECHNICAL QUESTIONS',
                    ...questions.technical.map((q,i) => `Q${i+1}. ${q}`),
                    '\n👔 HR QUESTIONS',
                    ...questions.hr.map((q,i) => `Q${i+1}. ${q}`),
                    '\n📄 RESUME-BASED QUESTIONS',
                    ...questions.resume_based.map((q,i) => `Q${i+1}. ${q}`)
                ].join('\n')
                navigator.clipboard.writeText(all)
            }}
            className="w-full bg-slate-700 hover:bg-slate-800 text-white py-2 rounded-lg text-sm transition"
        >
            📋 Copy All Questions
        </button>

    </div>
)}

    {/* Side by Side */}
    {rewrittenText && (
      <div className="grid grid-cols-2 gap-4">

        {/* Original */}
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-sm font-semibold text-red-600 mb-3">
            📄 Original Resume
          </p>
          <pre className="text-xs text-slate-600 whitespace-pre-wrap font-sans">
            {result.resume_text}
          </pre>
        </div>

        {/* Improved */}
        <div className="bg-green-50 border border-green-200 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-green-600">
              ✨ Polished Resume
            </p>
            {/* Copy Button */}
            <button
              onClick={() => navigator.clipboard.writeText(rewrittenText)}
              className="text-xs bg-green-600 text-white px-3 py-1 rounded-lg hover:bg-green-700 transition"
            >
              📋 Copy
            </button>
          </div>
          <pre className="text-xs text-slate-600 whitespace-pre-wrap font-sans">
            {rewrittenText}
          </pre>
        </div>

      </div>
    )}

  </div>
)}

      {history.length > 0 && (
  <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
    
    <h3 className="text-lg font-semibold text-slate-700 mb-6">
      📈 ATS Score History
    </h3>

    {/* Bar Chart */}
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={history.map((item, i) => ({
        name: `V${i + 1}`,
        score: item.ats_score
      }))}>
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Bar dataKey="score" radius={[6, 6, 0, 0]}>
          {history.map((item, i) => (
            <Cell
              key={i}
              fill={
                item.ats_score >= 71 ? '#22c55e' :
                item.ats_score >= 41 ? '#eab308' : '#ef4444'
              }
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>

    {/* History List */}
    <div className="space-y-3 mt-4">
      {history.map((item, i) => (
        <div key={i} className="flex items-center justify-between border border-slate-100 rounded-lg px-3 py-2">
          <div>
            <p className="text-xs font-medium text-slate-700">
              {item.job_description?.slice(0, 50)}...
            </p>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {new Date(item.created_at).toLocaleDateString()}
            </p>
          </div>
          <ScoreCard score={item.ats_score} small />
        </div>
      ))}
    </div>

  </div>
)}

    </div>
  </div>
)
}