import ConfidenceScore from './ConfidenceScore'

export default function FieldExtractDisplay({ caseData }) {
  const {
    customer_name, request_type, business_type, amount_mentioned,
    recommended_team, confidence_score, missing_documents, risk_flags,
  } = caseData

  return (
    <div className="field-grid">
      <Field label="Customer Name" value={customer_name}/>
      <Field label="Request Type" value={request_type}/>
      <Field label="Business Type" value={business_type}/>
      <Field label="Amount Mentioned" value={amount_mentioned}/>
      <Field label="Recommended Team" value={recommended_team}/>
      <div className="field-card">
        <span className="field-card__label label">Confidence Score</span>
        <div style={{ marginTop: 4 }}>
          <ConfidenceScore value={confidence_score}/>
        </div>
      </div>
      <div className="field-card field-card--wide">
        <span className="field-card__label label">Missing Documents</span>
        {!missing_documents || missing_documents.length === 0 ? (
          <span className="muted" style={{ fontSize: 13 }}>No missing documents identified.</span>
        ) : (
          <div className="field-card__chips">
            {missing_documents.map((d, i) => (
              <span key={i} className="chip chip--red"><span className="chip__dot"/>{d}</span>
            ))}
          </div>
        )}
      </div>
      <div className="field-card field-card--wide">
        <span className="field-card__label label">Risk Flags</span>
        {!risk_flags || risk_flags.length === 0 ? (
          <span className="muted" style={{ fontSize: 13 }}>No risk flags raised.</span>
        ) : (
          <div className="field-card__chips">
            {risk_flags.map((f, i) => (
              <span key={i} className="chip chip--amber"><span className="chip__dot"/>{f}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div className="field-card">
      <span className="field-card__label label">{label}</span>
      <span className="field-card__value">{value || '—'}</span>
    </div>
  )
}
