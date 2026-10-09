import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import {
  Bell,
  Search,
  CheckCircle2,
  Trash2,
  AlertTriangle,
  ShieldAlert,
  Info,
} from "lucide-react";

export default function Notification() {
  const [notifications, setNotifications] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");

  useEffect(() => {
    loadNotifications();
  }, []);

  async function loadNotifications() {
    try {
      const res = await api.get("/notifications/");
      setNotifications(res.data);
    } catch {}
  }

  async function markRead(id:number) {
    await api.put(`/notifications/${id}/read`);
    loadNotifications();
  }

  async function deleteNotification(id:number) {
    await api.delete(`/notifications/${id}`);
    loadNotifications();
  }

  async function markAllRead() {
    await api.put("/notifications/read-all");
    loadNotifications();
  }

  const filtered = useMemo(() => {
    return notifications.filter((note:any) => {
      const text =
        note.title.toLowerCase().includes(search.toLowerCase()) ||
        note.message.toLowerCase().includes(search.toLowerCase());

      const priority =
        filter === "All" || note.priority === filter;

      return text && priority;
    });
  }, [notifications, search, filter]);

  return (
    <div className="p-8 bg-slate-100 dark:bg-slate-900 min-h-screen">

      <div className="flex justify-between items-center mb-8">

        <div>
          <h1 className="text-4xl font-bold text-cyan-700 dark:text-cyan-400 flex items-center gap-3">
            <Bell/>
            Notification Center
          </h1>

          <p className="text-gray-500 mt-2">
            Medicine alerts, AI predictions, supplier updates and expiry reminders.
          </p>
        </div>

        <button
          onClick={markAllRead}
          className="bg-cyan-700 hover:bg-cyan-800 text-white rounded-xl px-5 py-3"
        >
          Mark All Read
        </button>

      </div>

      {/* SEARCH */}

      <div className="bg-white dark:bg-slate-800 rounded-2xl p-5 shadow flex flex-wrap gap-4 items-center mb-8">

        <div className="flex items-center bg-slate-100 dark:bg-slate-700 rounded-xl px-4 py-3 flex-1">
          <Search/>
          <input
            value={search}
            onChange={(e)=>setSearch(e.target.value)}
            placeholder="Search notifications..."
            className="bg-transparent ml-3 outline-none w-full dark:text-white"
          />
        </div>

        {["All","Critical","Warning","Info"].map((type)=>(
          <button
            key={type}
            onClick={()=>setFilter(type)}
            className={`px-4 py-2 rounded-full ${
              filter===type
                ? "bg-cyan-700 text-white"
                : "bg-slate-200 dark:bg-slate-700 dark:text-white"
            }`}
          >
            {type}
          </button>
        ))}

      </div>

      {/* LIST */}

      <div className="space-y-5">

        {filtered.map((note:any)=>(
          <div
            key={note.id}
            className={`bg-white dark:bg-slate-800 rounded-2xl shadow p-6 border-l-4 ${
              note.priority==="Critical"
                ? "border-red-600"
                : note.priority==="Warning"
                ? "border-orange-500"
                : "border-cyan-600"
            }`}
          >

            <div className="flex justify-between gap-4">

              <div className="flex gap-4">

                {note.priority==="Critical" && (
                  <ShieldAlert className="text-red-600 mt-1"/>
                )}

                {note.priority==="Warning" && (
                  <AlertTriangle className="text-orange-500 mt-1"/>
                )}

                {note.priority==="Info" && (
                  <Info className="text-cyan-700 mt-1"/>
                )}

                <div>

                  <h3 className="font-bold text-lg dark:text-white">
                    {note.title}
                  </h3>

                  <p className="text-gray-500 dark:text-gray-300">
                    {note.message}
                  </p>

                  <div className="flex gap-3 mt-3 items-center">

                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        note.priority==="Critical"
                          ? "bg-red-100 text-red-700"
                          : note.priority==="Warning"
                          ? "bg-orange-100 text-orange-700"
                          : "bg-cyan-100 text-cyan-700"
                      }`}
                    >
                      {note.priority}
                    </span>

                    {!note.is_read && (
                      <span className="text-xs text-red-600 font-semibold">
                        Unread
                      </span>
                    )}

                  </div>

                  <p className="text-xs text-gray-400 mt-3">
                    {new Date(note.created_at).toLocaleString()}
                  </p>

                </div>

              </div>

              <div className="flex flex-col gap-3">

                {!note.is_read && (
                  <button onClick={()=>markRead(note.id)}>
                    <CheckCircle2 className="text-green-600"/>
                  </button>
                )}

                <button onClick={()=>deleteNotification(note.id)}>
                  <Trash2 className="text-red-600"/>
                </button>

              </div>

            </div>

          </div>
        ))}

        {filtered.length===0 && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-12 text-center shadow">
            <Bell className="mx-auto text-gray-400" size={50}/>
            <p className="text-gray-500 mt-4">
              No notifications found.
            </p>
          </div>
        )}

      </div>

    </div>
  );
}