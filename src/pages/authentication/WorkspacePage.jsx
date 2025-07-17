import React, { useState, useRef } from 'react';
import { Plus, Upload, File, X } from 'lucide-react';
import Header from './Header';
import StepIndicator from '../../components/workspace/StepIndicator';
import AddMemberModal from '../../components/workspace/AddMemberModal';
import MemberTable from '../../components/workspace/MemberTable';

const WorkSpaceSetup = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [orgName, setOrgName] = useState('');
  const [members, setMembers] = useState([
    { id: 1, name: 'sakthivel', email: 'vel172683@gmail.com', role: 'Owner', status: 'Active' }
  ]);
  const [showAddMemberModal, setShowAddMemberModal] = useState(false);
  const [newMemberEmail, setNewMemberEmail] = useState('');
  const [newMemberRole, setNewMemberRole] = useState('Member');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const steps = [
    { number: 1, title: 'Create Organization', active: currentStep === 1, completed: currentStep > 1 },
    { number: 2, title: 'Invite Members', active: currentStep === 2, completed: currentStep > 2 },
    { number: 3, title: 'Upload HR Policy', active: currentStep === 3, completed: currentStep > 3 }
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
        role: newMemberRole,
        status: 'Invited'
      };
      setMembers([...members, newMember]);
      setNewMemberEmail('');
      setNewMemberRole('Member');
      setShowAddMemberModal(false);
    }
  };

  const handleFileUpload = (file) => {
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    handleFileUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Step 1: Create Org
  if (currentStep === 1) {
    return (
      <div className="min-h-screen">
        <Header />
        <div className="bg-white border-gray-200 py-8">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to WorkSpace Setup</h1>
            <p className="text-gray-600">Let's get started by creating your organization.</p>
          </div>
        </div>
        <div className="max-w-4xl mx-auto px-6 py-12 flex flex-col items-center space-y-8">
          <StepIndicator steps={steps} />
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 py-10 px-15">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">New Organization</h2>
            <p className="text-gray-600 mb-6">Organizations are used to manage your projects and teams.</p>
            <div className="space-y-4">
              <div className="flex flex-col gap-4">
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
                className="w-1/4 bg-gray-900 text-white py-2 px-6 rounded-md hover:bg-gray-800 transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Step 2: Invite Members
  if (currentStep === 2) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="w-full flex justify-center items-center">
            <StepIndicator steps={steps} />
          </div>
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Organization Members</h1>
            <p className="text-gray-600">Invite members to your organization to collaborate on projects. You can always add more members later.</p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <span className="text-sm text-gray-600">Columns 4/5</span>
              <button
                onClick={() => setShowAddMemberModal(true)}
                className="flex items-center space-x-2 font-medium bg-[#155DFD] hover:bg-[#0644D0]/90 text-white px-2 py-1.5 rounded-md transition-colors"
              >
                <Plus size={20} />
                <span>Add new member</span>
              </button>
            </div>
            <MemberTable members={members} />
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
          <div className="mt-8 flex justify-end">
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

  // Step 3: Upload HR Policy
  if (currentStep === 3) {
    const handleNextStep = () => {
      if (uploadedFile) {
        console.log('HR Policy uploaded:', uploadedFile.name);
        setCurrentStep(4);
      } else {
        alert('Please upload an HR policy file.');
      }
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-4xl mx-auto px-6 py-12">
          <div className="w-full flex justify-center items-center">
            <StepIndicator steps={steps} />
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 px-8 py-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload HR Policy</h2>
            <p className="text-gray-600 mb-2">
              Upload your organization's HR policy document (PDF only) to help manage your workspace.
            </p>
            <p className="text-blue-700 mb-6">
              <strong>Why upload your HR Policy?</strong><br/>
              WorkWise.AI uses your HR policy to automatically enforce HR roles, automate compliance, and ensure all workspace actions follow your company's rules and guidelines. This enables smart, policy-driven task assignment and helps your team stay compliant and efficient.
            </p>

            <div
              className={`border-2 border-dashed rounded-lg p-12 text-center ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div className="flex flex-col items-center justify-center p-4 space-y-4">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileInputChange}
                  className="hidden"
                  ref={fileInputRef}
                  id="file-upload"
                />
                {uploadedFile ? (
                  <div className="flex items-center justify-center space-x-3">
                    <File className="w-6 h-6 text-blue-600" />
                    <span className="text-sm text-gray-900">{uploadedFile.name}</span>
                    <button
                      onClick={handleRemoveFile}
                      className="text-red-600 hover:text-red-800"
                    >
                      <X size={20} />
                    </button>
                  </div>
                ) : (
                  <div>
                    <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600 mb-2">Drag and drop your HR policy PDF here, or</p>
                    <label
                      htmlFor="file-upload"
                      className="inline-block bg-blue-600 text-white text-[12px] px-2 py-1 rounded-md hover:bg-blue-700 cursor-pointer transition-colors"
                    >
                      Browse Files
                    </label>
                  </div>
                )}
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <button
                onClick={handleNextStep}
                className="bg-gray-900 text-white py-2 px-6 rounded-md hover:bg-gray-800 transition-colors"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
};

export default WorkSpaceSetup;