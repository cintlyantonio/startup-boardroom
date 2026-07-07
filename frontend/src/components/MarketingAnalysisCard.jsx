export default function MarketingAnalysisCard({ data }) {
  if (!data) return null;

  return (
    <div className="flex gap-4 mb-6">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-pink-500 shadow-sm">
          MKT
        </div>
      </div>
      <div className="flex-1 max-w-3xl">
        <div className="flex items-center gap-3 mb-1">
          <span className="font-semibold text-gray-800">Marketing Analysis</span>
        </div>
        <div className="bg-white rounded-2xl rounded-tl-none p-5 shadow-sm border border-gray-100 text-gray-700 leading-relaxed text-sm">
          
          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-1">Target Audience</h4>
            <p className="text-gray-600">{data.target_audience}</p>
          </div>

          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-1">Value Proposition</h4>
            <p className="text-gray-600">{data.value_proposition}</p>
          </div>

          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-2">Competitors</h4>
            <ul className="space-y-3">
              {(data.competitors || []).map((comp, idx) => (
                <li key={idx} className="bg-gray-50 p-3 rounded-lg border border-gray-100">
                  <span className="font-semibold text-gray-800 block mb-1">{comp.name || comp}</span>
                  {comp.description && <span className="text-xs text-gray-600 block mb-1">{comp.description}</span>}
                  {comp.differentiation && <span className="text-xs italic text-gray-500 block">Diff: {comp.differentiation}</span>}
                </li>
              ))}
            </ul>
          </div>

          <div className="mb-4">
            <h4 className="font-bold text-gray-800 mb-2">Acquisition Channels</h4>
            <div className="flex flex-wrap gap-2">
              {(data.acquisition_channels || []).map((channel, idx) => (
                <span key={idx} className="bg-pink-50 text-pink-700 border border-pink-100 px-3 py-1 rounded-full text-xs">
                  {channel}
                </span>
              ))}
            </div>
          </div>

          {data.market_notes && (
            <div className="mb-4 p-3 bg-indigo-50 border border-indigo-100 rounded-lg">
              <h4 className="font-bold text-indigo-900 mb-1 text-xs uppercase tracking-wider">Market Notes</h4>
              <p className="text-indigo-800 text-xs">{data.market_notes}</p>
            </div>
          )}

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
