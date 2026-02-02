import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";
import TicketCard from "../components/TicketCard";

export default function AllTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

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

  async function assignMechanic(ticketId, mechanicId) {
    try {
      await fetch(`${API_BASE_URL}/service_tickets/assign_mechanic/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          service_ticket_id: ticketId,
          mechanic_id: mechanicId,
        }),
      });

      window.location.reload();
    } catch (err) {
      console.error("Assign error:", err);
    }
  }

  async function removeMechanic(ticketId, mechanicId) {
    try {
      await fetch(`${API_BASE_URL}/service_tickets/remove_mechanic/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          service_ticket_id: ticketId,
          mechanic_id: mechanicId,
        }),
      });

      window.location.reload();
    } catch (err) {
      console.error("Remove error:", err);
    }
  }

  if (loading) return <p>Loading tickets...</p>;

  return (
    <div>
        <h2>All Service Tickets</h2>

        {tickets.length === 0 ? (
        <p>No tickets found.</p>
        ) : (
        <div className="ticket-grid">
            {tickets.map((t) => (
            <TicketCard
                key={t.id}
                ticket={t}
                onAssign={assignMechanic}
                onRemove={removeMechanic}
            />
            ))}
        </div>
        )}
    </div>
    );
}
