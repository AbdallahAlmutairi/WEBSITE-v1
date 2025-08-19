export function priceSocket(symbols: string[]): WebSocket {
  const url = (process.env.NEXT_PUBLIC_API_BASE || '').replace('http', 'ws');
  return new WebSocket(`${url}/ws/price-stream?symbols=${symbols.join(',')}`);
}
