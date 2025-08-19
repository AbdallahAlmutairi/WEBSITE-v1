import TrendBadge from '../../../components/TrendBadge';
import MetricsGrid from '../../../components/MetricsGrid';
import AiChat from '../../../components/AiChat';
import Chart from '../../../components/Chart';

export default async function SymbolPage({ params }: { params: { symbol: string } }) {
  const { symbol } = params;
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/history?symbol=${symbol}&interval=1m&lookback=5d`, { cache: 'no-store' });
  let rows: any[] = [];
  try {
    rows = await res.json();
  } catch {
    rows = [];
  }
  const candles = rows.map((c: any) => ({
    time: typeof c.ts === 'string' ? c.ts : new Date(c.ts).toISOString(),
    open: Number(c.open),
    high: Number(c.high),
    low: Number(c.low),
    close: Number(c.close),
    volume: Number(c.volume ?? 0),
  }));
  return (
    <main className="p-4 space-y-4">
      <h1 className="text-xl font-semibold">{symbol}</h1>
      <Chart candles={candles} />
      <TrendBadge symbol={symbol} />
      <MetricsGrid symbol={symbol} />
      <AiChat symbol={symbol} timeframe="1d" />
    </main>
  );
}
