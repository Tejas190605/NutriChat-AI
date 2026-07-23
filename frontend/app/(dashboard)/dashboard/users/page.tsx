"use client";

import React, { useEffect, useState } from "react";
import { usersService } from "@/services/users.service";
import { User } from "@/types/user";
import { DataTable, Column } from "@/components/data/DataTable";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Drawer } from "@/components/ui/drawer";
import { Users, Eye, Target, Calendar } from "lucide-react";

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        const res = await usersService.getUsers();
        setUsers(res.items);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

  const columns: Column<User>[] = [
    {
      header: "User Profile",
      cell: (item) => (
        <div className="flex items-center gap-3">
          <Avatar name={item.full_name} size="sm" />
          <div>
            <p className="font-semibold text-white">{item.full_name}</p>
            <p className="text-[11px] text-slate-400">{item.email}</p>
          </div>
        </div>
      ),
      sortable: true,
    },
    { header: "Phone Number", accessorKey: "phone_number" },
    {
      header: "Role",
      cell: (item) => (
        <Badge variant={item.role === "admin" ? "success" : "info"} className="capitalize">
          {item.role}
        </Badge>
      ),
      sortable: true,
    },
    {
      header: "Account Status",
      cell: (item) => (
        <Badge variant={item.is_active ? "success" : "error"}>
          {item.is_active ? "ACTIVE" : "INACTIVE"}
        </Badge>
      ),
    },
    {
      header: "Joined Date",
      cell: (item) => new Date(item.created_at).toLocaleDateString(),
      sortable: true,
    },
    {
      header: "Actions",
      cell: (item) => (
        <Button variant="ghost" size="sm" onClick={() => setSelectedUser(item)}>
          <Eye className="h-4 w-4 mr-1" /> Profile
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Users className="h-6 w-6 text-emerald-400" /> Users Management & Profiles
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Search, inspect user profiles, calorie goals, body weight history, and logged conversations.
          </p>
        </div>
      </div>

      <DataTable
        title="Registered Users Directory"
        columns={columns}
        data={users}
        keyExtractor={(u) => u.id}
        searchPlaceholder="Search users by name, email or phone..."
      />

      {/* User Profile Detail Drawer */}
      <Drawer
        isOpen={!!selectedUser}
        onClose={() => setSelectedUser(null)}
        title={selectedUser?.full_name || "User Details"}
      >
        {selectedUser && (
          <div className="space-y-6">
            <div className="flex items-center gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800">
              <Avatar name={selectedUser.full_name} size="lg" />
              <div>
                <h4 className="text-base font-bold text-white">{selectedUser.full_name}</h4>
                <p className="text-xs text-slate-400">{selectedUser.email}</p>
                <Badge variant="success" className="mt-2 capitalize">
                  {selectedUser.role} Account
                </Badge>
              </div>
            </div>

            <div className="space-y-3">
              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Target className="h-4 w-4 text-emerald-400" /> Nutrition Targets
              </h5>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500">Daily Calorie Target:</span>
                  <p className="text-base font-bold text-white mt-0.5">2,200 kcal</p>
                </div>
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500">Protein Target:</span>
                  <p className="text-base font-bold text-emerald-400 mt-0.5">160 g</p>
                </div>
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500">Carbs Target:</span>
                  <p className="text-base font-bold text-cyan-400 mt-0.5">220 g</p>
                </div>
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-slate-500">Fat Target:</span>
                  <p className="text-base font-bold text-purple-400 mt-0.5">65 g</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Calendar className="h-4 w-4 text-cyan-400" /> Account Meta
              </h5>
              <div className="text-xs space-y-1.5 text-slate-300">
                <p><strong>User ID:</strong> <span className="font-mono text-slate-400">{selectedUser.id}</span></p>
                <p><strong>Phone:</strong> {selectedUser.phone_number || "N/A"}</p>
                <p><strong>Joined:</strong> {new Date(selectedUser.created_at).toLocaleString()}</p>
              </div>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}
