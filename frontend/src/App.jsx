// In src/App.jsx
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import HomePage from './pages/HomePage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import ProjectListPage from './pages/ProjectListPage.jsx';
import ProjectDetailPage from './pages/ProjectDetailPage.jsx';
import CreateProjectPage from './pages/CreateProjectPage.jsx';
import ClientDashboardPage from './pages/ClientDashboardPage.jsx';
import MessagesPage from './pages/MessagePage.jsx';
import ProfilePage from './pages/profilePage.jsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* Public Routes */}
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />

        {/* Freelancer Routes */}
        <Route path="projects" element={<ProjectListPage />} />
        <Route path="project/:id" element={<ProjectDetailPage />} />

        {/* Client Routes */}
        <Route path="dashboard" element={<ClientDashboardPage />} />
        <Route path="create-project" element={<CreateProjectPage />} />
        <Route path="messages" element={<MessagesPage />} />
        <Route path="profile" element={<ProfilePage />} />
        
      </Route>
    </Routes>
  );
}

export default App;