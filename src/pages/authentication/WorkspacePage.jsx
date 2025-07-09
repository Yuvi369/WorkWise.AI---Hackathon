// WorkSpaceSetup.jsx
import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import Header from '../mainpages/Header';
import StepIndicator from '../../components/workspace/StepIndicator';
import AddMemberModal from '../../components/workspace/AddMemberModal';
import MemberTable from '../../components/workspace/MemberTable';

const WorkSpaceSetup = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [orgName, setOrgName] = useState('');
  const [members, setMembers] = useState([
    { id: 1, name: 'sakthivel', email: 'vel172683@gmail.com', role: 'Owner' }
  ]);
  const [showAddMemberModal, setShowAddMemberModal] = useState(false);
  const [newMemberEmail, setNewMemberEmail] = useState('');
  const [newMemberRole, setNewMemberRole] = useState('Member');

  const steps = [
    { number: 1, title: 'Create Organization', active: currentStep === 1, completed: currentStep > 1 },
    { number: 2, title: 'Invite Members', active: currentStep === 2, completed: currentStep > 2 },
    { number: 3, title: 'Create Project', active: currentStep === 3, completed: currentStep > 3 },
    { number: 4, title: 'Setup Tracing', active: currentStep === 4, completed: false }
  ];

  const handleCreateOrg = () => {
    if (orgName.trim()) setCurrentStep(2);
  };

  const handleAddMember = () => {
    if (newMemberEmail.trim()) {
      const newMember = {
        id: members.length + 1,
        name: newMemberEmail.split('@')[0],
        email: newMemberEmail,
        role: newMemberRole
      };
      setMembers([...members, newMember]);
      setNewMemberEmail('');
      setNewMemberRole('Member');
      setShowAddMemberModal(false);
    }
  };

  const handleRemoveMember = (id) => {
    setMembers(members.filter(member => member.id !== id));
  };

  if (currentStep === 1) {
    return (
      <div className="min-h-screen ">
        <Header />
        <div className="bg-white  border-gray-200 py-8">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to WorkSpace Setup</h1>
            <p className="text-gray-600">Let's get started by creating your organization.</p>
          </div>
        </div>
        <div className="max-w-4xl mx-auto px-6 py-12 flex flex-col items-center space-y-8">
          <StepIndicator steps={steps} />
          <div className="max-w-md mx-auto bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">New Organization</h2>
            <p className="text-gray-600 mb-6">Organizations are used to manage your projects and teams.</p>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Organization name</label>
                <input
                  type="text"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  placeholder="sakthivel"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-blue-50"
                />
              </div>
              <button
                onClick={handleCreateOrg}
                className="w-full bg-gray-900 text-white py-2 px-6 rounded-md hover:bg-gray-800 transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentStep === 2) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-6xl mx-auto px-6 py-12">
          <StepIndicator steps={steps} />
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Organization Members</h1>
            <p className="text-gray-600">Invite members to your organization to collaborate on projects. You can always add more members later.</p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <span className="text-sm text-gray-600">Columns 4/5</span>
              <button
                onClick={() => setShowAddMemberModal(true)}
                className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 font-medium"
              >
                <Plus size={16} />
                <span>Add new member</span>
              </button>
            </div>
            <MemberTable members={members} handleRemoveMember={handleRemoveMember} />
            <div className="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">Rows per page</span>
                <select className="text-sm border border-gray-300 rounded px-2 py-1">
                  <option>10</option>
                  <option>25</option>
                  <option>50</option>
                </select>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">Page 1 of 1</span>
                <div className="flex space-x-1">
                  <button className="p-1 text-gray-400 hover:text-gray-600">‹‹</button>
                  <button className="p-1 text-gray-400 hover:text-gray-600">‹</button>
                  <button className="p-1 text-gray-400 hover:text-gray-600">›</button>
                  <button className="p-1 text-gray-400 hover:text-gray-600">››</button>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => setCurrentStep(3)}
              className="bg-gray-900 text-white py-2 px-8 rounded-md hover:bg-gray-800 transition-colors"
            >
              Next
            </button>
          </div>
          {showAddMemberModal && (
            <AddMemberModal
              setShowAddMemberModal={setShowAddMemberModal}
              newMemberEmail={newMemberEmail}
              setNewMemberEmail={setNewMemberEmail}
              newMemberRole={newMemberRole}
              setNewMemberRole={setNewMemberRole}
              handleAddMember={handleAddMember}
            />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-4xl mx-auto px-6 py-12">
        <StepIndicator steps={steps} />
        <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Step {currentStep} - Coming Soon</h2>
          <p className="text-gray-600">This step will be implemented next.</p>
        </div>
      </div>
    </div>
  );
};

export default WorkSpaceSetup;
