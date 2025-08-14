'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, LoginData, RegisterData, AuthResponse, ApiErrorResponse } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: LoginData) => Promise<boolean>;
  register: (data: RegisterData) => Promise<boolean>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        
        if (token && userData) {
          try {
            setUser(JSON.parse(userData));
            // Verify token is still valid
            await api.get('/auth/profile/');
          } catch {
            // Token is invalid, clear storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            setUser(null);
          }
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (data: LoginData): Promise<boolean> => {
    try {
      // Generate device fingerprint
      const deviceFingerprint = generateDeviceFingerprint();
      
      const response = await api.post<AuthResponse>('/auth/login/', {
        ...data,
        device_fingerprint: deviceFingerprint,
      });

      const { access_token, refresh_token, user: userData } = response.data;

      // Store tokens and user data
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('user_data', JSON.stringify(userData));
      }

      setUser(userData);
      toast.success('Login successful!');
      return true;
    } catch (error: unknown) {
      const apiError = error as ApiErrorResponse;
      const errorMessage = apiError.response?.data?.error || 'Login failed';
      toast.error(errorMessage);
      return false;
    }
  };

  const register = async (data: RegisterData): Promise<boolean> => {
    try {
      await api.post('/auth/register/', data);
      toast.success('Registration successful! Please wait for admin approval.');
      return true;
    } catch (error: unknown) {
      const apiError = error as ApiErrorResponse;
      const errorMessage = apiError.response?.data?.message || 'Registration failed';
      toast.error(errorMessage);
      return false;
    }
  };

  const logout = () => {
    // Send logout request to backend
    if (typeof window !== 'undefined') {
      const deviceFingerprint = generateDeviceFingerprint();
      api.post('/auth/logout/', { device_fingerprint: deviceFingerprint }).catch(() => {
        // Ignore errors on logout
      });

      // Clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_data');
    }

    setUser(null);
    toast.success('Logged out successfully');
  };

  const updateProfile = async (data: Partial<User>): Promise<boolean> => {
    try {
      const response = await api.patch<User>('/auth/profile/', data);
      const updatedUser = response.data;
      
      setUser(updatedUser);
      if (typeof window !== 'undefined') {
        localStorage.setItem('user_data', JSON.stringify(updatedUser));
      }
      toast.success('Profile updated successfully!');
      return true;
    } catch (error: unknown) {
      const apiError = error as ApiErrorResponse;
      const errorMessage = apiError.response?.data?.message || 'Profile update failed';
      toast.error(errorMessage);
      return false;
    }
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Helper function to generate device fingerprint
function generateDeviceFingerprint(): string {
  if (typeof window === 'undefined') {
    return 'server-side-render';
  }
  
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (ctx) {
    ctx.textBaseline = 'top';
    ctx.font = '14px Arial';
    ctx.fillText('Device fingerprint', 2, 2);
  }
  
  const fingerprint = [
    navigator.userAgent,
    navigator.language,
    screen.width + 'x' + screen.height,
    Intl.DateTimeFormat().resolvedOptions().timeZone,
    canvas.toDataURL(),
  ].join('|');
  
  // Simple hash function
  let hash = 0;
  for (let i = 0; i < fingerprint.length; i++) {
    const char = fingerprint.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  
  return hash.toString(36);
}