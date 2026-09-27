import { useEffect, useRef } from "react";
import { animate } from "animejs";

interface Evaluation {
  relevance_score: number;
  completeness_score: number;
  evidence_score: number;
  factuality_score: number;
  overall_score: number;
  feedback: string | null;
}

interface EvaluationPanelProps {
  evaluation: Evaluation | null;
}

function ScoreCard({
  label,
  score,
}: {
  label: string;
  score: number;
}) {
  const percentage = Math.min(
    Math.max(score * 10, 0),
    100,
  );

  return (
    <div className="evaluation-score-card">

      <div className="evaluation-score-top">
        <span>{label}</span>

        <strong>
          {score.toFixed(1)}
        </strong>
      </div>

      <div className="evaluation-score-bar">
        <div
          className="evaluation-score-fill"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

      <span className="evaluation-score-max">
        / 10
      </span>

    </div>
  );
}


export default function EvaluationPanel({
  evaluation,
}: EvaluationPanelProps) {
  const panelRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!panelRef.current || !evaluation) {
      return;
    }

    animate(panelRef.current, {
      opacity: [0, 1],
      translateY: [20, 0],
      duration: 600,
      ease: "outExpo",
    });
  }, [evaluation]);


  if (!evaluation) {
    return null;
  }


  return (
    <section
      ref={panelRef}
      className="evaluation-panel"
    >

      <div className="evaluation-header">

        <div>
          <span className="section-eyebrow">
            AI QUALITY EVALUATION
          </span>

          <h2>
            Research Quality
          </h2>
        </div>


        <div className="evaluation-overall">

          <span>
            Overall
          </span>

          <strong>
            {evaluation.overall_score.toFixed(1)}
          </strong>

          <small>
            / 10
          </small>

        </div>

      </div>


      <div className="evaluation-grid">

        <ScoreCard
          label="Relevance"
          score={evaluation.relevance_score}
        />

        <ScoreCard
          label="Completeness"
          score={evaluation.completeness_score}
        />

        <ScoreCard
          label="Evidence"
          score={evaluation.evidence_score}
        />

        <ScoreCard
          label="Factuality"
          score={evaluation.factuality_score}
        />

      </div>


      {evaluation.feedback && (
        <div className="evaluation-feedback">

          <div className="evaluation-feedback-icon">
            ✓
          </div>

          <div>

            <span className="section-eyebrow">
              EVALUATOR FEEDBACK
            </span>

            <p>
              {evaluation.feedback}
            </p>

          </div>

        </div>
      )}

    </section>
  );
}