'use client';

import { useState } from 'react';

export default function AiChat({ symbol, timeframe }: { symbol: string; timeframe: string }) {
  const [messages, setMessages] = useState<string[]>([]);
  const [question, setQuestion] = useState('');

  const ask = async () => {
    const res = await fetch('/api/ai/stream', {
      method: 'POST',
      body: JSON.stringify({ symbol, timeframe, question }),
    });
    if (!res.body) return;
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      setMessages((prev) => [...prev, buffer]);
    }
  };

  return (
    <div className="space-y-2">
      <div className="max-h-60 overflow-y-auto border p-2 text-sm">
        {messages.map((m, i) => (
          <p key={i}>{m}</p>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border px-2 py-1"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about the symbol"
        />
        <button className="px-3 py-1 bg-blue-600 text-white" onClick={ask}>
          Ask
        </button>
      </div>
    </div>
  );
}
