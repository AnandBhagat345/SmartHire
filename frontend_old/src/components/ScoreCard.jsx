export default function ScoreCard({ score, small }) {
  
  const getColor = () => {
    if (score >= 71) return 'text-green-500'
    if (score >= 41) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getBgColor = () => {
    if (score >= 71) return 'bg-green-50 border-green-200'
    if (score >= 41) return 'bg-yellow-50 border-yellow-200'
    return 'bg-red-50 border-red-200'
  }

  const getLabel = () => {
    if (score >= 71) return 'Strong Match ✅'
    if (score >= 41) return 'Moderate Match ⚠️'
    return 'Weak Match ❌'
  }

  // -- Small Card --
  if (small) {
    return (
      <div className={`rounded-xl border p-3 text-center w-[110px] ${getBgColor()}`}>
        <div className={`text-2xl font-extrabold ${getColor()}`}>
          {score}%
        </div>
        <p className="text-xs text-slate-400 mt-1">ATS</p>
        <p className={`text-xs font-semibold mt-1 ${getColor()}`}>
          {getLabel()}
        </p>
      </div>
    )
  }

  // -- Big Card for result section --
  return (
    <div className={`rounded-xl border p-6 text-center ${getBgColor()}`}>
      <p className="text-sm font-medium text-slate-500 mb-2">ATS Score</p>
      
      <div className={`text-7xl font-extrabold ${getColor()}`}>
        {score}
      </div>
      
      <p className="text-sm text-slate-400 mt-1">out of 100</p>
      
      <p className={`mt-3 text-sm font-semibold ${getColor()}`}>
        {getLabel()}
      </p>

      <div className="mt-4 w-full bg-slate-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-700 ${
            score >= 71 ? 'bg-green-500' :
            score >= 41 ? 'bg-yellow-500' : 'bg-red-500'
          }`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  )
}