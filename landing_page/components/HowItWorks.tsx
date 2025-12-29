"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Reconnaissance",
    desc: "Mohtion scans your repo for high-complexity targets.",
    color: "from-blue-500 to-cyan-500",
  },
  {
    number: "02",
    title: "Refactoring",
    desc: "The agent generates a fix using LLM-driven analysis.",
    color: "from-indigo-500 to-purple-500",
  },
  {
    number: "03",
    title: "Verification",
    desc: "Tests run in a sandbox. Self-healing activates on failure.",
    color: "from-fuchsia-500 to-pink-500",
  },
  {
    number: "04",
    title: "Bounty Claim",
    desc: "A polished PR is opened only if all checks pass.",
    color: "from-emerald-500 to-teal-500",
  },
];

export function HowItWorks() {
  return (
    <section className="py-32 bg-[#020617] relative">
      <div className="container px-6 mx-auto">
        <div className="mb-20">
          <span className="text-indigo-400 font-mono text-sm tracking-widest uppercase mb-4 block">The Loop</span>
          <h2 className="text-3xl md:text-4xl font-bold text-white max-w-2xl">
            Autonomous Plan-Act-Verify Cycle
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
          {/* Connecting Line (Desktop) */}
          <div className="hidden md:block absolute top-12 left-0 w-full h-0.5 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-emerald-500/20" />

          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.2 }}
              className="relative z-10"
            >
              <div className={`w-24 h-24 rounded-2xl bg-gradient-to-br ${step.color} p-0.5 mb-8 shadow-2xl`}>
                <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center relative overflow-hidden group">
                  <div className={`absolute inset-0 bg-gradient-to-br ${step.color} opacity-10 group-hover:opacity-20 transition-opacity`} />
                  <span className="text-3xl font-bold text-white font-mono">{step.number}</span>
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                {step.title}
                {i < 3 && <ArrowRight className="md:hidden w-4 h-4 text-slate-500" />}
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed border-l-2 border-slate-800 pl-4 md:border-0 md:pl-0">
                {step.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
