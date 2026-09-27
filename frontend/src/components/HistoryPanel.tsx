import { useEffect, useRef } from "react";
import { animate } from "animejs";

import type { ResearchRunSummary } from "../services/api";

interface HistoryPanelProps {
  runs: ResearchRunSummary[];
  onSelect: (runId: number) => void;
}

export default function HistoryPanel({
  runs,
  onSelect,
}: HistoryPanelProps) {
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!panelRef.current || runs.length === 0) {
      return;
    }

    const items =
      panelRef.current.querySelectorAll(
        ".history-item",
      );

    animate(items, {
      opacity: [0, 1],
      translateX: [-15, 0],
      delay: 100,
      duration: 450,
      ease: "outExpo",
    });
  }, [runs]);

  if (runs.length === 0) {
    return null;
  }

  return (
    <section
      ref={panelRef}
      className="history-panel"
    >
      <div className="history-header">
        <div>
          <span className="section-eyebrow">
            RESEARCH HISTORY
          </span>

          <h2>Previous Research</h2>
        </div>

        <span className="history-count">
          {runs.length} runs
        </span>
      </div>

      <div className="history-list">
        {runs.map((run) => (
          <button
            key={run.id}
            type="button"
            className="history-item"
            onClick={() => onSelect(run.id)}
          >
            <div className="history-item-icon">
              ✦
            </div>

            <div className="history-item-content">
              <div className="history-query">
                {run.query}
              </div>

              <div className="history-meta">
                <span
                  className={`history-status ${run.status}`}
                >
                  {run.status}
                </span>

                <span>
                  Run #{run.id}
                </span>
              </div>
            </div>

            <span className="history-arrow">
              →
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}