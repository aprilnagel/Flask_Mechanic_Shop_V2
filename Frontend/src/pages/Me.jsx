import { useEffect, useState, useContext } from "react";
import { API_BASE_URL } from "../config";
import { AuthContext } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";

export default function Me() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMechanic() {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const res = await fetch(`${API_BASE_URL}/mechanics/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) {
          localStorage.removeItem("token");
          navigate("/login");
          return;
        }

        const data = await res.json();

        // Save mechanic to context
        login(token, data);

        // Keep loading screen visible for 0.8 seconds
        setTimeout(() => {
          setLoading(false);
          navigate("/profile");
        }, 800);

      } catch (err) {
        console.error("Error loading profile:", err);
        navigate("/login");
      }
    }

    loadMechanic();
  }, [login, navigate]);

  return (
    <div className="home-page">
      <h2>Loading profile...</h2>
    </div>
  );
}