"use client";

import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { API_BASE_URL } from "@/lib/api/client";
import type { AgentType, WsAgentUpdate } from "@/lib/types";
import { analysisKeys } from "./use-analyses";

export interface LiveAgentState {
  agent: AgentType;
  status: "pending" | "running" | "completed" | "failed";
}

/**
 * Subscribes to the analysis WebSocket and tracks per-agent live status.
 * Falls back gracefully if the socket cannot connect (the polling query in
 * `useAnalysis` still drives UI updates).
 */
export function useAnalysisSocket(analysisId: string | null) {
  const queryClient = useQueryClient();
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState<WsAgentUpdate[]>([]);
  const [agentStatus, setAgentStatus] = useState<Record<string, LiveAgentState["status"]>>({});
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!analysisId) return;
    const wsBase = API_BASE_URL.replace(/^http/, "ws");
    const ws = new WebSocket(`${wsBase}/ws/analyses/${analysisId}`);
    socketRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as WsAgentUpdate;
        setEvents((prev) => [...prev, message]);
        if (message.type === "agent_update" && message.agent && message.status) {
          setAgentStatus((prev) => ({
            ...prev,
            [message.agent as string]: message.status as LiveAgentState["status"],
          }));
        }
        if (message.type === "analysis_completed") {
          queryClient.invalidateQueries({ queryKey: analysisKeys.detail(analysisId) });
          queryClient.invalidateQueries({ queryKey: analysisKeys.all });
        }
      } catch {
        /* ignore malformed frames */
      }
    };

    return () => {
      ws.close();
      socketRef.current = null;
    };
  }, [analysisId, queryClient]);

  return { connected, events, agentStatus };
}
