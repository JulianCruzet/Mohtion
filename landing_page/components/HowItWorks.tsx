import { TracingBeam } from "@/components/ui/tracing-beam";
import { motion } from "framer-motion";
import { Code, GitMerge, Search, ShieldCheck } from "lucide-react";

const steps = [
  {
    title: "Reconnaissance",
    desc: "Mohtion scans your repository for high-complexity targets and technical debt hotspots.",
    icon: Search,
    badge: "Step 01",
  },
  {
    title: "Refactoring",
    desc: "The agent generates a fix using LLM-driven analysis, preserving external API signatures.",
    icon: Code,
    badge: "Step 02",
  },
  {
    title: "Verification",
    desc: "Tests run in a sandbox. If they fail, Mohtion self-heals by analyzing the logs and retrying.",
    icon: ShieldCheck,
    badge: "Step 03",
  },
  {
    title: "Bounty Claim",
    desc: "A polished PR is opened only if all checks pass. You review, merge, and close the debt.",
    icon: GitMerge,
    badge: "Step 04",
  },
];

export function HowItWorks() {
  return (
    <section className="py-24 bg-zinc-50 relative overflow-hidden">
        <div className="container mx-auto px-6 mb-12 text-center">
            <h2 className="text-3xl font-bold text-zinc-900 tracking-tight">
                The Lifecycle
            </h2>
            <p className="text-zinc-500 mt-2">Autonomous from start to finish.</p>
        </div>

      <TracingBeam className="px-6">
        <div className="max-w-2xl mx-auto antialiased pt-4 relative">
          {steps.map((item, index) => (
            <div key={`content-${index}`} className="mb-20 last:mb-0">
                <div className="flex items-center gap-4 mb-4">
                    <div className="bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-bold font-mono border border-orange-200">
                        {item.badge}
                    </div>
                    <h2 className="text-xl font-bold text-zinc-900">
                        {item.title}
                    </h2>
                </div>

              <div className="p-6 bg-white rounded-xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow">
                {/* Icon */}
                <div className="w-10 h-10 bg-zinc-100 rounded-lg flex items-center justify-center mb-4">
                    <item.icon className="w-5 h-5 text-zinc-600" />
                </div>
                <div className="text-sm prose prose-sm dark:prose-invert text-zinc-500">
                  {item.desc}
                </div>
              </div>
            </div>
          ))}
        </div>
      </TracingBeam>
    </section>
  );
}
