import { normalize } from '../lib/normalize';

describe('normalize', () => {
  it('returns a plain-JSON candle', () => {
    const out = normalize({ ts: new Date('2024-01-01T00:00:00Z'), open:1, high:2, low:0.5, close:1.5, volume:10 });
    const s = JSON.stringify(out);
    expect(JSON.parse(s)).toHaveProperty('time', '2024-01-01T00:00:00.000Z');
  });
});
