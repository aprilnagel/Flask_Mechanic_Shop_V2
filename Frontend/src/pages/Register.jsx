import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";

function Register() {
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

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      console.log("Status:", res.status);
      console.log("Parsed JSON:", data);

      if (res.ok) {
        setIsError(false);
        setMessage("Registration successful!");

        // Optional: clear form
        setForm({
          first_name: "",
          last_name: "",
          phone: "",
          specialty: "",
          email: "",
          password: "",
        });
      } else {
        setIsError(true);
        setMessage(data.message || "Registration failed.");
      }
    } catch (error) {
      setIsError(true);
      setMessage("Network error — please try again.");
    }
  };

  return (
    <div className="register-page">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register Mechanic</h2>

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
          Submit
        </button>

        <button
          type="button"
          className="register-btn"
          onClick={() => navigate("/login")}
          style={{ background: "#6b7280" }}
        >
          Back to Login
        </button>

        {message && (
          <p
            className="register-message"
            style={{ color: isError ? "#dc2626" : "#4f46e5" }}
          >
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

export default Register;