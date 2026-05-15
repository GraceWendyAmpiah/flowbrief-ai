export default function UrgencyBadge({ value }) {
  const cls = value === 'High' ? 'badge--high' : value === 'Medium' ? 'badge--medium' : 'badge--low'
  return <span className={`badge ${cls}`}>{value}</span>
}
