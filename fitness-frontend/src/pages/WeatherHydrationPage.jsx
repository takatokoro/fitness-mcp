import { useState } from 'react'
import { weatherAdjustedHydration } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

// ── Weather sky card ──────────────────────────────────────────
function WeatherCard({ city, temp, humidity }) {
  const t = parseFloat(temp)
  const isHot  = t >= 30
  const isWarm = t >= 20 && t < 30
  const isCool = t >= 10 && t < 20
  const textDark = isHot || isWarm

  const skyBg   = isHot  ? 'linear-gradient(160deg,#fde68a,#fbbf24)'
                : isWarm ? 'linear-gradient(160deg,#bae6fd,#38bdf8)'
                : isCool ? 'linear-gradient(160deg,#dbeafe,#93c5fd)'
                :          'linear-gradient(160deg,#e0e7ef,#94a3b8)'

  const sunColor   = isHot ? '#f59e0b' : '#facc15'
  const tempLabel  = isHot ? 'Hot' : isWarm ? 'Warm' : isCool ? 'Cool' : 'Cold'
  const humidColor = humidity >= 70 ? '#0369a1' : humidity >= 50 ? '#0284c7' : '#7dd3fc'

  const now = new Date()
  const dateStr = now.toLocaleDateString('en-AU', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  const timeStr = now.toLocaleTimeString('en-AU', { hour: '2-digit', minute: '2-digit', hour12: true })

  return (
    <div style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden', border: '1px solid var(--border)' }}>
      <div style={{ background: skyBg, padding: '1.25rem 1.5rem 1rem', position: 'relative', minHeight: 110 }}>
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
        <div style={{ fontSize: '0.68rem', fontWeight: 600, color: textDark ? '#92400e' : '#1e40af', opacity: 0.8, marginBottom: 5 }}>{dateStr} · {timeStr}</div>
        <div style={{ color: textDark ? '#78350f' : '#1e3a5f', fontWeight: 700, fontSize: '0.8rem', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 2 }}>{city}</div>
        <div style={{ color: textDark ? '#92400e' : '#1e3a5f', fontSize: '2.6rem', fontWeight: 700, lineHeight: 1, letterSpacing: '-0.04em', fontFamily: 'Space Mono, monospace' }}>{temp}°C</div>
        <div style={{ color: textDark ? '#a16207' : '#2563eb', fontSize: '0.78rem', fontWeight: 600, marginTop: 3 }}>{tempLabel}</div>
      </div>
      <div style={{ background: 'var(--surface)', display: 'grid', gridTemplateColumns: '1fr 1fr', borderTop: '1px solid var(--border)' }}>
        <div style={{ padding: '0.85rem 1.1rem', borderRight: '1px solid var(--border)' }}>
          <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 5 }}>Humidity</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ flex: 1, height: 6, background: 'var(--bg)', borderRadius: 3, overflow: 'hidden' }}>
              <div style={{ width: `${humidity}%`, height: '100%', background: humidColor, borderRadius: 3, transition: 'width 0.6s ease' }} />
            </div>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: humidColor, fontFamily: 'Space Mono, monospace', minWidth: 36 }}>{humidity}%</span>
          </div>
        </div>
        <div style={{ padding: '0.85rem 1.1rem' }}>
          <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 5 }}>Conditions</div>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text2)' }}>
            {humidity >= 70 ? '💧 High humidity' : humidity >= 50 ? '🌤 Moderate' : '☀️ Dry & clear'}
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Hydration adjustment visual ───────────────────────────────
function HydrationAdjustment({ result }) {
  const base      = result?.base_total_litres ?? result?.base_intake_litres ?? null
  const heatAdj   = result?.heat_adjustment_litres ?? 0
  const humidAdj  = result?.humidity_adjustment_litres ?? 0
  const total     = result?.adjusted_daily_target_litres ?? null
  if (!total) return null

  const items = [
    { label: 'Base intake', value: base, color: '#7dd3fc' },
    { label: 'Heat adjustment', value: heatAdj, color: '#f97316' },
    { label: 'Humidity adjustment', value: humidAdj, color: '#0284c7' },
  ].filter(i => i.value > 0)

  return (
    <div style={{ marginTop: '1.25rem' }}>
      <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 10 }}>How your target was calculated</div>

      {items.map((item, i) => (
        <div key={item.label} style={{ marginBottom: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text2)' }}>{item.label}</span>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: item.color, fontFamily: 'Space Mono, monospace' }}>+{item.value}L</span>
          </div>
          <div style={{ height: 7, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden', border: '1px solid var(--border)' }}>
            <div style={{ width: `${(item.value / total) * 100}%`, height: '100%', background: item.color, borderRadius: 4, transition: 'width 0.8s ease' }} />
          </div>
        </div>
      ))}

      <div style={{ marginTop: 12, padding: '0.75rem 1rem', background: '#f0fdf4', borderRadius: 'var(--radius-md)', border: '1px solid #86efac', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#15803d' }}>Total adjusted target</span>
        <span style={{ fontSize: '1.3rem', fontWeight: 700, color: '#15803d', fontFamily: 'Space Mono, monospace' }}>{total}L</span>
      </div>

      <p style={{ fontSize: '0.72rem', color: 'var(--text3)', marginTop: 8 }}>
        {result?.recommendation ?? ''}
      </p>
    </div>
  )
}

export default function WeatherHydrationPage({ token }) {
  const [weight, setWeight]   = useState('')
  const [minutes, setMinutes] = useState('')
  const [city, setCity]       = useState('Perth')
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  async function handleCalculate() {
    if (!weight || !minutes || !city) { setError('Please fill in all fields.'); return }
    setLoading(true); setResult(null); setError(null)
    const { data, error: err } = await weatherAdjustedHydration(weight, minutes, city, token)
    setLoading(false)
    if (err) { setError(err); return }
    setResult(data)
  }

  const temp     = result?.weather?.temperature_celsius
  const humidity = result?.weather?.relative_humidity_percent
  const hasResult = result !== null

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">Tool 3 — Live Weather</div>
        <h1 className="hero-title">Weather-Adjusted Hydration</h1>
        <p className="hero-sub">Hydration targets change with the heat. Fetches live weather for your city and adjusts your recommendation automatically.</p>
      </div>

      <div className="card">
        <div className="card-title"><span className="icon">🌡️</span>Your Workout + Location</div>
        <div className="form-row three">
          <div className="field">
            <label>Body Weight (kg)</label>
            <input type="number" placeholder="e.g. 75" value={weight} onChange={e => setWeight(e.target.value)} min="20" max="300" />
          </div>
          <div className="field">
            <label>Workout (min)</label>
            <input type="number" placeholder="e.g. 60" value={minutes} onChange={e => setMinutes(e.target.value)} min="0" max="480" />
          </div>
          <div className="field">
            <label>City</label>
            <input type="text" placeholder="e.g. Perth" value={city} onChange={e => setCity(e.target.value)} />
          </div>
        </div>
        <button className="btn btn-primary" onClick={handleCalculate} disabled={loading}>
          {loading && <span className="spinner" />}
          Get Weather-Adjusted Target
        </button>
        {error && <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--danger)', padding: '0.6rem', background: '#d930250a', borderRadius: 'var(--radius-md)', border: '1px solid #d9302530' }}>{error}</div>}
      </div>

      {hasResult && !loading && temp !== undefined && (
        <div className="card">
          <div className="card-title"><span className="icon">🌡️</span>Live Weather — {city}</div>
          <WeatherCard city={city} temp={temp} humidity={humidity} />
          <HydrationAdjustment result={result} />
        </div>
      )}

      {result && !loading && (
        <div className="card">
          <div className="card-title"><span className="icon">📋</span>Full Response</div>
          <ResultBox result={result} error={null} loading={false} />
          <CoachingSummary toolData={result} token={token} context={{ weight_kg: weight, workout_minutes: minutes, city }} />
        </div>
      )}
    </>
  )
}
