import { useEffect, useRef, useState } from "react";

export default function useWebSocket(url) {
  const socketRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!url) return;
    const ws = new WebSocket(url);
    socketRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onerror = () => setIsConnected(false);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      } catch {
        setMessages((prev) => [...prev, { text: event.data }]);
      }
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = (payload) => {
    const ws = socketRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      const text = typeof payload === "string" ? payload : JSON.stringify(payload);
      ws.send(text);
    }
  };

  return { isConnected, messages, sendMessage };
}


