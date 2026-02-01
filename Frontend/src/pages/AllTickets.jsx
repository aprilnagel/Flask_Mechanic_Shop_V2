import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { API_BASE_URL } from "../config";



export default function AllTickets() {
  const { token } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  console.log("Token being sent:", token);
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
        console.log("🔍 Tickets API response:", data);

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

      const text = await res.text();
      console.log("🔧 Assign mechanic response:", text);

      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to assign mechanic.");
      }
    } catch (err) {
      console.error("❌ Assign error:", err);
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

      const text = await res.text();
      console.log("🔧 Remove mechanic response:", text);

      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to remove mechanic.");
      }
    } catch (err) {
      console.error("❌ Remove error:", err);
    }
  }

  if (loading) return <p>Loading tickets...</p>;

  // Prevent crash if backend returns an object instead of an array
  if (!Array.isArray(tickets)) {
    console.error("❌ Expected an array but got:", tickets);
    return (
      <p style={{ color: "red" }}>
        Unexpected server response. Check console for details.
      </p>
    );
  }

  return (
    <div>
      <h2>All Service Tickets</h2>

      {tickets.length === 0 ? (
        <p>No tickets found.</p>
      ) : (
        <ul>
          {tickets.map((t) => (
            <li key={t.id} style={{ marginBottom: "20px" }}>
              <strong>Ticket #{t.id}</strong>
              <br />
              Customer ID: {t.customer_id}
              <br />
              Vehicle: {t.vehicle_year} {t.vehicle_make} {t.vehicle_model}
              <br />
              Issue: {t.service_description}
              <br />
              Status: {t.status}
              <br />
              Mechanic: {t.mechanic_id ? t.mechanic_id : "Unassigned"}

              {/* Mechanic assignment UI */}
              <div style={{ marginTop: "10px" }}>
                {!t.mechanic_id ? (
                  <>
                    <input
                      type="number"
                      placeholder="Mechanic ID"
                      value={t._assignInput || ""}
                      onChange={(e) => {
                        const updated = [...tickets];
                        updated.find((x) => x.id === t.id)._assignInput =
                          e.target.value;
                        setTickets(updated);
                      }}
                    />
                    <button
                      style={{ marginLeft: "10px" }}
                      onClick={() => assignMechanic(t.id, t._assignInput)}
                    >
                      Assign Mechanic
                    </button>
                  </>
                ) : (
                  <button
                    style={{ marginTop: "5px" }}
                    onClick={() => removeMechanic(t.id, t.mechanic_id)}
                  >
                    Remove Mechanic
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}