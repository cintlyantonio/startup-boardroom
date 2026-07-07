export default function SkepticAnalysisCard({ data }) {
  if (!data) return null;

  const getSeverityColor = (severity) => {
    const s = (severity || '').toLowerCase();
    if (s.includes('high') || s.includes('critical')) return 'bg-red-100 text-red-800 border-red-200';
    if (s.includes('low')) return 'bg-green-100 text-green-800 border-green-200';
    return 'bg-yellow-100 text-yellow-800 border-yellow-200';
  };

  return (
    <div className="flex gap-4 mb-6">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-rose-500 shadow-sm">
          SKP
        </div>
      </div>
      <div className="flex-1 max-w-3xl">
        <div className="flex items-center gap-3 mb-1">
          <span className="font-semibold text-gray-800">Skeptic Analysis</span>
        </div>
        <div className="bg-white rounded-2xl rounded-tl-none p-5 shadow-sm border border-gray-100 text-gray-700 leading-relaxed text-sm">
          
          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-2">Identified Risks</h4>
            <div className="space-y-3">
              {(data.risks || []).map((risk, idx) => (
                <div key={idx} className="bg-gray-50 p-3 rounded-lg border border-gray-100">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-gray-800">{risk.category}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider border ${getSeverityColor(risk.severity)}`}>
                      {risk.severity}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">{risk.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-2">Assumptions Challenged</h4>
            <ul className="list-disc pl-5 space-y-1 text-gray-600">
              {(data.assumptions_challenged || []).map((assumption, idx) => (
                <li key={idx}>{assumption}</li>
              ))}
            </ul>
          </div>

          <div className="mb-4 p-4 bg-rose-50 border border-rose-100 rounded-lg shadow-sm">
            <h4 className="font-bold text-rose-900 mb-1">Overall Verdict</h4>
            <p className="text-rose-800 font-medium">{data.overall_verdict}</p>
          </div>

          {data.sources && data.sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-gray-100">
              <details className="group">
                <summary className="text-xs font-semibold text-gray-500 cursor-pointer list-none hover:text-gray-800 transition-colors flex items-center gap-1">
                  <svg className="w-4 h-4 transition-transform group-open:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  Fuentes ({data.sources.length})
                </summary>
                <ul className="mt-2 text-xs space-y-1 bg-gray-50 p-3 rounded-lg border border-gray-200">
                  {data.sources.map((src, idx) => (
                    <li key={idx} className="truncate">
                      <a href={src} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                        {src}
                      </a>
                    </li>
                  ))}
                </ul>
              </details>
            </div>
          )}
          
        </div>
      </div>
    </div>
  );
}
