// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CreateTest from './pages/CreateTest';
import TestList from './pages/TestList';
import TestDetails from './pages/TestDetails';

function App() {
  return (
    <Router>
      <div className="bg-gray-50 min-h-screen">
        <header className="bg-blue-600 text-white py-4 shadow-lg">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">
              <Link to="/">Gerenciamento de teste</Link>
            </h1>
            <nav>
              <Link to="/" className="px-4 hover:underline">
                Home
              </Link>
              <Link to="/create" className="px-4 hover:underline">
                Criar novos teste
              </Link>
            </nav>
          </div>
        </header>
        <main className="container mx-auto p-6">
          <Routes>
            <Route path="/" element={<TestList />} />
            <Route path="/create" element={<CreateTest />} />
            <Route path="/tests/:id" element={<TestDetails />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
