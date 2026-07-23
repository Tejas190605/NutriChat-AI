import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Compass } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center p-6 bg-slate-950 text-center">
      <div className="p-4 rounded-full bg-slate-900 border border-slate-800 text-emerald-400 mb-4">
        <Compass className="h-10 w-10 animate-spin" style={{ animationDuration: "12s" }} />
      </div>
      <h1 className="text-4xl font-extrabold text-white">404</h1>
      <h2 className="text-lg font-semibold text-slate-300 mt-2">Page Not Found</h2>
      <p className="text-xs text-slate-400 max-w-sm mt-1">
        The requested URL or resource does not exist or has been moved.
      </p>
      <Link href="/dashboard" className="mt-6">
        <Button size="sm">Back to Dashboard</Button>
      </Link>
    </div>
  );
}
