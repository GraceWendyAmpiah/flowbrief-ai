import Topbar from '../components/Topbar'
import DashboardStats from '../components/DashboardStats'
import Icon from '../components/Icon'

// TODO Phase 23 — wire getDashboard API call

const CRUMB = [{ label: 'Home', href: '/' }, { label: 'Dashboard' }]

export default function Dashboard() {
  return (
    <>
      <Topbar crumb={CRUMB} meta={<span>Auto-refresh: 5 min</span>}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">Operations Dashboard</h1>
            <div className="page__subtitle">Live case queue metrics</div>
          </div>
          <div className="page__head-actions">
            <button className="btn"><Icon name="refresh" size={14}/> Refresh</button>
            <button className="btn"><Icon name="download" size={14}/> Export CSV</button>
          </div>
        </div>

        <DashboardStats
          totalCases={0}
          highPriority={0}
          avgConfidence={0}
          missingDocCount={0}
        />

        <div className="chart-panel">
          <div className="chart-panel__head">
            <div>
              <h3 className="panel__title">Cases by Category</h3>
              <div className="muted" style={{ fontSize: 11, marginTop: 2 }}>Distribution across the five classification buckets</div>
            </div>
            <div className="muted" style={{ fontSize: 11 }}>Range: All time</div>
          </div>
          <div className="chart-panel__body" style={{ height: 280, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--c-text-3)', fontSize: 13 }}>
            No data — connect API to populate chart
          </div>
        </div>
      </div>
    </>
  )
}
