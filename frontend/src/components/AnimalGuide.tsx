import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Animal } from "../types/api";

export default function AnimalGuide() {
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getAnimals()
      .then(setAnimals)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load animals."))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <p className="status">Loading animal guide...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <section className="stack-page">
      <div className="page-title">
        <p className="eyebrow">Guide</p>
        <h1>Supported animals</h1>
      </div>
      <div className="guide-grid">
        {animals.map((animal) => (
          <article className="guide-item" key={animal.id}>
            <span className="guide-badge">{animal.name.slice(0, 2).toUpperCase()}</span>
            <div>
              <p className="eyebrow">{animal.category}</p>
              <h2>{animal.name}</h2>
              <p>{animal.description}</p>
              <strong>Safe support</strong>
              <p>{animal.safe_support_notes}</p>
              <strong>What not to feed or do</strong>
              <p>{animal.unsafe_foods}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
