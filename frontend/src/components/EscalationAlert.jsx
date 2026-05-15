import Icon from './Icon'

export default function EscalationAlert() {
  return (
    <div className="escalation" role="alert">
      <div className="escalation__icon"><Icon name="alert" size={18}/></div>
      <div>
        <p className="escalation__title">High Priority Case</p>
        <p className="escalation__body">
          Immediate escalation required. Route to team lead before processing. Notify compliance if AML risk flags are present.
        </p>
      </div>
    </div>
  )
}
