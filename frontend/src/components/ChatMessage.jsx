export default function ChatMessage({ agentName, colorClass, content, stance, tension }) {
  const getStanceColor = (st) => {
    switch(st) {
      case 'agree': return 'bg-green-100 text-green-800 border-green-200';
      case 'disagree': return 'bg-red-100 text-red-800 border-red-200';
      case 'partially_agree': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getAvatarColor = () => {
    const map = {
      'cto': 'bg-blue-500',
      'marketing': 'bg-pink-500',
      'cfo': 'bg-amber-500',
      'skeptic': 'bg-rose-500', // tailwind v3 coral alternative
      'ceo': 'bg-teal-500'
    };
    return map[agentName.toLowerCase()] || 'bg-gray-500';
  };

  return (
    <div className="flex gap-4 mb-6">
      <div className="flex-shrink-0">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm ${getAvatarColor()}`}>
          {agentName.substring(0, 3).toUpperCase()}
        </div>
      </div>
      <div className="flex-1 max-w-3xl">
        <div className="flex items-center gap-3 mb-1">
          <span className="font-semibold text-gray-800">{agentName.toUpperCase()}</span>
          {stance && (
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStanceColor(stance)}`}>
              {stance.replace('_', ' ')}
            </span>
          )}
        </div>
        <div className="bg-white rounded-2xl rounded-tl-none p-4 shadow-sm border border-gray-100 text-gray-700 leading-relaxed text-sm">
          {content}
        </div>
        
        {tension && (
          <div className="mt-2 ml-4">
            <details className="group">
              <summary className="text-xs font-semibold text-indigo-600 cursor-pointer list-none hover:text-indigo-800 transition-colors flex items-center gap-1">
                <svg className="w-4 h-4 transition-transform group-open:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                View Unresolved Tension
              </summary>
              <div className="mt-2 text-xs bg-indigo-50 text-indigo-900 border border-indigo-100 rounded-lg p-3 italic">
                "{tension}"
              </div>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
