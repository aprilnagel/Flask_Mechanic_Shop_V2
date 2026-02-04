import React from "react";
import "./TicketCard.css";

function TicketCard({
  ticket,
  assignMechanic,
  removeMechanic,
  mechanics,
  showAssignControls = false,
  onStatusChange,
}) {
  // Normalize backend statuses and map to display labels
  function getDisplayStatus(status) {
    const s = status?.toLowerCase();

    if (s === "open" || s === "pending") return "Open";
    if (s === "in progress") return "In Progress";
    if (s === "completed") return "Completed";

    return status || "Unknown";
  }

  // Map backend statuses to CSS badge classes
  function getStatusClass(status) {
    const s = status?.toLowerCase();

    if (s === "open" || s === "pending") return "open";
    if (s === "in progress") return "inprogress";
    if (s === "completed") return "completed";

    return "";
  }

  // Helper booleans for cleaner JSX
  const isOpen = ticket.status === "Open" || ticket.status === "Pending";
  const isInProgress = ticket.status === "In Progress";
  const isCompleted = ticket.status === "Completed";

  return (
    <div className="ticket-card">

      {/* Ticket ID */}
      <h3 className="ticket-id">Ticket #{ticket.id}</h3>

      {/* VEHICLE INFO */}
      <div className="ticket-section">
        <p><strong>Vehicle Make:</strong> {ticket.vehicle_make}</p>
        <p><strong>Vehicle Model:</strong> {ticket.vehicle_model}</p>
        <p><strong>Vehicle Year:</strong> {ticket.vehicle_year}</p>
        <p><strong>Service Description:</strong> {ticket.service_description}</p>
      </div>

      {/* ASSIGNED MECHANICS */}
      <div className="ticket-section">
        <strong>Assigned Mechanics:</strong>

        {ticket.mechanics && ticket.mechanics.length > 0 ? (
          ticket.mechanics.map((mech) => (
            <div key={mech.id} className="assigned-mech-item">
              ID #{mech.id} — {mech.name}
              {showAssignControls && (
                <button
                  className="remove-mech-btn"
                  onClick={() => removeMechanic(ticket.id, mech.id)}
                >
                  Remove
                </button>
              )}
            </div>
          ))
        ) : (
          <p>No mechanics assigned</p>
        )}
      </div>

      {/* STATUS + ACTIONS */}
      <div className="ticket-section status-section">
        <div className="status-row">
          <span className={`status-badge ${getStatusClass(ticket.status)}`}>
            {getDisplayStatus(ticket.status)}
          </span>

          {onStatusChange && (
            <>
              {isOpen && (
                <button
                  className="start-work-btn"
                  onClick={() => onStatusChange(ticket.id, "In Progress")}
                >
                  Start Work
                </button>
              )}

              {isInProgress && (
                <button
                  className="mark-complete-btn"
                  onClick={() => onStatusChange(ticket.id, "Completed")}
                >
                  Mark Complete
                </button>
              )}

              {isCompleted && (
                <button
                  className="reopen-btn"
                  onClick={() => onStatusChange(ticket.id, "Open")}
                >
                  Reopen
                </button>
              )}
            </>
          )}
        </div>
      </div>

      {/* ASSIGN MECHANIC */}
      {showAssignControls && (
        <div className="assign-section">
          <select
            onChange={(e) => assignMechanic(ticket.id, e.target.value)}
            defaultValue=""
          >
            <option value="" disabled>
              Assign a mechanic
            </option>

            {[...mechanics]
              .sort((a, b) => a.id - b.id)
              .map((mech) => (
                <option key={mech.id} value={mech.id}>
                  ID #{mech.id} — {mech.name}
                </option>
              ))}
          </select>
        </div>
      )}

    </div>
  );
}

export default TicketCard;