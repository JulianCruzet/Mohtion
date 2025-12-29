"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Terminal, Check, X, GitPullRequest, Search, Zap } from "lucide-react";
import clsx from "clsx";

const LOGS = [
  { type: "info", text: "Scanning repository...", icon: Search, color: "text-blue-500" },
  { type: "success", text: "Found target: Complexity > 15 (auth.py)", icon: Zap, color: "text-orange-500" },
  { type: "info", text: "Refactoring with Claude Sonnet...", icon: Terminal, color: "text-purple-500" },
  { type: "info", text: "Verifying changes with pytest...", icon: Terminal, color: "text-zinc-500" },
  { type: "success", text: "Tests passed (142/142)!", icon: Check, color: "text-emerald-500" },
  { type: "success", text: "PR Created: mohtion/bounty-8f2a", icon: GitPullRequest, color: "text-emerald-500" },
];

export function TerminalDemo() {
  const [lines, setLines] = useState<number>(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setLines((prev) => (prev < LOGS.length ? prev + 1 : 0));
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full mx-auto bg-white rounded-xl overflow-hidden border border-zinc-200 shadow-2xl shadow-zinc-200/50">
      {/* Window Controls (macOS Light Mode) */}
      <div className="flex items-center gap-2 px-4 py-3 bg-zinc-50 border-b border-zinc-200">
        <div className="w-3 h-3 rounded-full bg-[#FF5F56] border border-[#E0443E]" />
        <div className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-[#DEA123]" />
        <div className="w-3 h-3 rounded-full bg-[#27C93F] border border-[#1AAB29]" />
        <div className="ml-2 text-xs font-mono text-zinc-400">mohtion-worker — 85x24</div>
      </div>

      {/* Terminal Content (Light Mode Terminal) */}
      <div className="p-6 font-mono text-sm h-[320px] flex flex-col gap-3 bg-white text-zinc-700">
        {LOGS.slice(0, lines + 1).map((log, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <log.icon className={clsx("w-4 h-4", log.color)} />
            <span className={clsx("font-medium", log.type === "success" ? "text-zinc-800" : "text-zinc-600")}>
              {log.text}
            </span>
          </motion.div>
        ))}
        {lines < LOGS.length && (
          <motion.div
            animate={{ opacity: [0, 1] }}
            transition={{ repeat: Infinity, duration: 0.8 }}
            className="w-2 h-4 bg-zinc-400"
          />
        )}
      </div>
    </div>
  );
}