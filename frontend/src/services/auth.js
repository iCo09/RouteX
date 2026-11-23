import { apiClient } from './api';

export const authService = {
  // 1. Register a new user (Customer or Operator)
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  // 2. Authenticate user and persist credentials
  async login(email, password) {
    const response = await apiClient.post('/auth/login', { email, password });
    const { access_token, refresh_token, user } = response.data;
    
    // Store tokens and basic user profile in browser local storage
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { token: access_token, user };
  },

  // 3. Fetch latest profile using the current Bearer token
  async getMe() {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // 4. Clear storage on logout
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Helper to read cached user on app load
  getStoredUser() {
    const userStr = localStorage.getItem('user');
    try {
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  },

  // Helper to check if a session exists
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },
};
