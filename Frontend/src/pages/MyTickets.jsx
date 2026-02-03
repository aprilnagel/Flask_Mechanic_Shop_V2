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

  return (
    <div>
      <h2>My Tickets</h2>

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