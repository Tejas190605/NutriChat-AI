"use client";

import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import { ThemeToggle } from "./theme-toggle";
import { NotificationCenter } from "./notification-center";
import { Avatar } from "../ui/avatar";
import { Dropdown } from "../ui/dropdown";
import { Search, LogOut, User as UserIcon, Settings } from "lucide-react";
import { Input } from "../ui/input";

export const Topbar: React.FC = () => {
  const { user, logout } = useAuth();

  const userMenuItems = [
    {
      id: "profile",
      label: "My Profile",
      icon: UserIcon,
      onClick: () => {},
    },
    {
      id: "settings",
      label: "Settings",
      icon: Settings,
      onClick: () => {},
    },
    {
      id: "logout",
      label: "Logout",
      icon: LogOut,
      danger: true,
      onClick: () => logout(),
    },
  ];

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/60 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Search Input */}
      <div className="w-72 relative">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
        <input
          type="text"
          placeholder="Search meals, food items, logs..."
          className="w-full h-9 rounded-lg border border-slate-800 bg-slate-900/80 pl-9 pr-3 text-xs text-slate-200 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
        />
      </div>

      {/* Actions & Profile */}
      <div className="flex items-center gap-4">
        <ThemeToggle />
        <NotificationCenter />

        <div className="h-4 w-px bg-slate-800" />

        {/* User Dropdown */}
        <Dropdown
          trigger={
            <button className="flex items-center gap-3 hover:opacity-85 transition-opacity cursor-pointer">
              <Avatar name={user?.full_name || "Admin User"} size="sm" />
              <div className="text-left hidden sm:block">
                <p className="text-xs font-semibold text-white leading-tight">{user?.full_name || "Tejas Admin"}</p>
                <p className="text-[10px] text-slate-400 capitalize">{user?.role || "Administrator"}</p>
              </div>
            </button>
          }
          items={userMenuItems}
        />
      </div>
    </header>
  );
};
