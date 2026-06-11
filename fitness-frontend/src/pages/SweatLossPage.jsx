import { useState } from 'react'
import { estimateSweatLoss, estimateSweatLossV2 } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

// ── Mineral bar chart ─────────────────────────────────────────
function MineralBars({ sodium, potassium, magnesium }) {
  const minerals = [
    { label: 'Sodium',    value: sodium,    unit: 'mg', color: '#f59e0b', bg: '#fef3c7', max: 2000, food: 'Salt, pretzels, sports drink' },
    { label: 'Potassium', value: potassium, unit: 'mg', color: '#3b82f6', bg: '#dbeafe', max: 500,  food: 'Banana, orange, yogurt' },
    { label: 'Magnesium', value: magnesium, unit: 'mg', color: '#8b5cf6', bg: '#ede9fe', max: 100,  food: 'Nuts, seeds, dark chocolate' },
  ]

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {minerals.map(m => {
        const pct = Math.min(100, (m.value / m.max) * 100)
        return (
          <div key={m.label} style={{ background: m.bg, borderRadius: 'var(--radius-md)', padding: '0.85rem 1rem', border: `1px solid ${m.color}30` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: m.color }}>{m.label}</span>
              <span style={{ fontSize: '1rem', fontWeight: 700, color: m.color, fontFamily: 'Space Mono, monospace' }}>{m.value} {m.unit}</span>
            </div>
            <div style={{ height: 8, background: 'white', borderRadius: 4, overflow: 'hidden', marginBottom: 8 }}>
              <div style={{ width: `${pct}%`, height: '100%', background: m.color, borderRadius: 4, transition: 'width 0.8s ease', opacity: 0.85 }} />
            </div>
            <div style={{ fontSize: '0.72rem', color: m.color, fontWeight: 500, opacity: 0.8 }}>
              Replenish with: {m.food}
            </div>
          </div>
        )
      })}
      <p style={{ fontSize: '0.7rem', color: 'var(--text3)', marginTop: 2 }}>Bar shows % of typical daily max for reference</p>
    </div>
  )
}

// ── Sweat drop visual ─────────────────────────────────────────
function SweatGauge({ fluidLoss, duration, intensity }) {
  const intensityColor = intensity === 'high' ? '#ef4444' : intensity === 'moderate' ? '#f59e0b' : '#3b82f6'
  const intensityBg    = intensity === 'high' ? '#fee2e2' : intensity === 'moderate' ? '#fef3c7' : '#dbeafe'
  const sweatRate = fluidLoss ? (fluidLoss / duration * 60).toFixed(1) : null

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.6rem', marginBottom: '1.25rem' }}>
      <div style={{ background: '#dbeafe', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center', border: '1px solid #bfdbfe' }}>
        <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'Space Mono, monospace', color: '#2563eb', lineHeight: 1 }}>{duration}</div>
        <div style={{ fontSize: '0.62rem', color: '#1d4ed8', textTransform: 'uppercase', letterSpacing: '0.07em', fontWeight: 600, marginTop: 3 }}>minutes</div>
      </div>
      <div style={{ background: intensityBg, borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center', border: `1px solid ${intensityColor}30` }}>
        <div style={{ fontSize: '1rem', fontWeight: 700, color: intensityColor, lineHeight: 1.2, textTransform: 'capitalize' }}>{intensity}</div>
        <div style={{ fontSize: '0.62rem', color: intensityColor, textTransform: 'uppercase', letterSpacing: '0.07em', fontWeight: 600, marginTop: 3 }}>intensity</div>
      </div>
      {sweatRate && (
        <div style={{ background: '#f0fdf4', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center', border: '1px solid #bbf7d0' }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'Space Mono, monospace', color: '#16a34a', lineHeight: 1 }}>{sweatRate}L</div>
          <div style={{ fontSize: '0.62rem', color: '#15803d', textTransform: 'uppercase', letterSpacing: '0.07em', fontWeight: 600, marginTop: 3 }}>per hour</div>
        </div>
      )}
    </div>
  )
}

// ── Food tips from v2 ─────────────────────────────────────────
function FoodTips({ result }) {
  const foods = result?.recovery_foods ?? result?.food_recommendations ?? null
  if (!foods) return null

  const foodList = Array.isArray(foods) ? foods : Object.entries(foods).map(([k, v]) => `${k}: ${v}`)

  return (
    <div style={{ marginTop: '1rem' }}>
      <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 8 }}>Recovery food tips</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {foodList.slice(0, 6).map((food, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 8, padding: '0.5rem 0.75rem', background: 'var(--bg)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)', fontSize: '0.82rem', color: 'var(--text2)' }}>
            <span style={{ color: 'var(--accent)', fontWeight: 700, flexShrink: 0 }}>→</span>
            {typeof food === 'string' ? food : JSON.stringify(food)}
          </div>
        ))}
      </div>
    </div>
  )
}

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
  const fluidLoss = result?.fluid_loss_litres ?? result?.total_fluid_loss_litres ?? null
  const hasResults = sodium !== null || potassium !== null || magnesium !== null

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">Tool 2</div>
        <h1 className="hero-title">Sweat Loss Estimator</h1>
        <p className="hero-sub">Find out which minerals you lose during a workout — and what foods can replace them (v2).</p>
      </div>

      <div className="card">
        <div className="card-title"><span className="icon">🧂</span>Workout Info</div>
        <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '1.1rem' }}>
          {['v1', 'v2'].map(v => (
            <button key={v}
              className={`btn ${version === v ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.8rem', padding: '0.4rem 1rem' }}
              onClick={() => { setVersion(v); setResult(null); setError(null) }}>
              {v === 'v1' ? 'Basic (v1)' : 'With Food Tips (v2)'}
            </button>
          ))}
        </div>
        {version === 'v2' && <div className="alert alert-warn">⚡ v2 calls the Ninjas Nutrition API — takes a few extra seconds.</div>}
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
        {error && <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--danger)', padding: '0.6rem', background: '#d930250a', borderRadius: 'var(--radius-md)', border: '1px solid #d9302530' }}>{error}</div>}
      </div>

      {hasResults && !loading && (
        <div className="card">
          <div className="card-title"><span className="icon">🧂</span>Minerals Lost</div>
          <SweatGauge fluidLoss={fluidLoss} duration={parseInt(duration)} intensity={intensity} />
          <MineralBars sodium={sodium} potassium={potassium} magnesium={magnesium} />
          <FoodTips result={result} />
        </div>
      )}

      {result && !loading && (
        <div className="card">
          <div className="card-title"><span className="icon">📋</span>Full Response</div>
          <ResultBox result={result} error={null} loading={false} />
          <CoachingSummary toolData={result} token={token} context={{ workout_duration_min: duration, intensity_level: intensity }} />
        </div>
      )}
    </>
  )
}
