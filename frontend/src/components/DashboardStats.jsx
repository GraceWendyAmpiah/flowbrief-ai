export default function DashboardStats({ totalCases, highPriority, avgConfidence, missingDocCount }) {
  return (
    <div className="stats">
      <div className="stat">
        <span className="stat__label label">Total Cases Processed</span>
        <span className="stat__value">{(totalCases || 0).toLocaleString()}</span>
        <span className="stat__sub">All time · across all teams</span>
      </div>
      <div className="stat">
        <span className="stat__label label">High Priority Cases</span>
        <span className={`stat__value ${highPriority > 0 ? 'stat__value--red' : ''}`}>{highPriority || 0}</span>
        <span className="stat__sub">{highPriority > 0 ? 'Requires immediate escalation' : 'No high-priority items'}</span>
      </div>
      <div className="stat">
        <span className="stat__label label">Average Confidence</span>
        <span className="stat__value">{avgConfidence || 0}%</span>
        <span className="stat__sub">Mean across AI extractions</span>
      </div>
      <div className="stat">
        <span className="stat__label label">Missing Document Instances</span>
        <span className="stat__value">{missingDocCount || 0}</span>
        <span className="stat__sub">Total across open cases</span>
      </div>
    </div>
  )
}
