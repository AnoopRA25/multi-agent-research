import { useEffect, useRef, useState } from "react";
import { animate } from "animejs";

interface ResearchInputProps {
  onSubmit: (query: string) => void;
  loading?: boolean;
}

export default function ResearchInput({
  onSubmit,
  loading = false,
}: ResearchInputProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const [query, setQuery] = useState("");

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    animate(containerRef.current, {
      opacity: [0, 1],
      translateY: [30, 0],
      duration: 900,
      ease: "outExpo",
    });
  }, []);

  const handleSubmit = () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery || loading) {
      return;
    }

    onSubmit(trimmedQuery);
  };

  const handleButtonEnter = () => {
    if (!buttonRef.current || loading) {
      return;
    }

    animate(buttonRef.current, {
      scale: 1.04,
      duration: 250,
      ease: "outQuad",
    });
  };

  const handleButtonLeave = () => {
    if (!buttonRef.current || loading) {
      return;
    }

    animate(buttonRef.current, {
      scale: 1,
      duration: 250,
      ease: "outQuad",
    });
  };

  return (
    <div ref={containerRef} className="research-input-container">
      <div className="research-input-glow" />

      <div className="research-input-card">
        <div className="research-input-header">
          <span className="research-input-icon">✦</span>

          <div>
            <h2>What do you want to research?</h2>
            <p>
              Ask a question and let the research agents investigate it.
            </p>
          </div>
        </div>

        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Example: What are the latest applications of AI in healthcare?"
          rows={4}
          disabled={loading}
        />

        <div className="research-input-footer">
          <span>
            {query.length > 0
              ? `${query.length} characters`
              : "Enter a research question"}
          </span>

          <button
            ref={buttonRef}
            type="button"
            onClick={handleSubmit}
            onMouseEnter={handleButtonEnter}
            onMouseLeave={handleButtonLeave}
            disabled={loading || !query.trim()}
          >
            {loading ? "Researching..." : "Start Research"}
            <span>→</span>
          </button>
        </div>
      </div>
    </div>
  );
}