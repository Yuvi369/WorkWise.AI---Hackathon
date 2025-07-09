import React from 'react';
import { Edit, Trash2, ChevronDown } from 'lucide-react';

const MemberTable = ({ members, handleRemoveMember }) => (
  <div className="overflow-x-auto">
    <table className="w-full">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Name</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Email</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Role</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500">Actions</th>
        </tr>
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {members.map((member) => (
          <tr key={member.id} className="hover:bg-gray-50">
            <td className="px-6 py-4 whitespace-nowrap">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <span className="text-blue-600 font-medium text-sm">
                    {member.name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <span className="text-gray-900">{member.name}</span>
              </div>
            </td>
            <td className="px-6 py-4 text-gray-600">{member.email}</td>
            <td className="px-6 py-4">
              <div className="flex items-center space-x-2">
                <span className="text-gray-900">{member.role}</span>
                <ChevronDown size={16} className="text-gray-400" />
              </div>
            </td>
            <td className="px-6 py-4">
              <div className="flex items-center space-x-2">
                <button className="text-gray-400 hover:text-gray-600">
                  <Edit size={16} />
                </button>
                {member.role !== 'Owner' && (
                  <button 
                    onClick={() => handleRemoveMember(member.id)}
                    className="text-gray-400 hover:text-red-600"
                  >
                    <Trash2 size={16} />
                  </button>
                )}
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default MemberTable;
