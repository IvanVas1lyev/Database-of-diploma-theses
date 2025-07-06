import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import StudentPage from './pages/StudentPage';
import YearPage from './pages/YearPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/student/:id" element={<StudentPage />} />
          <Route path="/year/:year" element={<YearPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;