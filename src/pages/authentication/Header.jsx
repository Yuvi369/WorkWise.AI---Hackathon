import React from 'react';
import { Brain, User, Bell, Settings } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 shadow-sm sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-indigo-600 to-cyan-600 rounded-xl flex items-center justify-center shadow-lg">
              <Brain className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-cyan-600 bg-clip-text text-transparent">
                WorkWise.AI
              </h1>
              <p className="text-sm text-gray-600">Intelligent Task Assignment</p>
            </div>
          </div>

          {/* Navigation and Actions */}
          <div className="flex items-center space-x-6">
            {/* Quick Stats */}
            <div className="hidden md:flex items-center space-x-4">
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-800">4</p>
                <p className="text-xs text-gray-500">Pending</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-800">6</p>
                <p className="text-xs text-gray-500">Team</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-3">
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors relative">
                <Bell className="w-5 h-5 text-gray-600" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Settings className="w-5 h-5 text-gray-600" />
              </button>
            </div>

            {/* User Profile */}
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-800">Welcome back, Manager</p>
                <p className="text-xs text-gray-500">Last login: Today, 9:30 AM</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-r from-indigo-600 to-cyan-600 rounded-full flex items-center justify-center shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                <User className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;