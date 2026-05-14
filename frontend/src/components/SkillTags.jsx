export default function SkillTags({ keywords }) {
  
  if (!keywords || keywords.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-center">
        <p className="text-green-600 text-sm font-medium">
          ✅ No missing keywords — Great match!
        </p>
      </div>
    )
  }

  return (
    <div>
      <p className="text-sm font-semibold text-slate-700 mb-3">
        ⚠️ Missing Keywords ({keywords.length})
      </p>
      <div className="flex flex-wrap gap-2">
        {keywords.map((kw, i) => (
          <span
            key={i}
            className="bg-red-100 text-red-600 text-xs font-medium px-3 py-1 rounded-full border border-red-200"
          >
            ❌ {kw}
          </span>
        ))}
      </div>
    </div>
  )
}