import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.svg";
import { FaGithub } from "react-icons/fa";

import "./LandingPage.css";

const LandingPage = () => {
  const navigate = useNavigate();
  const customerRouteChange = () => {
    const path = "/customer-login";
    navigate(path);
  };
  const contractorRouteChange = () => {
    const path = "/contractor-login";
    navigate(path);
  };

  return (
    <main>
      <div className="content-container">
        <h1>Warepair</h1>
        <img className="logo" src={logo} alt="Warepair Logo" />
        <h2>All your repairs in one click.</h2>
        <h3>Connecting local contractors with your reparis.</h3>
        <hr className="landing-page-divider" />
        <div className="button-container">
          <button
            id="customer-login"
            className="button"
            onClick={customerRouteChange}
          >
            Customer Login
          </button>
          <button
            id="contractor-login"
            className="button"
            onClick={contractorRouteChange}
          >
            Contractor Login
          </button>
        </div>
      </div>
      <footer>
        <p>
          Copyright © <script>document.write(new Date().getFullYear())</script>
          thomasjuhoonkim
          <a
            href="https://github.com/thomasjuhoonkim/warepair"
            target="_blank"
            rel="noreferrer"
          >
            <FaGithub className="fa-github" />
          </a>
        </p>
      </footer>
    </main>
  );
};

export default LandingPage;
