"use client";

import { motion } from "framer-motion";
import { TerminalDemo } from "./TerminalDemo";
import { ArrowRight, Terminal } from "lucide-react";

export function Hero() {
  return (
    <section className="relative min-h-[90vh] flex flex-col items-center justify-center bg-zinc-50 overflow-hidden pt-20">
      
      {/* Background Pattern */}
      <div className="absolute inset-0 w-full h-full bg-zinc-50 bg-dot-black/[0.2] pointer-events-none flex items-center justify-center">
        {/* Radial gradient mask */}
        <div className="absolute pointer-events-none inset-0 flex items-center justify-center bg-zinc-50 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>
      </div>

      <div className="relative z-10 container px-6 mx-auto flex flex-col items-center text-center">
        
        {/* Badge */}
        <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-zinc-200 bg-white shadow-sm mb-8"
        >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-orange-500"></span>
            </span>
            <span className="text-xs font-semibold text-zinc-600 tracking-wide uppercase">Mohtion Public Beta</span>
        </motion.div>

        {/* Headline */}
        <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold tracking-tighter text-zinc-900 mb-6 max-w-4xl"
        >
          Pay Down Tech Debt <br/>
          <span className="text-zinc-400">While You Sleep.</span>
        </motion.h1>

        {/* Subhead */}
        <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-lg md:text-xl text-zinc-500 max-w-2xl mb-10 leading-relaxed"
        >
          The autonomous agent that monitors your repositories, identifies complexity, and opens Pull Requests with verified fixes.
        </motion.p>

        {/* Buttons */}
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center gap-4 mb-20"
        >
            <button className="px-8 py-3 bg-zinc-900 text-white rounded-lg font-medium hover:bg-zinc-800 transition-colors shadow-lg shadow-zinc-900/20 flex items-center gap-2">
                <Terminal className="w-4 h-4" />
                Install GitHub App
            </button>
            <button className="px-8 py-3 bg-white text-zinc-600 border border-zinc-200 rounded-lg font-medium hover:bg-zinc-50 transition-colors flex items-center gap-2 group">
                Read Documentation
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
        </motion.div>

        {/* Terminal Visual */}
        <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 40 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="w-full max-w-3xl relative"
        >
            <div className="absolute -inset-1 bg-gradient-to-r from-orange-500 to-blue-500 rounded-2xl blur-lg opacity-20" />
            <TerminalDemo />
        </motion.div>

      </div>
    </section>
  );
}