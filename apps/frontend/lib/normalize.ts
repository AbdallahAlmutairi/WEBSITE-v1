export type Candle = { ts: string|number|Date; open:number; high:number; low:number; close:number; volume?:number };
export function normalize(c: Candle) {
  return {
    time: typeof c.ts === 'string' ? c.ts : (c.ts instanceof Date ? c.ts.toISOString() : new Date(c.ts).toISOString()),
    open: Number(c.open),
    high: Number(c.high),
    low: Number(c.low),
    close: Number(c.close),
    volume: Number(c.volume ?? 0),
  };
}
