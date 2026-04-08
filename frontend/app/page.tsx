import Link from "next/link";

export default function HomePage() {
  return (
    <main className="page">
      <div className="container">
        <section className="hero">
          <div className="tag">Human-in-the-Loop</div>
          <h1>Academic Writing Copilot</h1>
          <p className="muted">
            A real-product starter for topic discovery, outline generation,
            section drafting, citation auto-fill, and reference audit.
          </p>
          <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
            <Link href="/projects" className="btn primary">
              Open Workspace
            </Link>
            <a href="http://localhost:8000/docs" className="btn">
              Backend Docs
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}
