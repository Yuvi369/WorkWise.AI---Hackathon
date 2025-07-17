import React from 'react';
import { X } from 'lucide-react';

const EmployeeDetailsPage = ({ employees, onClose }) => {
  // Check if employees data is available
  const hasEmployees = employees && employees.length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
      </div>
      <div className="relative z-10 max-w-7xl mx-auto p-6">
        <button
          onClick={onClose}
          className="mb-6 bg-gradient-to-r from-purple-500 to-teal-500 px-4 py-2 rounded-lg text-white hover:from-purple-600 hover:to-teal-600 transition-all duration-300 transform hover:scale-105 flex items-center"
        >
          <X className="w-5 h-5 mr-2" /> Back
        </button>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent mb-6">
          Top 3 Employee Details
        </h2>
        {hasEmployees ? (
          <div className="grid gap-6 md:grid-cols-3">
            {employees.map((emp, index) => (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/10 shadow-sm hover:shadow-lg transition-all duration-300 hover:transform hover:scale-105"
              >
                <div className="flex items-center mb-4">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full flex items-center justify-center text-2xl mr-4">
                    {emp.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-white">{emp.name}</h3>
                    <p className="text-sm text-gray-300">{emp.role}</p>
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      emp.status === 'Available' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                    }`}>
                      {emp.status}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-gray-300 mb-2">Email: {emp.email}</p>
                <p className="text-sm text-gray-300">Assigned Tickets: {emp.assignedTickets.length}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <X className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-xl font-semibold text-gray-300 mb-2">No Employee Data Available</p>
            <p className="text-gray-400 mb-4">Please generate AI suggestions or check data.</p>
            <button
              onClick={onClose}
              className="bg-gradient-to-r from-purple-500 to-teal-500 text-white px-6 py-3 rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all duration-300 flex items-center mx-auto transform hover:scale-105"
            >
              <X className="w-5 h-5 mr-2" /> Go Back
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmployeeDetailsPage;