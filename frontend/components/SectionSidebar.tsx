type Section = {
  id: string;
  title: string;
  status: string;
};

const defaultSections: Section[] = [
  { id: "sec-intro", title: "Introduction", status: "draft" },
  { id: "sec-related", title: "Related Work", status: "draft" },
  { id: "sec-core", title: "Core Analysis", status: "draft" },
  { id: "sec-discussion", title: "Discussion", status: "draft" }
];

export default function SectionSidebar() {
  return (
    <div className="card">
      <div className="panel-title">Sections</div>
      <div className="list">
        {defaultSections.map((section) => (
          <div key={section.id} className="card">
            <strong>{section.title}</strong>
            <div className="muted">Status: {section.status}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
