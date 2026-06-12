"use client";
import { useState } from "react";

export function AiSidebar() {
  const [open, setOpen] = useState(true);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Array<{ from: string; text: string }>>([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input) return;
    const text = input;
    setMessages((m) => [...m, { from: "user", text }]);
    setInput("");
    setLoading(true);
    try {
      // Use relative API path so dev proxy handles routing and avoids CORS.
      const res = await fetch(`/api/ai/test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: text }),
      });
      const j = await res.json();
      const reply = j.result ?? JSON.stringify(j);
      setMessages((m) => [...m, { from: "ai", text: String(reply) }]);
    } catch (e) {
      setMessages((m) => [...m, { from: "ai", text: "Error calling AI" }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ position: "fixed", right: 0, top: 0, bottom: 0, width: open ? 360 : 40, background: "#f8fafc", borderLeft: "1px solid #e5e7eb", display: "flex", flexDirection: "column", zIndex: 50 }}>
      <div style={{ padding: 8, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        {open && <strong>AI Assistant</strong>}
        <button onClick={() => setOpen((s) => !s)} style={{ marginLeft: 8 }}>{open ? "‹" : "›"}</button>
      </div>
      {open && (
        <div style={{ padding: 8, display: "flex", flexDirection: "column", flex: 1 }}>
          <div style={{ flex: 1, overflow: "auto", padding: 4 }}>
            {messages.map((m, i) => (
              <div key={i} style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 12, color: "#6b7280" }}>{m.from}</div>
                <div style={{ background: m.from === "ai" ? "#eef2ff" : "#f1f5f9", padding: 8, borderRadius: 6 }}>{m.text}</div>
              </div>
            ))}
          </div>

          <div style={{ display: "flex", gap: 8 }}>
            <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask the AI..." style={{ flex: 1, padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
            <button onClick={send} disabled={loading} style={{ padding: "8px 12px", borderRadius: 6, background: "#753991", color: "white", border: "none" }}>{loading ? "..." : "Send"}</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default AiSidebar;
