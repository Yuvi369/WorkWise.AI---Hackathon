import React from 'react';
import { MessageCircle, FileText, Users } from 'lucide-react';

const Header = ({ activeTab, setActiveTab }) => (
  <div className="relative z-10 px-6 py-4 backdrop-blur-sm bg-white/5 border-b border-white/10">
    <div className="max-w-7xl mx-auto flex items-center justify-between">
      <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
        Task Assignment Dashboard
      </h1>
      <nav className="flex space-x-4">
        <a
          href="#reports"
          onClick={(e) => { e.preventDefault(); setActiveTab('reports'); }}
          className={`py-3 px-6 font-semibold transition-all duration-300 text-gray-300 hover:text-white ${
            activeTab === 'reports' ? 'border-b-2 border-teal-400 text-white' : 'hover:border-b-2 hover:border-purple-400'
          }`}
        >
          <MessageCircle className="w-5 h-5 inline mr-2" />
          Reports
        </a>
        <a
          href="#tickets"
          onClick={(e) => { e.preventDefault(); setActiveTab('tickets'); }}
          className={`py-3 px-6 font-semibold transition-all duration-300 text-gray-300 hover:text-white ${
            activeTab === 'tickets' ? 'border-b-2 border-teal-400 text-white' : 'hover:border-b-2 hover:border-purple-400'
          }`}
        >
          <FileText className="w-5 h-5 inline mr-2" />
          Tickets
        </a>
        <a
          href="#team"
          onClick={(e) => { e.preventDefault(); setActiveTab('team'); }}
          className={`py-3 px-6 font-semibold transition-all duration-300 text-gray-300 hover:text-white ${
            activeTab === 'team' ? 'border-b-2 border-teal-400 text-white' : 'hover:border-b-2 hover:border-purple-400'
          }`}
        >
          <Users className="w-5 h-5 inline mr-2" />
          Team
        </a>
      </nav>
    </div>
  </div>
);

export default Header;