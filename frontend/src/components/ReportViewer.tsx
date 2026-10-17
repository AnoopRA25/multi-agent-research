
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ReportViewerProps {
  report: string;
  critique?: string;
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

          <h2>Research Report</h2>
        </div>

        <div className="report-badge">
          AI Generated
        </div>
      </div>

      <article className="report-content">
        {report.trim() ? (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {report}
          </ReactMarkdown>
        ) : (
          <p className="report-paragraph">
            No report is available for this run yet.
          </p>
        )}
      </article>

      {critique && (
        <div className="critique-panel">
          <div className="critique-header">
            <span className="critique-icon">✓</span>

            <div>
              <span className="section-eyebrow">
                QUALITY REVIEW
              </span>

              <h3>Agent Critique</h3>
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
