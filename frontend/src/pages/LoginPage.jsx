import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const BASE_URL = "http://127.0.0.1:5000"; // Flask backend URL

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${BASE_URL}/api/login`, { email, password });
      // Save JWT to localStorage
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      alert(res.data.message);
      navigate("/"); // redirect to homepage or dashboard
    } catch (err) {
      setError(err.response?.data?.message || "Login failed");
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-[#F3F4F6] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-[#0052CC]">
            TalentLink
          </h2>
          <p className="mt-2 text-center text-sm text-[#6B7280]">
            Sign in to your account
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6 bg-[#FFFFFF] p-8 shadow-md rounded-lg">
          {error && <p className="text-red-500">{error}</p>}

          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                id="email-address"
                name="email"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                autoComplete="email"
                required
                className="relative block w-full appearance-none rounded-t-md border border-[#6B7280]/50 px-3 py-2 text-[#222222] placeholder-[#6B7280] focus:z-10 focus:border-[#1DBF73] focus:outline-none focus:ring-[#1DBF73] sm:text-sm"
                placeholder="Email address"
              />
            </div>
            <div>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                autoComplete="current-password"
                required
                className="relative block w-full appearance-none rounded-b-md border border-[#6B7280]/50 px-3 py-2 text-[#222222] placeholder-[#6B7280] focus:z-10 focus:border-[#1DBF73] focus:outline-none focus:ring-[#1DBF73] sm:text-sm"
                placeholder="Password"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative flex w-full justify-center rounded-md border border-transparent bg-[#1DBF73] py-2 px-4 text-sm font-medium text-white hover:bg-[#0E7C4D] focus:outline-none focus:ring-2 focus:ring-[#0E7C4D] focus:ring-offset-2"
            >
              Sign in
            </button>
          </div>
        </form>

        <p className="mt-4 text-center text-sm text-[#6B7280]">
          Don't have an account?{' '}
          <Link to="/register" className="font-medium text-[#00B8D9] hover:text-[#0052CC]">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
