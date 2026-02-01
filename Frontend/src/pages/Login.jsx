import { useState, useContext } from "react";
import { API_BASE_URL } from "../config";
import { AuthContext } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { setMechanic } = useContext(AuthContext);
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: ""
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    console.log("Submitting login form...");

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      const data = await res.json();
      console.log("FULL RESPONSE FROM BACKEND:", data);



      if (!res.ok) {
        setError(data.message || "Login failed");
        return;
      }

      // Save mechanic to global context
      setMechanic(data.mechanic);

      // Redirect AFTER successful login
      navigate("/profile");

      console.log("Logged in:", data.mechanic);
    } catch (err) {
      setError("Server error — try again later");
      console.error(err);
    }
  };
  console.log("Using API:", API_BASE_URL);


  return (
  <form onSubmit={handleSubmit}>
    <h2>Mechanic Login</h2>

    {error && <p style={{ color: "red" }}>{error}</p>}

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

    <button type="submit">Login</button>

    <button type="button" onClick={() => navigate("/register")}>
      Create an Account
    </button>
  </form>
);
}