// App.tsx
import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Room from "./Room";
import "./App.css";

function Home() {
  return (
    <div className="container">
      <div className="header">
        <h1>Pair Proto</h1>
        <div className="divider" />
      </div>
      <div className="content">
        <p className="instruction">
          Create a room via <code>POST /rooms</code>, then navigate to{" "}
          <code>/room/&lt;roomId&gt;</code>
        </p>
        <Link to="/room/demo" className="button">
          Open Demo Room →
        </Link>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/room/:roomId" element={<Room />} />
        <Route path="/room" element={<Room />} />
      </Routes>
    </BrowserRouter>
  );
}