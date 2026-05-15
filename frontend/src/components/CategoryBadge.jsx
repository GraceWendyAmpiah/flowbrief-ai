const CATEGORY_META = {
  'KYC':             { cls: 'badge--kyc',       label: 'KYC' },
  'Complaint':       { cls: 'badge--complaint', label: 'Complaint' },
  'SME Advisory':    { cls: 'badge--sme',       label: 'SME Advisory' },
  'Trade Finance':   { cls: 'badge--trade',     label: 'Trade Finance' },
  'Account Opening': { cls: 'badge--account',   label: 'Acct Opening' },
}

export default function CategoryBadge({ value }) {
  const m = CATEGORY_META[value] || { cls: 'badge--kyc', label: value }
  return <span className={`badge ${m.cls}`}>{m.label}</span>
}
