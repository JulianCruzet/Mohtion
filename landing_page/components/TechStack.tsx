"use client";
import { motion } from "framer-motion";
import Image from "next/image";

export function TechStack() {
  const techs = [
    { name: "Python", logo: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" },
    { name: "Claude AI", logo: "https://avatars.githubusercontent.com/u/76263028?s=200&v=4" },
    { name: "GitHub", logo: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" },
    { name: "FastAPI", logo: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" },
    { name: "Docker", logo: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" },
  ];

  return (
    <section className="py-12 bg-zinc-900 border-y border-zinc-800 relative overflow-hidden">
      
      <div className="container mx-auto px-6 relative z-10">
        <p className="text-center text-[10px] font-bold text-zinc-400 tracking-[0.2em] uppercase mb-8">
          Built with Industry Leading Tech
        </p>
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-16 transition-all duration-700">
          {techs.map((tech) => (
            <motion.div
              key={tech.name}
              className="flex items-center gap-2"
              whileHover={{ y: -2 }}
            >
              <Image
                src={tech.logo}
                alt={tech.name}
                width={24}
                height={24}
                className="h-6 w-auto object-contain"
                unoptimized
              />
              <span className="text-zinc-100 font-bold text-sm tracking-tight">{tech.name}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
