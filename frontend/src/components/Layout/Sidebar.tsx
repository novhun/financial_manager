// src/components/Layout/Sidebar.tsx
import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  HomeIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  ClipboardListIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

interface SidebarProps {
  onClose?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const menuItems = [
    { path: '/', icon: HomeIcon, label: 'Dashboard' },
    { path: '/incomes', icon: CurrencyDollarIcon, label: 'Incomes' },
    { path: '/expenses', icon: CurrencyDollarIcon, label: 'Expenses' },
    { path: '/budgets', icon: ChartBarIcon, label: 'Budgets' },
    { path: '/projects', icon: ClipboardListIcon, label: 'Projects' },
    { path: '/analytics', icon: ChartBarIcon, label: 'Analytics' },
    { path: '/groups', icon: UserGroupIcon, label: 'Groups' },
    { path: '/types', icon: Cog6ToothIcon, label: 'Types Management' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="h-full flex flex-col bg-white shadow-lg">
      {/* Close button for mobile */}
      {onClose && (
        <div className="flex justify-end p-4 md:hidden">
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
      )}

      {/* User info */}
      <div className="px-4 py-6 border-b border-gray-200">
        <div className="flex items-center">
          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center">
            <span className="text-white font-semibold">
              {user?.username?.charAt(0).toUpperCase()}
            </span>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">{user?.username}</p>
            <p className="text-xs text-gray-500">{user?.email}</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                isActive
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
              onClick={onClose}
            >
              <Icon className="h-5 w-5 mr-3" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Logout button */}
      <div className="px-2 py-4 border-t border-gray-200">
        <button
          onClick={handleLogout}
          className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-md w-full"
        >
          <ArrowRightOnRectangleIcon className="h-5 w-5 mr-3" />
          Sign out
        </button>
      </div>
    </div>
  );
};

export default Sidebar;