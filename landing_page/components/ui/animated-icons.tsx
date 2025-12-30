"use client";
import { motion } from "framer-motion";
import { Code, GitMerge, Search, ShieldCheck } from "lucide-react";

export const ScanIcon = () => (
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

export const CodeIcon = () => (
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

export const ShieldIcon = () => (
  <div className="relative flex items-center justify-center w-10 h-10">
    <motion.div
      className="absolute inset-0 border border-orange-200 rounded-full"
      animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
      transition={{ duration: 3, repeat: Infinity }}
    />
    <ShieldCheck className="w-5 h-5 text-orange-600 relative z-10" />
  </div>
);

export const MergeIcon = () => (
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
