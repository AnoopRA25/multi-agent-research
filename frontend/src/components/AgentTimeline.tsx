import { useEffect, useRef } from "react";
import { animate } from "animejs";

import type { AgentExecution } from "../services/api";

interface AgentTimelineProps {
  executions: AgentExecution[];
}

const agentLabels: Record<string, string> = {
  planner: "Planner",
  researcher: "Researcher",
  analyst: "Analyst",
  writer: "Report Writer",
  critic: "Critic",
  revision_writer: "Revision Writer",
};

const agentIcons: Record<string, string> = {
  planner: "◈",
  researcher: "⌕",
  analyst: "◉",
  writer: "✦",
  critic: "✓",
  revision_writer: "↻",
};

export default function AgentTimeline({
  executions,
}: AgentTimelineProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (
      !containerRef.current ||
      executions.length === 0
    ) {
      return;
    }

    const items =
      containerRef.current.querySelectorAll(
        ".agent-step",
      );

    animate(items, {
      opacity: [0, 1],
      translateX: [-20, 0],
      delay: 100,
      duration: 500,
      ease: "outExpo",
    });
  }, [executions]);

  if (executions.length === 0) {
    return null;
  }

  return (
    <section
      ref={containerRef}
      className="agent-timeline"
    >
      <div className="timeline-header">
        <div>
          <span className="section-eyebrow">
            AGENT ACTIVITY
          </span>

          <h2>
            Research Pipeline
          </h2>
        </div>

        <span className="agent-count">
          {executions.length} agents
        </span>
      </div>

      <div className="timeline-list">
        {executions.map(
          (execution, index) => {
            const label =
              agentLabels[
                execution.agent_name
              ] ?? execution.agent_name;

            const icon =
              agentIcons[
                execution.agent_name
              ] ?? "•";

            return (
              <div
                className="agent-step"
                key={execution.id}
              >
                <div className="agent-icon">
                  {icon}
                </div>

                <div className="agent-info">
                  <div className="agent-name">
                    {label}
                  </div>

                  <div className="agent-meta">
                    {execution.status}

                    {execution.latency_ms !==
                      null && (
                      <>
                        {" · "}
                        {Math.round(
                          execution.latency_ms,
                        )}
                        ms
                      </>
                    )}
                  </div>
                </div>

                {execution.output_tokens !==
                  null && (
                  <div className="agent-tokens">
                    {execution.output_tokens} tokens
                  </div>
                )}

                {index <
                  executions.length - 1 && (
                  <div className="timeline-line" />
                )}
              </div>
            );
          },
        )}
      </div>
    </section>
  );
}