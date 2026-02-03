import { useState } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";
import BackToProfile from "../components/Back To Profile/BackToProfile";

export default function UpdateMechanic() {
  const { mechanic, setMechanic, token } = useAuth();
  const navigate = useNavigate();

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

    // Build update payload ONLY with fields that changed
    const body = {};

    if (formData.first_name !== mechanic.first_name)
      body.first_name = formData.first_name;

    if (formData.last_name !== mechanic.last_name)
      body.last_name = formData.last_name;

    if (formData.email !== mechanic.email)
      body.email = formData.email;

    if (formData.phone !== mechanic.phone)
      body.phone = formData.phone;

    if (formData.specialty !== mechanic.specialty)
      body.specialty = formData.specialty;

    // Only send password if user typed something
    if (formData.password.trim() !== "") {
      body.password = formData.password;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics`, {
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
      setSuccess("Profile updated successfully!");

      

    } catch (err) {
      setError("Server error. Please try again later.");
    }
  }

  return (
    <div className="update-page ticket-details-page page-with-floating-button">
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
        

        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
      </form>
      <BackToProfile />
    </div>
  );
}