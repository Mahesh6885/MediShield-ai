import { useEffect, useState } from "react";
import { Bell, Moon, Sun, Search, UserCircle, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Header() {
  const navigate = useNavigate();

  const [darkMode, setDarkMode] = useState(false);
  const [search, setSearch] = useState("");
  const [notificationCount, setNotificationCount] = useState(0);
  const [showProfile, setShowProfile] = useState(false);

  // Fetch notification count
  useEffect(() => {
    api
      .get("/inventory")
      .then((res) => {
        const count = res.data.filter(
          (m: any) => m.status === "LOW STOCK" || m.expiry_days <= 30
        ).length;

        setNotificationCount(count);
      })
      .catch(() => {
        setNotificationCount(0);
      });
  }, []);

  // Dark Mode Toggle
  const toggleDarkMode = () => {
    const html = document.documentElement;

    if (darkMode) {
      html.classList.remove("dark");
    } else {
      html.classList.add("dark");
    }

    setDarkMode(!darkMode);
  };

  // Search Medicines
  const handleSearch = () => {
    if (search.trim() !== "") {
      navigate(`/medicines?search=${encodeURIComponent(search)}`);
    }
  };

  // Logout
  const logout = () => {
    localStorage.removeItem("role");
    navigate("/login");
  };

  return (
    <header className="bg-white dark:bg-slate-900 shadow-sm px-8 py-4 flex justify-between items-center border-b dark:border-slate-700">
      {/* Search Box */}
      <div className="relative w-[380px]">
        <Search
          size={18}
          className="absolute left-4 top-3 text-gray-400 dark:text-gray-300"
        />

        <input
          type="text"
          placeholder="Search medicines..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className="w-full pl-11 pr-4 py-2 rounded-xl border border-gray-300 dark:border-slate-600 bg-gray-50 dark:bg-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-600"
        />
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-6">
        {/* Dark Mode */}
        <button
          onClick={toggleDarkMode}
          className="bg-cyan-50 dark:bg-slate-700 p-2 rounded-full hover:bg-cyan-100 dark:hover:bg-slate-600 transition"
        >
          {darkMode ? (
            <Sun size={20} className="text-yellow-500" />
          ) : (
            <Moon size={20} className="text-cyan-700" />
          )}
        </button>

        {/* Notifications */}
        <div
          className="relative cursor-pointer"
          onClick={() => navigate("/notifications")}
        >
          <Bell
            size={22}
            className="text-cyan-700 dark:text-cyan-300 hover:scale-110 transition"
          />

          {notificationCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
              {notificationCount}
            </span>
          )}
        </div>

        {/* Profile */}
        <div className="relative">
          <button
            onClick={() => setShowProfile(!showProfile)}
            className="flex items-center gap-2"
          >
            <UserCircle
              size={34}
              className="text-cyan-700 dark:text-cyan-300"
            />

            <div className="hidden md:block text-left">
              <p className="font-semibold text-gray-700 dark:text-white">
                Admin
              </p>

              <p className="text-xs text-gray-500 dark:text-gray-300">
                Hospital Administrator
              </p>
            </div>
          </button>

          {/* Profile Dropdown */}
          {showProfile && (
            <div className="absolute right-0 mt-3 w-56 bg-white dark:bg-slate-800 rounded-xl shadow-xl border dark:border-slate-700 z-50">
              <div className="p-4 border-b dark:border-slate-700">
                <h3 className="font-bold text-cyan-700 dark:text-cyan-300">
                  Admin
                </h3>

                <p className="text-sm text-gray-500 dark:text-gray-300">
                  admin@medishield.ai
                </p>
              </div>

              <button
                onClick={() => navigate("/profile")}
                className="w-full text-left px-4 py-3 hover:bg-cyan-50 dark:hover:bg-slate-700 dark:text-white"
              >
                View Profile
              </button>

              <button
                onClick={() => navigate("/settings")}
                className="w-full text-left px-4 py-3 hover:bg-cyan-50 dark:hover:bg-slate-700 dark:text-white"
              >
                Settings
              </button>

              <button
                onClick={logout}
                className="w-full flex items-center gap-2 px-4 py-3 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30"
              >
                <LogOut size={18} />
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}