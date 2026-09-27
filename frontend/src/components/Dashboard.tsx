import {
  useEffect,
  useRef,
  useState,
} from "react";

import { animate } from "animejs";

import ResearchInput from "./ResearchInput";
import AgentTimeline from "./AgentTimeline";
import ReportViewer from "./ReportViewer";
import SourceCards from "./SourceCards";
import HistoryPanel from "./HistoryPanel";
import EvaluationPanel from "./EvaluationPanel";

import {
  getEvaluation,
  getExecutions,
  getRun,
  getRuns,
  getSources,
  type AgentExecution,
  type Evaluation,
  type ResearchRunSummary,
  type ResearchSource,
  type RunResponse,
  submitResearch,
} from "../services/api";


export default function Dashboard() {

  const heroRef =
    useRef<HTMLDivElement>(null);


  const [run, setRun] =
    useState<RunResponse | null>(null);


  const [runs, setRuns] =
    useState<ResearchRunSummary[]>([]);


  const [evaluation, setEvaluation] =
    useState<Evaluation | null>(null);


  const [loading, setLoading] =
    useState(false);


  const [error, setError] =
    useState("");


  const [executions, setExecutions] =
    useState<AgentExecution[]>([]);


  const [sources, setSources] =
    useState<ResearchSource[]>([]);


  /* =========================
     HERO ANIMATION
  ========================= */

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


  /* =========================
     LOAD HISTORY
  ========================= */

  useEffect(() => {

    loadHistory();

  }, []);


  const loadHistory = async () => {

    try {

      const data =
        await getRuns();

      setRuns(
        data.runs,
      );

    } catch {

      // History is optional.

    }

  };


  /* =========================
     LOAD EVALUATION
  ========================= */

  const loadEvaluation = async (
    runId: number,
  ) => {

    try {

      const data =
        await getEvaluation(runId);

      /*
       * The backend returns the
       * evaluation object directly.
       */

      setEvaluation(data);

    } catch {

      setEvaluation(null);

    }

  };


  /* =========================
     LOAD EXISTING RUN
  ========================= */

  const loadRunDetails = async (
    runId: number,
  ) => {

    setError("");

    setEvaluation(null);

    setExecutions([]);

    setSources([]);


    try {

      const currentRun =
        await getRun(runId);


      setRun(
        currentRun,
      );


      const executionData =
        await getExecutions(runId);


      setExecutions(
        executionData.executions,
      );


      const sourceData =
        await getSources(runId);


      setSources(
        sourceData.sources,
      );


      if (
        currentRun.status ===
        "completed"
      ) {

        await loadEvaluation(
          runId,
        );

      }

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load research run.",
      );

    }

  };


  /* =========================
     START NEW RESEARCH
  ========================= */

  const handleResearch = async (
    query: string,
  ) => {

    setLoading(true);

    setError("");

    setRun(null);

    setEvaluation(null);

    setExecutions([]);

    setSources([]);


    try {

      const job =
        await submitResearch(
          query,
        );


      const initialRun =
        await getRun(
          job.run_id,
        );


      setRun(
        initialRun,
      );


      pollRun(
        job.run_id,
      );

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong.",
      );

      setLoading(false);

    }

  };


  /* =========================
     POLL RUN STATUS
  ========================= */

  const pollRun = async (
    runId: number,
  ) => {

    try {

      const currentRun =
        await getRun(runId);


      setRun(
        currentRun,
      );


      /* =========================
         COMPLETED / FAILED
      ========================= */

      if (
        currentRun.status ===
          "completed" ||
        currentRun.status ===
          "failed"
      ) {


        /* =========================
           LOAD EXECUTIONS
        ========================= */

        try {

          const executionData =
            await getExecutions(
              runId,
            );


          setExecutions(
            executionData.executions,
          );

        } catch {

          // Optional.

        }


        /* =========================
           LOAD SOURCES
        ========================= */

        try {

          const sourceData =
            await getSources(
              runId,
            );


          setSources(
            sourceData.sources,
          );

        } catch {

          // Optional.

        }


        /* =========================
           LOAD EVALUATION
        ========================= */

        if (
          currentRun.status ===
          "completed"
        ) {

          await loadEvaluation(
            runId,
          );

        }


        /* =========================
           REFRESH HISTORY
        ========================= */

        await loadHistory();


        setLoading(false);

        return;

      }


      /* =========================
         CONTINUE POLLING
      ========================= */

      setTimeout(() => {

        pollRun(
          runId,
        );

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


  /* =========================
     UI
  ========================= */

  return (

    <main className="dashboard">


      {/* =========================
          NAVBAR
      ========================= */}

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


      {/* =========================
          HERO
      ========================= */}

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

          Ask a research question and let a
          team of specialized AI agents
          investigate, analyze, write, and
          critique the results.

        </p>

      </section>


      {/* =========================
          RESEARCH INPUT
      ========================= */}

      <ResearchInput
        onSubmit={handleResearch}
        loading={loading}
      />


      {/* =========================
          ERROR
      ========================= */}

      {error && (

        <div className="error-message">

          {error}

        </div>

      )}


      {/* =========================
          RESEARCH HISTORY
      ========================= */}

      <HistoryPanel
        runs={runs}
        onSelect={loadRunDetails}
      />


      {/* =========================
          CURRENT RESEARCH RUN
      ========================= */}

      {run && (

        <section className="research-status">


          {/* =========================
              RUN RESULT / STATUS
          ========================= */}

          <div className="status-card">

            <div className="status-card-header">

              <div>

                <span className="section-eyebrow">
                  RESEARCH RUN
                </span>

                <h2>
                  Research Result
                </h2>

              </div>


              <span
                className={`job-status ${run.status}`}
              >

                {run.status}

              </span>

            </div>


            {/* =========================
                QUERY
            ========================= */}

            <div className="job-query-container">

              <span className="section-eyebrow">
                RESEARCH QUESTION
              </span>

              <p className="job-query">

                {run.query}

              </p>

            </div>


            {/* =========================
                RUNNING
            ========================= */}

            {run.status ===
              "running" && (

              <div className="research-loading">

                <div className="loading-spinner" />

                <span>

                  AI agents are researching...

                </span>

              </div>

            )}


            {/* =========================
                COMPLETED
            ========================= */}

            {run.status ===
              "completed" && (

              <ReportViewer
                report={run.report}
                critique={run.critique}
              />

            )}


            {/* =========================
                FAILED
            ========================= */}

            {run.status ===
              "failed" && (

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


          {/* =========================
              COMPLETED RUN DETAILS
          ========================= */}

          {run.status ===
            "completed" && (

            <>

              {/* =====================
                  RESEARCH QUALITY
                  IMMEDIATELY AFTER
                  THE RUN RESULT
              ===================== */}

              <EvaluationPanel
                evaluation={evaluation}
              />


              {/* =====================
                  AGENT ACTIVITY
              ===================== */}

              <AgentTimeline
                executions={executions}
              />


              {/* =====================
                  SOURCES
              ===================== */}

              <SourceCards
                sources={sources}
              />

            </>

          )}

        </section>

      )}

    </main>

  );

}