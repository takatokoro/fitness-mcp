import { useState } from 'react'
import { getCoachingSummary } from '../api'

// ── Weather visual ────────────────────────────────────────────
function WeatherCard({ city, temp, humidity }) {
  const t = parseFloat(temp)

  const isHot  = t >= 30
  const isWarm = t >= 20 && t < 30
  const isCool = t >= 10 && t < 20

  const skyBg   = isHot  ? 'linear-gradient(160deg,#fde68a,#fbbf24)'
                : isWarm ? 'linear-gradient(160deg,#bae6fd,#38bdf8)'
                : isCool ? 'linear-gradient(160deg,#dbeafe,#93c5fd)'
                :          'linear-gradient(160deg,#e0e7ef,#94a3b8)'

  const sunColor   = isHot ? '#f59e0b' : '#facc15'
  const tempLabel  = isHot ? 'Hot' : isWarm ? 'Warm' : isCool ? 'Cool' : 'Cold'
  const humidColor = humidity >= 70 ? '#0369a1' : humidity >= 50 ? '#0284c7' : '#7dd3fc'
  const textDark   = isHot || isWarm

  // Date + time stamped at the moment the card renders
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-AU', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  const timeStr = now.toLocaleTimeString('en-AU', { hour: '2-digit', minute: '2-digit', hour12: true })

  return (
    <div style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden', border: '1px solid var(--border)', marginBottom: '1rem' }}>
      {/* Sky */}
      <div style={{ background: skyBg, padding: '1.25rem 1.5rem 1rem', position: 'relative', minHeight: 120 }}>
        {/* Sun or cloud */}
        {(isHot || isWarm) ? (
          <svg width="64" height="64" viewBox="0 0 64 64" style={{ position: 'absolute', top: 12, right: 20 }}>
            <circle cx="32" cy="32" r="14" fill={sunColor} />
            {[0,45,90,135,180,225,270,315].map((deg, i) => {
              const r = deg * Math.PI / 180
              const x1 = 32 + 18 * Math.cos(r), y1 = 32 + 18 * Math.sin(r)
              const x2 = 32 + 25 * Math.cos(r), y2 = 32 + 25 * Math.sin(r)
              return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={sunColor} strokeWidth="2.5" strokeLinecap="round" />
            })}
          </svg>
        ) : (
          <svg width="72" height="48" viewBox="0 0 72 48" style={{ position: 'absolute', top: 12, right: 16 }}>
            <ellipse cx="36" cy="34" rx="28" ry="14" fill="white" opacity="0.9" />
            <circle cx="26" cy="28" r="14" fill="white" opacity="0.9" />
            <circle cx="44" cy="26" r="16" fill="white" opacity="0.9" />
          </svg>
        )}

        {/* Date + time top-left */}
        <div style={{ fontSize: '0.68rem', fontWeight: 600, color: textDark ? '#92400e' : '#1e40af', opacity: 0.8, marginBottom: 6, letterSpacing: '0.02em' }}>
          {dateStr} · {timeStr}
        </div>

        {/* City + temp */}
        <div style={{ color: textDark ? '#78350f' : '#1e3a5f', fontWeight: 700, fontSize: '0.8rem', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 3 }}>{city}</div>
        <div style={{ color: textDark ? '#92400e' : '#1e3a5f', fontSize: '2.8rem', fontWeight: 700, lineHeight: 1, letterSpacing: '-0.04em', fontFamily: 'Space Mono, monospace' }}>
          {temp}°C
        </div>
        <div style={{ color: textDark ? '#a16207' : '#2563eb', fontSize: '0.78rem', fontWeight: 600, marginTop: 4 }}>{tempLabel}</div>
      </div>

      {/* Stats row */}
      <div style={{ background: 'var(--surface)', display: 'grid', gridTemplateColumns: '1fr 1fr', borderTop: '1px solid var(--border)' }}>
        <div style={{ padding: '0.85rem 1.1rem', borderRight: '1px solid var(--border)' }}>
          <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 4 }}>Humidity</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ flex: 1, height: 6, background: 'var(--bg)', borderRadius: 3, overflow: 'hidden' }}>
              <div style={{ width: `${humidity}%`, height: '100%', background: humidColor, borderRadius: 3, transition: 'width 0.6s ease' }} />
            </div>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: humidColor, fontFamily: 'Space Mono, monospace', minWidth: 36 }}>{humidity}%</span>
          </div>
        </div>
        <div style={{ padding: '0.85rem 1.1rem' }}>
          <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 4 }}>Conditions</div>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text2)' }}>
            {humidity >= 70 ? '💧 High humidity' : humidity >= 50 ? '🌤 Moderate' : '☀️ Dry & clear'}
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Mineral bar chart ─────────────────────────────────────────
function MineralChart({ sodium, potassium, magnesium }) {
  const minerals = [
    { label: 'Sodium',    value: sodium,    unit: 'mg', color: '#f59e0b', max: 2000 },
    { label: 'Potassium', value: potassium, unit: 'mg', color: '#3b82f6', max: 500  },
    { label: 'Magnesium', value: magnesium, unit: 'mg', color: '#8b5cf6', max: 100  },
  ]

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
      {minerals.map(m => {
        const pct = Math.min(100, (m.value / m.max) * 100)
        return (
          <div key={m.label}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5 }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text2)' }}>{m.label}</span>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: m.color, fontFamily: 'Space Mono, monospace' }}>{m.value} {m.unit}</span>
            </div>
            <div style={{ height: 8, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden', border: '1px solid var(--border)' }}>
              <div style={{ width: `${pct}%`, height: '100%', background: m.color, borderRadius: 4, transition: 'width 0.7s ease', opacity: 0.85 }} />
            </div>
          </div>
        )
      })}
      <p style={{ fontSize: '0.72rem', color: 'var(--text3)', marginTop: 2 }}>Bar shows % of typical daily max for reference</p>
    </div>
  )
}

