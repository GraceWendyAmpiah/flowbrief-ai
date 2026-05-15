import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import CategoryBadge from '../components/CategoryBadge'
import UrgencyBadge from '../components/UrgencyBadge'
import ConfidenceScore from '../components/ConfidenceScore'
import Icon from '../components/Icon'

// TODO Phase 24 — wire listCases API call
// Change 5 applied: filter state initialised as '' (not 'All') to match option values

const CRUMB = [{ label: 'Home', href: '/' }, { label: 'Case History' }]

export default function History() {
  const navigate = useNavigate()
  const [q, setQ] = useState('')
  const [category, setCategory] = useState('')
  const [urgency, setUrgency] = useState('')
  const [page, setPage] = useState(1)

  useEffect(() => { setPage(1) }, [q, category, urgency])

  return (
    <>
      <Topbar crumb={CRUMB} meta={null}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">
              Case History
              <span className="count-badge">0 cases</span>
            </h1>
            <div className="page__subtitle">Searchable archive of all processed cases</div>
          </div>
          <div className="page__head-actions">
            <button className="btn"><Icon name="download" size={14}/> Export CSV</button>
          </div>
        </div>

        <div className="filterbar">
          <input
            className="input input--search"
            placeholder="Search raw document text, customer name, or case ID…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          <select className="select" value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="">All Categories</option>
            <option value="KYC">KYC</option>
            <option value="Complaint">Complaint</option>
            <option value="SME Advisory">SME Advisory</option>
            <option value="Trade Finance">Trade Finance</option>
            <option value="Account Opening">Account Opening</option>
          </select>
          <select className="select" value={urgency} onChange={(e) => setUrgency(e.target.value)}>
            <option value="">All Urgency</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <button className="btn" onClick={() => { setQ(''); setCategory(''); setUrgency('') }}>
            Clear
          </button>
        </div>

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Case ID</th>
                <th>Classification</th>
                <th>Urgency</th>
                <th>Confidence</th>
                <th>Customer</th>
                <th>Created</th>
                <th className="col-action">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', padding: 'var(--s-8)', color: 'var(--c-text-3)' }}>
                  No cases — connect API to load data
                </td>
              </tr>
            </tbody>
          </table>
          <div className="pagination">
            <div className="pagination__meta">Showing 0–0 of 0</div>
            <div className="pagination__pager">
              <button className="btn" disabled>
                <Icon name="chev-left" size={12}/> Previous
              </button>
              <div className="btn" style={{ fontVariantNumeric: 'tabular-nums', cursor: 'default', background: 'var(--c-bg-2)' }}>
                Page 1 of 1
              </div>
              <button className="btn" disabled>
                Next <Icon name="chev-right" size={12}/>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
