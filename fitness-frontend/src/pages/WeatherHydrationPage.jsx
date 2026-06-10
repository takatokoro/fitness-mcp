import { useState } from 'react'
import { weatherAdjustedHydration } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

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

  const litres = result?.adjusted_daily_target_litres ?? result?.total_daily_target_litres ?? null
  const temp   = result?.temperature_celsius ?? result?.weather?.temperature_celsius ?? null

  return (
    <>
      <div className="hero">
        <div className="hero-eyebrow">Tool 3 — Live Weather</div>
        <h1 className="hero-title">Weather-Adjusted Hydration</h1>
        <p className="hero-sub">Hydration targets change with the heat. This tool fetches live weather for your city and adjusts your recommendation automatically.</p>
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

        {(litres || temp) && !loading && (
          <div className="metrics-grid">
            {litres !== null && <div className="metric-tile"><div className="metric-value">{litres}L</div><div className="metric-label">Adjusted target</div></div>}
            {temp   !== null && <div className="metric-tile"><div className="metric-value">{temp}°C</div><div className="metric-label">Live temp</div></div>}
          </div>
        )}

        <ResultBox result={result} error={error} loading={loading} />

        <CoachingSummary
          toolData={result}
          token={token}
          context={{ weight_kg: weight, workout_minutes: minutes, city }}
        />
      </div>
    </>
  )
}
