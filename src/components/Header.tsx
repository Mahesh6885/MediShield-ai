import { useEffect, useState } from "react";
import {
  Search,
  Bell,
  Moon,
  Sun,
  CircleUser,
  Settings,
  LogOut,
  User,
  CheckCircle,
  Trash2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

interface Medicine {
  id: number;
  name: string;
  inventory: number;
  risk_level?: string;
}

interface Notification {
  id: number;
  title: string;
  message: string;
  priority: string;
  is_read: boolean;
  created_at: string;
}

interface Profile {
  full_name: string;
  role: string;
  hospital: string;
}

export default function Header() {
  const navigate = useNavigate();

  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  const [search, setSearch] = useState("");
  const [results, setResults] = useState<Medicine[]>([]);
  const [showSearch, setShowSearch] = useState(false);

  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [showNotification, setShowNotification] = useState(false);

  const [profile, setProfile] = useState<Profile>({
    full_name: "Admin",
    role: "Hospital Administrator",
    hospital: "MediShield General Hospital",
  });

  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    loadProfile();
    loadNotifications();

    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    }
  }, []);

  async function loadProfile() {
    try {
      const res = await api.get("/profile/");
      setProfile(res.data);
    } catch {}
  }

  async function loadNotifications() {
    try {
      const res = await api.get("/notifications/");
      setNotifications(res.data);
    } catch {}
  }

  async function searchMedicine(value: string) {
    setSearch(value);

    if (value.trim().length === 0) {
      setShowSearch(false);
      return;
    }

    try {
      const res = await api.get(`/search/?query=${value}`);
      setResults(res.data);
      setShowSearch(true);
    } catch {}
  }

  async function markRead(id: number) {
    await api.put(`/notifications/${id}/read`);
    loadNotifications();
  }

  async function deleteNotification(id: number) {
    await api.delete(`/notifications/${id}`);
    loadNotifications();
  }

  async function markAllRead() {
    await api.put("/notifications/read-all");
    loadNotifications();
  }

  function toggleTheme() {
    if (theme === "light") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
      setTheme("dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
      setTheme("light");
    }
  }

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-slate-900 shadow-md border-b border-slate-200 dark:border-slate-700">

      <div className="flex justify-between items-center px-8 py-4">

        {/* Left */}
        <div>
          <h2 className="text-3xl font-bold text-cyan-700 dark:text-cyan-400">
            Healthcare Inventory Intelligence
          </h2>

          <p className="text-gray-500 dark:text-gray-300 text-sm">
            Explainable AI for Medicine Shortage Prediction
          </p>
        </div>

        {/* Right */}
        <div className="flex items-center gap-5">

          {/* SEARCH */}

          <div className="relative">

            <div className="flex items-center bg-slate-100 dark:bg-slate-800 rounded-xl px-4 py-2 w-72">

              <Search className="text-gray-500"/>

              <input
                type="text"
                value={search}
                placeholder="Search medicines..."
                onChange={(e)=>searchMedicine(e.target.value)}
                className="bg-transparent ml-3 outline-none w-full dark:text-white"
              />

            </div>

            {showSearch && (
              <div className="absolute mt-2 w-full bg-white dark:bg-slate-800 rounded-xl shadow-xl border dark:border-slate-700 max-h-72 overflow-auto">

                {results.length === 0 ? (
                  <div className="p-4 text-gray-500">
                    No medicines found.
                  </div>
                ) : (
                  results.map((m)=>(
                    <button
                      key={m.id}
                      onClick={()=>{
                        navigate("/medicines");
                        setShowSearch(false);
                        setSearch("");
                      }}
                      className="w-full text-left px-4 py-3 hover:bg-cyan-50 dark:hover:bg-slate-700 border-b dark:border-slate-700"
                    >
                      <div className="font-semibold dark:text-white">
                        {m.name}
                      </div>

                      <div className="text-xs text-gray-500">
                        Stock : {m.inventory}
                      </div>
                    </button>
                  ))
                )}

              </div>
            )}

          </div>

          {/* DARK MODE */}

          <button
            onClick={toggleTheme}
            className="rounded-full bg-cyan-50 dark:bg-slate-800 p-3 hover:scale-105 transition"
          >
            {theme === "dark" ? (
              <Sun className="text-yellow-400"/>
            ) : (
              <Moon className="text-cyan-700"/>
            )}
          </button>

          {/* NOTIFICATION */}

          <div className="relative">

            <button
              onClick={()=>setShowNotification(!showNotification)}
              className="relative p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700"
            >
              <Bell className="text-cyan-700 dark:text-cyan-300"/>

              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-600 text-white rounded-full text-xs h-5 w-5 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            {showNotification && (
              <div className="absolute right-0 mt-3 w-[380px] bg-white dark:bg-slate-800 rounded-2xl shadow-xl border dark:border-slate-700">

                <div className="flex justify-between items-center p-4 border-b dark:border-slate-700">

                  <h3 className="font-bold dark:text-white">
                    Notifications
                  </h3>

                  <button
                    onClick={markAllRead}
                    className="text-sm text-cyan-700"
                  >
                    Mark all read
                  </button>

                </div>

                <div className="max-h-80 overflow-auto">

                  {notifications.length === 0 ? (
                    <div className="p-5 text-center text-gray-500">
                      No Notifications
                    </div>
                  ) : (
                    notifications.map((n)=>(
                      <div
                        key={n.id}
                        className={`border-b dark:border-slate-700 p-4 ${
                          !n.is_read
                            ? "bg-cyan-50 dark:bg-slate-700"
                            : ""
                        }`}
                      >
                        <div className="flex justify-between gap-2">

                          <div>

                            <h4 className="font-semibold dark:text-white">
                              {n.title}
                            </h4>

                            <p className="text-sm text-gray-500 dark:text-gray-300">
                              {n.message}
                            </p>

                            <span
                              className={`inline-block mt-2 text-xs font-semibold px-2 py-1 rounded-full ${
                                n.priority === "Critical"
                                  ? "bg-red-100 text-red-700"
                                  : n.priority === "Warning"
                                  ? "bg-orange-100 text-orange-700"
                                  : "bg-green-100 text-green-700"
                              }`}
                            >
                              {n.priority}
                            </span>

                          </div>

                          <div className="flex flex-col gap-3">

                            {!n.is_read && (
                              <button onClick={()=>markRead(n.id)}>
                                <CheckCircle className="text-green-600" size={18}/>
                              </button>
                            )}

                            <button onClick={()=>deleteNotification(n.id)}>
                              <Trash2 className="text-red-600" size={18}/>
                            </button>

                          </div>

                        </div>
                      </div>
                    ))
                  )}

                </div>

                <button
                  onClick={()=>{
                    navigate("/notifications");
                    setShowNotification(false);
                  }}
                  className="w-full py-3 font-semibold text-cyan-700 hover:bg-cyan-50 dark:hover:bg-slate-700 rounded-b-2xl"
                >
                  View All Notifications
                </button>

              </div>
            )}

          </div>

          {/* PROFILE */}

          <div className="relative">

            <button
              onClick={()=>setShowProfile(!showProfile)}
              className="flex items-center gap-3"
            >
              <CircleUser className="text-cyan-700 dark:text-cyan-300" size={36}/>

              <div className="hidden md:block text-left">
                <h4 className="font-semibold dark:text-white">
                  {profile.full_name}
                </h4>

                <p className="text-xs text-gray-500">
                  {profile.role}
                </p>
              </div>

            </button>

            {showProfile && (
              <div className="absolute right-0 mt-3 bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-64 border dark:border-slate-700">

                <div className="p-5 border-b dark:border-slate-700 text-center">

                  <CircleUser
                    className="mx-auto text-cyan-700"
                    size={64}
                  />

                  <h3 className="mt-2 font-bold dark:text-white">
                    {profile.full_name}
                  </h3>

                  <p className="text-sm text-gray-500">
                    {profile.role}
                  </p>

                  <p className="text-xs text-cyan-700 mt-1">
                    {profile.hospital}
                  </p>

                </div>

                <button
                  onClick={()=>{
                    navigate("/profile");
                    setShowProfile(false);
                  }}
                  className="flex items-center gap-3 w-full px-5 py-3 hover:bg-slate-100 dark:hover:bg-slate-700"
                >
                  <User size={18}/>
                  My Profile
                </button>

                <button
                  onClick={()=>{
                    navigate("/settings");
                    setShowProfile(false);
                  }}
                  className="flex items-center gap-3 w-full px-5 py-3 hover:bg-slate-100 dark:hover:bg-slate-700"
                >
                  <Settings size={18}/>
                  Settings
                </button>

                <button
                  onClick={()=>navigate("/login")}
                  className="flex items-center gap-3 w-full px-5 py-3 text-red-600 hover:bg-red-50 rounded-b-2xl"
                >
                  <LogOut size={18}/>
                  Logout
                </button>

              </div>
            )}

          </div>

        </div>

      </div>

    </header>
  );
}