import Link from 'next/link';
import SymbolSearch from '../components/SymbolSearch';

export default function Home() {
  return (
    <main className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Stock Analysis</h1>
      <SymbolSearch />
      <p className="text-sm text-gray-500">Enter a symbol to view details.</p>
    </main>
  );
}
