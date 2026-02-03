import { useState, useEffect } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate, useLocation } from "react-router-dom";
import { API_BASE_URL } from "../config";
import BackToProfile from "../components/Back To Profile/BackToProfile";

export default function CreateServiceTicket() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const prefilledCustomerId = location.state?.customerId || "";

  const [customers, setCustomers] = useState([]);

  const [formData, setFormData] = useState({
    vehicle_make: "",
    vehicle_model: "",
    vehicle_year: "",
    service_description: "",
    customer_id: prefilledCustomerId,
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch customers for dropdown
  useEffect(() => {
    async function fetchCustomers() {
      try {
        const res = await fetch(`${API_BASE_URL}/customers`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.ok) {
          const data = await res.json();
          setCustomers(data);
        }
      } catch (err) {
        console.error("Error fetching customers:", err);
      }
    }

    fetchCustomers();
  }, [token]);

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

    try {
      const res = await fetch(`${API_BASE_URL}/service_tickets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        setError("Failed to create ticket. Please check your inputs.");
        return;
      }

      await res.json();
      setSuccess("Service ticket created!");

      // Reset form but keep prefilled ID if coming from NewCustomer
      setFormData({
        vehicle_make: "",
        vehicle_model: "",
        vehicle_year: "",
        service_description: "",
        customer_id: prefilledCustomerId,
      });
    } catch (err) {
      setError("Server error. Try again later.");
    }
  }

  return (
    <div className="create-ticket-page page-with-floating-button">
      <h2 className="page-title">Create New Service Ticket</h2>

      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}

      <form className="create-ticket-form" onSubmit={handleSubmit}>
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

        <label>Customer:</label>
        <select
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          required
          disabled={!!prefilledCustomerId}
        >
          <option value="">Select a customer</option>

          {[...customers]
            .sort((a, b) => a.id - b.id)
            .map((c) => (
              <option key={c.id} value={c.id}>
                ID #{c.id}: {c.first_name} {c.last_name}
              </option>
            ))}
        </select>

        <button type="submit">Create Ticket</button>
      </form>

      <BackToProfile />
    </div>
  );
}
