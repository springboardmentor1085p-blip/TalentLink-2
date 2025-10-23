import React from 'react'
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    
    <nav className="bg-[#FFFFFF] shadow-sm border-b border-[#6B7280]/30">

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">

        <div className="flex justify-between items-center h-16">
          
          {/* 1. Left Side: Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-2xl font-bold text-[#0052CC]">
              TalentLink
            </Link>
          </div>

          {/* 2. Right Side: Auth Buttons */}
          <div className="flex items-center space-x-3">
            
            {/* --- BLOCK A: IF USER IS LOGGED OUT --- */}
            {/* You will add your logic here: e.g., !user && ( ... ) */}
            <div className="flex items-center space-x-3">
              <Link
                to="/login"
                
                className="px-4 py-2 rounded-md text-sm font-medium text-[#222222] bg-[#F3F4F6] border border-[#6B7280]/30 hover:bg-gray-200"
              >
                Login
              </Link>
              <Link
                to="/register"
                
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-[#1DBF73] hover:bg-[#0E7C4D]"
              >
                Register
              </Link>
            </div>

            {/* --- BLOCK B: IF USER IS LOGGED IN --- */}
            {/* You will add your logic here: e.g., user && ( ... ) */}
            {/* <div className="flex items-center space-x-3">
              <button
                // onClick={logout}  <-- Add your logout logic here
                // Updated Logout button colors
                className="px-4 py-2 rounded-md text-sm font-medium text-[#222222] bg-[#F3F4F6] border border-[#6B7280]/30 hover:bg-gray-200"
              >
                Logout
              </button>
              <Link to="/dashboard" className="text-[#222222] hover:text-[#1DBF73]">
                {/* You can add a profile name or icon here later */}
                {/* Profile
              </Link>
            </div> */}

          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar
