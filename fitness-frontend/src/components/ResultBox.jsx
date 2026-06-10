export default function ResultBox({ result, error, loading }) {
  if (loading) return (
    <div style={{ padding: '1rem', textAlign: 'center', color: 'var(--text3)', fontSize: '0.82rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
      <span className="spinner" style={{ borderTopColor: 'var(--accent)' }} />
      Calling server…
    </div>
  )
  if (error) return (
    <div className="result-box error" style={{ marginTop: '1rem' }}>
      <div className="result-header">Error</div>
      <div className="result-body" style={{ color: 'var(--danger)' }}>{error}</div>
    </div>
  )
  if (!result) return null
  return (
    <div className="result-box success" style={{ marginTop: '1rem' }}>
      <div className="result-header">Response</div>
      <div className="result-body">{JSON.stringify(result, null, 2)}</div>
    </div>
  )
}
