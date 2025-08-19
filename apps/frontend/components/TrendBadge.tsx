'use client';

import { useQuery } from '@tanstack/react-query';

const colorMap: Record<string, string> = {
  Uptrend: 'bg-green-200 text-green-800',
  Downtrend: 'bg-red-200 text-red-800',
  Ranging: 'bg-gray-200 text-gray-800',
};

export default function TrendBadge({ symbol }: { symbol: string }) {
  const { data } = useQuery({
    queryKey: ['trend', symbol],
    queryFn: async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/trend?symbol=${symbol}`);
      return res.json();
    },
  });

  if (!data) return <span className="text-gray-500">Loading...</span>;
  return <span className={`px-2 py-1 rounded ${colorMap[data.label]}`}>{data.label}</span>;
}
