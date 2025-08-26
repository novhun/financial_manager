// src/components/Layout/BottomMenu.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  ClipboardListIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';

const BottomMenu: React.FC = () => {
  const location = useLocation();
  
  const menuItems = [
    { path: '/', icon: HomeIcon, label: 'Dashboard' },
    { path: '/incomes', icon: CurrencyDollarIcon, label: 'Finance' },
    { path: '/projects', icon: ClipboardListIcon, label: 'Projects' },
    { path: '/analytics', icon: ChartBarIcon, label: 'Analytics' },
    { path: '/groups', icon: UserGroupIcon, label: 'Groups' },
  ];

  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-30">
      <div className="flex justify-around">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center py-2 px-3 ${isActive ? 'text-blue-600' : 'text-gray-600'}`}
            >
              <Icon className="h-6 w-6" />
              <span className="text-xs mt-1">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default BottomMenu;