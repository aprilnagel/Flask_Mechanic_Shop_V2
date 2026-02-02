import { useAuth } from "../contexts/Auth";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Profile() {
  const { mechanic, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  if (!mechanic) {
    return (
      <div>
        <p style={{ color: "red" }}>You are not logged in.</p>
        <Link to="/login">Go to Login</Link>
      </div>
    );
  }

  return (
    <div>
      {location.state?.success && (
        <p style={{ color: "green" }}>{location.state.success}</p>
      )}

      <h2>Mechanic Profile</h2>
      <p> Name: {mechanic.first_name} {mechanic.last_name}
      </p>
      <p>Mechanic ID: {mechanic.id}</p>
      <p>Email: {mechanic.email}</p>
      <p>Phone: {mechanic.phone}</p>
      <p>Specialty: {mechanic.specialty}</p>
      <p>Service Tickets Assigned: {(mechanic.service_tickets || []).length}</p>
      {console.log("MECHANIC FROM BACKEND:", mechanic)}


      <hr />
      
      <div className="profile-actions">
        <button onClick={() => navigate("/update")}>Update Profile</button>

        <button onClick={() => navigate("/my_tickets")}>View My Tickets</button>

        <button onClick={() => navigate("/tickets")}>View All Tickets</button>
        
        <button onClick={() => navigate("/tickets/new")}>
          Create New Ticket
        </button>
    
        <button onClick={logout} style={{ color: "red" }}>
          Logout
        </button>
      </div>
    </div>
  );
}
