import { useState } from "react";
import { API_BASE_URL } from "../config";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    specialty: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setIsError(false);

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      console.log("Registration response:", data);

      if (!res.ok) {
        setIsError(true);
        setMessage(data.message || "Registration failed");
        return;
      }

      // Success
      setMessage("Registration successful!");

    } catch (error) {
      console.error("Error registering mechanic:", error);
      setIsError(true);
      setMessage("Server error — try again later");
    }
  };

  return (
    <div className="register-page">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register Mechanic</h2>

        {message && (
          <p
            className="register-message"
            style={{ color: isError ? "#dc2626" : "#4f46e5" }}
          >
            {message}
          </p>
        )}

        <input
          name="first_name"
          placeholder="First Name"
          value={form.first_name}
          onChange={handleChange}
        />

        <input
          name="last_name"
          placeholder="Last Name"
          value={form.last_name}
          onChange={handleChange}
        />

        <input
          name="specialty"
          placeholder="Specialty"
          value={form.specialty}
          onChange={handleChange}
        />

        <input
          name="phone"
          placeholder="Phone"
          value={form.phone}
          onChange={handleChange}
        />

        <input
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
        />

        <button className="register-btn" type="submit">
          Register
        </button>

        {/* Show Back to Login ONLY after successful registration */}
        {!isError && message === "Registration successful!" && (
          <button
            type="button"
            className="register-btn"
            style={{ background: "#6b7280" }}
            onClick={() => navigate("/login")}
          >
            Back to Login
          </button>
        )}
      </form>
    </div>
  );
}