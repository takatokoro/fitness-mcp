import { useState } from 'react'
import { calculateWaterIntake } from '../api'
import ResultBox from '../components/ResultBox'
import CoachingSummary from '../components/CoachingSummary'

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

        {litres && !loading && (
          <div className="metrics-grid">
            <div className="metric-tile">
              <div className="metric-value">{litres}L</div>
              <div className="metric-label">Daily target</div>
            </div>
          </div>
        )}

        <ResultBox result={result} error={error} loading={loading} />

        <CoachingSummary
          toolData={result}
          token={token}
          context={{ weight_kg: weight, workout_minutes: minutes }}
        />
      </div>
    </>
  )
}
