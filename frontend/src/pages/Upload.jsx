import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Topbar from '../components/Topbar'
import Icon from '../components/Icon'

// TODO Phase 21 — wire processDocument API call

const CRUMB = [{ label: 'Home', href: '/' }, { label: 'New Case' }]

export default function Upload() {
  const navigate = useNavigate()
  const [tab, setTab] = useState('paste')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const canSubmit = tab === 'paste' ? text.trim().length > 0 : !!file

  const onDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) setFile(f)
  }

  return (
    <>
      <Topbar crumb={CRUMB} meta={<span>Production · WAF-1</span>}/>
      <div className="page">
        <div className="page__head">
          <div>
            <h1 className="page__title">New Case</h1>
            <div className="page__subtitle">Submit a customer document for AI extraction and routing</div>
          </div>
          <div className="page__head-actions">
            <button className="btn"><Icon name="history" size={14}/> Open last case</button>
          </div>
        </div>

        <div className="panel">
          <div className="tabs" role="tablist" style={{ padding: '0 var(--s-5)' }}>
            <button role="tab" aria-selected={tab === 'paste'} className={`tab ${tab === 'paste' ? 'is-active' : ''}`} onClick={() => setTab('paste')}>
              <Icon name="doc" size={14}/> Paste Text
            </button>
            <button role="tab" aria-selected={tab === 'upload'} className={`tab ${tab === 'upload' ? 'is-active' : ''}`} onClick={() => setTab('upload')}>
              <Icon name="upload" size={14}/> Upload File
            </button>
          </div>

          <div className="panel__body">
            {tab === 'paste' && (
              <div className="field">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <label className="field__label" htmlFor="paste">Document Text</label>
                  <span className="char-count">{text.length.toLocaleString()} characters</span>
                </div>
                <textarea
                  id="paste"
                  className="textarea"
                  placeholder="Paste customer request, loan application, KYC note, or complaint here..."
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
                <div className="muted" style={{ fontSize: 12 }}>
                  Text is processed in-region and is not retained after the case is closed.
                </div>
              </div>
            )}

            {tab === 'upload' && (
              <div>
                <label className="field__label" style={{ display: 'block', marginBottom: 6 }}>Document File</label>
                <div
                  className={`dropzone ${dragOver ? 'is-over' : ''}`}
                  onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={onDrop}
                  onClick={() => fileInputRef.current && fileInputRef.current.click()}
                  role="button"
                  tabIndex={0}
                >
                  <Icon name="upload" size={28}/>
                  <div className="dropzone__title">Drop file here or click to browse</div>
                  <div className="dropzone__hint">PDF, JPG or PNG · 10 MB maximum</div>
                  <div className="dropzone__types">
                    <span className="filetype">PDF</span>
                    <span className="filetype">JPG</span>
                    <span className="filetype">PNG</span>
                  </div>
                  <input
                    ref={fileInputRef} type="file" accept=".pdf,.jpg,.jpeg,.png"
                    style={{ display: 'none' }}
                    onChange={(e) => setFile(e.target.files[0])}
                  />
                  {file && (
                    <div className="dropzone__file" onClick={(e) => e.stopPropagation()}>
                      <Icon name="file" size={16}/>
                      <span>{file.name}</span>
                      <span className="dropzone__file-meta">{(file.size / 1024).toFixed(0)} KB</span>
                      <button className="btn btn--ghost" style={{ padding: '2px 6px' }} onClick={() => setFile(null)} aria-label="Remove file">
                        <Icon name="x" size={14}/>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            <div style={{ marginTop: 'var(--s-4)' }}>
              <button
                className="btn btn--primary btn--block"
                disabled={!canSubmit}
              >
                Process Document
              </button>
            </div>
          </div>
        </div>

        {/* Recent Cases */}
        <div className="section-title">
          <h2>Recent Cases</h2>
          <div className="rule"/>
          <button className="btn btn--ghost" onClick={() => navigate('/history')} style={{ fontSize: 12 }}>
            View all <Icon name="chev-right" size={12}/>
          </button>
        </div>

        <div className="panel">
          <div className="recent-list">
            <div style={{ padding: 'var(--s-8)', textAlign: 'center', color: 'var(--c-text-3)', fontSize: 13 }}>
              No recent cases.
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
