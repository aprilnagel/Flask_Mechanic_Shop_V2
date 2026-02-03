export default function TicketCard({ ticket, onAssign, onRemove, onStatusChange }) {
  return (
    <div className="ticket-card">
      <h3>Ticket #{ticket.id}</h3>

      <p><strong>Status:</strong> {ticket.status}</p>
      <p><strong>Customer:</strong> {ticket.customer_name}</p>
      <p><strong>Vehicle:</strong> {ticket.vehicle}</p>
      <p><strong>Description:</strong> {ticket.description}</p>

      {/* Assigned mechanics */}
      {ticket.mechanics && ticket.mechanics.length > 0 ? (
        <div>
          <strong>Assigned Mechanics:</strong>
          <ul className="mechanic-list">
            {ticket.mechanics.map((m) => (
              <li key={m.id} className="mechanic-item">
                {m.name}
                {onRemove && (
                  <button onClick={() => onRemove(ticket.id, m.id)}>Remove</button>
                )}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p><em>No mechanics assigned</em></p>
      )}

      {/* Admin assign controls (AllTickets only) */}
      {onAssign && (
        <button onClick={() => onAssign(ticket.id, prompt("Mechanic ID:"))}>
          Assign Mechanic
        </button>
      )}

      {/* Mechanic status controls (MyTickets only) */}
      {onStatusChange && (
        <div className="status-actions">
          {ticket.status !== "In Progress" && (
            <button onClick={() => onStatusChange(ticket.id, "In Progress")}>
              Start Work
            </button>
          )}

          {ticket.status !== "Completed" && (
            <button onClick={() => onStatusChange(ticket.id, "Completed")}>
              Mark Complete
            </button>
          )}

          {ticket.status !== "Pending" && (
            <button onClick={() => onStatusChange(ticket.id, "Pending")}>
              Reopen
            </button>
          )}
        </div>
      )}
    </div>
  );
}