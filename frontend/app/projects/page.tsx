import ProjectCard from "../../components/ProjectCard";

const sampleProjects = [
  {
    id: "demo-project-1",
    title: "LLM-Assisted Citation Reliability",
    domain: "computer_science",
    paperType: "survey",
    status: "draft"
  },
  {
    id: "demo-project-2",
    title: "Educational Policy Literature Review",
    domain: "education",
    paperType: "empirical",
    status: "researching"
  }
];

export default function ProjectsPage() {
  return (
    <main className="page">
      <div className="container">
        <div className="topbar">
          <div>
            <div className="tag">Workspace</div>
            <h1>Projects</h1>
          </div>
          <button className="btn primary">New Project</button>
        </div>

        <div className="project-grid">
          {sampleProjects.map((project) => (
            <ProjectCard
              key={project.id}
              id={project.id}
              title={project.title}
              domain={project.domain}
              paperType={project.paperType}
              status={project.status}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
