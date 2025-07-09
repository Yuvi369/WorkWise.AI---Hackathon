import React from 'react';
import { X, ChevronDown } from 'lucide-react';

const AddMemberModal = ({
  setShowAddMemberModal,
  newMemberEmail,
  setNewMemberEmail,
  newMemberRole,
  setNewMemberRole,
  handleAddMember
}) => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Add new member</h2>
        <button onClick={() => setShowAddMemberModal(false)} className="text-gray-400 hover:text-gray-600">
          <X size={20} />
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            type="email"
            value={newMemberEmail}
            onChange={(e) => setNewMemberEmail(e.target.value)}
            placeholder="jsdoe@example.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Organization Role</label>
          <div className="relative">
            <select
              value={newMemberRole}
              onChange={(e) => setNewMemberRole(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md appearance-none"
            >
              <option value="Member">Member</option>
              <option value="Admin">Admin</option>
              <option value="Manager">Manager</option>
            </select>
            <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      <button
        onClick={handleAddMember}
        className="w-full mt-6 bg-gray-900 text-white py-2 px-4 rounded-md"
      >
        Grant access
      </button>
    </div>
  </div>
);

export default AddMemberModal;