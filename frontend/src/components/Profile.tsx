import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Profile as ProfileType, User } from "../types/api";
import AnimalCard from "./AnimalCard";
import StatsCard from "./StatsCard";

type Props = {
  user: User;
};

export default function Profile({ user }: Props) {
  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getProfile(user.id)
      .then(setProfile)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load profile."));
  }, [user.id]);

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!profile) {
    return <p className="status">Loading profile...</p>;
  }

  return (
    <section className="stack-page">
      <div className="page-title">
        <p className="eyebrow">Profile</p>
        <h1>{profile.username}</h1>
      </div>
      <div className="stats-grid">
        <StatsCard label="Points" value={profile.total_points} />
        <StatsCard label="Rank" value={profile.current_rank} />
        <StatsCard label="Current streak" value={profile.current_streak} />
        <StatsCard label="Best streak" value={profile.best_streak} />
      </div>
      <section>
        <h2>Collected animal cards</h2>
        <div className="card-grid">
          {profile.collected_cards.length > 0 ? (
            profile.collected_cards.map((card, index) => <AnimalCard key={`${card.id}-${index}`} card={card} />)
          ) : (
            <p className="notice">No cards yet. Complete a daily action to unlock your first one.</p>
          )}
        </div>
      </section>
      <section className="two-column">
        <div>
          <h2>Recent actions</h2>
          <ul className="history-list">
            {profile.recent_actions.map((action) => (
              <li key={action.id}>
                <strong>{action.tip_title}</strong>
                <span>{new Date(action.completed_at).toLocaleDateString()} · +{action.points_awarded} point</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h2>Favorite animals helped</h2>
          <ul className="history-list">
            {profile.favorite_animals.map((animal) => (
              <li key={animal.animal_name}>
                <strong>{animal.animal_name}</strong>
                <span>{animal.help_count} helpful action{animal.help_count === 1 ? "" : "s"}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </section>
  );
}
