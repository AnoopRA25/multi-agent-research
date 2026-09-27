interface ReportViewerProps {
  report: string;
  critique?: string;
}

function renderReport(report: string) {
  return report.split("\n").map((line, index) => {
    const trimmed = line.trim();

    if (!trimmed) {
      return <div className="report-space" key={index} />;
    }

    if (trimmed.startsWith("# ")) {
      return (
        <h1 className="report-title" key={index}>
          {trimmed.replace("# ", "")}
        </h1>
      );
    }

    if (trimmed.startsWith("## ")) {
      return (
        <h2 className="report-heading" key={index}>
          {trimmed.replace("## ", "")}
        </h2>
      );
    }

    if (trimmed.startsWith("### ")) {
      return (
        <h3 className="report-subheading" key={index}>
          {trimmed.replace("### ", "")}
        </h3>
      );
    }

    if (
      trimmed.startsWith("- ") ||
      trimmed.startsWith("* ")
    ) {
      return (
        <div className="report-bullet" key={index}>
          <span>•</span>
          <p>{trimmed.substring(2)}</p>
        </div>
      );
    }

    return (
      <p className="report-paragraph" key={index}>
        {trimmed}
      </p>
    );
  });
}


export default function ReportViewer({
  report,
  critique,
}: ReportViewerProps) {
  return (
    <div className="report-viewer">

      <div className="report-viewer-header">

        <div>
          <span className="section-eyebrow">
            GENERATED RESEARCH
          </span>

          <h2>
            Research Report
          </h2>
        </div>

        <div className="report-badge">
          AI Generated
        </div>

      </div>


      <article className="report-content">
        {renderReport(report)}
      </article>


      {critique && (
        <div className="critique-panel">

          <div className="critique-header">

            <span className="critique-icon">
              ✓
            </span>

            <div>
              <span className="section-eyebrow">
                QUALITY REVIEW
              </span>

              <h3>
                Agent Critique
              </h3>
            </div>

          </div>

          <pre className="critique-content">
            {critique}
          </pre>

        </div>
      )}

    </div>
  );
}