import { useState } from 'react'
import { estimateSweatLoss, estimateSweatLossV2 } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

export default function SweatLossPage({ token }) {
  const [duration, setDuration]   = useState('')
  const [intensity, setIntensity] = useState('moderate')
  const [version, setVersion]     = useState('v1')
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState(null)
  const [error, setError]         = useState(null)

  async function handleCalculate() {
    if (!duration) { setError('Please enter workout duration.'); return }
    setLoading(true); setResult(null); setError(null)
    const fn = version === 'v2' ? estimateSweatLossV2 : estimateSweatLoss
    const { data, error: err } = await fn(duration, intensity, token)
    setLoading(false)
    if (err) { setError(err); return }
    setResult(data)
  }

  const sodium    = result?.sodium_lost_mg    ?? result?.sodium_mg    ?? null
  const potassium = result?.potassium_lost_mg ?? result?.potassium_mg ?? null
  const magnesium = result?.magnesium_lost_mg ?? result?.magnesium_mg ?? null

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">Tool 2</div>
        <h1 className="hero-title">Sweat Loss Estimator</h1>
        <p className="hero-sub">Find out which minerals you lose during a workout — and what foods can replace them (v2).</p>
      </div>

      <div className="card">
        <div className="card-title"><span className="icon">🧂</span>Workout Info</div>

        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem' }}>
          {['v1', 'v2'].map(v => (
            <button
              key={v}
              className={`btn ${version === v ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.8rem', padding: '0.4rem 1rem' }}
              onClick={() => { setVersion(v); setResult(null); setError(null) }}
            >
              {v === 'v1' ? 'Basic (v1)' : 'With Food Tips (v2)'}
            </button>
          ))}
        </div>

        {version === 'v2' && (
          <div className="alert alert-warn">
            ⚡ v2 calls the Ninjas Nutrition API — takes a few extra seconds.
          </div>
        )}

        <div className="form-row">
          <div className="field">
            <label>Duration (min)</label>
            <input type="number" placeholder="e.g. 60" value={duration} onChange={e => setDuration(e.target.value)} min="5" max="480" />
          </div>
          <div className="field">
            <label>Intensity</label>
            <select value={intensity} onChange={e => setIntensity(e.target.value)}>
              <option value="low">Low</option>
              <option value="moderate">Moderate</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <button className="btn btn-primary" onClick={handleCalculate} disabled={loading}>
          {loading && <span className="spinner" />}
          Estimate Sweat Loss
        </button>

        {(sodium || potassium || magnesium) && !loading && (
          <div className="metrics-grid">
            {sodium    !== null && <div className="metric-tile"><div className="metric-value">{sodium}</div><div className="metric-label">Sodium (mg)</div></div>}
            {potassium !== null && <div className="metric-tile"><div className="metric-value">{potassium}</div><div className="metric-label">Potassium (mg)</div></div>}
            {magnesium !== null && <div className="metric-tile"><div className="metric-value">{magnesium}</div><div className="metric-label">Magnesium (mg)</div></div>}
          </div>
        )}

        <ResultBox result={result} error={error} loading={loading} />

        <CoachingSummary
          toolData={result}
          token={token}
          context={{ workout_duration_min: duration, intensity_level: intensity }}
        />
      </div>
    </>
  )
}
