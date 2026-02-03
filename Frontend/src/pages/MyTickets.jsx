import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";
import TicketCard from "../components/TicketCard/TicketCard";

export default function MyTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch tickets assigned to this mechanic
  useEffect(() => {
    async function fetchMyTickets() {
      try {
        const res = await fetch(`${API_BASE_URL}/mechanics/my_tickets`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();
        setTickets(data);
      } catch (err) {
        console.error("Error fetching mechanic tickets:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchMyTickets();
  }, [token]);

  // Update ticket status
  async function updateStatus(ticketId, newStatus) {
    try {
      const res = await fetch(`${API_BASE_URL}/service_tickets`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          service_ticket_id: ticketId,
          status: newStatus,
        }),
      });

      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to update status.");
      }
    } catch (err) {
      console.error("Status update error:", err);
    }
  }

  if (loading) return <p>Loading your tickets...</p>;

  // COUNTERS
  const total = tickets.length;
  const open = tickets.filter((t) => t.status === "Open").length;
  const inProgress = tickets.filter((t) => t.status === "In Progress").length;
  const completed = tickets.filter((t) => t.status === "Completed").length;

  return (
    <div>
      {/* PAGE TITLE */}
      <h2 className="page-title">My Tickets</h2>

      {/* COUNTERS */}
      {tickets.length > 0 && (
        <div className="ticket-counts">
          <span>Total: {total}</span>
          <span>Open: {open}</span>
          <span>In Progress: {inProgress}</span>
          <span>Completed: {completed}</span>
        </div>
      )}

      {/* TICKET GRID */}
      {tickets.length === 0 ? (
        <p>You have no assigned tickets.</p>
      ) : (
        <div className="ticket-grid">
          {tickets.map((t) => (
            <TicketCard
              key={t.id}
              ticket={t}
              onStatusChange={updateStatus}
            />
          ))}
        </div>
      )}
    </div>
  );
}