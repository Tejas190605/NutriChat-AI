import React from "react";
import Image from "next/image";
import { clsx } from "clsx";

export interface AvatarProps {
  src?: string;
  name: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({ src, name, size = "md", className }) => {
  const initials = name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const sizes = {
    sm: "h-8 w-8 text-xs",
    md: "h-10 w-10 text-sm",
    lg: "h-12 w-12 text-base",
  };

  const pixelSizes = {
    sm: 32,
    md: 40,
    lg: 48,
  };

  if (src) {
    return (
      <Image
        src={src}
        alt={name}
        width={pixelSizes[size]}
        height={pixelSizes[size]}
        className={clsx("rounded-full object-cover border border-slate-700", sizes[size], className)}
      />
    );
  }

  return (
    <div
      className={clsx(
        "rounded-full bg-emerald-600/20 text-emerald-400 font-bold flex items-center justify-center border border-emerald-500/30",
        sizes[size],
        className
      )}
    >
      {initials}
    </div>
  );
};
