import React, { useState } from 'react';
import { FileText, Brain, Search, Star, Clock, Target, Users, Bug, Award, ArrowLeft } from 'lucide-react';

const AIReportsTab = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterComplexity, setFilterComplexity] = useState('all');
  const [selectedTicket, setSelectedTicket] = useState(null);

  // Mock AI Report Data
  const aiReportData = [
    {
      id: 1,
      ticketNumber: 'TK-2024-001',
      ticketDescription: 'Implement real-time chat system with WebSocket integration for customer support',
      userQuery: 'Need a developer for chat feature implementation with real-time messaging capabilities',
      aiResponse: 'Recommend Senior Full-Stack Developer with React/Node.js and WebSocket skills. Estimated completion: 5-7 days.',
      aiSummary: 'AI suggests a skilled developer for real-time chat system. High match with WebSocket and Node.js expertise. Completion: 5-7 days.',
      aiRating: 4.8,
      priority: 'High',
      complexity: 'Advanced',
      estimatedHours: 40,
      recommendedSkills: ['React', 'WebSocket', 'Node.js', 'Real-time Systems'],
      matchScore: 94,
      status: 'Analyzed',
      timestamp: '2024-07-15 10:30:00',
      aiConfidence: 'High',
      category: 'Full-Stack Development',
      topDevelopers: [
        {
          id: 1,
          name: 'Rajesh Kumar',
          avatar: 'RK',
          skillMatch: 98,
          experience: '5+ years',
          rating: 4.9,
          completedTickets: 45,
          bugsSolved: 23,
          currentStatus: 'Available',
          hourlyRate: '$45/hr',
          location: 'Bangalore, India',
          skills: ['React', 'WebSocket', 'Node.js', 'Real-time Systems', 'MongoDB', 'Express.js', 'Socket.io', 'Redis'],
          recentWork: [
            { ticket: 'TK-2024-089', title: 'Chat Integration for E-commerce Platform', status: 'Completed', duration: '3 days', client: 'ShopEasy Ltd', rating: 5.0 },
            { ticket: 'TK-2024-076', title: 'Real-time Notification System', status: 'Completed', duration: '4 days', client: 'NotifyApp Inc', rating: 4.8 },
            { ticket: 'TK-2024-065', title: 'WebSocket Performance Optimization', status: 'Completed', duration: '2 days', client: 'SpeedChat Co', rating: 4.9 }
          ],
          bugHistory: [
            { bug: 'BUG-001', title: 'Memory leak in WebSocket connection', severity: 'High', resolved: true, timeToResolve: '2 hours', impact: 'System Performance' },
            { bug: 'BUG-002', title: 'Real-time sync issues between clients', severity: 'Medium', resolved: true, timeToResolve: '4 hours', impact: 'User Experience' },
            { bug: 'BUG-003', title: 'Connection timeout in high traffic', severity: 'High', resolved: true, timeToResolve: '1.5 hours', impact: 'System Stability' }
          ],
          achievements: ['Top Performer Q2 2024', 'WebSocket Expert Certification', 'Real-time Systems Specialist'],
          heavyWorkload: 'Heavy (45 tickets, 23 bugs handled)'
        },
        {
          id: 2,
          name: 'Priya Sharma',
          avatar: 'PS',
          skillMatch: 95,
          experience: '4+ years',
          rating: 4.8,
          completedTickets: 38,
          bugsSolved: 18,
          currentStatus: 'Available',
          hourlyRate: '$42/hr',
          location: 'Mumbai, India',
          skills: ['React', 'Node.js', 'WebSocket', 'TypeScript', 'Redis', 'PostgreSQL', 'Socket.io', 'AWS'],
          recentWork: [
            { ticket: 'TK-2024-082', title: 'Live Chat Dashboard Development', status: 'Completed', duration: '5 days', client: 'ChatPro Systems', rating: 4.9 },
            { ticket: 'TK-2024-071', title: 'Socket.io Implementation & Scaling', status: 'Completed', duration: '3 days', client: 'ScaleChat Ltd', rating: 4.7 },
            { ticket: 'TK-2024-058', title: 'Real-time Analytics Dashboard', status: 'Completed', duration: '6 days', client: 'AnalyticsPro', rating: 4.8 }
          ],
          bugHistory: [
            { bug: 'BUG-004', title: 'WebSocket reconnection failure', severity: 'High', resolved: true, timeToResolve: '1.5 hours', impact: 'Connection Stability' },
            { bug: 'BUG-005', title: 'Message ordering issues in group chats', severity: 'Medium', resolved: true, timeToResolve: '3 hours', impact: 'Message Integrity' },
            { bug: 'BUG-006', title: 'TypeScript compilation errors', severity: 'Low', resolved: true, timeToResolve: '1 hour', impact: 'Development Speed' }
          ],
          achievements: ['TypeScript Expert', 'React Advanced Certification', 'Cloud Architecture Specialist'],
          heavyWorkload: 'Moderate (38 tickets, 18 bugs handled)'
        },
        {
          id: 3,
          name: 'Arjun Patel',
          avatar: 'AP',
          skillMatch: 92,
          experience: '3+ years',
          rating: 4.7,
          completedTickets: 32,
          bugsSolved: 14,
          currentStatus: 'Busy',
          hourlyRate: '$38/hr',
          location: 'Pune, India',
          skills: ['React', 'Node.js', 'Socket.io', 'Express.js', 'PostgreSQL', 'Docker', 'Kubernetes', 'GraphQL'],
          recentWork: [
            { ticket: 'TK-2024-079', title: 'Chat Message Encryption System', status: 'Completed', duration: '4 days', client: 'SecureChat Inc', rating: 4.8 },
            { ticket: 'TK-2024-067', title: 'Real-time File Sharing Feature', status: 'Completed', duration: '5 days', client: 'FileShare Pro', rating: 4.6 },
            { ticket: 'TK-2024-054', title: 'Group Chat Features Implementation', status: 'Completed', duration: '7 days', client: 'TeamChat Co', rating: 4.7 }
          ],
          bugHistory: [
            { bug: 'BUG-007', title: 'File upload in chat failing', severity: 'Medium', resolved: true, timeToResolve: '2 hours', impact: 'Feature Functionality' },
            { bug: 'BUG-008', title: 'Group message delivery delay', severity: 'Low', resolved: true, timeToResolve: '1 hour', impact: 'Performance' },
            { bug: 'BUG-009', title: 'Docker container memory leak', severity: 'High', resolved: true, timeToResolve: '3 hours', impact: 'System Resources' }
          ],
          achievements: ['Docker Certified', 'GraphQL Specialist', 'Security Best Practices'],
          heavyWorkload: 'Light (32 tickets, 14 bugs handled)'
        }
      ]
    },
    // Additional related ticket
    {
      id: 2,
      ticketNumber: 'TK-2024-002',
      ticketDescription: 'Enhance real-time chat with WebSocket security features',
      userQuery: 'Need developer to add security to existing chat system using WebSocket',
      aiResponse: 'Recommend developer with WebSocket and security expertise. Estimated completion: 4-6 days.',
      aiSummary: 'AI suggests a developer for enhancing chat security. High match with WebSocket skills. Completion: 4-6 days.',
      aiRating: 4.7,
      priority: 'High',
      complexity: 'Advanced',
      estimatedHours: 35,
      recommendedSkills: ['WebSocket', 'Node.js', 'Security', 'React'],
      matchScore: 92,
      status: 'Analyzed',
      timestamp: '2024-07-16 09:15:00',
      aiConfidence: 'High',
      category: 'Full-Stack Development',
      topDevelopers: [
        {
          id: 1,
          name: 'Rajesh Kumar',
          avatar: 'RK',
          skillMatch: 97,
          experience: '5+ years',
          rating: 4.9,
          completedTickets: 45,
          bugsSolved: 23,
          currentStatus: 'Available',
          hourlyRate: '$45/hr',
          location: 'Bangalore, India',
          skills: ['React', 'WebSocket', 'Node.js', 'Real-time Systems', 'MongoDB', 'Express.js', 'Socket.io', 'Redis'],
          recentWork: [
            { ticket: 'TK-2024-089', title: 'Chat Integration', status: 'Completed', duration: '3 days', client: 'ShopEasy Ltd', rating: 5.0 },
            { ticket: 'TK-2024-076', title: 'Notification System', status: 'Completed', duration: '4 days', client: 'NotifyApp Inc', rating: 4.8 },
            { ticket: 'TK-2024-065', title: 'WebSocket Optimization', status: 'Completed', duration: '2 days', client: 'SpeedChat Co', rating: 4.9 }
          ],
          bugHistory: [
            { bug: 'BUG-001', title: 'Memory leak', severity: 'High', resolved: true, timeToResolve: '2 hours', impact: 'Performance' },
            { bug: 'BUG-002', title: 'Sync issues', severity: 'Medium', resolved: true, timeToResolve: '4 hours', impact: 'User Experience' },
            { bug: 'BUG-003', title: 'Timeout', severity: 'High', resolved: true, timeToResolve: '1.5 hours', impact: 'Stability' }
          ],
          achievements: ['WebSocket Expert', 'Top Performer Q2 2024'],
          heavyWorkload: 'Heavy (45 tickets, 23 bugs handled)'
        },
        // Other developers omitted for brevity
      ]
    }
  ];

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Critical': return 'bg-red-600/20 text-red-300 border-red-500/30';
      case 'High': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'Medium': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'Low': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getComplexityColor = (complexity) => {
    switch (complexity) {
      case 'Expert': return 'bg-purple-600/20 text-purple-300 border-purple-500/30';
      case 'Advanced': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'Intermediate': return 'bg-teal-500/20 text-teal-400 border-teal-500/30';
      case 'Basic': return 'bg-green-500/20 text-green-400 border-green-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'Very High': return 'bg-emerald-600/20 text-emerald-300 border-emerald-500/30';
      case 'High': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'Medium': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'Low': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const filteredReports = aiReportData.filter(report => {
    const matchesSearch = report.ticketNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.userQuery.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPriority = filterPriority === 'all' || report.priority === filterPriority;
    const matchesComplexity = filterComplexity === 'all' || report.complexity === filterComplexity;
    return matchesSearch && matchesPriority && matchesComplexity;
  });

  const handleRowClick = (report) => {
    setSelectedTicket(report);
  };

  return (
    <div className="">
   

      <div className="relative z-10 max-w-7xl mx-auto p-6">
        {selectedTicket ? (
          <>
            {/* Panel Header */}
            <div className="mb-8">
              <button
                onClick={() => setSelectedTicket(null)}
                className="flex items-center space-x-2 text-purple-400 hover:text-purple-300 transition-colors mb-4 group"
              >
                <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                <span>Back to Reports</span>
              </button>
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent mb-2">
                    {selectedTicket.ticketNumber}
                  </h1>
                  <p className="text-gray-300 text-lg mb-2">{selectedTicket.ticketDescription}</p>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-400">Category: {selectedTicket.category}</span>
                    <span className="text-sm text-gray-400">•</span>
                    <span className="text-sm text-gray-400">Created: {selectedTicket.timestamp}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium border ${getPriorityColor(selectedTicket.priority)}`}>
                    {selectedTicket.priority}
                  </span>
                  <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium border ${getComplexityColor(selectedTicket.complexity)}`}>
                    {selectedTicket.complexity}
                  </span>
                </div>
              </div>
            </div>

            {/* Panel Content */}
            <div className="space-y-8">
              {/* AI Summary */}
              <div className="bg-gradient-to-r from-purple-500/10 to-teal-500/10 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20">
                <div className="flex items-center space-x-2 mb-4">
                  <Brain className="w-5 h-5 text-purple-400" />
                  <h3 className="text-xl font-semibold text-white">AI Suggestion</h3>
                </div>
                <div className="text-gray-300 space-y-4">
                  <p>{selectedTicket.aiSummary}</p>
                  <div className="flex items-center space-x-2">
                    <Star className="w-5 h-5 text-yellow-400" />
                    <span className="text-lg font-semibold">AI Rating: {selectedTicket.aiRating}/5</span>
                  </div>
                </div>
              </div>

              {/* Top Developers */}
              <div>
                <h3 className="text-2xl font-semibold text-white mb-6">Top Recommended Developers</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {selectedTicket.topDevelopers.map(developer => (
                    <div key={developer.id} className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
                      <div className="mb-4">
                        <h4 className="text-lg font-semibold text-white">{developer.name}</h4>
                        <p className="text-sm text-gray-400">{developer.experience}</p>
                        <p className="text-sm font-semibold text-teal-300">Match: {developer.skillMatch}%</p>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-400 font-medium mb-2">Matched Skills:</p>
                          <ul className="list-disc list-inside text-gray-300 space-y-1">
                            {selectedTicket.recommendedSkills.map((skill, idx) =>
                              developer.skills.includes(skill) && <li key={idx}>{skill}</li>
                            )}
                          </ul>
                        </div>
                        <div>
                          <p className="text-sm text-gray-400 font-medium mb-2">Previous Tickets:</p>
                          <ul className="list-disc list-inside text-gray-300 space-y-1">
                            {developer.recentWork
                              .filter(work => selectedTicket.recommendedSkills.some(skill => work.title.toLowerCase().includes(skill.toLowerCase())))
                              .map((work, idx) => (
                                <li key={idx}>
                                  {work.ticket} - {work.title} ({work.status}, {work.duration}, Client: {work.client}, Rating: {work.rating}/5)
                                </li>
                              ))}
                          </ul>
                        </div>
                        <div>
                          <p className="text-sm text-gray-400 font-medium mb-2">Handled Bugs:</p>
                          <ul className="list-disc list-inside text-gray-300 space-y-1">
                            {developer.bugHistory
                              .filter(bug => selectedTicket.recommendedSkills.some(skill => bug.title.toLowerCase().includes(skill.toLowerCase())))
                              .map((bug, idx) => (
                                <li key={idx}>
                                  {bug.bug} - {bug.title} ({bug.severity}, {bug.resolved ? 'Resolved' : 'Unresolved'}, Time: {bug.timeToResolve}, Impact: {bug.impact})
                                </li>
                              ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Header Section */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent mb-2">
                    AI Analysis Reports
                  </h1>
                  <p className="text-gray-300 text-lg">Comprehensive ticket analysis and AI-powered assignment recommendations</p>
                </div>
              </div>

              {/* Filters and Search */}
              <div className="flex flex-wrap gap-4 mb-6">
                <div className="flex-1 min-w-64">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search tickets or queries..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-white placeholder-gray-400"
                    />
                  </div>
                </div>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white"
                >
                  <option value="all">All Priorities</option>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
               
              </div>
            </div>

            {/* Report Table */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gradient-to-r from-purple-500/20 to-teal-500/20 border-b border-white/10">
                    <tr>
                      <th className="text-left py-4 px-6 font-bold text-white">Ticket Number</th>
                      <th className="text-left py-4 px-6 font-bold text-white">User Query</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/10">
                    {filteredReports.map((report) => (
                      <tr
                        key={report.id}
                        className="hover:bg-white/5 transition-all duration-300 group cursor-pointer"
                        onClick={() => handleRowClick(report)}
                      >
                        <td className="py-6 px-6">
                          <span className="font-semibold text-white text-lg underline cursor-pointer">
                            {report.ticketNumber}
                          </span>
                        </td>
                        <td className="py-6 px-6">
                          <p className="text-sm text-gray-300 italic leading-relaxed underline cursor-pointer">
                            "{report.userQuery}"
                          </p>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AIReportsTab;