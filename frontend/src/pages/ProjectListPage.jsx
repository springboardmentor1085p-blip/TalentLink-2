import React from "react";

function ProjectListPage() {
  const projects = [
    {
      id: 1,
      title: "TalentLink Platform UI",
      description: "A modern freelancer hiring platform built using React and Node.js.",
      status: "Ongoing",
      budget: "$1500",
      deadline: "2025-11-15",
    },
    {
      id: 2,
      title: "Chat Integration Module",
      description: "Real-time chat feature using Flask-SocketIO for smooth communication.",
      status: "Completed",
      budget: "$800",
      deadline: "2025-09-30",
    },
    {
      id: 3,
      title: "E-Commerce Backend API",
      description: "Developed REST APIs with Node.js and MongoDB for order management.",
      status: "Pending",
      budget: "$2000",
      deadline: "2025-12-10",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6">
      <h1 className="text-3xl font-bold text-[#0052CC] mb-8 text-center">
        Projects List
      </h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <div
            key={project.id}
            className="bg-white shadow-md rounded-2xl p-6 hover:shadow-lg transition-shadow border border-gray-200"
          >
            <h2 className="text-xl font-semibold text-[#0052CC] mb-2">
              {project.title}
            </h2>
            <p className="text-gray-600 text-sm mb-4">{project.description}</p>

            <div className="text-sm space-y-1 text-gray-700">
              <p>
                <span className="font-medium text-gray-800">Status:</span>{" "}
                <span
                  className={`px-2 py-1 rounded-full text-white text-xs ${
                    project.status === "Completed"
                      ? "bg-green-600"
                      : project.status === "Ongoing"
                      ? "bg-blue-600"
                      : "bg-yellow-600"
                  }`}
                >
                  {project.status}
                </span>
              </p>
              <p>
                <span className="font-medium text-gray-800">Budget:</span>{" "}
                {project.budget}
              </p>
              <p>
                <span className="font-medium text-gray-800">Deadline:</span>{" "}
                {project.deadline}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProjectListPage;
