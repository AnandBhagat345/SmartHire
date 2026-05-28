import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { Link } from 'react-router-dom'

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
      
      {/* Logo */}
      <h1 className="text-xl font-extrabold bg-gradient-to-r from-blue-600 via-cyan-500 to-indigo-600 bg-clip-text text-transparent">
        SmartHire 🚀
      </h1>

      {/* Links */}
      <div className="flex items-center gap-6 text-sm font-medium text-slate-600">
        <Link to="/dashboard" className="hover:text-blue-600 transition">Dashboard</Link>
        <Link to="/tracker" className="hover:text-blue-600 transition">Job Tracker</Link>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
        >
          Logout
        </button>
      </div>

    </nav>
  )
}