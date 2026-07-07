import { useBusinessSimulation } from './hooks/useBusinessSimulation';
import IdeaInput from './components/IdeaInput';
import AgentStatusPills from './components/AgentStatusPills';
import ChatMessage from './components/ChatMessage';
import DebateDivider from './components/DebateDivider';
import FinalPlanCard from './components/FinalPlanCard';
import CTOAnalysisCard from './components/CTOAnalysisCard';
import MarketingAnalysisCard from './components/MarketingAnalysisCard';
import CFOAnalysisCard from './components/CFOAnalysisCard';
import SkepticAnalysisCard from './components/SkepticAnalysisCard';

function App() {
  const { status, data, error, submitIdea, handleDownload } = useBusinessSimulation();

  const renderAnalysisCard = (agentId, analysisObj) => {
    if (!analysisObj) return null;
    switch(agentId) {
      case 'cto': return <CTOAnalysisCard key={`analysis-cto`} data={analysisObj} />;
      case 'marketing': return <MarketingAnalysisCard key={`analysis-marketing`} data={analysisObj} />;
      case 'cfo': return <CFOAnalysisCard key={`analysis-cfo`} data={analysisObj} />;
      case 'skeptic': return <SkepticAnalysisCard key={`analysis-skeptic`} data={analysisObj} />;
      default:
        // Fallback for CEO or any unknown agent in the analysis round
        return (
          <ChatMessage 
            key={`analysis-${agentId}`} 
            agentName={agentId} 
            content={analysisObj.summary || "Agent analysis complete."} 
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center pt-12 pb-24 px-4 font-sans">
      <div className="w-full max-w-4xl">
        
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
            The Virtual Boardroom
          </h1>
          <p className="text-lg text-gray-600">
            Submit your startup idea to a team of autonomous AI executives.
          </p>
        </div>

        {/* Input */}
        <IdeaInput onSubmit={submitIdea} disabled={status === 'loading'} />

        {/* Error message */}
        {status === 'error' && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded shadow-sm">
            <h3 className="text-red-800 font-medium">Pipeline Error</h3>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        )}

        {/* Status Pills */}
        {(status !== 'idle' || data) && (
          <AgentStatusPills status={status} />
        )}

        {/* Chat Area */}
        {status === 'success' && data && (
          <div className="flex flex-col gap-2 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            
            {/* Analysis Round */}
            {data.analysis && Object.entries(data.analysis).map(([agentId, analysisObj]) => 
              renderAnalysisCard(agentId, analysisObj)
            )}

            {/* Divider */}
            {data.debate && data.debate.length > 0 && (
              <DebateDivider />
            )}

            {/* Debate Round */}
            {data.debate && data.debate.map((reaction, idx) => {
                const r = reaction.reaction;
                return (
                  <ChatMessage 
                    key={`debate-${idx}`}
                    agentName={reaction.agent_name}
                    content={r.key_response}
                    stance={r.stance}
                    tension={r.unresolved_tension}
                  />
                );
            })}

            {/* Final Plan */}
            {data.final_plan && (
              <div className="mt-8 pt-8 border-t border-teal-100">
                <FinalPlanCard 
                  markdown={data.final_plan}
                  onDownload={handleDownload}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
