import React from "react";
import "./TicketCard.css";

const TicketCard = ({
  ticket,
  assignMechanic,
  removeMechanic,
  mechanics,
  showAssignControls = false,
  onStatusChange,
}) => {
  return (
    <div className="ticket-card">

      {/* Centered Ticket ID */}
      <h3 className="ticket-id">Ticket #{ticket.id}</h3>

      {/* VEHICLE + SERVICE INFO */}
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
              ID: #{mech.id} - {mech.name}
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

      {/* STATUS SECTION — unified badge styling */}
      <div className="ticket-section status-section">

        {/* COMPLETED */}
        {ticket.status === "Completed" && (
          <div className="status-row">
            <span className="status-badge completed">✓ Completed</span>

            {onStatusChange && (
              <button
                className="reopen-btn"
                onClick={() => onStatusChange(ticket.id, "Pending")}
              >
                Reopen
              </button>
            )}
          </div>
        )}

        {/* OPEN (backend = Pending) */}
        {ticket.status === "Pending" && (
          <div className="status-row">
            <span className="status-badge open">Open</span>

            {onStatusChange && (
              <button
                className="start-work-btn"
                onClick={() => onStatusChange(ticket.id, "In Progress")}
              >
                Start Work
              </button>
            )}
          </div>
        )}

        {/* IN PROGRESS */}
        {ticket.status === "In Progress" && (
          <div className="status-row">
            <span className="status-badge inprogress">In Progress</span>

            {onStatusChange && (
              <button
                className="mark-complete-btn"
                onClick={() => onStatusChange(ticket.id, "Completed")}
              >
                Mark Complete
              </button>
            )}
          </div>
        )}

      </div>

      {/* ASSIGN MECHANIC DROPDOWN */}
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
                  ID: #{mech.id} - {mech.name}
                </option>
              ))}
          </select>
        </div>
      )}

    </div>
  );
};

export default TicketCard;