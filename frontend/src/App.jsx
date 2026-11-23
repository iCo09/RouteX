import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import { checkHealth } from './services/api';
import { Bus, Database, Server, CheckCircle2, AlertCircle, RefreshCw, LogOut, X } from 'lucide-react';

function AppContent() {
  const { user, isAuthenticated, logout } = useAuth();
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'register'

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await checkHealth();
      setHealth(data);
    } catch (err) {
      setError(err.customMessage || 'Failed to connect to RouteX backend service');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-rose-600 rounded-lg text-white">
              <Bus className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white">RouteX</h1>
              <p className="text-xs text-slate-400">Next-Gen Bus Ticket Booking Platform</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <span className="hidden sm:inline-block text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              Milestone 2: Auth & RBAC
            </span>

            {/* Auth State Button / Profile */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5">
                <div className="flex items-center space-x-2">
                  <div className="w-6 h-6 rounded-full bg-rose-600 flex items-center justify-center text-xs font-bold text-white">
                    {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
                  </div>
                  <div className="text-left hidden sm:block">
                    <p className="text-xs font-semibold text-white leading-tight">{user?.full_name}</p>
                    <span className="text-[10px] text-rose-400 font-medium capitalize">{user?.role}</span>
                  </div>
                </div>
                <button
                  onClick={logout}
                  title="Sign Out"
                  className="text-slate-400 hover:text-rose-400 p-1 transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => {
                    setAuthMode('login');
                    setShowAuthModal(true);
                  }}
                  className="text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition"
                >
                  Sign In
                </button>
                <button
                  onClick={() => {
                    setAuthMode('register');
                    setShowAuthModal(true);
                  }}
                  className="text-xs font-medium bg-rose-600 hover:bg-rose-500 text-white px-3 py-1.5 rounded-lg transition shadow-md shadow-rose-950/50"
                >
                  Register
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-10 space-y-8">
        {/* Banner */}
        <section className="bg-gradient-to-r from-rose-950/40 via-slate-900 to-indigo-950/30 border border-slate-800 rounded-2xl p-6 sm:p-8">
          <div className="max-w-3xl space-y-3">
            <span className="text-rose-400 text-xs font-semibold uppercase tracking-wider">
              {isAuthenticated ? `Welcome back, ${user?.full_name}` : 'Milestone 2 Active'}
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              {isAuthenticated ? `Authenticated as ${user?.role?.toUpperCase()}` : 'Authentication & Role-Based Access Control'}
            </h2>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              {isAuthenticated
                ? `You are logged in with a cryptographically verified JWT Bearer token. Role-based privileges are active for ${user?.role} operations.`
                : 'JWT Authentication, Bcrypt password hashing, and Role-Based Access Control (Customer & Operator) are operational. Test registration and login above.'}
            </p>
          </div>
        </section>

        {/* System Health Check Panel */}
        <section className="bg-slate-950 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <Server className="w-5 h-5 text-indigo-400" />
              <h3 className="font-semibold text-lg text-white">System Connectivity & Health</h3>
            </div>
            <button
              onClick={fetchHealth}
              disabled={loading}
              className="flex items-center space-x-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-md border border-slate-700 transition"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Refresh Status</span>
            </button>
          </div>

          {loading ? (
            <div className="py-8 text-center text-slate-400 text-sm">
              Checking backend and database status...
            </div>
          ) : error ? (
            <div className="p-4 bg-rose-950/40 border border-rose-800/50 rounded-lg flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-rose-300">Connection Error</p>
                <p className="text-xs text-rose-400/90 mt-1">{error}</p>
                <p className="text-xs text-slate-400 mt-2">
                  Make sure the FastAPI backend is running (<code className="text-slate-300">uvicorn app.main:app --reload</code>).
                </p>
              </div>
            </div>
          ) : health ? (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-slate-400 uppercase tracking-wide">API Gateway</span>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                </div>
                <div className="text-base font-semibold text-white capitalize">{health.status}</div>
                <div className="text-xs text-slate-400 mt-1">{health.app} (v{health.version})</div>
              </div>

              <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-slate-400 uppercase tracking-wide">Database</span>
                  <Database className="w-4 h-4 text-emerald-400" />
                </div>
                <div className="text-base font-semibold text-emerald-400 capitalize">{health.database}</div>
                <div className="text-xs text-slate-400 mt-1">PostgreSQL 16 Async Connection</div>
              </div>

              <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-slate-400 uppercase tracking-wide">Auth Service</span>
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                </div>
                <div className="text-base font-semibold text-white">Active</div>
                <div className="text-xs text-slate-400 mt-1">JWT + Bcrypt RBAC Ready</div>
              </div>
            </div>
          ) : null}
        </section>

        {/* Development Roadmap */}
        <section className="space-y-4">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
            Development Roadmap
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-5 bg-slate-950 border border-rose-500/30 rounded-xl space-y-2">
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Milestone 2 - Ready
              </span>
              <h4 className="font-semibold text-white">Auth & RBAC</h4>
              <p className="text-xs text-slate-400">
                User registration, password hashing (Bcrypt), JWT access/refresh tokens, and roles (Customer, Operator, Admin).
              </p>
            </div>

            <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Milestone 3 (Next)
              </span>
              <h4 className="font-semibold text-white">Fleet & Trip Scheduling</h4>
              <p className="text-xs text-slate-400">
                Operator bus management, customizable seat layouts (sleeper/seater), routes with intermediate stops, and calendar schedules.
              </p>
            </div>

            <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Milestone 4 & Beyond
              </span>
              <h4 className="font-semibold text-white">Booking & Redis Locks</h4>
              <p className="text-xs text-slate-400">
                Atomic seat locks, Razorpay gateway integration, Celery notification reminders, and WebSockets live trip chat.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Minimal Auth Modal */}
      {showAuthModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="relative w-full max-w-md">
            <button
              onClick={() => setShowAuthModal(false)}
              className="absolute right-4 top-4 text-slate-400 hover:text-white p-1 z-10"
            >
              <X className="w-5 h-5" />
            </button>
            {authMode === 'login' ? (
              <Login
                onSwitchToRegister={() => setAuthMode('register')}
                onSuccess={() => setShowAuthModal(false)}
              />
            ) : (
              <Register
                onSwitchToLogin={() => setAuthMode('login')}
                onSuccess={() => setShowAuthModal(false)}
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
