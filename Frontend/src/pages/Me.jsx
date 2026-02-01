import { useEffect } from "react";
import { useAuth } from "../contexts/Auth";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";

export default function Me() {
  const { setMechanic } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    async function loadMechanic() {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const response = await fetch(`${API_BASE_URL}/mechanics/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      const data = await response.json();
      setMechanic(data);
      navigate("/profile");
    }

    loadMechanic();
  }, []);

  return (
    <div>
      <h2>Loading your account...</h2>
    </div>
  );
}