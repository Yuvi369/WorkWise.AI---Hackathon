import React, { useState } from 'react';
import { CheckCircle, X, MessageCircle, Send,Bot } from 'lucide-react';
import Header from './Header';
import Reports from './Reports';
import Tickets from './Tickets';
import Team from './Team';
import EmployeeDetailsPage from './EmployeeDetailsPage';

const TaskAssignmentDashboard = () => {
  const [showChatBox, setShowChatBox] = useState(false);
  const [chatPrompt, setChatPrompt] = useState('');
  const [showPersonDashboard, setShowPersonDashboard] = useState(false);
  const [showAIPanel, setShowAIPanel] = useState(false);
  const [aiPrompt, setAIPrompt] = useState('');
  const [numEmployees, setNumEmployees] = useState('');
  const [aiSuggestions, setAISuggestions] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('reports');
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [assignedTickets, setAssignedTickets] = useState([]);
  const [showEmployeeDetails, setShowEmployeeDetails] = useState(false);

  const personDetails = [
    { id: 1, name: 'Raj Kumar', role: 'Senior Developer', email: 'raj.kumar@company.com', status: 'Available', assignedTickets: ['TK001'] },
    { id: 2, name: 'Priya Sharma', role: 'UI/UX Designer', email: 'priya.sharma@company.com', status: 'Busy', assignedTickets: ['TK002'] },
    { id: 3, name: 'Arjun Patel', role: 'Data Analyst', email: 'arjun.patel@company.com', status: 'Available', assignedTickets: ['TK003'] }
  ];

  const employees = [
    { id: 1, name: 'Priya Sharma', role: 'Senior Developer', assignedTickets: ['TK001'], email: 'priya.sharma@company.com', status: 'Available' },
    { id: 2, name: 'Rajesh Kumar', role: 'UI/UX Designer', assignedTickets: ['TK002', 'TK003'], email: 'rajesh.kumar@company.com', status: 'Busy' },
    { id: 3, name: 'Anita Patel', role: 'Data Analyst', assignedTickets: ['TK004'], email: 'anita.patel@company.com', status: 'Available' },
    { id: 4, name: 'Vikram Singh', role: 'DevOps Engineer', assignedTickets: [], email: 'vikram.singh@company.com', status: 'Available' },
    { id: 5, name: 'Sneha Reddy', role: 'QA Engineer', assignedTickets: ['TK009'], email: 'sneha.reddy@company.com', status: 'Available' },
    { id: 6, name: 'Arjun Nair', role: 'Backend Developer', assignedTickets: [], email: 'arjun.nair@company.com', status: 'Available' }
  ];

  const [tickets, setTickets] = useState([
    { id: 1, code: 'TK001', title: 'User Dashboard Analytics', assignee: 'Anita Patel', status: 'Completed', priority: 'High', description: 'Implement analytics dashboard for user behavior tracking' },
    { id: 2, code: 'TK002', title: 'Mobile App Redesign', assignee: 'Rajesh Kumar', status: 'In Progress', priority: 'Medium', description: 'Redesign mobile app interface for better user experience' },
    { id: 3, code: 'TK003', title: 'API Integration', assignee: 'Priya Sharma', status: 'Review', priority: 'High', description: 'Integrate third-party APIs for payment processing' },
    { id: 4, code: 'TK004', title: 'Database Optimization', assignee: 'Vikram Singh', status: 'Pending', priority: 'Low', description: 'Optimize database queries for better performance' },
    { id: 5, code: 'TK005', title: 'New Feature Implementation', assignee: null, status: 'To Do', priority: 'Medium', description: 'Implement new chat feature for customer support' },
    { id: 6, code: 'TK006', title: 'Bug Fix for Payment Module', assignee: null, status: 'To Do', priority: 'High', description: 'Fix critical bug in payment processing module' },
    { id: 7, code: 'TK007', title: 'Security Update', assignee: null, status: 'To Do', priority: 'High', description: 'Update security protocols and implement new authentication' },
    { id: 8, code: 'TK008', title: 'Performance Optimization', assignee: null, status: 'To Do', priority: 'Medium', description: 'Optimize application performance and reduce load times' }
  ]);

  const mockAISuggestions = [
    { employee: employees[2], reasons: ['Perfect skill match for data analysis tasks', 'Low current workload', 'Excellent track record'], matchScore: 94 },
    { employee: employees[0], reasons: ['Strong technical background', 'Moderate workload', 'High performance rating'], matchScore: 87 },
    { employee: employees[1], reasons: ['Relevant design experience', 'High workload but manageable', 'Good collaboration history'], matchScore: 72 }
  ];

  const unassignedTickets = tickets.filter(ticket => !ticket.assignee && ticket.status === 'To Do');

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if (!chatPrompt.trim()) return;
    setShowPersonDashboard(true);
    setShowChatBox(false);
    setChatPrompt('');
  };

  const handleAIAssist = (ticket) => {
    setSelectedTicket(ticket);
    setShowAIPanel(true);
    setAIPrompt('');
    setNumEmployees('');
    setAISuggestions([]);
  };

  const handleSubmitPrompt = async () => {
    if (!aiPrompt.trim()) return;
    setAiLoading(true);
    await new Promise(resolve => setTimeout(resolve, 2000));
    const num = parseInt(numEmployees) || mockAISuggestions.length;
    const suggestions = mockAISuggestions.slice(0, Math.min(num, mockAISuggestions.length));
    setAISuggestions(suggestions);
    setAiLoading(false);
  };

  const handleAssignClick = (employee) => {
    if (unassignedTickets.length === 0) {
      alert('No unassigned tickets available');
      return;
    }
    setSelectedEmployee(employee);
    setShowAssignModal(true);
  };

  const handleConfirmAssignment = (ticket) => {
    setTickets(prevTickets => 
      prevTickets.map(t => 
        t.id === ticket.id 
          ? { ...t, assignee: selectedEmployee.name, status: 'Assigned' }
          : t
      )
    );
    setAssignedTickets(prev => [...prev, { ticket, employee: selectedEmployee }]);
    setShowSuccessMessage(true);
    setShowAssignModal(false);
    setSelectedEmployee(null);
    setTimeout(() => setShowSuccessMessage(false), 3000);
  };

  const handleCloseAIPanel = () => {
    setShowAIPanel(false);
    setSelectedTicket(null);
    setAISuggestions([]);
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'High': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'Medium': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'Low': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'Available': return 'bg-green-500/20 text-green-400';
      case 'Busy': return 'bg-red-500/20 text-red-400';
      case 'Away': return 'bg-yellow-500/20 text-yellow-400';
      default: return 'bg-gray-500/20 text-gray-400';
    }
  };

  return (
    <div>
      {!showEmployeeDetails ? (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
          </div>

          <Header activeTab={activeTab} setActiveTab={setActiveTab} />

          {/* Success Message */}
          {showSuccessMessage && (
            <div className="fixed top-24 right-6 z-50 bg-gradient-to-r from-purple-500 to-teal-500 text-white px-6 py-4 rounded-xl shadow-2xl animate-bounce">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6" />
                <div>
                  <p className="font-semibold">Assignment Successful!</p>
                  {assignedTickets.slice(-1).map((item, index) => (
                    <p key={index} className="text-sm opacity-90">
                      {item.ticket.code} assigned to {item.employee.name}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Floating Chat Button */}
          {!showChatBox && (
            <button
              onClick={() => setShowChatBox(true)}
              className="fixed bottom-6 right-6 bg-gradient-to-r from-purple-500 to-teal-500 p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 z-50 transform hover:scale-105"
            >
              <MessageCircle className="w-6 h-6 text-white" />
            </button>
          )}

          {/* Chat Box */}
          {showChatBox && (
            <div className="fixed bottom-6 right-6 w-1/4 h-3/4 bg-white/10 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/10 z-50">
              <div className="p-4 bg-gradient-to-r from-purple-500 to-teal-500 rounded-t-2xl">
                <div className="flex items-center justify-between">
                  <h3 className="text-white font-semibold flex items-center">
                    <Bot className="w-5 h-5 mr-2" />
                    AI Assistant
                  </h3>
                  <button
                    onClick={() => setShowChatBox(false)}
                    className="text-white hover:bg-white/20 p-1 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="p-4">
                <div className="mb-4">
                  <div className="bg-white/10 rounded-lg p-3 text-sm text-gray-300">
                    👋 Hello! I'm your AI assistant. Enter a prompt to get person details and dashboard information.
                  </div>
                </div>
                <form onSubmit={handleChatSubmit} className="space-y-3">
                  <textarea
                    value={chatPrompt}
                    onChange={(e) => setChatPrompt(e.target.value)}
                    placeholder="Enter your prompt here..."
                    className="w-full p-3 bg-white/5 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-sm text-gray-300"
                    rows="3"
                  />
                  <button
                    type="submit"
                    className="w-full bg-gradient-to-r from-purple-500 to-teal-500 text-white py-2 px-4 rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all duration-300 flex items-center justify-center text-sm font-medium transform hover:scale-105"
                  >
                    <Send className="w-4 h-4 mr-2" />
                    Send
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Main Content */}
          <div className="relative z-10 max-w-7xl mx-auto p-6">
            {activeTab === 'reports' && (
              <Reports
                personDetails={personDetails}
                showPersonDashboard={showPersonDashboard}
                setShowChatBox={setShowChatBox}
                showEmployeeDetails={showEmployeeDetails}
                setShowEmployeeDetails={setShowEmployeeDetails}
              />
            )}
            {activeTab === 'tickets' && (
              <Tickets
                unassignedTickets={unassignedTickets}
                handleAIAssist={handleAIAssist}
                getPriorityColor={getPriorityColor}
              />
            )}
            {activeTab === 'team' && (
              <Team
                employees={employees}
                handleAssignClick={handleAssignClick}
                getStatusColor={getStatusColor}
              />
            )}
          </div>

          {/* AI Bottom Panel */}
          {aiSuggestions.length > 0 && (
            <div className="fixed bottom-0 left-0 right-0 bg-white/10 backdrop-blur-sm border-t border-white/10 shadow-2xl z-40">
              <div className="max-w-7xl mx-auto p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white flex items-center">
                    <Bot className="w-5 h-5 mr-2 text-purple-400" />
                    AI Recommendations Ready
                  </h3>
                  <button
                    onClick={() => setActiveTab('team')}
                    className="bg-gradient-to-r from-purple-500 to-teal-500 px-6 py-2 rounded-lg text-sm font-medium text-white hover:from-purple-600 hover:to-teal-600 transition-all duration-300 shadow-md transform hover:scale-105"
                  >
                    View Team
                  </button>
                </div>
                <p className="text-sm text-gray-300">
                  AI has analyzed {aiSuggestions.length} employees for "{selectedTicket?.title}".
                  Go to Team tab to assign the task.
                </p>
                <div className="mt-4">
                  {aiSuggestions.map((suggestion, index) => (
                    <div key={index} className="bg-white/10 p-4 rounded-lg mb-2">
                      <p className="font-semibold text-white">{suggestion.employee.name} ({suggestion.matchScore}% match)</p>
                      <ul className="list-disc list-inside text-sm text-gray-300">
                        {suggestion.reasons.map((reason, idx) => (
                          <li key={idx}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* AI Panel Modal */}
          {showAIPanel && selectedTicket && (
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 max-w-lg w-full shadow-2xl max-h-[90vh] overflow-y-auto border border-white/10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-white flex items-center">
                    <Bot className="w-6 h-6 mr-2 text-purple-400" />
                    AI Task Analysis
                  </h3>
                  <button
                    onClick={handleCloseAIPanel}
                    className="p-2 hover:bg-white/20 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-300" />
                  </button>
                </div>
                <div className="mb-4">
                  <p className="text-sm font-semibold text-white">Task: {selectedTicket.title}</p>
                  <p className="text-sm text-gray-300">{selectedTicket.description}</p>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      AI Prompt
                    </label>
                    <textarea
                      value={aiPrompt}
                      onChange={(e) => setAIPrompt(e.target.value)}
                      placeholder="Enter AI prompt for task assignment..."
                      className="w-full p-3 bg-white/5 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-sm text-gray-300"
                      rows="4"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Number of Employee Suggestions
                    </label>
                    <input
                      type="number"
                      value={numEmployees}
                      onChange={(e) => setNumEmployees(e.target.value)}
                      placeholder="Enter number (e.g., 3)"
                      className="w-full p-3 bg-white/5 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-sm text-gray-300"
                    />
                  </div>
                  <button
                    onClick={handleSubmitPrompt}
                    disabled={aiLoading}
                    className={`w-full bg-gradient-to-r from-purple-500 to-teal-500 text-white py-3 px-4 rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all duration-300 flex items-center justify-center text-sm font-medium transform hover:scale-105 ${
                      aiLoading ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                  >
                    {aiLoading ? (
                      <span className="flex items-center">
                        <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                        </svg>
                        Processing...
                      </span>
                    ) : (
                      <>
                        <Bot className="w-4 h-4 mr-2" />
                        Get AI Suggestions
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Assign Task Modal */}
          {showAssignModal && selectedEmployee && (
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 max-w-lg w-full shadow-2xl border border-white/10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-white">
                    Assign Task to {selectedEmployee.name}
                  </h3>
                  <button
                    onClick={() => setShowAssignModal(false)}
                    className="p-2 hover:bg-white/20 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-300" />
                  </button>
                </div>
                <div className="space-y-4">
                  <p className="text-sm text-gray-300">Select a ticket to assign:</p>
                  <div className="space-y-2">
                    {unassignedTickets.map((ticket) => (
                      <div
                        key={ticket.id}
                        className="flex items-center justify-between p-3 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
                      >
                        <div>
                          <p className="text-sm font-semibold text-white">{ticket.code}: {ticket.title}</p>
                          <p className="text-xs text-gray-300">{ticket.description}</p>
                        </div>
                        <button
                          onClick={() => handleConfirmAssignment(ticket)}
                          className="bg-gradient-to-r from-purple-500 to-teal-500 px-4 py-2 rounded-lg text-sm font-medium text-white hover:from-purple-600 hover:to-teal-600 transition-all duration-300 transform hover:scale-105"
                        >
                          Assign
                        </button>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={() => setShowAssignModal(false)}
                    className="w-full bg-white/10 text-gray-300 py-2 px-4 rounded-lg hover:bg-white/20 transition-all duration-300 text-sm font-medium"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <EmployeeDetailsPage employees={mockAISuggestions.slice(0, 3).map(s => s.employee)} onClose={() => setShowEmployeeDetails(false)} />
      )}
    </div>
  );
};

export default TaskAssignmentDashboard;