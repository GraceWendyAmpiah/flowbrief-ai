export default function ConfidenceScore({ value }) {
  const v = Math.max(0, Math.min(100, value))
  const tone = v >= 75 ? 'green' : v >= 50 ? 'amber' : 'red'
  return (
    <div className="confidence" role="meter" aria-valuenow={v} aria-valuemin="0" aria-valuemax="100">
      <div className="confidence__track">
        <div className={`confidence__fill confidence__fill--${tone}`} style={{ width: `${v}%` }} />
      </div>
      <div className="confidence__label">{v}%</div>
    </div>
  )
}
