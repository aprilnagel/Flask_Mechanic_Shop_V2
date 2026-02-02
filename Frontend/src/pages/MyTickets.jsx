import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";
import TicketCard from "../components/TicketCard";

export default function MyTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

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

  if (loading) return <p>Loading your tickets...</p>;

  return (
    <div>
        <h2>My Assigned Tickets</h2>

        {tickets.length === 0 ? (
        <p>You have no assigned tickets.</p>
        ) : (
        <div className="ticket-grid">
            {tickets.map((t) => (
            <TicketCard key={t.id} ticket={t} />
            ))}
        </div>
        )}
    </div>
    );
}
