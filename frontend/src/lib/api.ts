type BoardData = any;

const isOnlineApi = async (path: string, opts?: RequestInit) => {
  try {
    const res = await fetch(path, { ...opts, credentials: "include" });
    if (!res.ok) throw new Error("bad");
    return res;
  } catch (e) {
    return null;
  }
};

export async function login(username: string, password: string) {
  const res = await isOnlineApi("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (res) return true;

  // fallback: validate against localStorage users
  const users = JSON.parse(localStorage.getItem("pm_users") || "{}");
  if (users[username] && users[username] === password) {
    localStorage.setItem("pm_session", username);
    return true;
  }
  return false;
}

export async function register(username: string, password: string) {
  const res = await isOnlineApi("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (res) return true;

  // fallback: save to localStorage
  const users = JSON.parse(localStorage.getItem("pm_users") || "{}");
  if (users[username]) return false;
  users[username] = password;
  localStorage.setItem("pm_users", JSON.stringify(users));
  return true;
}

export async function getSession(): Promise<string | null> {
  const res = await isOnlineApi("/api/session");
  if (res) {
    const data = await res.json();
    return data.user || null;
  }
  return localStorage.getItem("pm_session");
}

export async function logout() {
  await isOnlineApi("/api/logout", { method: "POST" });
  localStorage.removeItem("pm_session");
}

export async function getKanban(): Promise<BoardData> {
  const res = await isOnlineApi("/api/kanban");
  if (res) return res.json();

  const user = localStorage.getItem("pm_session") || "guest";
  const data = localStorage.getItem("pm_board_" + user);
  if (data) return JSON.parse(data);
  // default board shape
  return {
    cards: {},
    columns: [
      { id: "col-todo", title: "To do", cardIds: [] },
      { id: "col-inprogress", title: "In progress", cardIds: [] },
      { id: "col-review", title: "Review", cardIds: [] },
      { id: "col-done", title: "Done", cardIds: [] },
      { id: "col-backlog", title: "Backlog", cardIds: [] },
    ],
  };
}

export async function saveKanban(board: BoardData) {
  const res = await isOnlineApi("/api/kanban", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(board),
  });
  if (res) return true;

  const user = localStorage.getItem("pm_session") || "guest";
  localStorage.setItem("pm_board_" + user, JSON.stringify(board));
  return true;
}

export default {
  login,
  register,
  getSession,
  logout,
  getKanban,
  saveKanban,
};
