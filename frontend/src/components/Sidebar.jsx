import { useNavigate } from 'react-router-dom'
import Icon from './Icon'

const NAV_ITEMS = [
  { id: 'upload',    label: 'New Case',     icon: 'plus',      path: '/' },
  { id: 'dashboard', label: 'Dashboard',    icon: 'dashboard', path: '/dashboard' },
  { id: 'history',   label: 'Case History', icon: 'history',   path: '/history' },
]

export default function Sidebar({ currentPath }) {
  const navigate = useNavigate()

  const isActive = (path) =>
    path === '/'
      ? currentPath === '/' || currentPath.startsWith('/cases')
      : currentPath.startsWith(path)

  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <div className="sidebar__logo">
          <span className="sidebar__logo-mark" aria-hidden="true"></span>
          <span>FlowBrief AI</span>
        </div>
        <div className="sidebar__sub">Workflow Intelligence</div>
      </div>
      <nav className="sidebar__nav" aria-label="Primary">
        <div className="sidebar__section-label">Workspace</div>
        {NAV_ITEMS.map(item => (
          <button
            type="button"
            key={item.id}
            className={`nav-item ${isActive(item.path) ? 'is-active' : ''}`}
            onClick={() => navigate(item.path)}
          >
            <Icon name={item.icon} size={15} className="nav-item__icon"/>
            <span>{item.label}</span>
          </button>
        ))}
        <div className="sidebar__section-label" style={{ marginTop: 'var(--s-3)' }}>Environment</div>
        <div style={{ padding: '4px var(--s-5) 0', fontSize: 12, color: 'var(--c-side-text-2)', display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#37B24D' }}></span>
          <span>Production · WAF-1</span>
        </div>
        <div style={{ padding: '4px var(--s-5) 0', fontSize: 11, color: 'var(--c-side-text-2)' }}>v2.4.1 · Build 8814</div>
      </nav>
      <div className="sidebar__foot">
        <strong>AI-assisted.</strong>
        Human judgment required. All extractions must be verified before processing.
      </div>
    </aside>
  )
}
