import { useAuth } from "../contexts/Auth";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";

export default function Profile() {
  const { mechanic, token, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [myTickets, setMyTickets] = useState([]);

  useEffect(() => {
    async function fetchMyTickets() {
      try {
        const res = await fetch(`${API_BASE_URL}/mechanics/my_tickets`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setMyTickets(data);
        }
      } catch (err) {
        console.error("Error fetching mechanic tickets:", err);
      }
    }

    fetchMyTickets();
  }, [token]);

  if (!mechanic) {
    return (
      <div>
        <p style={{ color: "red" }}>You are not logged in.</p>
        <Link to="/login">Go to Login</Link>
      </div>
    );
  }

  // Count active tickets
  const activeTickets = myTickets.filter(
    (t) => t.status === "Pending" || t.status === "In Progress"
  ).length;

  return (
    <div className="profile-page">
      <h2>Your Profile</h2>

      <p>ID: {mechanic.id}</p>
      <p>Name: {mechanic.first_name} {mechanic.last_name}</p>
      <p>Email: {mechanic.email}</p>
      <p>Phone: {mechanic.phone}</p>
      <p>Specialty: {mechanic.specialty}</p>

      <p>Total Assigned Tickets: {myTickets.length}</p>
      <p>Active Tickets: {activeTickets}</p>

      <div className="profile-actions">
        <button onClick={() => navigate("/tickets")}>View All Tickets</button>
        <button onClick={() => navigate("/my_tickets")}>My Tickets</button>
        <button onClick={() => navigate("/update_profile")}>Update Profile</button>
        <button onClick={() => navigate("/create_ticket")}>Create Ticket</button>
        <button className="danger" onClick={logout}>Logout</button>
      </div>
    </div>
  );
}