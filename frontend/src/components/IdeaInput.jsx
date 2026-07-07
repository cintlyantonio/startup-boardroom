import { useState } from 'react';
import { Send } from 'lucide-react';

export default function IdeaInput({ onSubmit, disabled }) {
  const [idea, setIdea] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (idea.trim() && !disabled) {
      onSubmit(idea.trim());
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-2">Simulate a Business Idea</h2>
      <p className="text-gray-500 text-sm mb-4">Enter a startup concept to have the AI executive team analyze and debate it.</p>
      
      <form onSubmit={handleSubmit} className="relative">
        <textarea
          className="w-full bg-gray-50 border border-gray-200 rounded-lg p-4 pr-12 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none h-24 text-gray-700"
          placeholder="e.g., A smart home mirror that acts as a virtual personal trainer..."
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !idea.trim()}
          className="absolute right-3 bottom-3 p-2 bg-teal-600 text-white rounded-full hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
