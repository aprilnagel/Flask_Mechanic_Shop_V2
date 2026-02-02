import { Link } from "react-router-dom";
import "./Header.css";

export default function Header() {
  return (
    <header className="app-header">
      <Link to="/" className="header-title">
        Bagel's Mechanic Shop
      </Link>
    </header>
  );
}