import type { TodayTip } from "../types/api";

type Props = {
  tip: TodayTip;
};

export default function TipCard({ tip }: Props) {
  return (
    <article className="tip-card">
      <div className="tip-heading">
        <p className="eyebrow">{tip.month_or_season} tip</p>
        <span className="reward-pill">+{tip.points_reward} point</span>
      </div>
      <h2>{tip.title}</h2>
      <p>{tip.description}</p>
      <div className="action-box">
        <strong>Today&apos;s action</strong>
        <p>{tip.action_instruction}</p>
      </div>
      <div className="animal-chips" aria-label="Supported animals">
        {tip.supported_animals.map((animal) => (
          <span key={animal.id}>{animal.name}</span>
        ))}
      </div>
      <p className="warning">{tip.safety_warning}</p>
    </article>
  );
}
