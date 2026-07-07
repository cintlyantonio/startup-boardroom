import Markdown from 'react-markdown';
import { Download } from 'lucide-react';

export default function FinalPlanCard({ markdown, onDownload }) {
  if (!markdown) return null;

  return (
    <div className="flex gap-4 mb-12">
      <div className="flex-shrink-0">
        <div className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg bg-teal-500 shadow-md ring-4 ring-teal-50">
          CEO
        </div>
      </div>
      <div className="flex-1 max-w-4xl">
        <div className="flex items-center justify-between mb-2">
          <span className="font-bold text-teal-800 text-lg">Final Synthesis & Business Plan</span>
          <button 
            onClick={onDownload}
            className="flex items-center gap-2 bg-teal-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-teal-700 transition-colors shadow-sm"
          >
            <Download size={16} />
            Download PDF
          </button>
        </div>
        
        <div className="bg-white rounded-2xl rounded-tl-none p-8 shadow-lg border border-teal-100 prose prose-teal max-w-none prose-headings:text-teal-900 prose-h2:border-b prose-h2:pb-2 prose-h2:border-gray-100">
          <Markdown>{markdown}</Markdown>
        </div>
      </div>
    </div>
  );
}
