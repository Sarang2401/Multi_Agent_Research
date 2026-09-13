/**
 * useHistory.ts — Simple in-memory session history hook.
 */
import { useState } from "react";

export interface HistoryEntry {
  id: string;
  type: string;
  title: string;
  content: string;
  timestamp: Date;
}

export function useHistory() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  const addEntry = (type: string, title: string, content: string) => {
    setHistory((prev) => [
      {
        id: Date.now().toString(),
        type,
        title,
        content,
        timestamp: new Date(),
      },
      ...prev,
    ]);
  };

  return { history, addEntry };
}
