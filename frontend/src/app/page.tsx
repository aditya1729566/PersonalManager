"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { KanbanBoard } from "@/components/KanbanBoard";

export default function Home() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    api.getSession()
      .then((user) => {
        if (!user) throw new Error("unauth");
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
