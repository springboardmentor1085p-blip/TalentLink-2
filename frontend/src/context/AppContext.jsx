import { createContext, useState } from 'react';

// 1. Create the context
export const AppContext = createContext();

// 2. Create the provider 
export function AppProvider({ children }) {

  const [user, setUser] = useState(null);

  // --- You can add more global state here later ---
  // const [projects, setProjects] = useState([]);

  // --- AUTH FUNCTIONS (for now) ---

  const login = (email, password) => {
    // Fake logic:
    if (email.includes('client')) {
      setUser({ email: email, role: 'client' });
    } else {
      setUser({ email: email, role: 'freelancer' });
    }
  };

  const logout = () => {
    setUser(null);
  };

  // --- Value to be "provided" to all components ---
  const value = {
    user, 
    login, 
    logout, 
    
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}