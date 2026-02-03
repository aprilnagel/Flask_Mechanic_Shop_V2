import "./TicketCard.css";

export default function TicketCard({ ticket, onAssign, onRemove }) {
  return (
    <div className="ticket-card">
      <h3>Ticket # : {ticket.id}</h3>

      <p><strong>Customer ID:</strong> {ticket.customer_id}</p>
      <p>
        <strong>Vehicle:</strong> {ticket.vehicle_year} {ticket.vehicle_make}{" "}
        {ticket.vehicle_model}
      </p>
      <p><strong>Issue:</strong> {ticket.service_description}</p>
      <p><strong>Status:</strong> {ticket.status}</p>

      <div className="mechanics-section">
        <strong>Assigned Mechanics:</strong>
        <ul className="mechanic-list">
          {(ticket.mechanics || []).length > 0 ? (
            (ticket.mechanics || []).map((m) => (
              <li key={m.id} className="mechanic-item">
                {m.id} — {m.first_name} {m.last_name}

                {onRemove && (
                  <button
                    className="danger"
                    onClick={() => onRemove(ticket.id, m.id)}
                  >
                    Remove
                  </button>
                )}
              </li>
            ))
          ) : (
            <li className="mechanic-item">None</li>
          )}
        </ul>
      </div>

      {onAssign && (
        <div className="assign-section">
          <input
            type="number"
            placeholder="Mechanic ID"
            value={ticket._assignInput || ""}
            onChange={(e) => {
              ticket._assignInput = e.target.value;
            }}
          />
          <button onClick={() => onAssign(ticket.id, ticket._assignInput)}>
            Assign
          </button>
        </div>
      )}
    </div>
  );
}