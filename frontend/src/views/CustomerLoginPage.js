import React from "react";
import { useNavigate } from "react-router-dom";
import Map from "../assets/map.jpg";
import axios from "axios";

import "./LoginPage.css";

const baseURL = "http://www.warepair.herokuapp.com";

function LandingPage() {
  // email: 'johndoe@gmail.com',
  // password: "password"

  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [res, setRes] = React.useState("");

  function login(email, password) {
    axios
      .post(
        baseURL + "/login",
        {
          email: email,
          password: password,
        },
        { withCredentials: true }
      )
      .then((response) => {
        setRes(response);
        console.log(response);
      });
  }

  const navigate = useNavigate();

  const createAccountRouteChange = () => {
    const path = "/create-account";
    navigate(path);
  };

  return (
    <div>
      <p className="warepair">Warepair</p>
      <div className="left">
        <div className="center-div">
          <h1 className="login">Customer Login</h1>
          <form>
            <span className="label">Email</span>
            <input
              className="email input"
              placeholder="example@email.com"
              id="#email"
              type="email"
              onChange={(event) => setEmail(event.target.value)}
              value={email}
            ></input>
            <span className="label">Password</span>
            <input
              className="password input"
              placeholder="e.g. ilovedavid"
              id="#password"
              type="password"
              onChange={(event) => setPassword(event.target.value)}
              value={password}
            ></input>
            <hr className="divider" />
            <button
              type="submit"
              className="login-button"
              onClick={() => {
                login(email, password);
                navigate("/map");
              }}
            >
              Login
            </button>
            <p className="createAccountText">
              Don't have an account?{" "}
              <span
                onClick={createAccountRouteChange}
                className="createAccount"
              >
                Create an Account
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
