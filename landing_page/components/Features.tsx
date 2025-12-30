"use client";

import { BentoGrid, BentoGridItem } from "@/components/ui/bento-grid";
import { Code2, Shield, GitPullRequest, Zap } from "lucide-react";
import { motion } from "framer-motion";

const Skeleton = ({ children }: { children?: React.ReactNode }) => (
  <div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl bg-gradient-to-br from-zinc-100 to-zinc-200 border border-zinc-100 overflow-hidden relative">
    {children}
    <div className="absolute inset-0 bg-white/50 backdrop-blur-[1px]" />
    <div className="relative z-10 w-full h-full p-4">{children}</div>
  </div>
);

const items = [
  {
    title: "Deep AST Analysis",
    description: "Parsing your codebase into an Abstract Syntax Tree to identify cyclomatic complexity and structural debt.",
    header: (
      <Skeleton>
        <div className="space-y-2 font-mono text-xs text-zinc-400">
          <div className="bg-zinc-300 h-2 w-3/4 rounded" />
          <div className="bg-zinc-300 h-2 w-1/2 rounded ml-4" />
          <div className="bg-red-200 h-2 w-2/3 rounded ml-8" />
          <div className="bg-zinc-300 h-2 w-1/2 rounded ml-4" />
        </div>
      </Skeleton>
    ),
    icon: <Code2 className="h-4 w-4 text-zinc-500" />,
    className: "md:col-span-2",
  },
  {
    title: "Safety Sandbox",
    description: "Tests run in isolated ephemeral containers. No PR is ever created if the test suite fails.",
    header: (
      <Skeleton>
        <div className="flex items-center justify-center h-full">
          <Shield className="w-12 h-12 text-zinc-300" />
        </div>
      </Skeleton>
    ),
    icon: <Shield className="h-4 w-4 text-zinc-500" />,
    className: "md:col-span-1",
  },
  {
    title: "Autonomous Refactoring",
    description: "Powered by Claude Sonnet, replacing brittle logic with robust, clean patterns.",
    header: (
      <Skeleton>
         <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-red-400 rounded-full" />
            <div className="h-1 w-12 bg-zinc-300 rounded" />
         </div>
         <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full" />
            <div className="h-1 w-16 bg-zinc-300 rounded" />
         </div>
      </Skeleton>
    ),
    icon: <Zap className="h-4 w-4 text-zinc-500" />,
    className: "md:col-span-1",
  },
  {
    title: "Native GitHub App",
    description: "Zero config CI/CD. Installs as a bot on your repository and listens for webhooks.",
    header: (
        <Skeleton>
            <div className="flex items-center justify-center h-full">
                <GitPullRequest className="w-12 h-12 text-zinc-300" />
            </div>
        </Skeleton>
    ),
    icon: <GitPullRequest className="h-4 w-4 text-zinc-500" />,
    className: "md:col-span-2",
  },
];

export function Features() {
  return (
    <section className="py-24 bg-white relative">
      <div className="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-zinc-100/50 to-transparent pointer-events-none" />
      <div className="container mx-auto px-6 mb-12">
        <h2 className="text-3xl font-bold text-zinc-900 mb-4 tracking-tight">
          Engineered for <span className="text-orange-500">Autonomy</span>.
        </h2>
        <p className="text-zinc-500 max-w-2xl">
          Mohtion is not a linter. It is an agent that acts on your behalf to clean up the mess you don't have time for.
        </p>
      </div>
      <BentoGrid className="max-w-6xl mx-auto px-6">
        {items.map((item, i) => (
          <BentoGridItem
            key={i}
            title={item.title}
            description={item.description}
            header={item.header}
            icon={item.icon}
            className={item.className}
          />
        ))}
      </BentoGrid>
    </section>
  );
}