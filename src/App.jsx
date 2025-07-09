import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/authentication/LoginPage';
import SignupPage from './pages/authentication/SignupPage';
import WorkspacePage from './pages/authentication/WorkspacePage';
import './styles/tailwind.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/workspace" element={<WorkspacePage />} />
                <Route path="/" element={<LoginPage />} />
            </Routes>
        </Router>
    );
}

export default App;