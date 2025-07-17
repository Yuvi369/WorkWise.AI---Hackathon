import React from 'react';
import { AlertCircle, Clock, Bot } from 'lucide-react';

const Tickets = ({ unassignedTickets, handleAIAssist, getPriorityColor }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
        Unassigned Tickets
      </h2>
      <div className="text-sm text-gray-300">{unassignedTickets.length} tickets pending assignment</div>
    </div>
    {unassignedTickets.length === 0 ? (
      <div className="text-center py-12">
        <CheckCircle className="w-16 h-16 text-teal-400 mx-auto mb-4" />
        <p className="text-xl font-semibold text-white">All tickets assigned!</p>
        <p className="text-gray-300">Great job managing your team's workload.</p>
      </div>
    ) : (
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {unassignedTickets.map((ticket) => (
          <div
            key={ticket.id}
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/10 shadow-sm hover:shadow-lg transition-all duration-300 hover:transform hover:scale-105"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-teal-500 rounded-lg flex items-center justify-center">
                  <span className="text-sm font-bold text-white">{ticket.code.slice(-2)}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-white">{ticket.code}</h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getPriorityColor(ticket.priority)}`}>
                    {ticket.priority === 'High' && <AlertCircle className="w-3 h-3 mr-1" />}
                    {ticket.priority === 'Medium' && <Clock className="w-3 h-3 mr-1" />}
                    {ticket.priority}
                  </span>
                </div>
              </div>
            </div>
            <h4 className="font-semibold text-white mb-2">{ticket.title}</h4>
            <p className="text-sm text-gray-300 mb-4 line-clamp-3">{ticket.description}</p>
            <div className="flex items-center justify-between">
              <div className="text-xs text-gray-300">
                Status: <span className="font-medium">{ticket.status}</span>
              </div>
              <button
                onClick={() => handleAIAssist(ticket)}
                className="bg-gradient-to-r from-purple-500 to-teal-500 px-4 py-2 rounded-lg text-sm font-medium text-white hover:from-purple-600 hover:to-teal-600 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
              >
                <Bot className="w-4 h-4 inline mr-2" />
                AI Assist
              </button>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

export default Tickets;