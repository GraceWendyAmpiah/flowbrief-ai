import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import DashboardStats from '../components/DashboardStats'
import Icon from '../components/Icon'
import { getDashboard } from '../api/client'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, LabelList,
} from 'recharts'

const CRUMB = [{ label: 'Home', href: '/' }, { label: 'Dashboard' }]
const CATS = ['KYC', 'Complaint', 'SME Advisory', 'Trade Finance', 'Account Opening']

function fmtTime(d) {
  return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [refreshedAt, setRefreshedAt] = useState(new Date())

  const load = () => {
    setLoading(true)
    getDashboard()
      .then((res) => {
        setStats(res)
        setLoading(false)
        setRefreshedAt(new Date())
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }

  useEffect(() => { load() }, [])

  const chartData = stats
    ? CATS.map((name) => ({ name, count: stats.by_category?.[name] || 0 }))
    : []

  return (
    <>
      <Topbar crumb={CRUMB} meta={<span>Auto-refresh: 5 min</span>}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">Operations Dashboard</h1>
            <div className="page__subtitle">
              {loading ? 'Loading…' : `Last refreshed at ${fmtTime(refreshedAt)}`}
            </div>
          </div>
          <div className="page__head-actions">
            <button type="button" className="btn" onClick={load} disabled={loading}>
              <Icon name="refresh" size={14}/> Refresh
            </button>
            <button type="button" className="btn"><Icon name="download" size={14}/> Export CSV</button>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {loading && !stats ? (
          <div className="muted" style={{ textAlign: 'center', padding: 'var(--s-10)', fontSize: 13 }}>
            Loading dashboard…
          </div>
        ) : stats ? (
          <>
            <DashboardStats
              totalCases={stats.total_cases}
              highPriority={stats.high_priority_count}
              avgConfidence={stats.average_confidence}
              missingDocCount={stats.missing_document_count}
              onTotalCasesClick={() => navigate('/history')}
              onHighPriorityClick={() => navigate('/history?urgency=High')}
            />

            <div className="chart-panel">
              <div className="chart-panel__head">
                <div>
                  <h3 className="panel__title">Cases by Category</h3>
                  <div className="muted" style={{ fontSize: 11, marginTop: 2 }}>Distribution across the five classification buckets</div>
                  <div className="muted" style={{ fontSize: 11, marginTop: 2 }}>Click a bar to view cases by category</div>
                </div>
                <div className="muted" style={{ fontSize: 11 }}>Range: All time</div>
              </div>
              <div className="chart-panel__body" style={{ height: 280 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} layout="vertical" margin={{ top: 4, right: 40, bottom: 4, left: 8 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false}/>
                    <XAxis type="number" tick={{ fontSize: 11 }} allowDecimals={false}/>
                    <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 12 }}/>
                    <Tooltip/>
                    <Bar
                      dataKey="count"
                      fill="var(--c-blue)"
                      barSize={22}
                      radius={[0, 2, 2, 0]}
                      cursor="pointer"
                      onClick={(data) => {
                        navigate(`/history?category=${encodeURIComponent(data.name)}`)
                      }}
                    >
                      <LabelList
                        dataKey="count"
                        position="right"
                        style={{
                          fontSize: 12,
                          fill: 'var(--c-text)',
                          fontWeight: 600
                        }}
                      />
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        ) : null}
      </div>
    </>
  )
}
