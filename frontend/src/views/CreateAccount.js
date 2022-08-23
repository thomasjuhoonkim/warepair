import React from "react";
import { useNavigate } from "react-router-dom";
import Map from "../assets/map.jpg";

import "./LoginPage.css";

function LandingPage() {
  const navigate = useNavigate();
  const loginRouteChange = () => {
    const path = "/";
    navigate(path);
  };

  return (
    <div>
      <p className="warepair">Warepair</p>
      <div className="left">
        <div className="center-div">
          <h1 className="login">Create an Account</h1>
          <form>
            <div className="slider-container">
              <span className="slider-label label">Are you a contractor?</span>
              <label class="switch">
                <input type="checkbox" />
                <span class="slider round"></span>
              </label>
            </div>
            <span className="label">Email</span>
            <input
              className="email input"
              placeholder="example@email.com"
              id="#email"
              type="email"
            ></input>
            <span className="label">Password</span>
            <input
              className="password input"
              placeholder="e.g. ilovedavid"
              id="#password"
              type="password"
            ></input>
            <span className="label">Access Code</span>
            <input
              className="access-code input"
              placeholder="e.g. 123456"
              id="#access-code"
              type="text"
            ></input>
            <hr className="divider" />
            <button
              className="login-button"
              onClick={() => navigate("/map", { replace: true })}
            >
              Login
            </button>
            <p className="createAccountText">
              Already have an account?{" "}
              <span onClick={loginRouteChange} className="createAccount">
                Sign in
              </span>
            </p>
          </form>
        </div>
      </div>
      <div className="right">
        <img src={Map} alt="Map" className="Map" />
      </div>
    </div>
  );
}

export default LandingPage;
