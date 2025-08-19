import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const data = await req.json();
  const resp = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/ai/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return new Response(resp.body, {
    headers: {
      'Content-Type': 'text/event-stream',
    },
  });
}
