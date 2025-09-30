async function resolveTerm(q: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  try {
    const res = await fetch(`${base}/resolve/?q=${encodeURIComponent(q)}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Request failed');
    return res.json();
  } catch {
    return { query: q, error: 'unreachable' };
  }
}

export default async function Page() {
  const sample = await resolveTerm('permian');
  return (
    <main>
      <h1>GeoResolve</h1>
      <p>Connected to API at <code>{process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}</code></p>
      <pre>{JSON.stringify(sample, null, 2)}</pre>
      <p style={{ color: '#666' }}>Edit this page at <code>clients/web/app/page.tsx</code></p>
    </main>
  );
}

