import { useState } from 'react'
import AuthPage from './pages/AuthPage'
import WaterIntakePage from './pages/WaterIntakePage'
import SweatLossPage from './pages/SweatLossPage'
import WeatherHydrationPage from './pages/WeatherHydrationPage'
import CoachingPage from './pages/CoachingPage'

const TABS = [
  { id: 'water',    label: '💧 Water' },
  { id: 'sweat',    label: '🧂 Sweat' },
  { id: 'weather',  label: '🌡️ Weather' },
  { id: 'coaching', label: '✨ AI Coach' },
]

export default function App() {
  const [user, setUser] = useState(null)
  const [tab, setTab]   = useState('water')

  function handleLogin(username, token) { setUser({ username, token }) }
  function handleLogout() { setUser(null); setTab('water') }

  return (
    <div className="app-shell">
      <nav className="nav">
        <div className="nav-logo">
          <span className="nav-logo-dot" />
          FitHydrate
        </div>

        {user && (
          <div className="nav-tabs">
            {TABS.map(t => (
              <button
                key={t.id}
                className={`nav-tab ${tab === t.id ? 'active' : ''}`}
                onClick={() => setTab(t.id)}
              >
                {t.label}
              </button>
            ))}
          </div>
        )}

        <div className="nav-auth">
          {user ? (
            <>
              <span className="user-chip">✓ {user.username}</span>
              <button className="btn btn-ghost" style={{ fontSize: '0.78rem', padding: '0.3rem 0.75rem' }} onClick={handleLogout}>
                Log out
              </button>
            </>
          ) : (
            <span style={{ fontSize: '0.78rem', color: 'var(--text3)' }}>Sign in to continue</span>
          )}
        </div>
      </nav>

      <main className="main-content">
        {!user ? (
          <AuthPage onLogin={handleLogin} />
        ) : (
          <>
            {tab === 'water'    && <WaterIntakePage token={user.token} />}
            {tab === 'sweat'    && <SweatLossPage   token={user.token} />}
            {tab === 'weather'  && <WeatherHydrationPage token={user.token} />}
            {tab === 'coaching' && <CoachingPage token={user.token} />}
          </>
        )}
      </main>
    </div>
  )
}
