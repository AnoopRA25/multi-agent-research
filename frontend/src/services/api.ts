const API_BASE_URL = "http://127.0.0.1:8000";


export interface QueryResponse {
  run_id: number;

  status:
    | "queued"
    | "running"
    | "completed"
    | "failed";
}


export interface RunResponse {
  run_id: number;

  query: string;

  status:
    | "queued"
    | "running"
    | "completed"
    | "failed";

  report: string;

  critique: string;

  latency_ms: number;
}


export interface AgentExecution {
  id: number;

  run_id: number;

  agent_name: string;

  status: string;

  latency_ms: number | null;

  input_tokens: number | null;

  output_tokens: number | null;

  estimated_cost_usd: number | null;

  created_at: string;
}


export interface ExecutionsResponse {
  run_id: number;

  executions: AgentExecution[];
}


export interface ResearchSource {
  id: number;

  run_id: number;

  title: string;

  url: string;

  snippet: string;

  created_at: string;
}


export interface SourcesResponse {
  run_id: number;

  sources: ResearchSource[];
}


export interface ResearchRunSummary {
  id: number;

  query: string;

  status: string;

  report: string | null;

  critique: string | null;

  latency_ms: number | null;

  created_at: string;
}


export interface RunsResponse {
  runs: ResearchRunSummary[];
}


/* =========================
   EVALUATION
========================= */

export interface Evaluation {
  evaluation_id?: number;

  id: number;

  run_id: number;

  relevance_score: number;

  completeness_score: number;

  evidence_score: number;

  factuality_score: number;

  overall_score: number;

  feedback: string | null;

  created_at: string;
}


export type EvaluationResponse =
  Evaluation | null;


/* =========================
   RESEARCH
========================= */

export async function submitResearch(
  query: string,
): Promise<QueryResponse> {

  const response = await fetch(
    `${API_BASE_URL}/query`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        query,
      }),
    },
  );


  if (!response.ok) {
    throw new Error(
      "Failed to submit research request.",
    );
  }


  return response.json();
}


/* =========================
   RUN
========================= */

export async function getRun(
  runId: number,
): Promise<RunResponse> {

  const response = await fetch(
    `${API_BASE_URL}/runs/${runId}`,
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch research job.",
    );
  }


  return response.json();
}


/* =========================
   AGENT EXECUTIONS
========================= */

export async function getExecutions(
  runId: number,
): Promise<ExecutionsResponse> {

  const response = await fetch(
    `${API_BASE_URL}/runs/${runId}/executions`,
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch agent executions.",
    );
  }


  return response.json();
}


/* =========================
   SOURCES
========================= */

export async function getSources(
  runId: number,
): Promise<SourcesResponse> {

  const response = await fetch(
    `${API_BASE_URL}/runs/${runId}/sources`,
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch research sources.",
    );
  }


  return response.json();
}


/* =========================
   HISTORY
========================= */

export async function getRuns(): Promise<RunsResponse> {

  const response = await fetch(
    `${API_BASE_URL}/runs`,
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch research history.",
    );
  }


  return response.json();
}


/* =========================
   EVALUATION
========================= */

export async function getEvaluation(
  runId: number,
): Promise<EvaluationResponse> {

  const response = await fetch(
    `${API_BASE_URL}/evaluate/${runId}`,
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch evaluation.",
    );
  }


  return response.json();
}