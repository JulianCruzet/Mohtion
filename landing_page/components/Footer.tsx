export function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 py-12">
      <div className="container px-6 mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-indigo-500 rounded-md" />
          <span className="text-white font-bold tracking-tight">Mohtion</span>
        </div>
        
        <div className="text-slate-500 text-sm">
          © {new Date().getFullYear()} Mohtion Labs. All rights reserved.
        </div>

        <div className="flex gap-6">
          <a href="#" className="text-slate-400 hover:text-white transition-colors text-sm">GitHub</a>
          <a href="#" className="text-slate-400 hover:text-white transition-colors text-sm">Twitter</a>
          <a href="#" className="text-slate-400 hover:text-white transition-colors text-sm">Docs</a>
        </div>
      </div>
    </footer>
  );
}
