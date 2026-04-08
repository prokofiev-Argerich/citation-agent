const samplePapers = [
  {
    title: "Attention Is All You Need",
    source: "crossref",
    year: 2017
  },
  {
    title: "Longformer: The Long-Document Transformer",
    source: "semantic_scholar",
    year: 2020
  }
];

export default function CitationPanel() {
  return (
    <div className="card">
      <div className="panel-title">Evidence and Citations</div>
      <div className="list">
        {samplePapers.map((paper) => (
          <div key={`${paper.title}-${paper.year}`} className="card">
            <strong>{paper.title}</strong>
            <div className="muted">
              {paper.source} · {paper.year}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
