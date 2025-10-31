import React, { useState } from "react";
import axios from "axios";

const CreateProjectPage = () => {
  // State variables to store form data
  const [title, setTitle] = useState(""); // Project title
  const [description, setDescription] = useState(""); // Short project description
  const [category, setCategory] = useState(""); // Project category
  const [budget, setBudget] = useState(""); // Budget entered by user
  const [message, setMessage] = useState(""); // Feedback message (success or error)

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents page reload on form submit

    try {
      // Sending project data to backend API
      const response = await axios.post("http://127.0.0.1:5000/create_project", {
        title,
        description,
        category,
        budget,
      });

      // If successful, show success message
      setMessage("✅ Project created successfully!");
      console.log("Server Response:", response.data);

      // Clear the form fields
      setTitle("");
      setDescription("");
      setCategory("");
      setBudget("");
    } catch (error) {
      // If error occurs, display error message
      console.error("Error creating project:", error);
      setMessage("❌ Failed to create project. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      {/* Main container card */}
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-lg">
        {/* Page heading */}
        <h2 className="text-2xl font-bold mb-6 text-center">Create a New Project</h2>

        {/* Feedback message */}
        {message && (
          <p
            className={`text-center mb-4 ${
              message.includes("✅") ? "text-green-600" : "text-red-600"
            }`}
          >
            {message}
          </p>
        )}

        {/* Project creation form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title input field */}
          <div>
            <label className="block text-gray-700 mb-1">Project Title</label>
            <input
              type="text"
              placeholder="Enter project title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Description input field */}
          <div>
            <label className="block text-gray-700 mb-1">Description</label>
            <textarea
              placeholder="Enter project description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Category input field */}
          <div>
            <label className="block text-gray-700 mb-1">Category</label>
            <input
              type="text"
              placeholder="Enter category (e.g., Web Dev, AI, Design)"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Budget input field */}
          <div>
            <label className="block text-gray-700 mb-1">Budget (₹)</label>
            <input
              type="number"
              placeholder="Enter budget"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              required
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Submit button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Create Project
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateProjectPage;
