type Props = {
  label: string;
  value: string | number;
};

export default function StatsCard({ label, value }: Props) {
  return (
    <div className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
