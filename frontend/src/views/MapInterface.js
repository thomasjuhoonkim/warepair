import React, { Component, useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  GoogleMap,
  InfoWindow,
  LoadScript,
  Marker,
  useJsApiLoader,
  DistanceMatrixService,
} from "@react-google-maps/api";
import axios from "axios";

import "./MapInterface.css";

const MapInterface = () => {
  const baseURL = "http://www.warepair.herokuapp.com/";

  const [helpLocation, setHelpLocation] = useState({});

  const [requests, setRequests] = useState();
  //const [center, setCenter] = useState();
  const [map, setMapInstance] = useState();

  useEffect(() => {
    axios
      .get(baseURL + "/helpRequests", { withCredentials: true })
      .then((response) => {
        setRequests(response.data);
        console.log(response.data);
      });
  }, []);

  // for (let i = 0; i < requests.length; i++) {
  //   requests[i] =
  //             {
  //               title: requests[2],
  //               description: requests[3],
  //               location: requests[4],
  //               contact: {
  //                 phone: requests[5],
  //                 email: requests[6]
  //               }
  //             };
  // }

  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: "AIzaSyCi4Z6r3IAxS0ywrRniNwvzUFreM7poFyk",
  });

  const defaultMapOptions = {
    streetViewControl: true,
    fullscreenControl: false,
  };

  const containerStyle = {
    width: "100vw",
    height: "100vh",
  };

  const center = {
    lat: -3.745,
    lng: -38.523,
  };

  // const helpRequests = [
  //   {
  //     title: "Clogged Toilet",
  //     description: "Help me unclog toilet!",
  //     location: {
  //       lat: -3.745,
  //       lng: -38.523
  //     },
  //     contact: {
  //       phone: "647-647-6477",
  //       email: "myemail@gmail.com"
  //     }
  //   },
  //   {
  //     title: "Clogged Urinal",
  //     description: "Help me unclog urinal!",
  //     location: {
  //       lat: 43.66336,
  //       lng: -79.3870336
  //     },
  //     contact: {
  //       phone: "647-647-6477",
  //       email: "myemail@gmail.com"
  //     }
  //   }
  // ];

  const navigate = useNavigate();
  const landingRouteChange = () => {
    const path = "/";
    navigate(path);
  };
  const createPostRouteChange = () => {
    const path = "/create-post";
    navigate(path);
  };

  return requests ? (
    <div className="main-container">
      <p className="warepair">Warepair</p>
      <button className="sign-out-button" onClick={landingRouteChange}>
        Sign Out
      </button>
      <div className="sidebar">
        <div className="post-container">
          <button
            className="create-post-button"
            onClick={createPostRouteChange}
          >
            Create Post
          </button>
        </div>
      </div>
      <GoogleMap
        center={center}
        mapContainerStyle={containerStyle}
        zoom={15}
        options={defaultMapOptions}
        onClick={() => setHelpLocation({})}
        onLoad={(map) => setTimeout(() => setMapInstance(map))}
      >
        {requests &&
          map &&
          requests.map((item) => {
            let pos = { lat: parseFloat(item[6]), lng: parseFloat(item[5]) };
            console.log(center);
            return (
              <Marker
                position={pos}
                onClick={() => {
                  setHelpLocation(item);
                }}
              />
            );
          })}
        {helpLocation[4] && (
          <InfoWindow
            position={{
              lat: parseFloat(helpLocation[6]),
              lng: parseFloat(helpLocation[5]),
            }}
            clickable={true}
            onCloseClick={() => setHelpLocation({})}
          >
            <div>
              <img
                src={
                  "https://fox5sandiego.com/wp-content/uploads/sites/15/2022/05/okmulgeeimage2crop.jpg?w=768"
                }
                width="300px"
                alt="Clogged Toilet"
                style={{ marginTop: 10 }}
              />
              <h2>{helpLocation[2]}</h2>
              <p>{helpLocation[7]}</p>
              <p>{helpLocation[3]}</p>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </div>
  ) : (
    <h1>The Map Cannot Load</h1>
  );
};

export default MapInterface;
