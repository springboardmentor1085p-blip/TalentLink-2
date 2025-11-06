import React, { useState } from "react";
import { ArrowLeft, FileText, Tag, DollarSign } from "lucide-react";

const CreateProjectPage = () => {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    budget: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("✅ Project created:", formData);
    alert("🎉 Project created successfully!");
    setFormData({ title: "", description: "", category: "", budget: "" });
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-10 font-inter">
      <div className="max-w-3xl mx-auto bg-white p-10 rounded-2xl shadow-2xl border border-gray-200">
        {/* Back Button */}
        <button
          onClick={() => window.history.back()}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 mb-6 transition"
        >
          <ArrowLeft size={18} />
          <span className="font-semibold">Back</span>
        </button>

        {/* Header */}
        <h1 className="text-4xl font-bold mb-8 text-black tracking-tight">
          Create a <span className="text-blue-600">New Project</span>
        </h1>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-7">
          {/* Project Title */}
          <div>
            <label className="block text-sm font-semibold text-black mb-2">
              Project Title
            </label>
            <div className="flex items-center border rounded-lg px-3 py-2 bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500">
              <FileText className="text-blue-600 mr-2" size={18} />
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g. E-commerce Website Redesign"
                className="w-full bg-transparent outline-none text-black placeholder-gray-500"
                required
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-semibold text-black mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe your project in detail..."
              rows={5}
              className="w-full border rounded-lg px-3 py-2 bg-gray-100 outline-none text-black placeholder-gray-500 focus:ring-2 focus:ring-blue-500 resize-none"
              required
            ></textarea>
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-semibold text-black mb-2">
              Category
            </label>
            <div className="flex items-center border rounded-lg px-3 py-2 bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500">
              <Tag className="text-blue-600 mr-2" size={18} />
              <input
                type="text"
                name="category"
                value={formData.category}
                onChange={handleChange}
                placeholder="e.g. Web Development, UI/UX Design"
                className="w-full bg-transparent outline-none text-black placeholder-gray-500"
                required
              />
            </div>
          </div>

          {/* Budget */}
          <div>
            <label className="block text-sm font-semibold text-black mb-2">
              Budget (₹)
            </label>
            <div className="flex items-center border rounded-lg px-3 py-2 bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500">
              <DollarSign className="text-blue-600 mr-2" size={18} />
              <input
                type="number"
                name="budget"
                value={formData.budget}
                onChange={handleChange}
                placeholder="Enter your project budget"
                className="w-full bg-transparent outline-none text-black placeholder-gray-500"
                required
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition-transform transform hover:scale-[1.02] shadow-md"
          >
            🚀 Submit Project
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateProjectPage;
