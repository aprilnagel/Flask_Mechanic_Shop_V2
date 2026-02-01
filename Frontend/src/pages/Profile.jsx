import { useContext } from "react";
import { AuthContext } from "../contexts/Auth";

export default function Profile() {
  const { mechanic } = useContext(AuthContext);

  if (!mechanic) {
    return <p>No mechanic is logged in.</p>;
  }

  return (
    <div>
      <h2>Mechanic Profile</h2>
      <p>Welcome {mechanic.first_name} {mechanic.last_name}!</p>
      <p>Email: {mechanic.email}</p>
      <p>Phone: {mechanic.phone}</p>
      <p>Specialty: {mechanic.specialty}</p>      
    </div>
  );
}