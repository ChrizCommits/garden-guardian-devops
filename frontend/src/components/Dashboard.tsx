import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { CompleteResult, TodayTip, User } from "../types/api";
import AnimalCard from "./AnimalCard";
import StatsCard from "./StatsCard";
import TipCard from "./TipCard";

type Props = {
  user: User;
  onUserUpdate: (user: User) => void;
};

export default function Dashboard({ user, onUserUpdate }: Props) {
  const [tip, setTip] = useState<TodayTip | null>(null);
  const [result, setResult] = useState<CompleteResult | null>(null);
  const [encouragement, setEncouragement] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isWorking, setIsWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getToday()
      .then(setTip)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load today's tip."))
      .finally(() => setIsLoading(false));
  }, []);

  async function intend() {
    if (!tip) return;
    setIsWorking(true);
    setError(null);
    try {
      const response = await api.intendTip(tip.id, user.id);
      setEncouragement(response.message);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save your intention.");
    } finally {
      setIsWorking(false);
    }
  }

  async function complete() {
    if (!tip) return;
    setIsWorking(true);
    setError(null);
    try {
      const completion = await api.completeTip(tip.id, user.id);
      setResult(completion);
      onUserUpdate({
        ...user,
        total_points: completion.total_points,
        current_rank: completion.current_rank,
        current_streak: completion.current_streak,
        best_streak: completion.best_streak
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not complete this action.");
    } finally {
      setIsWorking(false);
    }
  }

  if (isLoading) {
    return <p className="status">Loading today&apos;s garden tip...</p>;
  }

  if (error && !tip) {
    return <p className="error">{error}</p>;
  }

  if (!tip) {
    return <p className="error">No seasonal tip is available.</p>;
  }

  return (
    <section className="dashboard">
      <div className="page-title">
        <p className="eyebrow">Welcome, {user.username}</p>
        <h1>Today in the garden</h1>
      </div>
      <div className="stats-grid">
        <StatsCard label="Points" value={result?.total_points ?? user.total_points} />
        <StatsCard label="Rank" value={result?.current_rank ?? user.current_rank} />
        <StatsCard label="Streak" value={`${result?.current_streak ?? user.current_streak} day`} />
      </div>
      <div className="dashboard-grid">
        <div>
          <TipCard tip={tip} />
          <div className="button-row">
            <button type="button" onClick={intend} disabled={isWorking}>I&apos;ll do this</button>
            <button className="primary" type="button" onClick={complete} disabled={isWorking}>
              {isWorking ? "Saving..." : "Done"}
            </button>
          </div>
          {encouragement ? <p className="success">{encouragement}</p> : null}
          {error ? <p className="error">{error}</p> : null}
          {result ? <p className={result.awarded ? "success" : "notice"}>{result.message}</p> : null}
        </div>
        <aside className="side-panel">
          <h2>Possible card rewards</h2>
          <div className="mini-card-list">
            {tip.possible_reward_cards.slice(0, 3).map((card) => (
              <AnimalCard key={card.id} card={card} />
            ))}
          </div>
        </aside>
      </div>
      {result?.unlocked_card ? (
        <section className="unlock-section">
          <p className="eyebrow">Unlocked</p>
          <AnimalCard card={result.unlocked_card} />
        </section>
      ) : null}
    </section>
  );
}
