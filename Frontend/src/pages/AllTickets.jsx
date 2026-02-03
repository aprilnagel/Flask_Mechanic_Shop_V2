import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";
import TicketCard from "../components/TicketCard/TicketCard";
import BackToProfile from "../components/Back To Profile/BackToProfile";

export default function AllTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("All");

  // Fetch all tickets
  useEffect(() => {
    async function fetchTickets() {
      try {
        const res = await fetch(`${API_BASE_URL}/service_tickets`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();
        setTickets(data);
      } catch (err) {
        console.error("Error fetching tickets:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchTickets();
  }, [token]);

  // Assign mechanic
  async function assignMechanic(ticketId, mechanicId) {
    try {
      const res = await fetch(
        `${API_BASE_URL}/service_tickets/assign_mechanic/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            service_ticket_id: ticketId,
            mechanic_id: mechanicId,
          }),
        }
      );

      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to assign mechanic.");
      }
    } catch (err) {
      console.error("Assign error:", err);
    }
  }

  // Remove mechanic
  async function removeMechanic(ticketId, mechanicId) {
    try {
      const res = await fetch(
        `${API_BASE_URL}/service_tickets/remove_mechanic/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            service_ticket_id: ticketId,
            mechanic_id: mechanicId,
          }),
        }
      );

      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to remove mechanic.");
      }
    } catch (err) {
      console.error("Remove error:", err);
    }
  }

  if (loading) return <p>Loading tickets...</p>;

  if (!Array.isArray(tickets)) {
    return <p style={{ color: "red" }}>Unexpected server response.</p>;
  }

  // Status counts
  const total = tickets.length;
  const pending = tickets.filter((t) => t.status === "Pending").length;
  const inProgress = tickets.filter((t) => t.status === "In Progress").length;
  const completed = tickets.filter((t) => t.status === "Completed").length;
  const unassigned = tickets.filter((t) => t.mechanics.length === 0).length;

  // Filter logic
  const filteredTickets = tickets.filter((t) => {
    if (filter === "All") return true;
    if (filter === "Unassigned") return t.mechanics.length === 0;
    return t.status === filter;
  });

  return (
    <div className="ticket-details-page page-with-floating-button">
      {/* PAGE TITLE */}
      <h2 className="page-title">All Service Tickets</h2>

      {/* COUNTERS */}
      <div className="ticket-counts">
        <span>Total: {total}</span>
        <span>Pending: {pending}</span>
        <span>In Progress: {inProgress}</span>
        <span>Completed: {completed}</span>
        <span>Unassigned: {unassigned}</span>
      </div>

      {/* FILTER BUTTONS */}
      <div className="ticket-filters">
        <button
          className={filter === "All" ? "active" : ""}
          onClick={() => setFilter("All")}
        >
          All
        </button>

        <button
          className={filter === "Pending" ? "active" : ""}
          onClick={() => setFilter("Pending")}
        >
          Pending
        </button>

        <button
          className={filter === "In Progress" ? "active" : ""}
          onClick={() => setFilter("In Progress")}
        >
          In Progress
        </button>

        <button
          className={filter === "Completed" ? "active" : ""}
          onClick={() => setFilter("Completed")}
        >
          Completed
        </button>

        <button
          className={filter === "Unassigned" ? "active" : ""}
          onClick={() => setFilter("Unassigned")}
        >
          Unassigned
        </button>
      </div>

      {/* TICKET GRID */}
      {filteredTickets.length === 0 ? (
        <p>No tickets match this filter.</p>
      ) : (
        <div className="ticket-grid">
          {filteredTickets.map((t) => (
            <TicketCard
              key={t.id}
              ticket={t}
              onAssign={assignMechanic}
              onRemove={removeMechanic}
            />
          ))}
        </div>
      )}
      <BackToProfile />
    </div>
  );
}