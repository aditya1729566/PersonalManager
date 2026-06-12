"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";

export default function Home() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    fetch(`/api/session`, { credentials: "include" })
      .then((r) => {
        if (!r.ok) throw new Error("unauth");
        return r.json();
      })
      .then(() => {
        if (mounted) setLoading(false);
      })
      .catch(() => {
        window.location.href = "/login";
      });
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) return <div>Loading...</div>;

  return <KanbanBoard />;
}
