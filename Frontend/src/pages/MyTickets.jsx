import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";

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
        <ul>
          {tickets.map((t) => (
            <li key={t.id} style={{ marginBottom: "10px" }}>
              <strong>Ticket #{t.id}</strong><br />
              Customer ID: {t.customer_id}<br />
              Vehicle: {t.vehicle_year} {t.vehicle_make} {t.vehicle_model}<br />
              Issue: {t.service_description}<br />
              Status: {t.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}