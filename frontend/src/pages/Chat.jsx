import { useMemo, useRef, useState, useEffect } from "react";
import useWebSocket from "../hooks/useWebSocket";

export default function Chat() {
  const [input, setInput] = useState("");
  const wsUrl = useMemo(() => {
    const token = localStorage.getItem("access_token");
    const base = import.meta.env.VITE_WS_BASE || "ws://localhost:8000";
    // Example: /ws/chat/ path in Django Channels (adjust if different)
    const url = `${base}/ws/chat/?token=${token || ""}`;
    return url;
  }, []);

  const { isConnected, messages, sendMessage } = useWebSocket(wsUrl);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage({ type: "message", text: input });
    setInput("");
  };

  return (
    <div className="pt-20 px-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI Coach Chat</h1>
      <div className="text-sm mb-2">Status: {isConnected ? "Connected" : "Disconnected"}</div>
      <div className="h-96 overflow-y-auto bg-white rounded shadow p-4">
        {messages.map((m, idx) => (
          <div key={idx} className="mb-2">
            <span className="font-semibold">{m.role || m.sender || "Bot"}:</span> {m.text || m.message || ""}
          </div>
        ))}
        <div ref={endRef} />
      </div>
      <div className="mt-3 flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about meals, workouts, or nutrition..."
        />
        <button onClick={handleSend} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
          Send
        </button>
      </div>
    </div>
  );
}


