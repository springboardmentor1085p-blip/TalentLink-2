import React from 'react';
import {
  Tag,
  DollarSign,
  ClipboardText, // Note: This icon was imported but not used, I'll keep it in case you need it.
  User,
  Clock,
  ArrowLeft,
  MessageSquare,
} from 'lucide-react'; // Importing icons from the lucide-react library for UI elements

// --- MOCK DATA ---
// This is placeholder data. In a real application, you would fetch this
// from an API based on the project's ID (e.g., from the URL).

/**
 * Mock data object representing a single project.
 */
const mockProject = {
  id: 'p1',
  title: 'E-commerce Website Redesign',
  description:
    'We are looking to completely overhaul our existing e-commerce platform. This includes a new UI/UX design, backend migration to a modern framework, and integration with new payment gateways. The goal is to improve performance, scalability, and user engagement.',
  category: 'Web Development',
  budget: 500000,
  postedBy: 'Jane Doe, TechCorp',
  status: 'Open for Bids',
  postedDate: 'October 28, 2025',
};

/**
 * Mock data array representing bids placed on the project.
 */
const mockBids = [
  {
    id: 'b1',
    user: 'Freelancer A',
    amount: 480000,
    proposal: 'I have 5 years of experience in e-commerce migration...',
  },
  {
    id: 'b2',
    user: 'DevAgency B',
    amount: 510000,
    proposal: 'Our agency can deliver a high-quality product within 3 months...',
  },
];

// --- COMPONENT DEFINITION ---

/**
 * ProjectDetailPage Component
 *
 * Renders a detailed view of a single project, including its description,
 * budget, category, and a list of current bids.
 */
const ProjectDetailPage = () => {
  // In a real app, you'd use useState and useEffect to fetch project data.
  // For this example, we just assign the mock data to variables.
  const project = mockProject;
  const bids = mockBids;

  // The 'return' statement describes what the component renders to the screen (JSX).
  return (
    // Main container div
    <div className="min-h-screen bg-gray-100 p-6 md:p-10 font-inter">
      {/* Back button */}
      <div className="max-w-4xl mx-auto mb-4">
        {/* In a real app, this button would use a router (like React Router) 
            or a state management function to navigate back. */}
        <button className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition">
          <ArrowLeft size={18} />
          Back to Projects
        </button>
      </div>

      {/* Main content area, using a responsive grid layout */}
      <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Project Details Card */}
        {/* Spans 2 out of 3 columns on large screens (lg:col-span-2) */}
        <div className="lg:col-span-2 bg-white p-8 rounded-2xl shadow-lg">
          {/* Header section */}
          
          {/* Project status badge */}
          <span className="inline-block bg-green-100 text-green-700 text-xs font-semibold px-3 py-1 rounded-full mb-3">
            {project.status}
          </span>
          
          {/* Project title */}
          <h2 className="text-3xl font-bold mb-4 text-gray-800">
            {project.title}
          </h2>

          {/* Meta Info (Posted by, Posted date) */}
          <div className="flex flex-wrap gap-x-6 gap-y-2 text-gray-600 mb-6">
            <div className="flex items-center gap-2">
              <User size={16} />
              <span>Posted by {project.postedBy}</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={16} />
              <span>Posted on {project.postedDate}</span>
            </div>
          </div>

          {/* Project Description section */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-700">
              Project Description
            </h3>
            <p className="text-gray-700 leading-relaxed">
              {project.description}
            </p>
          </div>
        </div>

        {/* Right Column: Budget & Bids Cards */}
        {/* This column stacks its children vertically (space-y-6) */}
        <div className="space-y-6">
          
          {/* Budget Card */}
          <div className="bg-white p-6 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold text-gray-700 mb-4">
              Project Info
            </h3>
            {/* Container for Budget and Category info */}
            <div className="space-y-3">
              {/* Budget display */}
              <div className="flex items-center gap-3">
                <DollarSign
                  size={20}
                  className="text-green-600 flex-shrink-0"
                />
                <div>
                  <span className="block text-sm text-gray-500">Budget</span>
                  <span className="block text-lg font-semibold text-gray-800">
                    {/* Formats the number as Indian Rupee currency */}
                    ₹{project.budget.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>
              {/* Category display */}
              <div className="flex items-center gap-3">
                <Tag size={20} className="text-blue-600 flex-shrink-0" />
                <div>
                  <span className="block text-sm text-gray-500">Category</span>
                  <span className="block text-lg font-semibold text-gray-800">
                    {project.category}
                  </span>
                </div>
              </div>
            </div>
            {/* "Place a Bid" button. In a real app, this might open a modal or navigate to a new page. */}
            <button className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mt-6">
              Place a Bid
            </button>
          </div>

          {/* Bids Card */}
          <div className="bg-white p-6 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <MessageSquare size={20} />
              Bids ({bids.length}) {/* Dynamically shows the number of bids */}
            </h3>
            {/* Container for the list of bids */}
            <div className="space-y-4">
              {/* We map over the 'bids' array to render a new div for each bid object. */}
              {bids.map((bid) => (
                // 'key' is a required prop for lists in React for performance.
                <div key={bid.id} className="border-b pb-3 last:border-b-0">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-gray-800">
                      {bid.user}
                    </span>
                    <span className="font-bold text-blue-600">
                      ₹{bid.amount.toLocaleString('en-IN')}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">{bid.proposal}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- APP EXPORT ---

/**
 * Main App component.
 * This is the root component that renders our ProjectDetailPage.
 * In a larger app, this component would handle routing to show different pages.
 */
export default function App() {
  return <ProjectDetailPage />;
}

