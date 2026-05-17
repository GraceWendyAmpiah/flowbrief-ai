import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import Icon from '../components/Icon'
import CategoryBadge from '../components/CategoryBadge'
import UrgencyBadge from '../components/UrgencyBadge'
import EscalationAlert from '../components/EscalationAlert'
import FieldExtractDisplay from '../components/FieldExtractDisplay'
import ReportView from '../components/ReportView'
import { getCase } from '../api/client'

function truncate(s, n) { return s.length > n ? s.slice(0, n) + '…' : s }

function formatDate(iso) {
  const d = new Date(iso)
  const day = String(d.getDate()).padStart(2, '0')
  const mon = d.toLocaleString('en-GB', { month: 'short' })
  const year = d.getFullYear()
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${day} ${mon} ${year} · ${hh}:${mm}`
}

export default function Report() {
  const { case_id } = useParams()
  const navigate = useNavigate()
  const [caseData, setCaseData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getCase(case_id)
      .then((res) => { setCaseData(res); setLoading(false) })
      .catch((err) => { setError(err.message); setLoading(false) })
  }, [case_id])

  const handleExportPdf = () => {
    if (!caseData) return
    const blob = new Blob([caseData.handoff_report], {
      type: 'text/markdown'
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `handoff_${caseData.case_id.slice(0, 8)}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  const crumb = [
    { label: 'Home', href: '/' },
    { label: 'Cases', href: '/history' },
    { label: truncate(case_id.replace('CASE-WAF-2026-', ''), 14) },
  ]

  if (loading) {
    return (
      <>
        <Topbar crumb={crumb} meta={<span className="mono" style={{ fontSize: 11 }}>{case_id}</span>}/>
        <div className="page">
          <div style={{ padding: 'var(--s-10)', textAlign: 'center', color: 'var(--c-text-3)', fontSize: 13 }}>
            Loading case…
          </div>
        </div>
      </>
    )
  }

  if (error && !caseData) {
    return (
      <>
        <Topbar crumb={crumb} meta={null}/>
        <div className="page">
          <div className="page__head">
            <div>
              <h1 className="page__title">Case not found</h1>
              <div className="page__subtitle muted">{case_id}</div>
            </div>
            <div className="page__head-actions">
              <button type="button" className="btn" onClick={() => navigate('/')}>
                <Icon name="arrow-left" size={14}/> Back
              </button>
            </div>
          </div>
        </div>
      </>
    )
  }

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
            <button type="button" className="btn" onClick={() => navigate('/')}>
              <Icon name="arrow-left" size={14}/> Back
            </button>
            <button type="button" className="btn"><Icon name="print" size={14}/> Print</button>
            <button
              type="button"
              className="btn"
              onClick={handleExportPdf}
            >
              <Icon name="download" size={14}/> Download Report
            </button>
          </div>
        </div>

        <div className="statusbar">
          <div className="statusbar__field">
            <span className="label">Case ID</span>
            <span className="value mono">{caseData.case_id}</span>
          </div>
          <div className="statusbar__divider"/>
          <div className="statusbar__field">
            <span className="label">Created</span>
            <span className="value">{formatDate(caseData.created_at)}</span>
          </div>
          <div className="statusbar__divider"/>
          <div className="statusbar__badges">
            <CategoryBadge value={caseData.classification}/>
            <UrgencyBadge value={caseData.urgency}/>
          </div>
        </div>

        {caseData.urgency === 'High' && <EscalationAlert/>}

        <div className="section-title">
          <h2>Extracted Fields</h2>
          <div className="rule"/>
          <span className="muted" style={{ fontSize: 11 }}>Auto-extracted · Human verification required</span>
        </div>

        <FieldExtractDisplay caseData={caseData}/>

        <div className="section-title" style={{ marginTop: 'var(--s-6)' }}>
          <h2>Handoff Report</h2>
          <div className="rule"/>
        </div>

        <div className="handoff">
          <div className="handoff__head">
            <span className="label">Document</span>
            <span className="muted" style={{ fontSize: 11 }}>{caseData.case_id}_handoff.md</span>
          </div>
          <ReportView markdown={caseData.handoff_report}/>
        </div>
      </div>
    </>
  )
}
