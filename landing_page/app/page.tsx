import { Hero } from "@/components/Hero";
import { Features } from "@/components/Features";
import { HowItWorks } from "@/components/HowItWorks";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 selection:bg-indigo-500/30">
      <Hero />
      <HowItWorks />
      <Features />
      <Footer />
    </main>
  );
}
