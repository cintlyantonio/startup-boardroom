export default function CFOAnalysisCard({ data }) {
  if (!data) return null;

  const getConfidenceColor = (confidence) => {
    const c = (confidence || '').toLowerCase();
    if (c.includes('high')) return 'bg-green-100 text-green-800 border-green-200';
    if (c.includes('low')) return 'bg-red-100 text-red-800 border-red-200';
    return 'bg-yellow-100 text-yellow-800 border-yellow-200';
  };

  return (
    <div className="flex gap-4 mb-6">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-amber-500 shadow-sm">
          CFO
        </div>
      </div>
      <div className="flex-1 max-w-3xl">
        <div className="flex items-center gap-3 mb-1">
          <span className="font-semibold text-gray-800">CFO Analysis</span>
        </div>
        <div className="bg-white rounded-2xl rounded-tl-none p-5 shadow-sm border border-gray-100 text-gray-700 leading-relaxed text-sm">
          
          <div className="flex flex-wrap gap-3 mb-4 items-center">
            <div className="bg-amber-50 text-amber-900 border border-amber-200 px-4 py-2 rounded-lg font-bold text-lg shadow-sm">
              Breakeven: {data.breakeven_estimate}
            </div>
            <div className={`px-3 py-1 rounded-full text-xs font-semibold border ${getConfidenceColor(data.confidence_level)}`}>
              Confidence: {data.confidence_level}
            </div>
          </div>

          <div className="mb-2">
            <h4 className="font-bold text-gray-800 mb-2">Financial Assumptions</h4>
            <ul className="list-disc pl-5 space-y-1 text-gray-600">
              {(data.assumptions || []).map((assumption, idx) => (
                <li key={idx}>{assumption}</li>
              ))}
            </ul>
          </div>
          
        </div>
      </div>
    </div>
  );
}
