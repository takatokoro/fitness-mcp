import { useState } from 'react'

const BASE_URL = 'https://fitness-mcp-6vuf.onrender.com'

export default function CoachingSummary({ toolData, token, context = {} }) {
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState(null)
  const [error, setError]     = useState(null)

  if (!toolData) return null

  async function handleAsk() {
    setLoading(true); setSummary(null); setError(null)
    const dataStr = JSON.stringify(toolData, null, 2)
    const ctxStr  = Object.entries(context).map(([k,v]) => `${k}: ${v}`).join(', ')
    try {
      const res = await fetch(`${BASE_URL}/ai-coaching-summary-simple`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ tool_result: dataStr, context: ctxStr })
      })
      const json = await res.json()
      if (!res.ok) { setError(json?.detail || json?.error || `Error ${res.status}`); setLoading(false); return }
      setSummary(json.coaching_summary)
    } catch (err) {
      setError(err.message)
    }
    setLoading(false)
  }

  return (
    <div style={{ marginTop: '1rem' }}>
      <hr className="divider" />
      <button className="btn btn-ghost" onClick={handleAsk} disabled={loading} style={{ fontSize: '0.82rem' }}>
        {loading ? <><span className="spinner" /> Asking Gemini…</> : '✨ Get AI Coaching Tip'}
      </button>

      {error && (
        <div className="result-box error" style={{ marginTop: '0.75rem' }}>
          <div className="result-header">Error</div>
          <div className="result-body" style={{ color: 'var(--danger)' }}>{error}</div>
        </div>
      )}

      {summary && (
        <div className="coaching-box" style={{ marginTop: '0.75rem' }}>
          <div className="coaching-label">✨ Gemini's Coaching Tip</div>
          {summary}
        </div>
      )}
    </div>
  )
}
