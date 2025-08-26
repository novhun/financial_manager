import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';
import { User, LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (data: LoginForm) => Promise<{ success: boolean; message?: string }>;
  register: (data: RegisterForm) => Promise<{ success: boolean; message?: string }>;
  forgetPassword: (data: ForgetPasswordForm) => Promise<{ success: boolean; message?: string }>;
  resetPassword: (data: ResetPasswordForm) => Promise<{ success: boolean; message?: string }>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (data: LoginForm): Promise<{ success: boolean; message?: string }> => {
    try {
      const response = await authAPI.login(data);
      setToken(response.access_token);
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const register = async (data: RegisterForm): Promise<{ success: boolean; message?: string }> => {
    try {
      await authAPI.register(data);
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Registration failed' 
      };
    }
  };

  const forgetPassword = async (data: ForgetPasswordForm): Promise<{ success: boolean; message?: string }> => {
    try {
      await authAPI.forgetPassword(data);
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Password reset request failed' 
      };
    }
  };

  const resetPassword = async (data: ResetPasswordForm): Promise<{ success: boolean; message?: string }> => {
    try {
      await authAPI.resetPassword(data);
      return { success: true };
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Password reset failed' 
      };
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    forgetPassword,
    resetPassword,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};