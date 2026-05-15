import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import CategoryBadge from '../components/CategoryBadge'
import UrgencyBadge from '../components/UrgencyBadge'
import ConfidenceScore from '../components/ConfidenceScore'
import Icon from '../components/Icon'
import { listCases } from '../api/client'

const CRUMB = [{ label: 'Home', href: '/' }, { label: 'Case History' }]
const LIMIT = 20

function formatDate(iso) {
  const d = new Date(iso)
  const day = String(d.getDate()).padStart(2, '0')
  const mon = d.toLocaleString('en-GB', { month: 'short' })
  const year = d.getFullYear()
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${day} ${mon} ${year} · ${hh}:${mm}`
}

export default function History() {
  const navigate = useNavigate()
  const [cases, setCases] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')
  const [category, setCategory] = useState('')
  const [urgency, setUrgency] = useState('')
  const [page, setPage] = useState(1)

  useEffect(() => {
    setLoading(true)
    listCases({ search, category, urgency, page, limit: LIMIT })
      .then((res) => {
        setCases(res.cases)
        setTotal(res.total)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [search, category, urgency, page])

  const totalPages = Math.ceil(total / LIMIT) || 1
  const startItem = total === 0 ? 0 : (page - 1) * LIMIT + 1
  const endItem = Math.min(page * LIMIT, total)

  const handleSearch = () => {
    setSearch(searchInput)
    setPage(1)
  }

  const handleClear = () => {
    setSearch('')
    setSearchInput('')
    setCategory('')
    setUrgency('')
    setPage(1)
  }

  return (
    <>
      <Topbar crumb={CRUMB} meta={null}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">
              Case History
              <span className="count-badge">{total} {total === 1 ? 'case' : 'cases'}</span>
            </h1>
            <div className="page__subtitle">Searchable archive of all processed cases</div>
          </div>
          <div className="page__head-actions">
            <button type="button" className="btn"><Icon name="download" size={14}/> Export CSV</button>
          </div>
        </div>

        <div className="filterbar">
          <input
            className="input input--search"
            placeholder="Search raw document text, customer name, or case ID…"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleSearch() }}
          />
          <button type="button" className="btn" onClick={handleSearch}>
            <Icon name="search" size={14}/> Search
          </button>
          <select
            className="select"
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1) }}
          >
            <option value="">All Categories</option>
            <option value="KYC">KYC</option>
            <option value="Complaint">Complaint</option>
            <option value="SME Advisory">SME Advisory</option>
            <option value="Trade Finance">Trade Finance</option>
            <option value="Account Opening">Account Opening</option>
          </select>
          <select
            className="select"
            value={urgency}
            onChange={(e) => { setUrgency(e.target.value); setPage(1) }}
          >
            <option value="">All Urgency</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <button type="button" className="btn" onClick={handleClear}>
            Clear
          </button>
        </div>

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-id">Case ID</th>
                <th>Classification</th>
                <th>Urgency</th>
                <th className="col-conf">Confidence</th>
                <th>Created</th>
                <th className="col-action">Action</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', padding: 'var(--s-8)', color: 'var(--c-text-3)' }}>
                    Loading cases…
                  </td>
                </tr>
              ) : cases.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', padding: 'var(--s-8)', color: 'var(--c-text-3)' }}>
                    No cases match the current filters.
                  </td>
                </tr>
              ) : (
                cases.map((c) => (
                  <tr
                    key={c.case_id}
                    className="table-link"
                    onClick={() => navigate(`/cases/${c.case_id}`)}
                    style={{ cursor: 'pointer' }}
                  >
                    <td className="col-id mono" style={{ fontSize: 12 }}>
                      {c.case_id.slice(0, 12)}
                    </td>
                    <td><CategoryBadge value={c.classification}/></td>
                    <td><UrgencyBadge value={c.urgency}/></td>
                    <td className="col-conf"><ConfidenceScore value={c.confidence_score}/></td>
                    <td style={{ fontSize: 12, color: 'var(--c-text-2)' }}>{formatDate(c.created_at)}</td>
                    <td className="col-action">
                      <button
                        type="button"
                        className="btn"
                        style={{ fontSize: 12 }}
                        onClick={(e) => { e.stopPropagation(); navigate(`/cases/${c.case_id}`) }}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <div className="pagination">
            <div className="pagination__meta">
              Showing {startItem}–{endItem} of {total}
            </div>
            <div className="pagination__pager">
              <button
                type="button"
                className="btn"
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
              >
                <Icon name="chev-left" size={12}/> Previous
              </button>
              <div className="btn" style={{ fontVariantNumeric: 'tabular-nums', cursor: 'default', background: 'var(--c-bg-2)' }}>
                Page {page} of {totalPages}
              </div>
              <button
                type="button"
                className="btn"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next <Icon name="chev-right" size={12}/>
              </button>
            </div>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}
      </div>
    </>
  )
}
