import { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [mechanic, setMechanic] = useState(null);

  return (
    <AuthContext.Provider value={{ mechanic, setMechanic }}>
      {children}
    </AuthContext.Provider>
  );
};