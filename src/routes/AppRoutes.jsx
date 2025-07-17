import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPage from '../pages/authentication/LoginPage';
import SignupPage from '../pages/authentication/SignupPage';
import WorkspacePage from '../pages/authentication/WorkspacePage';
import WorkWiseHomepage from '../pages/authentication/WorkWiseHomepage';
import ProjectManagementUI from '../pages/authentication/ProjectManagementUI';
import TaskAssignmentDashboard from '../pages/authentication/Home page/TaskAssignmentDashboard';

const AppRoutes =() => {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/workspace" element={<WorkspacePage />} />
            <Route path="/WorkWiseHomepage" element={<WorkWiseHomepage />} />
            <Route path="/ProjectManagementUI" element={<ProjectManagementUI />} />
            <Route path="/TaskAssignmentDashboard" element={<TaskAssignmentDashboard />} />
            <Route path="/" element={<WorkWiseHomepage />} />
        </Routes>
    );
}
export default AppRoutes;