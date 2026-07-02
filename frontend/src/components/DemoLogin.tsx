import { FormEvent, useState } from "react";
import { api } from "../api/client";
import type { User } from "../types/api";

type Props = {
  onLogin: (user: User) => void;
};

export default function DemoLogin({ onLogin }: Props) {
  const [username, setUsername] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const user = await api.demoLogin(username);
      onLogin(user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not start the demo session.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="login-layout">
      <div className="intro-panel">
        <p className="eyebrow">Kind, seasonal, responsible</p>
        <h1>GardenGuardian</h1>
        <p>Track simple wildlife-support actions, collect animal cards, and build a gentle garden habit.</p>
      </div>
      <form className="login-card" onSubmit={submit}>
        <h2>Demo login</h2>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          placeholder="e.g. meadow"
          autoComplete="username"
        />
        {error ? <p className="error">{error}</p> : null}
        <button className="primary" type="submit" disabled={isLoading || username.trim().length === 0}>
          {isLoading ? "Starting..." : "Start"}
        </button>
        <p className="fine-print">Username-only demo access. No password or email is used.</p>
      </form>
    </section>
  );
}
