import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <h1>Welcome</h1>

      <div className="portal-buttons">
        <button
          className="portal-btn"
          onClick={() => navigate("/customers/new")}
        >
          Customer Intake
        </button>

        <button
          className="portal-btn"
          onClick={() => navigate("/login")}
        >
          Mechanic Login
        </button>
      </div>
    </div>
  );
}

export default Home;