"use client";
import { TracingBeam } from "@/components/ui/tracing-beam";
import { GlowingCard } from "@/components/ui/glowing-card";
import { motion } from "framer-motion";
import { Code, GitMerge, Search, ShieldCheck } from "lucide-react";

// Inline Animated Icons to prevent SSR/Module issues
const ScanIcon = () => (
  <div className="relative flex items-center justify-center w-10 h-10">
    <motion.div
      className="absolute inset-0 bg-orange-100 rounded-full opacity-50"
      animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
    />
    <motion.div
      animate={{ rotate: [0, 15, 0, -15, 0] }}
      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
    >
      <Search className="w-5 h-5 text-orange-600 relative z-10" />
    </motion.div>
  </div>
);

const CodeIcon = () => (
  <div className="relative flex items-center justify-center w-10 h-10">
    <motion.div
      animate={{ scale: [1, 1.1, 1] }}
      transition={{ duration: 2, repeat: Infinity }}
      className="flex gap-0.5"
    >
      <Code className="w-5 h-5 text-orange-600" />
    </motion.div>
  </div>
);

const ShieldIcon = () => (
  <div className="relative flex items-center justify-center w-10 h-10">
    <motion.div
      className="absolute inset-0 border border-orange-200 rounded-full"
      animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
      transition={{ duration: 3, repeat: Infinity }}
    />
    <ShieldCheck className="w-5 h-5 text-orange-600 relative z-10" />
  </div>
);

const MergeIcon = () => (
  <div className="relative flex items-center justify-center w-10 h-10">
    <GitMerge className="w-5 h-5 text-orange-600" />
    <motion.div
        className="absolute w-1 h-1 bg-orange-500 rounded-full"
        initial={{ x: -6, y: 6 }}
        animate={{ x: 0, y: -2 }}
        transition={{ duration: 1.5, repeat: Infinity, repeatDelay: 1 }}
    />
  </div>
);

export function HowItWorks() {
  const steps = [
    {
      title: "Reconnaissance",
      desc: "Mohtion scans your repository for high-complexity targets and technical debt hotspots.",
      icon: ScanIcon,
      badge: "Step 01",
    },
    {
      title: "Refactoring",
      desc: "The agent generates a fix using LLM-driven analysis, preserving external API signatures.",
      icon: CodeIcon,
      badge: "Step 02",
    },
    {
      title: "Verification",
      desc: "Tests run in a sandbox. If they fail, Mohtion self-heals by analyzing the logs and retrying.",
      icon: ShieldIcon,
      badge: "Step 03",
    },
    {
      title: "Bounty Claim",
      desc: "A polished PR is opened only if all checks pass. You review, merge, and close the debt.",
      icon: MergeIcon,
      badge: "Step 04",
    },
  ];

  return (
    <section className="py-24 bg-zinc-50 relative overflow-hidden" id="how-it-works">
        <div className="container mx-auto px-6 mb-12 text-center">
            <h2 className="text-3xl font-bold text-zinc-900 tracking-tight">
                The Lifecycle
            </h2>
            <p className="text-zinc-500 mt-2">Autonomous from start to finish.</p>
        </div>

      <TracingBeam className="px-6">
        <div className="max-w-2xl mx-auto antialiased pt-4 relative">
          {steps.map((item, index) => (
            <motion.div 
                key={`content-${index}`} 
                className="mb-20 last:mb-0"
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
            >
                <div className="flex items-center gap-4 mb-4">
                    <div className="relative bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-bold font-mono border border-orange-200 overflow-hidden">
                        <span className="relative z-10">{item.badge}</span>
                        <motion.div 
                            className="absolute inset-0 bg-white/50"
                            animate={{ x: ["-100%", "200%"] }}
                            transition={{ duration: 2, repeat: Infinity, repeatDelay: 1 }}
                        />
                    </div>
                    <h2 className="text-xl font-bold text-zinc-900">
                        {item.title}
                    </h2>
                </div>

              <GlowingCard className="p-6">
                {/* Icon */}
                <div className="w-10 h-10 bg-zinc-100 rounded-lg flex items-center justify-center mb-4 overflow-hidden">
                    <item.icon />
                </div>
                <div className="text-sm prose prose-sm dark:prose-invert text-zinc-500 leading-relaxed font-medium">
                  {item.desc}
                </div>
              </GlowingCard>
            </motion.div>
          ))}
        </div>
      </TracingBeam>
    </section>
  );
}
