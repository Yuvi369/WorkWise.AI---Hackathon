import React from 'react';

const Team = ({ employees, handleAssignClick, getStatusColor }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
        Team Members
      </h2>
      <div className="text-sm text-gray-300">{employees.length} team members</div>
    </div>
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/10 shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-white/5 border-b border-white/10">
            <tr>
              <th className="text-left py-4 px-6 font-semibold text-gray-300">Employee</th>
              <th className="text-left py-4 px-6 font-semibold text-gray-300">Role</th>
              <th className="text-left py-4 px-6 font-semibold text-gray-300">Status</th>
              <th className="text-left py-4 px-6 font-semibold text-gray-300">Assigned Tickets</th>
              <th className="text-left py-4 px-6 font-semibold text-gray-300">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10">
            {employees.map((employee) => (
              <tr key={employee.id} className="hover:bg-white/10 transition-colors">
                <td className="py-4 px-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full flex items-center justify-center">
                      <span className="text-sm font-bold text-white">
                        {employee.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <p className="font-semibold text-white">{employee.name}</p>
                      <p className="text-sm text-gray-300">{employee.email}</p>
                    </div>
                  </div>
                </td>
                <td className="py-4 px-6">
                  <span className="text-sm font-medium text-gray-300">{employee.role}</span>
                </td>
                <td className="py-4 px-6">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(employee.status)}`}>
                    {employee.status}
                  </span>
                </td>
                <td className="py-4 px-6">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-300">{employee.assignedTickets.length}</span>
                    {employee.assignedTickets.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {employee.assignedTickets.slice(0, 3).map((ticketCode, index) => (
                          <span key={index} className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded-full">
                            {ticketCode}
                          </span>
                        ))}
                        {employee.assignedTickets.length > 3 && (
                          <span className="px-2 py-1 bg-gray-500/20 text-gray-300 text-xs rounded-full">
                            +{employee.assignedTickets.length - 3}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </td>
                <td className="py-4 px-6">
                  <button
                    onClick={() => handleAssignClick(employee)}
                    className="bg-gradient-to-r from-purple-500 to-teal-500 px-4 py-2 rounded-lg text-sm font-medium text-white hover:from-purple-600 hover:to-teal-600 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
                  >
                    Assign Task
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
);

export default Team;