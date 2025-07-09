import React from 'react';

const StepIndicator = ({ steps }) => (
  <div className="flex items-center space-x-2 mb-8">
    {steps.map((step, index) => (
      <React.Fragment key={step.number}>
        <div className="flex items-center space-x-2">
          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-medium ${
            step.completed 
              ? 'bg-blue-600 text-white' 
              : step.active 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 text-gray-600'
          }`}>
            {step.number}
          </div>
          <span className={`text-sm ${step.active ? 'text-blue-600 font-medium' : 'text-gray-500'}`}>
            {step.title}
          </span>
        </div>
        {index < steps.length - 1 && <div className="w-4 h-px bg-gray-300"></div>}
      </React.Fragment>
    ))}
  </div>
);

export default StepIndicator;
