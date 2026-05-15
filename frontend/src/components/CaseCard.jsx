import { useNavigate } from 'react-router-dom'
import CategoryBadge from './CategoryBadge'
import UrgencyBadge from './UrgencyBadge'

function relTime(ts) {
  const diff = Math.max(0, Math.round((Date.now() - ts) / 1000))
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.round(diff / 60)} min ago`
  if (diff < 86400) return `${Math.round(diff / 3600)} hours ago`
  const d = Math.round(diff / 86400)
  return d === 1 ? '1 day ago' : `${d} days ago`
}

export default function CaseCard({ id, classification, urgency, customer, requestType, created }) {
  const navigate = useNavigate()
  return (
    <button className="recent-row" onClick={() => navigate(`/cases/${id}`)}>
      <span className="recent-row__id">{id}</span>
      <CategoryBadge value={classification}/>
      <UrgencyBadge value={urgency}/>
      <span className="muted" style={{ fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
        {customer} — {requestType}
      </span>
      <span className="recent-row__time">{relTime(created)}</span>
    </button>
  )
}
