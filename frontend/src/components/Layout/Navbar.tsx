// src/components/Layout/Navbar.tsx
import React from 'react';
import { Bars3Icon } from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';

interface NavbarProps {
  onMenuClick: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onMenuClick }) => {
  const { user } = useAuth();

  return (
    <header className="bg-white shadow-sm z-10">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center">
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            <Bars3Icon className="h-6 w-6" />
          </button>
          <h1 className="ml-2 text-xl font-semibold text-gray-900">Finance App</h1>
        </div>
        
        <div className="flex items-center">
          <div className="hidden md:flex items-center">
            <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center mr-2">
              <span className="text-white text-sm font-semibold">
                {user?.username?.charAt(0).toUpperCase()}
              </span>
            </div>
            <span className="text-sm text-gray-700">{user?.username}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;