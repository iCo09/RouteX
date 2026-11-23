import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Lock, Phone, UserCheck, AlertCircle } from 'lucide-react';

export default function Register({ onSwitchToLogin, onSuccess }) {
  const { register, login } = useAuth();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await register({
        full_name: fullName,
        email,
        phone_number: phone || null,
        password,
        role,
      });
      // Automatically log in upon successful registration
      await login(email, password);
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.customMessage || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 max-w-md w-full mx-auto shadow-2xl">
      <h2 className="text-xl font-bold text-white mb-1">Create Account</h2>
      <p className="text-xs text-slate-400 mb-4">Join RouteX as a traveler or bus operator</p>

      {error && (
        <div className="mb-4 p-3 bg-rose-950/40 border border-rose-800/60 rounded-lg flex items-center space-x-2 text-rose-300 text-xs">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Role Picker */}
      <div className="grid grid-cols-2 gap-2 p-1 bg-slate-900 rounded-lg mb-3">
        <button
          type="button"
          onClick={() => setRole('customer')}
          className={`py-1.5 text-xs font-semibold rounded-md transition ${
            role === 'customer' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-white'
          }`}
        >
          Customer
        </button>
        <button
          type="button"
          onClick={() => setRole('operator')}
          className={`py-1.5 text-xs font-semibold rounded-md transition ${
            role === 'operator' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-white'
          }`}
        >
          Bus Operator
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Full Name</label>
          <div className="relative">
            <User className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Your Name"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Email</label>
          <div className="relative">
            <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Phone Number (Optional)</label>
          <div className="relative">
            <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+91 98765 43210"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Password</label>
          <div className="relative">
            <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Min 8 chars"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full mt-2 flex items-center justify-center space-x-2 bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white font-medium py-2 rounded-lg text-sm transition"
        >
          <UserCheck className="w-4 h-4" />
          <span>{loading ? 'Creating...' : `Register as ${role}`}</span>
        </button>
      </form>

      <div className="mt-4 pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
        Already registered?{' '}
        <button onClick={onSwitchToLogin} className="text-rose-400 hover:underline font-medium">
          Sign In
        </button>
      </div>
    </div>
  );
}
