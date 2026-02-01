import { createContext, useContext, useState, useEffect } from "react";
import { API_BASE_URL } from "../config";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [mechanic, setMechanic] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  useEffect(() => {
    async function fetchMechanic() {
      if (!token) return;

      try {
        const res = await fetch(`${API_BASE_URL}/mechanics/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          logout();
          return;
        }

        const data = await res.json();
        setMechanic(data);
      } catch (err) {
        console.error("Error loading mechanic:", err);
        logout();
      }
    }

    fetchMechanic();
  }, [token]);

  function login(tokenValue, mechanicData) {
    localStorage.setItem("token", tokenValue);
    setToken(tokenValue);
    setMechanic(mechanicData);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setMechanic(null);
  }

  return (
    <AuthContext.Provider
      value={{
        mechanic,
        setMechanic,
        token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
