import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Me from "./pages/Me";
import UpdateMechanic from "./pages/UpdateMechanic";
import CreateServiceTicket from "./pages/CreateServiceTicket";
import NewCustomer from "./pages/NewCustomer";
import AllTickets from "./pages/AllTickets";
import MyTickets from "./pages/MyTickets";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/me" element={<Me />} />
      <Route path="/update" element={<UpdateMechanic />} />
      <Route path="/tickets/new" element={<CreateServiceTicket />} />
      <Route path="/customers/new" element={<NewCustomer />} />
      <Route path="/tickets" element={<AllTickets />} />
      <Route path="/my_tickets" element={<MyTickets />} />
    

    </Routes>
  );
}
