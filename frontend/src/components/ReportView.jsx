import ReactMarkdown from 'react-markdown'

export default function ReportView({ markdown }) {
  return (
    <div className="handoff__body">
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  )
}
