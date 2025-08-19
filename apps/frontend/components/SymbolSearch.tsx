'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function SymbolSearch() {
  const router = useRouter();
  const [symbol, setSymbol] = useState('');

  return (
    <div className="flex gap-2">
      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="AAPL, MSFT, 2222.SR"
        className="border px-2 py-1 flex-1"
      />
      <button
        className="px-3 py-1 bg-blue-600 text-white"
        onClick={() => symbol && router.push(`/symbols/${symbol.toUpperCase()}`)}
      >
        Go
      </button>
    </div>
  );
}
