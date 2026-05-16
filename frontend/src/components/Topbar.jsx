import { Link } from 'react-router-dom'
import Icon from './Icon'

export default function Topbar({ crumb, meta }) {
  return (
    <header className="topbar">
      <nav className="topbar__crumb" aria-label="Breadcrumb">
        {crumb.map((c, i) => (
          <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            {i > 0 && <Icon name="chev-right" size={12} className="sep"/>}
            {c.href ? (
              <Link to={c.href}>{c.label}</Link>
            ) : (
              <span className="here">{c.label}</span>
            )}
          </span>
        ))}
      </nav>
      <div className="topbar__meta">
        {meta}
        <div style={{
          width: 32,
          height: 32,
          borderRadius: 'var(--r-md)',
          border: '1px solid var(--c-border)',
          background: 'var(--c-bg-2)',
          display: 'grid',
          placeItems: 'center',
          color: 'var(--c-text-3)'
        }}>
          <Icon name="user" size={16} />
        </div>
      </div>
    </header>
  )
}
