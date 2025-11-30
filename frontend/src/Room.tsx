// Room.tsx
import React, { useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import "./App.css";

const API_BASE = process.env.REACT_APP_API || "http://localhost:8000";

export default function Room() {
  const { roomId } = useParams();
  const wsRef = useRef<WebSocket | null>(null);
  const [code, setCode] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [connected, setConnected] = useState(false);
  const typingTimer = useRef<number | null>(null);
  const debounceAutocomplete = 600;

  useEffect(() => {
    if (!roomId) return;
    const ws = new WebSocket(
      API_BASE.replace(/^http/, "ws") + `/ws/${roomId}`
    );
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("ws open");
      setConnected(true);
    };
    ws.onmessage = (ev) => {
      const data = JSON.parse(ev.data);
      if (data.type === "init") {
        setCode(data.code || "");
      } else if (data.type === "remote_update") {
        setCode(data.code || "");
      }
    };

    ws.onclose = () => {
      console.log("ws closed");
      setConnected(false);
    };
    return () => ws.close();
  }, [roomId]);

  function sendUpdate(nextCode: string) {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "code_update", code: nextCode }));
    }
  }

  function onChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    const next = e.target.value;
    setCode(next);
    sendUpdate(next);

    if (typingTimer.current) window.clearTimeout(typingTimer.current);
    typingTimer.current = window.setTimeout(() => {
      callAutocomplete(next, e.target.selectionStart || next.length);
    }, debounceAutocomplete);
  }

  async function callAutocomplete(c: string, cursor: number) {
    try {
      const r = await fetch(API_BASE + "/autocomplete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: c,
          cursorPosition: cursor,
          language: "python",
        }),
      });
      const j = await r.json();
      setSuggestion(j.suggestion || "");
    } catch (err) {
      setSuggestion("");
    }
  }

  function acceptSuggestion() {
    if (!suggestion) return;
    const next = code + suggestion;
    setCode(next);
    sendUpdate(next);
    setSuggestion("");
  }

  return (
    <div className="container">
      <div className="header">
        <div className="room-info">
          <Link to="/" className="back-link">
            ← Home
          </Link>
          <h2>Room: {roomId || "demo"}</h2>
          <span className={`status ${connected ? "connected" : "disconnected"}`}>
            {connected ? "● Connected" : "○ Disconnected"}
          </span>
        </div>
        <div className="divider" />
      </div>
      <div className="editor-container">
        <div className="editor-panel">
          <div className="panel-header">Editor</div>
          <textarea
            value={code}
            onChange={onChange}
            className="code-editor"
            placeholder="Start typing your code..."
            spellCheck={false}
          />
        </div>
        <div className="suggestion-panel">
          <div className="panel-header">Autocomplete</div>
          <div className="suggestion-box">
            {suggestion || <span className="empty-state">Idle</span>}
          </div>
          <button
            onClick={acceptSuggestion}
            className="button"
            disabled={!suggestion}
          >
            Insert Suggestion
          </button>
        </div>
      </div>
    </div>
  );
}