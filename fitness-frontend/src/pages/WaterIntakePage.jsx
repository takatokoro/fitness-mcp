import { useState } from 'react'
import { calculateWaterIntake } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

// ── Water bottle fill visual ──────────────────────────────────
function WaterBottle({ litres, maxLitres = 5 }) {
  const pct = Math.min(100, (litres / maxLitres) * 100)
  const glasses = Math.round(litres / 0.25)

  return (
    <div style={{ display: 'flex', gap: '2rem', alignItems: 'center', flexWrap: 'wrap' }}>
      {/* Bottle SVG */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
        <svg width="80" height="160" viewBox="0 0 80 160">
          <defs>
            <clipPath id="bottleClip">
              <path d="M28 10 Q28 0 40 0 Q52 0 52 10 L56 30 Q64 36 64 50 L64 140 Q64 152 52 152 L28 152 Q16 152 16 140 L16 50 Q16 36 24 30 Z" />
            </clipPath>
          </defs>
          {/* Bottle outline */}
          <path d="M28 10 Q28 0 40 0 Q52 0 52 10 L56 30 Q64 36 64 50 L64 140 Q64 152 52 152 L28 152 Q16 152 16 140 L16 50 Q16 36 24 30 Z"
            fill="var(--bg)" stroke="var(--border2)" strokeWidth="1.5" />
          {/* Water fill */}
          <rect
            x="16" y={152 - (102 * pct / 100)} width="48" height={102 * pct / 100}
            fill="#bae6fd" clipPath="url(#bottleClip)"
            style={{ transition: 'y 1s ease, height 1s ease' }}
          />
          {/* Ripple line */}
          <line x1="16" y1={152 - (102 * pct / 100)} x2="64" y2={152 - (102 * pct / 100)}
            stroke="#7dd3fc" strokeWidth="1" clipPath="url(#bottleClip)"
            style={{ transition: 'y 1s ease' }}
          />
          {/* Bottle shine */}
          <path d="M26 50 Q26 30 32 28" stroke="white" strokeWidth="2" fill="none" opacity="0.6" strokeLinecap="round" />
          {/* Label line markers */}
          {[1,2,3,4].map(i => (
            <line key={i} x1="58" y1={152 - (102 * i / 4)} x2="64" y2={152 - (102 * i / 4)}
              stroke="var(--border2)" strokeWidth="1" />
          ))}
        </svg>
        <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'Space Mono, monospace', color: '#0284c7', lineHeight: 1 }}>{litres}L</div>
        <div style={{ fontSize: '0.65rem', color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', fontWeight: 600 }}>daily target</div>
      </div>

      {/* Stats */}
      <div style={{ flex: 1, minWidth: 180 }}>
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 6 }}>Glasses of water (250ml)</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
            {Array.from({ length: Math.min(glasses, 20) }).map((_, i) => (
              <div key={i} style={{
                width: 20, height: 24, borderRadius: '0 0 4px 4px',
                background: i < glasses ? '#bae6fd' : 'var(--bg)',
                border: '1px solid var(--border2)',
                transition: 'background 0.3s'
              }} />
            ))}
            {glasses > 20 && <span style={{ fontSize: '0.75rem', color: 'var(--text3)', alignSelf: 'center' }}>+{glasses - 20} more</span>}
          </div>
          <div style={{ fontSize: '0.78rem', color: '#0284c7', fontWeight: 600, marginTop: 6 }}>{glasses} glasses per day</div>
        </div>

        <div>
          <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 6 }}>Hourly reminder (16hrs awake)</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ flex: 1, height: 8, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden', border: '1px solid var(--border)' }}>
              <div style={{ width: `${Math.min(100, (litres / 5) * 100)}%`, height: '100%', background: '#38bdf8', borderRadius: 4, transition: 'width 0.8s ease' }} />
            </div>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#0284c7', fontFamily: 'Space Mono, monospace', minWidth: 50 }}>{(litres / 16 * 1000).toFixed(0)}ml/hr</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Breakdown bars ────────────────────────────────────────────
function WaterBreakdown({ result }) {
  const base = result?.base_intake_litres ?? null
  const exercise = result?.exercise_intake_litres ?? null
  const total = result?.total_daily_target_litres ?? result?.daily_water_target_litres ?? null
  if (!total) return null

  const items = [
    { label: 'Base intake', value: base, color: '#7dd3fc', desc: 'for body functions' },
    { label: 'Exercise top-up', value: exercise, color: '#38bdf8', desc: 'lost during workout' },
  ].filter(i => i.value !== null)

  if (items.length === 0) return null

  return (
    <div style={{ marginTop: '1.25rem' }}>
      <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 10 }}>Breakdown</div>
      {items.map(item => (
        <div key={item.label} style={{ marginBottom: 10 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text2)' }}>{item.label} <span style={{ color: 'var(--text3)', fontWeight: 400 }}>— {item.desc}</span></span>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: item.color, fontFamily: 'Space Mono, monospace' }}>{item.value}L</span>
          </div>
          <div style={{ height: 8, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden', border: '1px solid var(--border)' }}>
            <div style={{ width: `${(item.value / total) * 100}%`, height: '100%', background: item.color, borderRadius: 4, transition: 'width 0.8s ease' }} />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function WaterIntakePage({ token }) {
  const [weight, setWeight]   = useState('')
  const [minutes, setMinutes] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  async function handleCalculate() {
    if (!weight || !minutes) { setError('Please fill in both fields.'); return }
    setLoading(true); setResult(null); setError(null)
    const { data, error: err } = await calculateWaterIntake(weight, minutes, token)
    setLoading(false)
    if (err) { setError(err); return }
    setResult(data)
  }

  const litres = result?.total_daily_target_litres ?? result?.daily_water_target_litres ?? null

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">Tool 1</div>
        <h1 className="hero-title">Daily Water Intake</h1>
        <p className="hero-sub">Calculate how much water you need based on your body weight and workout length.</p>
      </div>

      <div className="card">
        <div className="card-title"><span className="icon">💧</span>Your Details</div>
        <div className="form-row">
          <div className="field">
            <label>Body Weight (kg)</label>
            <input type="number" placeholder="e.g. 75" value={weight} onChange={e => setWeight(e.target.value)} min="20" max="300" />
          </div>
          <div className="field">
            <label>Workout Duration (min)</label>
            <input type="number" placeholder="e.g. 60" value={minutes} onChange={e => setMinutes(e.target.value)} min="0" max="480" />
          </div>
        </div>
        <button className="btn btn-primary" onClick={handleCalculate} disabled={loading}>
          {loading && <span className="spinner" />}
          Calculate
        </button>
        {error && <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--danger)', padding: '0.6rem', background: '#d930250a', borderRadius: 'var(--radius-md)', border: '1px solid #d9302530' }}>{error}</div>}
      </div>

      {litres && !loading && (
        <div className="card">
          <div className="card-title"><span className="icon">💧</span>Your Water Target</div>
          <WaterBottle litres={litres} />
          <WaterBreakdown result={result} />
        </div>
      )}

      {result && !loading && (
        <div className="card">
          <div className="card-title"><span className="icon">📋</span>Full Response</div>
          <ResultBox result={result} error={null} loading={false} />
          <CoachingSummary toolData={result} token={token} context={{ weight_kg: weight, workout_minutes: minutes }} />
        </div>
      )}
    </>
  )
}
