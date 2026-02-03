import { useNavigate } from "react-router-dom";
import "./BackToProfile.css";

export default function BackToProfile() {
  const navigate = useNavigate();

  return (
    <div className="back-to-profile-floating">
      <button
        type="button"
        className="back-to-profile-btn"
        onClick={() => navigate("/profile")}
      >
        Back to Profile
      </button>
    </div>
  );
}
