import { useParams, useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import Icon from '../components/Icon'

// TODO Phase 22 — wire getCase API call

function truncate(s, n) { return s.length > n ? s.slice(0, n) + '…' : s }

export default function Report() {
  const { case_id } = useParams()
  const navigate = useNavigate()

  const crumb = [
    { label: 'Home', href: '/' },
    { label: 'Cases', href: '/history' },
    { label: truncate(case_id.replace('CASE-WAF-2026-', ''), 14) },
  ]

  return (
    <>
      <Topbar crumb={crumb} meta={<span className="mono" style={{ fontSize: 11 }}>{case_id}</span>}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">Case Report</h1>
            <div className="page__subtitle">AI-extracted handoff document · Verify all fields before processing</div>
          </div>
          <div className="page__head-actions">
            <button className="btn" onClick={() => navigate('/')}>
              <Icon name="arrow-left" size={14}/> Back
            </button>
            <button className="btn"><Icon name="print" size={14}/> Print</button>
            <button className="btn"><Icon name="download" size={14}/> Export PDF</button>
          </div>
        </div>

        {/* Status bar placeholder */}
        <div className="statusbar">
          <div className="statusbar__field">
            <span className="label">Case ID</span>
            <span className="value mono">{case_id}</span>
          </div>
          <div className="statusbar__divider"/>
          <div className="statusbar__field">
            <span className="label">Status</span>
            <span className="value muted">Loading…</span>
          </div>
        </div>

        {/* Extracted fields placeholder */}
        <div className="section-title">
          <h2>Extracted Fields</h2>
          <div className="rule"/>
          <span className="muted" style={{ fontSize: 11 }}>Auto-extracted · Human verification required</span>
        </div>
        <div className="panel panel--pad" style={{ color: 'var(--c-text-3)', fontSize: 13 }}>
          Loading case data…
        </div>

        {/* Handoff Report placeholder */}
        <div className="section-title" style={{ marginTop: 'var(--s-6)' }}>
          <h2>Handoff Report</h2>
          <div className="rule"/>
        </div>
        <div className="handoff">
          <div className="handoff__head">
            <span className="label">Document</span>
          </div>
          <div className="handoff__body" style={{ color: 'var(--c-text-3)' }}>
            Loading report…
          </div>
        </div>
      </div>
    </>
  )
}
