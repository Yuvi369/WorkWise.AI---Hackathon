import React, { useState } from 'react';
import { Calendar, CheckCircle, Clock, User, Plus, X, MoreHorizontal } from 'lucide-react';

const ProjectManagementUI = () => {
  const [currentView, setCurrentView] = useState('List');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [tasks, setTasks] = useState([
    {
      id: 1,
      name: 'Draft project brief',
      assignee: 'User',
      dueDate: 'Today - 15 Jul',
      priority: 'Low',
      status: 'On track',
      category: 'To do',
      startDate: '11',
      endDate: '15'
    },
    {
      id: 2,
      name: 'Schedule kickoff meeting',
      assignee: 'User',
      dueDate: '14 - 16 Jul',
      priority: 'Medium',
      status: 'At risk',
      category: 'To do',
      startDate: '14',
      endDate: '16'
    },
    {
      id: 3,
      name: 'Share timeline with teammates',
      assignee: 'User',
      dueDate: '15 - 17 Jul',
      priority: 'High',
      status: 'Off track',
      category: 'To do',
      startDate: '15',
      endDate: '17'
    }
  ]);

  const categories = ['To do', 'In Progress', 'Review', 'Done'];

  const [newTask, setNewTask] = useState({
    name: '',
    description: '',
    priority: 'Medium',
    type: 'Story',
    category: 'To do'
  });

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Low': return 'bg-teal-100 text-teal-800';
      case 'Medium': return 'bg-orange-100 text-orange-800';
      case 'High': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'On track': return 'bg-green-100 text-green-800';
      case 'At risk': return 'bg-yellow-100 text-yellow-800';
      case 'Off track': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const TaskCard = ({ task, showDetails = true }) => (
    <div className="flex items-center space-x-3 p-3 bg-white rounded-lg border hover:shadow-sm transition-shadow">
      <CheckCircle className="w-5 h-5 text-gray-400" />
      <div className="flex-1">
        <div className="font-medium text-gray-900">{task.name}</div>
        {showDetails && (
          <div className="flex items-center space-x-3 mt-2">
            <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </span>
            <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(task.status)}`}>
              {task.status}
            </span>
            <div className="flex items-center space-x-1 text-xs text-gray-500">
              <User className="w-3 h-3" />
              <span>{task.dueDate}</span>
            </div>
          </div>
        )}
      </div>
      {!showDetails && (
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
            {task.priority}
          </span>
          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(task.status)}`}>
            {task.status}
          </span>
        </div>
      )}
    </div>
  );

  const ListView = () => (
    <div className="bg-white rounded-lg">
      <table className="w-full">
        <thead className="border-b border-gray-200">
          <tr className="text-left">
            <th className="py-3 px-4 font-medium text-gray-700">Task name</th>
            <th className="py-3 px-4 font-medium text-gray-700">Assignee</th>
            <th className="py-3 px-4 font-medium text-gray-700">Due date</th>
            <th className="py-3 px-4 font-medium text-gray-700">Priority</th>
            <th className="py-3 px-4 font-medium text-gray-700">Status</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((category) => (
            <React.Fragment key={category}>
              <tr className="border-b border-gray-100">
                <td colSpan="5" className="py-2 px-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-0 h-0 border-l-4 border-l-transparent border-r-4 border-r-transparent border-t-4 border-t-gray-600"></div>
                    <span className="font-medium text-gray-900">{category}</span>
                  </div>
                </td>
              </tr>
              {tasks.filter(task => task.category === category).map((task) => (
                <tr key={task.id} className="hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-gray-400" />
                      <span className="text-gray-900">{task.name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <User className="w-6 h-6 text-gray-400" />
                  </td>
                  <td className="py-3 px-4 text-gray-600">{task.dueDate}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(task.status)}`}>
                      {task.status}
                    </span>
                  </td>
                </tr>
              ))}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );

  const BoardView = () => (
    <div className="grid grid-cols-4 gap-6">
      {categories.map((category) => (
        <div key={category} className="space-y-4">
          <h3 className="font-semibold text-gray-900">{category}</h3>
          <div className="space-y-3">
            {tasks.filter(task => task.category === category).map((task) => (
              <TaskCard key={task.id} task={task} showDetails={true} />
            ))}
            {tasks.filter(task => task.category === category).length === 0 && (
              <div className="h-32 border-2 border-dashed border-gray-200 rounded-lg flex items-center justify-center text-gray-400">
                Drop tasks here
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );

  const TimelineView = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-8 gap-2 text-center text-sm font-medium text-gray-600 border-b pb-2">
        {['5', '6', '7', '8', '9', '10', '11', '12'].map((day) => (
          <div key={day} className="py-2">{day}</div>
        ))}
      </div>
      <div className="space-y-6">
        {categories.map((category) => (
          <div key={category} className="space-y-3">
            <div className="font-semibold text-gray-900">{category}</div>
            <div className="space-y-3">
              {tasks.filter(task => task.category === category).map((task, index) => (
                <div key={task.id} className="grid grid-cols-8 gap-2 items-center">
                  <div className={`col-span-2 rounded px-3 py-2 text-sm font-medium flex items-center space-x-2 ${
                    index === 0 ? 'bg-teal-200' : index === 1 ? 'bg-orange-200' : 'bg-gray-600 text-white'
                  }`}>
                    <User className="w-4 h-4" />
                    <span>{task.name}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const CalendarView = () => {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dates = [
      [6, 7, 8, 9, 10, 11, 12],
      [13, 14, 15, 16, 17, 18, 19],
      [20, 21, 22, 23, 24, 25, 26],
      [27, 28, 29, 30, 31, '', '']
    ];

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">July</h3>
        </div>
        <div className="grid grid-cols-7 gap-4">
          {days.map((day) => (
            <div key={day} className="text-center text-sm font-medium text-gray-600 py-2">
              {day}
            </div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-4">
          {dates.flat().map((date, index) => (
            <div key={index} className="h-32 border border-gray-200 p-2">
              {date && (
                <>
                  <div className="text-sm font-medium text-gray-900 mb-2">{date}</div>
                  {date === 11 && (
                    <div className="bg-teal-200 rounded px-2 py-1 text-xs mb-1">
                      <User className="w-3 h-3 inline mr-1" />
                      Draft project brief
                    </div>
                  )}
                  {(date === 14 || date === 15 || date === 16) && (
                    <div className="bg-orange-200 rounded px-2 py-1 text-xs mb-1">
                      <User className="w-3 h-3 inline mr-1" />
                      Schedule kickoff meeting
                    </div>
                  )}
                  {(date === 15 || date === 16 || date === 17) && (
                    <div className="bg-gray-600 text-white rounded px-2 py-1 text-xs">
                      <User className="w-3 h-3 inline mr-1" />
                      Share timeline with teammates
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  const CreateIssueModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-96 max-h-screen overflow-y-auto">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">Create issue</h2>
          <div className="flex items-center space-x-2">
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
            <button 
              onClick={() => setShowCreateModal(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Project *</label>
            <select className="w-full border border-gray-300 rounded px-3 py-2 bg-white">
              <option>Jira Musical Chairs (JMC)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Issue type *</label>
            <select 
              className="w-full border border-gray-300 rounded px-3 py-2 bg-white"
              value={newTask.type}
              onChange={(e) => setNewTask({...newTask, type: e.target.value})}
            >
              <option>Story</option>
              <option>Task</option>
              <option>Bug</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">Learn more</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select 
              className="w-full border border-gray-300 rounded px-3 py-2 bg-blue-50"
              value={newTask.category}
              onChange={(e) => setNewTask({...newTask, category: e.target.value})}
            >
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">This is the issue's initial status upon creation</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Summary *</label>
            <input 
              type="text" 
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="My fix test"
              value={newTask.name}
              onChange={(e) => setNewTask({...newTask, name: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea 
              className="w-full border border-gray-300 rounded px-3 py-2 h-24 resize-none"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
            />
          </div>

          <div className="flex items-center">
            <input type="checkbox" className="mr-2" />
            <label className="text-sm text-gray-700">Create another issue</label>
          </div>
        </div>

        <div className="flex items-center justify-between p-4 border-t bg-gray-50">
          <span className="text-xs text-gray-500">Ctrl+C, Come as You Are</span>
          <div className="flex space-x-2">
            <button 
              onClick={() => setShowCreateModal(false)}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
            >
              Cancel
            </button>
            <button 
              onClick={() => {
                if (newTask.name) {
                  setTasks([...tasks, {
                    id: tasks.length + 1,
                    name: newTask.name,
                    assignee: 'User',
                    dueDate: 'Today',
                    priority: newTask.priority,
                    status: 'On track',
                    category: newTask.category
                  }]);
                  setNewTask({ name: '', description: '', priority: 'Medium', type: 'Story', category: 'To do' });
                  setShowCreateModal(false);
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Create
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCurrentView = () => {
    switch (currentView) {
      case 'List': return <ListView />;
      case 'Board': return <BoardView />;
      case 'Timeline': return <TimelineView />;
      case 'Calendar': return <CalendarView />;
      default: return <ListView />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-teal-200 rounded flex items-center justify-center">
              <div className="w-3 h-3 bg-teal-600 rounded"></div>
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Cross-functional project plan</h1>
          </div>
          <div className="flex items-center space-x-2">
            <button 
              onClick={() => setShowCreateModal(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              <Plus className="w-4 h-4" />
              <span>Create Issue</span>
            </button>
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-blue-600" />
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-6 border-b border-gray-200 mb-6">
          {['List', 'Board', 'Timeline', 'Calendar'].map((view) => (
            <button
              key={view}
              onClick={() => setCurrentView(view)}
              className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                currentView === view
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {view}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="space-y-6">
          {renderCurrentView()}
        </div>

        {/* Create Issue Modal */}
        {showCreateModal && <CreateIssueModal />}
      </div>
    </div>
  );
};

export default ProjectManagementUI;