import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { getJobs, createJob, updateJob, deleteJob } from '../api/jobs'
import Navbar from '../components/Navbar'

export default function JobTracker() {
  
  // States
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  // Form state
  const [form, setForm] = useState({
    company_name: '',
    job_role: '',
    status: 'Applied',
    job_link: '',
    application_date: '',
    notes: '',
    follow_up_date: ''
  })

  const { token } = useAuth()

  // fetching jobs on page
  useEffect(() => {
    fetchJobs()
  }, [])

  // Jobs fetccing
  const fetchJobs = async () => {
    try{ 
      const data = await getJobs(token)
      setJobs(data)
   } catch(err){
    console.error(err)
   }
  }

  // Job create karo
  const handleCreate = async (e) => {
    e.preventDefault()
    if (!form.company_name || !form.job_role){
      setError('Company name aur job role zaroori hai!')
        return
    }
    try{
      const data = await createJob(form, token)
    fetchJobs()
    setForm({
            company_name: '', job_role: '', status: 'Applied',
            job_link: '', application_date: '', notes: '', follow_up_date: ''
        })
    }catch(err) {
        setError(err.response?.data?.detail || 'Something went wrong!')
    }
  }

  // Status update karo
  const handleUpdate = async (jobId, newStatus) => {
    try {
        await updateJob(jobId, { status: newStatus }, token)
        fetchJobs()
    } catch(err) {
        console.error(err)
    }
  }

  // Job delete karo
  const handleDelete = async (jobId) => {
    try {
        await deleteJob(jobId, token)
        fetchJobs()
    } catch(err) {
        console.error(err)
    }
  }

  return (
  <div className="min-h-screen bg-slate-100">
    <Navbar />

    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">

      {/* Header */}
      <h2 className="text-2xl font-bold text-slate-700">📋 Job Tracker</h2>

      {/* Add Job Form */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-700 mb-4">➕ Add New Job</h3>

        {error && (
          <div className="bg-red-100 border border-red-300 text-red-600 text-sm rounded-lg px-4 py-3 mb-4">
            {error}
          </div>
        )}

      <form onSubmit={handleCreate} className="grid grid-cols-2 gap-4">

  {/* Company Name */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Company Name *
    </label>
    <input
      type="text"
      placeholder="e.g. Google"
      value={form.company_name}
      onChange={(e) => setForm({...form, company_name: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  {/* Job Role */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Job Role *
    </label>
    <input
      type="text"
      placeholder="e.g. Backend Developer"
      value={form.job_role}
      onChange={(e) => setForm({...form, job_role: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  {/* Status */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Status *
    </label>
    <select
      value={form.status}
      onChange={(e) => setForm({...form, status: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option>Saved</option>
      <option>Applied</option>
      <option>Interview Scheduled</option>
      <option>OA Round</option>
      <option>HR Round</option>
      <option>Rejected</option>
      <option>Offer Received</option>
    </select>
  </div>

  {/* Application Date */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Application Date
    </label>
    <input
      type="date"
      value={form.application_date}
      onChange={(e) => setForm({...form, application_date: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  {/* Job Link */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Job Link (optional)
    </label>
    <input
      type="url"
      placeholder="e.g. https://linkedin.com/jobs/..."
      value={form.job_link}
      onChange={(e) => setForm({...form, job_link: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  {/* Follow Up Date */}
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Follow Up Date (optional)
    </label>
    <input
      type="date"
      value={form.follow_up_date}
      onChange={(e) => setForm({...form, follow_up_date: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  {/* Notes */}
  <div className="col-span-2">
    <label className="block text-sm font-medium text-slate-700 mb-1">
      Notes (optional)
    </label>
    <textarea
      placeholder="e.g. HR messaged on LinkedIn...."
      value={form.notes}
      onChange={(e) => setForm({...form, notes: e.target.value})}
      className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      rows={3}
    />
  </div>

  <button
    type="submit"
    className="col-span-2 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition"
  >
    ➕ Add Job
  </button>

</form>
      </div>

      {/* Jobs List */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-700 mb-4">
          🗂️ My Applications ({jobs.length})
        </h3>

        {jobs.length === 0 ? (
          <p className="text-sm text-slate-400 text-center py-8">
            No Jobs Avialable — Add Now! 👆
          </p>
        ) : (
          <div className="space-y-3">
            {jobs.map((job) => (
              <div key={job._id} className="border border-slate-200 rounded-xl px-5 py-4 flex items-center justify-between">

                {/* Left Side */}
                <div>
                  <p className="font-semibold text-slate-700">{job.company_name}</p>
                  <p className="text-sm text-slate-500">{job.job_role}</p>
                  {job.notes && (
                    <p className="text-xs text-slate-400 mt-1">📝 {job.notes}</p>
                  )}
                  {job.follow_up_date && (
                    <p className="text-xs text-slate-400">🗓️ Follow up: {job.follow_up_date}</p>
                  )}
                </div>

                {/* Right Side */}
                <div className="flex items-center gap-3">

                  {/* Status Dropdown */}
                  <select
                    value={job.status}
                    onChange={(e) => handleUpdate(job._id, e.target.value)}
                    className="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none"
                  >
                    <option>Saved</option>
                    <option>Applied</option>
                    <option>Interview Scheduled</option>
                    <option>OA Round</option>
                    <option>HR Round</option>
                    <option>Rejected</option>
                    <option>Offer Received</option>
                  </select>

                  {/* Delete Button */}
                  <button
                    onClick={() => handleDelete(job._id)}
                    className="text-red-500 hover:text-red-700 text-sm font-medium transition"
                  >
                    🗑️ Delete
                  </button>

                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  </div>
)
}