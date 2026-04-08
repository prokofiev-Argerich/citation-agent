import CitationPanel from "../../../components/CitationPanel";
    import SectionSidebar from "../../../components/SectionSidebar";

    export default async function ProjectWorkspacePage({
      params
    }: {
      params: Promise<{ projectId: string }>;
    }) {
      const { projectId } = await params;

      return (
        <main className="page">
          <div className="container">
            <div className="topbar">
              <div>
                <div className="tag">Project</div>
                <h1>{projectId}</h1>
                <p className="muted">
                  This page is the main writing workspace. Connect the UI to your
                  backend APIs step by step.
                </p>
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn">Generate Outline</button>
                <button className="btn">Auto-Fill Citations</button>
                <button className="btn primary">Review Section</button>
              </div>
            </div>

            <div className="workspace">
              <SectionSidebar />

              <div className="card">
                <div className="panel-title">Editor</div>
                <textarea
                  className="editor"
                  defaultValue={`Transformer models often face quadratic complexity in long sequence modeling.[ref]

This workspace is intentionally built for section-by-section writing.
Use the backend services to parse claims, search literature, auto-fill citations, and store versioned outputs.`}
                />
              </div>

              <CitationPanel />
            </div>
          </div>
        </main>
      );
    }
