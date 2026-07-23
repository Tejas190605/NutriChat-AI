import React from "react";
import { clsx } from "clsx";

export interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = "md", className }) => {
  const sizes = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-3",
    lg: "h-12 w-12 border-4",
  };

  return (
    <div
      className={clsx(
        "animate-spin rounded-full border-emerald-500 border-t-transparent",
        sizes[size],
        className
      )}
    />
  );
};
