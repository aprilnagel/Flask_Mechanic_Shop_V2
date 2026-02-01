import { useState } from "react";
import { API_BASE_URL } from "../config";

export default function Register() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    specialty: "",
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`${API_BASE_URL}/mechanics`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      const data = await res.json();
      console.log("Registration response:", data);
    } catch (error) {
      console.error("Error registering mechanic:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
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

      <button type="submit">Register</button>
    </form>
  );
}