import { useState, useEffect } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate, useLocation } from "react-router-dom";
import { API_BASE_URL } from "../config";

export default function CreateServiceTicket() {
  const { token, mechanic } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // If we came from NewCustomer.jsx, this will contain the new customer's ID
  const prefilledCustomerId = location.state?.customerId || "";

  const [formData, setFormData] = useState({
    vehicle_make: "",
    vehicle_model: "",
    vehicle_year: "",
    service_description: "",
    customer_id: prefilledCustomerId,
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    console.log("🔧 Submitting ticket...");
    console.log("➡️ Form data:", formData);
    console.log("➡️ Mechanic:", mechanic);

    const body = {
      ...formData,
    };

    try {
      const res = await fetch(`${API_BASE_URL}/service_tickets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        setError("Failed to create ticket. Please check your inputs.");
        return;
      }

      await res.json();
      setSuccess("Service ticket created!");

      setTimeout(() => {
        navigate("/tickets", { state: { success: "Ticket created!" } });
      }, 800);
    } catch (err) {
      setError("Server error. Try again later.");
    }
  }

  return (
    <div>
      <h2>Create New Service Ticket</h2>

      {location.state?.success && (
        <p style={{ color: "green" }}>{location.state.success}</p>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <form onSubmit={handleSubmit}>
        <label>Vehicle Make:</label>
        <input
          name="vehicle_make"
          value={formData.vehicle_make}
          onChange={handleChange}
          required
        />

        <label>Vehicle Model:</label>
        <input
          name="vehicle_model"
          value={formData.vehicle_model}
          onChange={handleChange}
          required
        />

        <label>Vehicle Year:</label>
        <input
          name="vehicle_year"
          value={formData.vehicle_year}
          onChange={handleChange}
          required
        />

        <label>Service Description:</label>
        <textarea
          name="service_description"
          value={formData.service_description}
          onChange={handleChange}
          required
        />

        <label>Customer ID:</label>
        <input
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          required
          disabled={!!prefilledCustomerId}
        />

        <button type="submit">Create Ticket</button>
      </form>
    </div>
  );
}
