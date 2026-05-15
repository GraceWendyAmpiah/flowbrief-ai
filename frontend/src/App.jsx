import React from 'react'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Upload from './pages/Upload'
import Report from './pages/Report'
import Dashboard from './pages/Dashboard'
import History from './pages/History'

export default function App() {
  const location = useLocation()
  return (
    <div className="app">
      <Sidebar currentPath={location.pathname} />
      <main className="main">
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/cases/:case_id" element={<Report />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/history" element={<History />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}
