import React from "react";
import {
  Tag,
  DollarSign,
  User,
  Clock,
  ArrowLeft,
  MessageSquare,
} from "lucide-react";

/**
 * Mock project data — In a real app, this would be fetched from an API.
 */
const mockProject = {
  id: "p1",
  title: "E-commerce Website Redesign",
  description:
    "We are looking to completely overhaul our existing e-commerce platform. This includes a new UI/UX design, backend migration to a modern framework, and integration with new payment gateways. The goal is to improve performance, scalability, and user engagement.",
  category: "Web Development",
  budget: 500000,
  postedBy: "Jane Doe, TechCorp",
  status: "Open for Bids",
  postedDate: "October 28, 2025",
};

/**
 * Mock list of bids — In a real app, fetched dynamically.
 */
const mockBids = [
  {
    id: "b1",
    user: "Freelancer A",
    amount: 480000,
    proposal: "I have 5 years of experience in e-commerce migration...",
  },
  {
    id: "b2",
    user: "DevAgency B",
    amount: 510000,
    proposal: "Our agency can deliver a high-quality product within 3 months...",
  },
];

const ProjectDetailPage = () => {
  const project = mockProject;
  const bids = mockBids;

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-10 font-inter text-black">
      {/* Back button */}
      <div className="max-w-5xl mx-auto mb-6">
        <button
          onClick={() => window.history.back()}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold transition"
        >
          <ArrowLeft size={18} />
          Back to Projects
        </button>
      </div>

      {/* Main grid */}
      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* LEFT: Project details */}
        <div className="lg:col-span-2 bg-white p-10 rounded-2xl shadow-2xl border border-gray-200">
          {/* Status badge */}
          <span className="inline-block bg-green-100 text-green-700 text-xs font-semibold px-3 py-1 rounded-full mb-3">
            {project.status}
          </span>

          {/* Title */}
          <h2 className="text-4xl font-bold mb-4 tracking-tight text-black">
            {project.title}
          </h2>

          {/* Meta info */}
          <div className="flex flex-wrap gap-x-8 gap-y-3 text-gray-700 mb-8">
            <div className="flex items-center gap-2">
              <User size={16} className="text-blue-600" />
              <span>
                <strong className="font-semibold text-black">Posted by:</strong>{" "}
                {project.postedBy}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={16} className="text-blue-600" />
              <span>
                <strong className="font-semibold text-black">Posted on:</strong>{" "}
                {project.postedDate}
              </span>
            </div>
          </div>

          {/* Description */}
          <div className="space-y-3">
            <h3 className="text-2xl font-semibold text-black">
              Project Description
            </h3>
            <p className="text-gray-800 leading-relaxed">
              {project.description}
            </p>
          </div>
        </div>

        {/* RIGHT: Info + Bids */}
        <div className="space-y-6">
          {/* Project Info */}
          <div className="bg-white p-8 rounded-2xl shadow-2xl border border-gray-200">
            <h3 className="text-2xl font-semibold text-black mb-6">
              Project Info
            </h3>
            <div className="space-y-4">
              {/* Budget */}
              <div className="flex items-center gap-3">
                <DollarSign
                  size={22}
                  className="text-green-600 flex-shrink-0"
                />
                <div>
                  <span className="block text-sm text-gray-500">Budget</span>
                  <span className="block text-xl font-semibold text-black">
                    ₹{project.budget.toLocaleString("en-IN")}
                  </span>
                </div>
              </div>

              {/* Category */}
              <div className="flex items-center gap-3">
                <Tag size={22} className="text-blue-600 flex-shrink-0" />
                <div>
                  <span className="block text-sm text-gray-500">Category</span>
                  <span className="block text-xl font-semibold text-black">
                    {project.category}
                  </span>
                </div>
              </div>
            </div>

            <button className="w-full bg-blue-600 text-white py-3 mt-8 rounded-xl font-semibold hover:bg-blue-700 transition-transform transform hover:scale-[1.02] shadow-md">
              💼 Place a Bid
            </button>
          </div>

          {/* Bids Section */}
          <div className="bg-white p-8 rounded-2xl shadow-2xl border border-gray-200">
            <h3 className="text-2xl font-semibold text-black mb-6 flex items-center gap-2">
              <MessageSquare className="text-blue-600" size={22} />
              Bids ({bids.length})
            </h3>

            <div className="space-y-5">
              {bids.map((bid) => (
                <div
                  key={bid.id}
                  className="border-b border-gray-200 pb-4 last:border-none"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-semibold text-black text-lg">
                      {bid.user}
                    </span>
                    <span className="font-bold text-blue-600 text-lg">
                      ₹{bid.amount.toLocaleString("en-IN")}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm">{bid.proposal}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- MAIN EXPORT ---
export default function App() {
  return <ProjectDetailPage />;
}
