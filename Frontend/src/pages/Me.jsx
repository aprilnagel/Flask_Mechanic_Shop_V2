import { useEffect, useState } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";

export default function Me() {
  const { setMechanic } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMechanic() {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("You must be logged in to access your account.");
        navigate("/login");
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/mechanics/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          setError("Your session has expired. Please log in again.");
          localStorage.removeItem("token");
          navigate("/login");
          return;
        }

        const data = await response.json();
        setMechanic(data);
        setTimeout(() => {
        navigate("/profile", { state: { success: "Welcome back!" } });
      }, 800);

      } catch (err) {
        setError("Unable to connect to the server. Please try again later.");
      }
    }

    loadMechanic();
  }, []);

  return (
    <div>
      <h2>Loading your account...</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
