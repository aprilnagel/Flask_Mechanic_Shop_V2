import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";
import TicketCard from "../components/TicketCard";

export default function AllTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

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

  return (
    <div>
      <h2>All Service Tickets</h2>

      {tickets.length === 0 ? (
        <p>No tickets found.</p>
      ) : (
        <ul>
          {tickets.map((t) => (
            <li key={t.id}>
              <TicketCard
                ticket={t}
                onAssign={assignMechanic}
                onRemove={removeMechanic}
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}