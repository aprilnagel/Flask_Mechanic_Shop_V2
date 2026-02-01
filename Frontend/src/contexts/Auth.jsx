import { createContext, useContext, useState } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [mechanic, setMechanic] = useState(null);

  return (
    <AuthContext.Provider value={{ mechanic, setMechanic }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}