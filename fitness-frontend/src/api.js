// ── All API calls live here ──────────────────────────────────
// Change this if you ever redeploy to a different URL
const BASE_URL = 'https://fitness-mcp-6vuf.onrender.com'

// Helper: wraps fetch and returns { data, error }
// Pass a JWT token string to send it as a Bearer header
async function call(endpoint, options = {}, token = null) {
  try {
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const res = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })
    const json = await res.json()
    if (!res.ok) {
      // FastAPI error shapes: { detail: "..." } or { error: "..." }
      const msg = json?.detail || json?.error || `HTTP ${res.status}`
      return { data: null, error: msg }
    }
    return { data: json, error: null }
  } catch (err) {
    return { data: null, error: err.message }
  }
}

// ── Auth (no token needed) ────────────────────────────────────
export async function register(username, password) {
  return call('/register', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function login(username, password) {
  return call('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

// ── Tools (token sent in Authorization header) ────────────────
export async function calculateWaterIntake(weight_kg, workout_minutes, token) {
  return call(
    `/calculate-water-intake?weight_kg=${weight_kg}&workout_minutes=${workout_minutes}`,
    { method: 'POST' },
    token
  )
}

export async function estimateSweatLoss(workout_duration_min, intensity_level, token) {
  return call(
    `/estimate-sweat-loss?workout_duration_min=${workout_duration_min}&intensity_level=${intensity_level}`,
    { method: 'POST' },
    token
  )
}

export async function estimateSweatLossV2(workout_duration_min, intensity_level, token) {
  return call(
    `/estimate-sweat-loss-v2?workout_duration_min=${workout_duration_min}&intensity_level=${intensity_level}`,
    { method: 'POST' },
    token
  )
}

export async function weatherAdjustedHydration(weight_kg, workout_minutes, city, token) {
  return call(
    `/weather-adjusted-hydration?weight_kg=${weight_kg}&workout_minutes=${workout_minutes}&city=${encodeURIComponent(city)}`,
    { method: 'POST' },
    token
  )
}

export async function getCoachingSummary(weight_kg, workout_minutes, city, intensity_level, token) {
  return call(
    `/ai-coaching-summary?weight_kg=${weight_kg}&workout_minutes=${workout_minutes}&city=${encodeURIComponent(city)}&intensity_level=${intensity_level}`,
    { method: 'POST' },
    token
  )
}
