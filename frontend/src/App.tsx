import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { FinanceDataProvider } from './contexts/FinanceDataContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import LoadingSpinner from './components/Common/LoadingSpinner';
import Modal from './components/Common/Modal';
import Sidebar from './components/Layout/Sidebar';
import Navbar from './components/Layout/Navbar';
import BottomMenu from './components/Layout/BottomMenu';
import Incomes from './components/Finance/Incomes';
import Expenses from './components/Finance/Expenses';
import { useLoading } from './hooks/useLoading';
import { useModal } from './hooks/useModal';

// Create placeholder components for missing ones
const ForgetPassword = () => <div>Forget Password Page - Coming Soon</div>;
const ResetPassword = () => <div>Reset Password Page - Coming Soon</div>;
const Budgets = () => <div>Budgets Page - Coming Soon</div>;
const Projects = () => <div>Projects Page - Coming Soon</div>;
const Tasks = () => <div>Tasks Page - Coming Soon</div>;
const Analytics = () => <div>Analytics Page - Coming Soon</div>;
const Groups = () => <div>Groups Page - Coming Soon</div>;
const TypesManagement = () => <div>Types Management Page - Coming Soon</div>;

function AppContent() {
  const { user, loading: authLoading } = useAuth();
  const { loading: appLoading } = useLoading();
  const { isOpen, closeModal } = useModal();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth >= 768) {
        setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (authLoading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forget-password" element={<ForgetPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    );
  }

  return (
    <FinanceDataProvider>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar for larger screens */}
        {!isMobile && <Sidebar />}
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
          
          {/* Mobile sidebar overlay */}
          {isMobile && sidebarOpen && (
            <div 
              className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75"
              onClick={() => setSidebarOpen(false)}
            >
              <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out">
                <Sidebar onClose={() => setSidebarOpen(false)} />
              </div>
            </div>
          )}
          
          <main className="flex-1 overflow-x-hidden overflow-y-auto pb-20 md:pb-0">
            <div className="container mx-auto px-4 py-6">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/incomes" element={<Incomes />} />
                <Route path="/expenses" element={<Expenses />} />
                <Route path="/budgets" element={<Budgets />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/projects/:projectId/tasks" element={<Tasks />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/groups" element={<Groups />} />
                <Route path="/types" element={<TypesManagement />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </div>
          </main>
          
          {/* Bottom menu for mobile */}
          {isMobile && <BottomMenu />}
        </div>
        
        {isOpen && <Modal />}
        {appLoading && <LoadingSpinner />}
      </div>
    </FinanceDataProvider>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;