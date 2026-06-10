import { useState } from 'react'
import { register, login } from '../api'

export default function AuthPage({ onLogin }) {
  const [mode, setMode]         = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)
  const [success, setSuccess]   = useState(null)

  async function handleSubmit() {
    if (!username || !password) { setError('Please fill in both fields.'); return }
    setLoading(true); setError(null); setSuccess(null)

    if (mode === 'register') {
      const { data, error: err } = await register(username, password)
      setLoading(false)
      if (err) { setError(err); return }
      setSuccess('Account created! Logging you in…')
      setTimeout(() => { setMode('login'); setSuccess(null) }, 1200)
    } else {
      const { data, error: err } = await login(username, password)
      setLoading(false)
      if (err) { setError(err); return }
      onLogin(username, data?.access_token || data?.token || JSON.stringify(data))
    }
  }

  return (
    <div className="auth-wrap">
      <div className="hero">
        <div className="hero-eyebrow">{mode === 'login' ? 'Welcome back' : 'Get started'}</div>
        <h1 className="hero-title">{mode === 'login' ? 'Log in to FitHydrate' : 'Create your account'}</h1>
        <p className="hero-sub">Your personal AI-powered hydration coach.</p>
      </div>

      <div className="auth-toggle">
        <button className={mode === 'login' ? 'active' : ''} onClick={() => { setMode('login'); setError(null) }}>Log in</button>
        <button className={mode === 'register' ? 'active' : ''} onClick={() => { setMode('register'); setError(null) }}>Register</button>
      </div>

      <div className="card">
        <div className="form-row full">
          <div className="field">
            <label>Username</label>
            <input type="text" placeholder="e.g. taka" value={username} onChange={e => setUsername(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSubmit()} />
          </div>
          <div className="field" style={{ marginTop: '0.75rem' }}>
            <label>Password</label>
            <input type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSubmit()} />
          </div>
        </div>

        {error && <div style={{ fontSize: '0.82rem', color: 'var(--danger)', marginBottom: '0.75rem', padding: '0.6rem 0.85rem', background: '#ff525210', borderRadius: 'var(--radius-md)', border: '1px solid #ff525230' }}>{error}</div>}
        {success && <div style={{ fontSize: '0.82rem', color: 'var(--accent)', marginBottom: '0.75rem', padding: '0.6rem 0.85rem', background: 'var(--accent-dim)', borderRadius: 'var(--radius-md)', border: '1px solid var(--accent-glow)' }}>{success}</div>}

        <button className="btn btn-primary btn-full" onClick={handleSubmit} disabled={loading}>
          {loading && <span className="spinner" />}
          {mode === 'login' ? 'Log in' : 'Create account'}
        </button>
      </div>
    </div>
  )
}
