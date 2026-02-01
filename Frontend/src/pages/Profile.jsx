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
      <p><strong>ID:</strong> {mechanic.id}</p>
      <p><strong>Name:</strong> {mechanic.name}</p>
      <p><strong>Email:</strong> {mechanic.email}</p>
    </div>
  );
}