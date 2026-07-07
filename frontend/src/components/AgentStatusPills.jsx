import { useEffect, useState } from 'react';

const AGENTS = [
  { id: 'cto', name: 'CTO', color: 'bg-blue-500', label: 'Technical Viability' },
  { id: 'marketing', name: 'Marketing', color: 'bg-pink-500', label: 'Market Demand' },
  { id: 'cfo', name: 'CFO', color: 'bg-amber-500', label: 'Financials' },
  { id: 'skeptic', name: 'Skeptic', color: 'bg-coral-500', label: 'Devil\'s Advocate' },
  { id: 'ceo', name: 'CEO', color: 'bg-teal-500', label: 'Orchestration' }
];

const LOADING_MESSAGES = [
  "The CTO is assessing the technical feasibility...",
  "Marketing is analyzing market demand...",
  "The CFO is calculating financial projections...",
  "The Skeptic is looking for hidden risks...",
  "The team is discussing the conclusions...",
  "The CEO is drafting the final plan..."
];

// Tailwind doesn't have coral built-in, so we'll map coral to rose for tailwind v3 out of the box
const COLOR_MAP = {
  'bg-blue-500': 'bg-blue-500',
  'bg-pink-500': 'bg-pink-500',
  'bg-amber-500': 'bg-amber-500',
  'bg-coral-500': 'bg-rose-500', 
  'bg-teal-500': 'bg-teal-500',
};

export default function AgentStatusPills({ status }) { // idle | loading | success | error
  const [loadingMsgIdx, setLoadingMsgIdx] = useState(0);
  const [staggeredDone, setStaggeredDone] = useState({});

  useEffect(() => {
    let interval;
    if (status === 'loading') {
      interval = setInterval(() => {
        setLoadingMsgIdx((prev) => (prev + 1) % LOADING_MESSAGES.length);
      }, 10000); // cycle every 10s to fit the 60s total
      setStaggeredDone({});
    } else if (status === 'success') {
      // Stagger the 'done' states when successful
      AGENTS.forEach((agent, i) => {
        setTimeout(() => {
          setStaggeredDone(prev => ({ ...prev, [agent.id]: true }));
        }, i * 200);
      });
    } else {
      setStaggeredDone({});
      setLoadingMsgIdx(0);
    }
    return () => clearInterval(interval);
  }, [status]);

  const getAgentStatus = (agentId) => {
    if (status === 'idle' || status === 'error') return 'idle';
    if (status === 'loading') return 'thinking';
    if (status === 'success') return staggeredDone[agentId] ? 'done' : 'thinking';
    return 'idle';
  };

  return (
    <div className="mb-8 flex flex-col items-center">
      <div className="flex flex-wrap gap-4 justify-center mb-4">
        {AGENTS.map((agent) => {
          const agentStatus = getAgentStatus(agent.id);
          
          return (
            <div key={agent.id} className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100 transition-all duration-300">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-xs ${COLOR_MAP[agent.color]} ${agentStatus === 'thinking' ? 'animate-pulse' : ''}`}>
                {agent.name.substring(0, 3)}
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold text-gray-700 leading-tight">{agent.name}</span>
                <span className="text-xs text-gray-400 leading-tight">{agent.label}</span>
              </div>
              
              <div className="ml-2">
                {agentStatus === 'idle' && <div className="w-2 h-2 rounded-full bg-gray-300"></div>}
                {agentStatus === 'thinking' && (
                  <div className="flex gap-1">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                )}
                {agentStatus === 'done' && (
                  <div className="w-4 h-4 rounded-full bg-green-500 flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      
      {status === 'loading' && (
        <div className="text-sm font-medium text-teal-600 animate-pulse bg-teal-50 px-4 py-2 rounded-full">
          {LOADING_MESSAGES[loadingMsgIdx]}
        </div>
      )}
    </div>
  );
}
