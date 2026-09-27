import { useEffect, useRef, useState } from "react";
import { animate } from "animejs";

import ResearchInput from "./ResearchInput";
import AgentTimeline from "./AgentTimeline";

import {
  getExecutions,
  getRun,
  type AgentExecution,
  type RunResponse,
  submitResearch,
} from "../services/api";


export default function Dashboard() {
  const heroRef = useRef<HTMLDivElement>(null);

  const [run, setRun] = useState<RunResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [executions, setExecutions] = useState<AgentExecution[]>([]);


  useEffect(() => {
    if (!heroRef.current) {
      return;
    }

    animate(heroRef.current, {
      opacity: [0, 1],
      translateY: [20, 0],
      duration: 800,
      ease: "outExpo",
    });
  }, []);


  const handleResearch = async (query: string) => {
    setLoading(true);
    setError("");
    setRun(null);
    setExecutions([]);

    try {
      const job = await submitResearch(query);

      const initialRun = await getRun(job.run_id);

      setRun(initialRun);

      pollRun(job.run_id);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong.",
      );

      setLoading(false);
    }
  };


  const pollRun = async (runId: number) => {
    try {
      const currentRun = await getRun(runId);

      setRun(currentRun);

      if (
        currentRun.status === "completed" ||
        currentRun.status === "failed"
      ) {
        try {
          const executionData = await getExecutions(runId);

          setExecutions(
            executionData.executions,
          );
        } catch {
          // Report remains usable if execution history fails.
        }

        setLoading(false);
        return;
      }

      setTimeout(() => {
        pollRun(runId);
      }, 2000);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to check research status.",
      );

      setLoading(false);
    }
  };


  return (
    <main className="dashboard">

      {/* Navigation */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-mark">
            ✦
          </div>

          <span className="brand-name">
            ResearchAI
          </span>

        </div>


        <div className="nav-status">

          <span className="status-dot" />

          System Online

        </div>

      </nav>


      {/* Hero */}

      <section
        ref={heroRef}
        className="hero"
      >

        <div className="hero-badge">
          ✦ Multi-Agent Research System
        </div>


        <h1>
          Research anything.
          <br />

          <span>
            Let AI investigate.
          </span>
        </h1>


        <p>
          Ask a research question and let a team
          of specialized AI agents investigate,
          analyze, write, and critique the results.
        </p>

      </section>


      {/* Research Input */}

      <ResearchInput
        onSubmit={handleResearch}
        loading={loading}
      />


      {/* Error */}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      {/* Research Result */}

      {run && (
        <section className="research-status">

          <div className="status-card">

            <div className="status-card-header">

              <span>
                Research Job
              </span>


              <span
                className={`job-status ${run.status}`}
              >
                {run.status}
              </span>

            </div>


            <p className="job-query">
              {run.query}
            </p>


            {run.status === "running" && (
              <div className="research-loading">

                <div className="loading-spinner" />

                <span>
                  AI agents are researching...
                </span>

              </div>
            )}


            {run.status === "completed" && (
              <div className="report-preview">

                <h2>
                  Research Report
                </h2>


                <pre>
                  {run.report}
                </pre>

              </div>
            )}


            {run.status === "failed" && (
              <div className="failure-message">

                <strong>
                  Research failed
                </strong>

                <p>
                  {run.critique}
                </p>

              </div>
            )}

          </div>


          {/* Agent Timeline */}

          {run.status === "completed" && (
            <AgentTimeline
              executions={executions}
            />
          )}

        </section>
      )}

    </main>
  );
}