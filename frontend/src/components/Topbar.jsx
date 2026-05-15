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
        <div className="topbar__user">
          <span className="topbar__avatar">AO</span>
          <span>A. Owusu · Operations</span>
        </div>
      </div>
    </header>
  )
}
