"use client";

import { motion } from "framer-motion";
import { Shield, Zap, GitPullRequest, Code2, RefreshCw, Lock } from "lucide-react";

const features = [
  {
    icon: Code2,
    title: "Deep AST Analysis",
    description: "Mohtion doesn't just regex your code. It builds an Abstract Syntax Tree to understand cyclomatic complexity and structural debt.",
  },
  {
    icon: Zap,
    title: "Autonomous Refactoring",
    description: "Powered by Claude 3.5 Sonnet, Mohtion rewrites complex functions while preserving their behavior and external API signatures.",
  },
  {
    icon: Shield,
    title: "Safety-First Architecture",
    description: "We never open a PR if your tests fail. Mohtion runs your test suite in a sandboxed environment before committing.",
  },
  {
    icon: RefreshCw,
    title: "Self-Healing Agents",
    description: "If a refactor breaks a test, Mohtion analyzes the error log, adjusts the code, and retries automatically (up to 2x).",
  },
  {
    icon: GitPullRequest,
    title: "Native GitHub App",
    description: "Installs directly on your repo. No complex CI/CD wiring required. Works via webhooks and background workers.",
  },
  {
    icon: Lock,
    title: "Zero-Trust Security",
    description: "Your code is processed in ephemeral containers. Credentials are encrypted. We only touch the branches we create.",
  },
];

export function Features() {
  return (
    <section className="py-32 bg-slate-950 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-500/10 blur-[100px] rounded-full" />

      <div className="container px-6 mx-auto relative z-10">
        <div className="text-center max-w-2xl mx-auto mb-20">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tighter text-white mb-6">
            Technical Debt is <br />
            <span className="text-indigo-400">No Longer Your Problem.</span>
          </h2>
          <p className="text-slate-400 text-lg">
            Mohtion operates as a senior engineer on your team, handling the cleanup work you never have time for.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="group p-8 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-indigo-500/30 transition-all hover:bg-slate-900/80"
            >
              <div className="w-12 h-12 rounded-lg bg-indigo-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-indigo-200 transition-colors">
                {feature.title}
              </h3>
              <p className="text-slate-400 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
