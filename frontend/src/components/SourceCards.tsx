import { useEffect, useRef } from "react";
import { animate } from "animejs";

import type { ResearchSource } from "../services/api";


interface SourceCardsProps {
  sources: ResearchSource[];
}


export default function SourceCards({
  sources,
}: SourceCardsProps) {
  const containerRef =
    useRef<HTMLDivElement>(null);


  useEffect(() => {
    if (
      !containerRef.current ||
      sources.length === 0
    ) {
      return;
    }

    const cards =
      containerRef.current.querySelectorAll(
        ".source-card",
      );

    animate(cards, {
      opacity: [0, 1],
      translateY: [15, 0],
      delay: 80,
      duration: 450,
      ease: "outExpo",
    });
  }, [sources]);


  if (sources.length === 0) {
    return null;
  }


  return (
    <section
      ref={containerRef}
      className="sources-section"
    >

      <div className="sources-header">

        <div>
          <span className="section-eyebrow">
            RESEARCH EVIDENCE
          </span>

          <h2>
            Sources
          </h2>
        </div>

        <span className="source-count">
          {sources.length} sources
        </span>

      </div>


      <div className="source-grid">

        {sources.map((source) => (
          <a
            key={source.id}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="source-card"
          >

            <div className="source-card-top">

              <span className="source-icon">
                ↗
              </span>

              <span className="source-domain">
                {new URL(source.url).hostname}
              </span>

            </div>


            <h3>
              {source.title}
            </h3>


            <p>
              {source.snippet}
            </p>


            <div className="source-link">
              Open source
              <span>→</span>
            </div>

          </a>
        ))}

      </div>

    </section>
  );
}