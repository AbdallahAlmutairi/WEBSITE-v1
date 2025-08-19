import TrendBadge from '../../../components/TrendBadge';
import MetricsGrid from '../../../components/MetricsGrid';
import AiChat from '../../../components/AiChat';

export default function SymbolPage({ params }: { params: { symbol: string } }) {
  const { symbol } = params;
  return (
    <main className="p-4 space-y-4">
      <h1 className="text-xl font-semibold">{symbol}</h1>
      <TrendBadge symbol={symbol} />
      <MetricsGrid symbol={symbol} />
      <AiChat symbol={symbol} timeframe="1d" />
    </main>
  );
}
