import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { EarnedAnimalCard, User } from "../types/api";
import AnimalCard from "./AnimalCard";

type Props = {
  user: User;
};

export default function CardCollection({ user }: Props) {
  const [cards, setCards] = useState<EarnedAnimalCard[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getCards(user.id)
      .then((response) => setCards(response.cards))
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load cards."))
      .finally(() => setIsLoading(false));
  }, [user.id]);

  if (isLoading) {
    return <p className="status">Loading card collection...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <section className="stack-page">
      <div className="page-title">
        <p className="eyebrow">Collection</p>
        <h1>Animal cards</h1>
      </div>
      <div className="card-grid">
        {cards.length > 0 ? (
          cards.map((card, index) => <AnimalCard key={`${card.id}-${index}`} card={card} />)
        ) : (
          <p className="notice">Complete a daily action to collect a matching animal card.</p>
        )}
      </div>
    </section>
  );
}
