import React, { useState } from 'react';
import { Menu, Search, Bell, MessageCircle, ChevronDown } from 'lucide-react';

const Header = () => {
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isMessagesOpen, setIsMessagesOpen] = useState(false);

  const notifications = [
    { id: 1, message: "New project assigned to you", time: "2 minutes ago", unread: true },
    { id: 2, message: "Meeting scheduled for tomorrow", time: "1 hour ago", unread: true },
    { id: 3, message: "Your report has been approved", time: "3 hours ago", unread: false }
  ];

  const messages = [
    { id: 1, sender: "Jane Smith", message: "Can we discuss the project?", time: "5 min ago", avatar: "J" },
    { id: 2, sender: "Mike Johnson", message: "Great work on the presentation!", time: "1 hour ago", avatar: "M" },
    { id: 3, sender: "Sarah Wilson", message: "Meeting rescheduled to 3 PM", time: "2 hours ago", avatar: "S" }
  ];

  return (
    <header className="bg-white border-b border-gray-200  flex items-center justify-between relative w-full">
      {/* Left side - Menu and Search */}
      <div className="flex items-center space-x-4">
        {/* Hamburger Menu */}
        <button className="p-2 hover:bg-gray-100 rounded-md transition-colors">
          <Menu size={20} className="text-gray-600" />
        </button>
        
        {/* Search */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={16} className="text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search..."
            className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
          />
        </div>
      </div>

      {/* Right side - Notifications and Profile */}
      <div className="flex items-center space-x-2">
        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => {
              setIsNotificationsOpen(!isNotificationsOpen);
              setIsMessagesOpen(false);
              setIsProfileDropdownOpen(false);
            }}
            className="p-2 hover:bg-gray-100 rounded-md transition-colors relative"
          >
            <Bell size={20} className="text-gray-600" />
            {/* Notification badge */}
            <span className="absolute -top-1 -right-1 bg-pink-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
              2
            </span>
          </button>
          
          {/* Notifications Dropdown */}
          {isNotificationsOpen && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
              <div className="p-4 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">Notifications</h3>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {notifications.map((notification) => (
                  <div key={notification.id} className="p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0">
                    <div className="flex items-start space-x-3">
                      <div className={`w-2 h-2 rounded-full mt-2 ${notification.unread ? 'bg-blue-500' : 'bg-gray-300'}`} />
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-4 border-t border-gray-200">
                <button className="text-sm text-blue-600 hover:text-blue-800">View all notifications</button>
              </div>
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="relative">
          <button
            onClick={() => {
              setIsMessagesOpen(!isMessagesOpen);
              setIsNotificationsOpen(false);
              setIsProfileDropdownOpen(false);
            }}
            className="p-2 hover:bg-gray-100 rounded-md transition-colors relative"
          >
            <MessageCircle size={20} className="text-gray-600" />
            {/* Message badge */}
            <span className="absolute -top-1 -right-1 bg-pink-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
              3
            </span>
          </button>
          
          {/* Messages Dropdown */}
          {isMessagesOpen && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
              <div className="p-4 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">Messages</h3>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {messages.map((message) => (
                  <div key={message.id} className="p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm font-medium">{message.avatar}</span>
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{message.sender}</p>
                        <p className="text-sm text-gray-600 mt-1">{message.message}</p>
                        <p className="text-xs text-gray-500 mt-1">{message.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-4 border-t border-gray-200">
                <button className="text-sm text-blue-600 hover:text-blue-800">View all messages</button>
              </div>
            </div>
          )}
        </div>

        {/* Profile */}
        <div className="relative">
          <button
            onClick={() => {
              setIsProfileDropdownOpen(!isProfileDropdownOpen);
              setIsNotificationsOpen(false);
              setIsMessagesOpen(false);
            }}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-md transition-colors"
          >
            <div className="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center">
              <img
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                alt="Profile"
                className="w-8 h-8 rounded-full object-cover"
              />
            </div>
            <span className="text-sm font-medium text-gray-700">John Doe</span>
            <ChevronDown size={16} className="text-gray-500" />
          </button>
          
          {/* Profile Dropdown */}
          {isProfileDropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
              <div className="p-4 border-b border-gray-200">
                <p className="text-sm font-medium text-gray-900">John Doe</p>
                <p className="text-xs text-gray-500">john.doe@example.com</p>
              </div>
              <div className="py-2">
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Your Profile
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Settings
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Team
                </button>
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Billing
                </button>
              </div>
              <div className="border-t border-gray-200 py-2">
                <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  Sign out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Overlay to close dropdowns when clicking outside */}
      {(isProfileDropdownOpen || isNotificationsOpen || isMessagesOpen) && (
        <div 
          className="fixed inset-0 z-40"
          onClick={() => {
            setIsProfileDropdownOpen(false);
            setIsNotificationsOpen(false);
            setIsMessagesOpen(false);
          }}
        />
      )}
    </header>
  );
};

export default Header;