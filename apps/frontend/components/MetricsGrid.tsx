'use client';

import { useQuery } from '@tanstack/react-query';

export default function MetricsGrid({ symbol }: { symbol: string }) {
  const { data } = useQuery({
    queryKey: ['quote', symbol],
    queryFn: async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/quote?symbol=${symbol}`);
      return res.json();
    },
  });
  if (!data) return null;
  return (
    <div className="grid grid-cols-2 gap-2 text-sm">
      <div>Price</div>
      <div className="font-medium">{data.price.toFixed(2)}</div>
      <div>Change%</div>
      <div className={data.change >= 0 ? 'text-green-600' : 'text-red-600'}>
        {data.change_percent.toFixed(2)}%
      </div>
    </div>
  );
}
