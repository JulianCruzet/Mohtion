"use client";

import { motion } from "framer-motion";
import { ArrowRight, Search, Code, ShieldCheck, GitMerge } from "lucide-react";

const steps = [
  {
    title: "Reconnaissance",
    desc: "Mohtion scans your repository for high-complexity targets and technical debt hotspots.",
    icon: Search,
  },
  {
    title: "Refactoring",
    desc: "The agent generates a fix using LLM-driven analysis, preserving external API signatures.",
    icon: Code,
  },
  {
    title: "Verification",
    desc: "Tests run in a sandbox. If they fail, Mohtion self-heals by analyzing the logs and retrying.",
    icon: ShieldCheck,
  },
  {
    title: "Bounty Claim",
    desc: "A polished PR is opened only if all checks pass. You review, merge, and close the debt.",
    icon: GitMerge,
  },
];

export function HowItWorks() {
  return (
    <section className="py-32 bg-white relative border-t border-zinc-100">
      <div className="container px-6 mx-auto">
        <div className="mb-20 text-center">
          <span className="text-orange-500 font-mono text-sm tracking-widest uppercase mb-4 block">The Lifecycle</span>
          <h2 className="text-3xl md:text-5xl font-bold text-zinc-900 tracking-tight">
            Autonomous from start to finish.
          </h2>
        </div>

        <div className="max-w-4xl mx-auto relative">
          {/* Vertical Line */}
          <div className="absolute left-[28px] md:left-1/2 top-0 bottom-0 w-px bg-zinc-200" />

          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className={`relative flex items-center gap-8 mb-16 md:mb-24 ${
                i % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"
              }`}
            >
              {/* Icon Marker */}
              <div className="absolute left-0 md:left-1/2 -translate-x-1/2 w-14 h-14 rounded-full bg-white border border-zinc-200 flex items-center justify-center z-10 shadow-sm">
                <step.icon className="w-6 h-6 text-zinc-600" />
              </div>

              {/* Spacer for mobile layout alignment */}
              <div className="w-14 md:w-1/2 shrink-0" />

              {/* Content Card */}
              <div className="flex-1 p-6 md:p-8 rounded-2xl bg-zinc-50 border border-zinc-100 hover:border-orange-200 transition-colors">
                <h3 className="text-xl font-bold text-zinc-900 mb-3">{step.title}</h3>
                <p className="text-zinc-500 leading-relaxed">
                  {step.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}