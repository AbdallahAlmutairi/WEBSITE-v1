'use client';

import { useEffect, useRef } from 'react';
import { createChart, CandlestickData } from 'lightweight-charts';

export default function Chart({ candles }: { candles: CandlestickData[] }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const chart = createChart(containerRef.current, { height: 300 });
    const series = chart.addCandlestickSeries();
    series.setData(candles);
    return () => {
      chart.remove();
    };
  }, [candles]);

  return <div ref={containerRef} className="w-full" />;
}
