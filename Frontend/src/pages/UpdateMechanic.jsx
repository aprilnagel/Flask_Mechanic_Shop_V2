import { useState } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";

export default function UpdateMechanic() {
  const { mechanic, setMechanic, token } = useAuth();
  const navigate = useNavigate();

  // Wait until mechanic is loaded
  if (!mechanic) {
    return <p>Loading profile...</p>;
  }

  const [formData, setFormData] = useState({
    first_name: mechanic.first_name,
    last_name: mechanic.last_name,
    email: mechanic.email,
    phone: mechanic.phone,
    specialty: mechanic.specialty,
    password: ""
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

    // Build partial update body
    const body = {};
    for (const key in formData) {
      if (formData[key] !== "" && formData[key] !== mechanic[key]) {
        body[key] = formData[key];
      }
    }

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json();
        setError(err.message || "Update failed. Please try again.");
        return;
      }

      const updated = await res.json();
      setMechanic(updated);

      // Show success message under button
      setSuccess("Profile updated successfully!");

      // Redirect after a moment
      setTimeout(() => {
        navigate("/profile", { state: { success: "Profile updated!" } });
      }, 1000);

    } catch (err) {
      setError("Server error. Please try again later.");
    }
  }

  return (
    <div className="update-page">
      <h2 className="page-title">Update Profile</h2>

      <form className="update-form" onSubmit={handleSubmit}>
        <label>First Name</label>
        <input
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
        />

        <label>Last Name</label>
        <input
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
        />

        <label>Email</label>
        <input
          name="email"
          value={formData.email}
          onChange={handleChange}
        />

        <label>Phone</label>
        <input
          name="phone"
          value={formData.phone}
          onChange={handleChange}
        />

        <label>Specialty</label>
        <input
          name="specialty"
          value={formData.specialty}
          onChange={handleChange}
        />

        <label>Password (optional)</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />

        <button type="submit" className="update-btn">
          Save Changes
        </button>

        {/* Confirmation + error messages directly under button */}
        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}