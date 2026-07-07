import { useState } from 'react';

export function useBusinessSimulation() {
  const [status, setStatus] = useState('idle'); // idle | loading | success | error
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const submitIdea = async (idea) => {
    setStatus('loading');
    setError(null);
    setData(null);

    try {
      const response = await fetch('http://localhost:8000/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to connect to the server');
      }

      const result = await response.json();
      setData(result);
      setStatus('success');
    } catch (err) {
      console.error('Simulation error:', err);
      setError(err.message);
      setStatus('error');
    }
  };

  const handleDownload = () => {
    if (data?.pdf_path) {
      // Create a hidden anchor and click it to trigger download
      const link = document.createElement('a');
      link.href = `http://localhost:8000${data.pdf_path}`;
      link.download = data.pdf_path.split('/').pop();
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return { status, data, error, submitIdea, handleDownload };
}
