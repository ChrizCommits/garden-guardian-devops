import type { AnimalCard as AnimalCardType, EarnedAnimalCard } from "../types/api";

type Props = {
  card: AnimalCardType | EarnedAnimalCard;
};

function initials(name: string) {
  return name.slice(0, 2).toUpperCase();
}

export default function AnimalCard({ card }: Props) {
  const earned = "earned_at" in card ? new Date(card.earned_at).toLocaleDateString() : null;

  return (
    <article className="animal-card">
      <div className="animal-art" aria-hidden="true">{initials(card.animal_name)}</div>
      <div>
        <div className="card-meta">
          <span>{card.rarity}</span>
          <span>{card.points_value} pt</span>
        </div>
        <h3>{card.title}</h3>
        <p className="animal-name">{card.animal_name}</p>
        <p>{card.fact}</p>
        {earned ? <small>Earned {earned}</small> : null}
      </div>
    </article>
  );
}
