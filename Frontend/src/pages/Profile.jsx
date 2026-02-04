import { useAuth } from "../contexts/Auth";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";
import ConfirmDeleteModal from "../components/ConfirmDelete/ConfirmDelete";

export default function Profile() {
  const { mechanic, token, logout } = useAuth();
  const navigate = useNavigate();
  const [myTickets, setMyTickets] = useState([]);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

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
      <div className="profile-page">
        <p style={{ color: "red" }}>You are not logged in.</p>
        <Link to="/login">Go to Login</Link>
      </div>
    );
  }

  //Multiple statues are present because of backend code. Old tickets may have "Pending" status but new ones use "Open".
  const activeTickets = myTickets.filter((t) => {
    const s = t.status?.toLowerCase();
    return s === "open" || s === "pending" || s === "in progress";
  }).length;

  async function handleDeleteAccount() {
    setShowDeleteModal(false);

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics/${mechanic.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        alert("Failed to delete account.");
        return;
      }

      logout();
      navigate("/login");
    } catch (err) {
      console.error("Error deleting account:", err);
      alert("Server error. Try again later.");
    }
  }

  return (
    <div className="profile-page">
      <h2 className="page-title">Your Profile</h2>

      <div className="profile-card">
        <p>
          <strong>ID:</strong> {mechanic.id}
        </p>
        <p>
          <strong>Name:</strong> {mechanic.first_name} {mechanic.last_name}
        </p>
        <p>
          <strong>Email:</strong> {mechanic.email}
        </p>
        <p>
          <strong>Phone:</strong> {mechanic.phone}
        </p>
        <p>
          <strong>Specialty:</strong> {mechanic.specialty}
        </p>

        <hr />

        <p>
          <strong>Total Assigned Tickets:</strong> {myTickets.length}
        </p>
        <p>
          <strong>Active Tickets:</strong> {activeTickets}
        </p>
      </div>

      <div className="profile-actions">
        <button onClick={() => navigate("/tickets")}>View All Tickets</button>
        <button onClick={() => navigate("/my_tickets")}>My Tickets</button>
        <button onClick={() => navigate("/update_profile")}>
          Update Profile
        </button>
        <button onClick={() => navigate("/service_tickets")}>
          Create Ticket
        </button>
        <button className="danger" onClick={logout}>
          Logout
        </button>

        {/* FIXED BUTTON — opens modal instead of deleting */}
        <button className="danger" onClick={() => setShowDeleteModal(true)}>
          Delete Account
        </button>
      </div>

      <ConfirmDeleteModal
        open={showDeleteModal}
        onCancel={() => setShowDeleteModal(false)}
        onConfirm={handleDeleteAccount}
      />
    </div>
  );
}
