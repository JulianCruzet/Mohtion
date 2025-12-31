"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Code, GitMerge, Search, ShieldCheck, Cpu } from "lucide-react";

// Data
const NODES = [
  {
    id: "scan",
    title: "RECONNAISSANCE",
    status: "SCANNING TARGETS...",
    icon: <Search className="w-5 h-5" />,
    color: "text-blue-500",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20",
    position: "top-0 left-1/2 -translate-x-1/2 -translate-y-[120%]", // Top
  },
  {
    id: "refactor",
    title: "REFACTORING",
    status: "GENERATING PATCH...",
    icon: <Code className="w-5 h-5" />,
    color: "text-orange-500",
    bg: "bg-orange-500/10",
    border: "border-orange-500/20",
    position: "right-0 top-1/2 translate-x-[120%] -translate-y-1/2", // Right
  },
  {
    id: "verify",
    title: "VERIFICATION",
    status: "RUNNING TESTS...",
    icon: <ShieldCheck className="w-5 h-5" />,
    color: "text-green-500",
    bg: "bg-green-500/10",
    border: "border-green-500/20",
    position: "bottom-0 left-1/2 -translate-x-1/2 translate-y-[120%]", // Bottom
  },
  {
    id: "pr",
    title: "BOUNTY CLAIM",
    status: "OPENING PR...",
    icon: <GitMerge className="w-5 h-5" />,
    color: "text-purple-500",
    bg: "bg-purple-500/10",
    border: "border-purple-500/20",
    position: "left-0 top-1/2 -translate-x-[120%] -translate-y-1/2", // Left
  },
];

const SatelliteNode = ({ node }: { node: typeof NODES[0] }) => {
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      whileInView={{ scale: 1, opacity: 1 }}
      className={cn(
        "absolute w-48 p-4 rounded-xl border backdrop-blur-sm bg-white/80 shadow-xl z-10 flex flex-col gap-2",
        node.position,
        node.border
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <div className={cn("p-1.5 rounded-md", node.bg, node.color)}>
          {node.icon}
        </div>
        <span className="text-xs font-bold text-zinc-600 tracking-wider">{node.title}</span>
      </div>
      <div className="font-mono text-[10px] text-zinc-400 animate-pulse">
        {">"} {node.status}
      </div>
      
      {/* Activity Bar */}
      <div className="h-1 w-full bg-zinc-100 rounded-full overflow-hidden">
        <motion.div 
            className={cn("h-full", node.color.replace("text-", "bg-"))}
            animate={{ x: ["-100%", "100%"] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />
      </div>
    </motion.div>
  );
};

const ConnectionBeam = ({ angle, delay }: { angle: number; delay: number }) => {
  return (
    <div
        className="absolute top-1/2 left-1/2 w-[200px] h-[2px] origin-left bg-zinc-200"
        style={{ transform: `rotate(${angle}deg)` }}
    >
        <motion.div
            className="absolute top-0 left-0 w-12 h-full bg-gradient-to-r from-transparent via-orange-500 to-transparent"
            animate={{ left: ["0%", "100%"], opacity: [0, 1, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear", delay }}
        />
    </div>
  );
};

export function NeuralLifecycle() {
  // Generate random delays once for each beam to maintain React purity
  // Using useState with lazy initializer to avoid calling Math.random during render
  const [beamDelays] = useState(() => [
    Math.random(),
    Math.random(),
    Math.random(),
    Math.random(),
  ]);

  return (
    <section className="py-40 bg-zinc-50 overflow-hidden relative min-h-[800px] flex items-center justify-center">

      {/* Background Grid */}
      <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:20px_20px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_70%,transparent_100%)] opacity-50" />

      <div className="relative w-[100px] h-[100px] flex items-center justify-center">

        {/* Core Node */}
        <motion.div
            className="relative z-20 w-24 h-24 bg-white rounded-full border-2 border-zinc-200 shadow-2xl flex items-center justify-center"
            animate={{ boxShadow: ["0 0 20px rgba(0,0,0,0.05)", "0 0 40px rgba(249,115,22,0.2)", "0 0 20px rgba(0,0,0,0.05)"] }}
            transition={{ duration: 3, repeat: Infinity }}
        >
            <Cpu className="w-10 h-10 text-zinc-800" />
            <div className="absolute inset-0 rounded-full border border-orange-500/30 animate-ping opacity-20" />
        </motion.div>

        {/* Beams */}
        <ConnectionBeam angle={-90} delay={beamDelays[0]} /> {/* Top */}
        <ConnectionBeam angle={0} delay={beamDelays[1]} />   {/* Right */}
        <ConnectionBeam angle={90} delay={beamDelays[2]} />  {/* Bottom */}
        <ConnectionBeam angle={180} delay={beamDelays[3]} /> {/* Left */}

        {/* Satellites */}
        {NODES.map((node) => (
            <SatelliteNode key={node.id} node={node} />
        ))}

      </div>

      <div className="absolute bottom-10 text-center">
        <p className="text-zinc-400 text-sm font-mono">SYSTEM STATUS: <span className="text-green-500">OPERATIONAL</span></p>
      </div>

    </section>
  );
}