// ── Water gauge ───────────────────────────────────────────────
function WaterGauge({ litres }) {
  const max = 5
  const pct = Math.min(100, (litres / max) * 100)
  const r = 36, cx = 48, cy = 48
  const circ = 2 * Math.PI * r
  const dash = (pct / 100) * circ

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="var(--border)" strokeWidth="8" />
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#3b82f6" strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`}
          style={{ transition: 'stroke-dasharray 0.8s ease' }}
        />
        <text x={cx} y={cy - 6} textAnchor="middle" style={{ fontSize: 16, fontWeight: 700, fill: '#3b82f6', fontFamily: 'Space Mono, monospace' }}>{litres}L</text>
        <text x={cx} y={cy + 10} textAnchor="middle" style={{ fontSize: 9, fill: 'var(--text3)', fontFamily: 'Space Grotesk, sans-serif', fontWeight: 600 }}>TARGET</text>
      </svg>
      <div>
        <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text2)', marginBottom: 4 }}>Daily water intake</div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text3)', lineHeight: 1.5 }}>
          {litres >= 3.5 ? 'High demand day — sip consistently' :
           litres >= 2.5 ? 'Moderate — stay topped up' :
           'Light day — easy to hit this target'}
        </div>
      </div>
    </div>
  )
}

// ── Main page ─────────────────────────────────────────────────
export default function CoachingPage({ token }) {
  const [weight, setWeight]       = useState('')
  const [minutes, setMinutes]     = useState('')
  const [city, setCity]           = useState('Perth')
  const [intensity, setIntensity] = useState('moderate')
  const [loading, setLoading]     = useState(false)
  const [summary, setSummary]     = useState(null)
  const [data, setData]           = useState(null)
  const [error, setError]         = useState(null)

  async function handleSubmit() {
    if (!weight || !minutes || !city) { setError('Please fill in all fields.'); return }
    setLoading(true); setSummary(null); setData(null); setError(null)
    const { data: res, error: err } = await getCoachingSummary(weight, minutes, city, intensity, token)
    setLoading(false)
    if (err) { setError(err); return }
    setSummary(res.coaching_summary)
    setData(res.data)
  }

  const temp     = data?.weather?.weather?.temperature_celsius
  const humidity = data?.weather?.weather?.relative_humidity_percent
  const litres   = data?.weather?.adjusted_daily_target_litres
  const sodium   = data?.sweat?.sodium_lost_mg
  const potassium= data?.sweat?.potassium_lost_mg
  const magnesium= data?.sweat?.magnesium_lost_mg

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">AI Coach — Gemini</div>
        <h1 className="hero-title">Your Coaching Summary</h1>
        <p className="hero-sub">Get a personalised hydration and recovery plan combining live weather, sweat loss, and water intake data.</p>
      </div>

      <div className="card">
        <div className="card-title"><span className="icon">✨</span>Workout Details</div>
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
        <div className="form-row">
          <div className="field">
            <label>City</label>
            <input type="text" placeholder="e.g. Perth" value={city} onChange={e => setCity(e.target.value)} />
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
        <button className="btn btn-primary btn-full" onClick={handleSubmit} disabled={loading}>
          {loading && <span className="spinner" />}
          {loading ? 'Asking Gemini…' : '✨ Get My Coaching Summary'}
        </button>
        {error && <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--danger)', padding: '0.6rem 0.85rem', background: '#d930250a', borderRadius: 'var(--radius-md)', border: '1px solid #d9302530' }}>{error}</div>}
      </div>

      {summary && (
        <div className="card">
          <div className="coaching-label" style={{ marginBottom: '0.6rem' }}>✨ Gemini's Coaching Advice</div>
          <p style={{ lineHeight: 1.8, fontSize: '0.92rem', color: 'var(--text)' }}>{summary}</p>
        </div>
      )}

      {data && (
        <>
          {/* Weather visual */}
          <div className="card">
            <div className="card-title"><span className="icon">🌡️</span>Live Weather — {city}</div>
            <WeatherCard city={city} temp={temp} humidity={humidity} />
          </div>

          {/* Water + minerals side by side */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div className="card" style={{ margin: 0 }}>
              <div className="card-title"><span className="icon">💧</span>Water Target</div>
              <WaterGauge litres={litres} />
            </div>
            <div className="card" style={{ margin: 0 }}>
              <div className="card-title"><span className="icon">🧂</span>Minerals Lost</div>
              <MineralChart sodium={sodium} potassium={potassium} magnesium={magnesium} />
            </div>
          </div>
        </>
      )}
    </>
  )
}
