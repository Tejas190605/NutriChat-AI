"use client";

import React, { useEffect } from "react";
import { ErrorState } from "@/components/ui/error-state";

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Unhandled runtime error:", error);
  }, [error]);

  return (
    <div className="flex h-screen w-full items-center justify-center p-6 bg-slate-950">
      <ErrorState
        title="Application Error"
        message={error.message || "An unexpected system error occurred."}
        onRetry={() => reset()}
      />
    </div>
  );
}
