"use client"

import { useState } from "react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [register, setRegister] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
        const path = register ? "/api/register" : "/api/login";
        const res = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
          credentials: "include",
      });
      if (res.ok) {
        if (register) {
          // after register, switch to login mode
          setRegister(false);
          setError("Registered successfully — please sign in");
        } else {
          window.location.href = "/";
        }
      } else {
        const data = await res.json();
        setError(data.detail || "Login failed");
      }
    } catch (err) {
      setError("Network error");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
        <h2 className="text-2xl font-semibold mb-4 text-[var(--navy-dark)]">{register ? "Create account" : "Sign in"}</h2>
        <form onSubmit={submit} className="flex flex-col gap-3">
          <label className="text-sm text-[var(--gray-text)]">Username</label>
          <input
            className="rounded-md border px-3 py-2"
            placeholder="username"
            name="username"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <label className="text-sm text-[var(--gray-text)]">Password</label>
          <input
            className="rounded-md border px-3 py-2"
            placeholder="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <div className="flex items-center gap-2">
            <button className="mt-2 rounded-md bg-[var(--primary-blue)] px-4 py-2 text-white font-semibold" type="submit">
              {register ? "Register" : "Sign in"}
            </button>
            <button type="button" className="mt-2 rounded-md border px-4 py-2" onClick={() => { setRegister(!register); setError(""); }}>
              {register ? "Back to Sign in" : "Create account"}
            </button>
          </div>
          {error && <div className="text-sm text-red-600">{error}</div>}
          <div className="mt-2 text-xs text-[var(--gray-text)]">Tip: create a new account or use demo: user / password</div>
        </form>
      </div>
    </main>
  );
}
