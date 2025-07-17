import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/tailwind.css';
import AppRoutes from "./routes/AppRoutes";

function App() {
  return (
    <Router>
      <div className='min-h-screen bg-gray-100'>
        <AppRoutes />
      </div>
    </Router>
  );
}

export default App;