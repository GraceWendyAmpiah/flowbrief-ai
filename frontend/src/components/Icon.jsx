export default function Icon({ name, size = 16, className }) {
  const s = size
  const props = {
    width: s, height: s, viewBox: '0 0 24 24',
    fill: 'none', stroke: 'currentColor', strokeWidth: '1.8',
    strokeLinecap: 'round', strokeLinejoin: 'round',
    className,
  }
  switch (name) {
    case 'plus': return <svg {...props}><path d="M12 5v14M5 12h14"/></svg>
    case 'doc': return <svg {...props}><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></svg>
    case 'dashboard': return <svg {...props}><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
    case 'history': return <svg {...props}><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l3 2"/></svg>
    case 'upload': return <svg {...props}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></svg>
    case 'file': return <svg {...props}><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></svg>
    case 'refresh': return <svg {...props}><path d="M3 12a9 9 0 0 1 15.5-6.4L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.4L3 16"/><path d="M3 21v-5h5"/></svg>
    case 'alert': return <svg {...props}><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.7 3.86a2 2 0 0 0-3.4 0z"/></svg>
    case 'chev-right': return <svg {...props}><path d="M9 18l6-6-6-6"/></svg>
    case 'chev-left': return <svg {...props}><path d="M15 18l-6-6 6-6"/></svg>
    case 'arrow-left': return <svg {...props}><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
    case 'search': return <svg {...props}><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    case 'download': return <svg {...props}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
    case 'print': return <svg {...props}><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
    case 'paperclip': return <svg {...props}><path d="m21 12-9.6 9.6a4 4 0 0 1-5.6-5.6L15 7a3 3 0 0 1 4 4l-9.6 9.6"/></svg>
    case 'x': return <svg {...props}><path d="M18 6 6 18M6 6l12 12"/></svg>
    default: return null
  }
}
