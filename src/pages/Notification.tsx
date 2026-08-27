import { useEffect, useState } from "react";
import api from "../services/api";
import {
  Bell,
  AlertTriangle,
  Package,
  CalendarClock,
  CheckCircle,
} from "lucide-react";

interface Alert {
  title: string;
  message: string;
  type: "red" | "orange" | "green";
}

export default function Notification() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const res = await api.get("/inventory");

      const data = res.data;
      const notificationList: Alert[] = [];

      data.forEach((medicine: any) => {
        // Low Stock Alert
        if (medicine.status === "LOW STOCK") {
          notificationList.push({
            title: "Low Stock Alert",
            message: `${medicine.name} has only ${medicine.inventory} units remaining. Immediate reorder recommended.`,
            type: "red",
          });
        }

        // Reorder Alert
        if (medicine.status === "REORDER") {
          notificationList.push({
            title: "Reorder Required",
            message: `${medicine.name} has reached its reorder point (${medicine.reorder_point} units). Suggested EOQ: ${medicine.eoq} units.`,
            type: "orange",
          });
        }

        // Expiry Alert
        if (medicine.expiry_days <= 30) {
          notificationList.push({
            title: "Expiry Warning",
            message: `${medicine.name} expires in ${medicine.expiry_days} days. Prioritize usage or replacement.`,
            type: "orange",
          });
        }
      });

      setAlerts(notificationList);
    } catch (error) {
      console.error("Notification Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 bg-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <Bell className="text-cyan-700" size={34} />
        <div>
          <h1 className="text-4xl font-bold text-cyan-800">
            Notification Center
          </h1>
          <p className="text-gray-500">
            Real-time inventory, expiry and procurement alerts.
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid md:grid-cols-3 gap-5 mb-8">
        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-red-500">
          <p className="text-gray-500">Critical Alerts</p>
          <h2 className="text-3xl font-bold text-red-600">
            {alerts.filter((a) => a.type === "red").length}
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-orange-500">
          <p className="text-gray-500">Warnings</p>
          <h2 className="text-3xl font-bold text-orange-500">
            {alerts.filter((a) => a.type === "orange").length}
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-green-600">
          <p className="text-gray-500">System Status</p>
          <h2 className="text-2xl font-bold text-green-600">Operational</h2>
        </div>
      </div>

      {/* Notification List */}
      {loading ? (
        <div className="bg-white rounded-xl p-6 shadow text-center text-gray-500">
          Loading notifications...
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white rounded-xl p-8 shadow text-center">
          <CheckCircle className="mx-auto text-green-600 mb-3" size={40} />
          <h3 className="text-xl font-bold text-green-700">
            No Active Notifications
          </h3>
          <p className="text-gray-500 mt-2">
            Inventory levels and medicine expiry dates are currently healthy.
          </p>
        </div>
      ) : (
        alerts.map((alert, index) => (
          <div
            key={index}
            className={`rounded-2xl p-5 mb-4 shadow border-l-8 ${
              alert.type === "red"
                ? "bg-red-50 border-red-600"
                : alert.type === "orange"
                ? "bg-orange-50 border-orange-500"
                : "bg-green-50 border-green-600"
            }`}
          >
            <div className="flex gap-4 items-start">
              {alert.type === "red" ? (
                <AlertTriangle className="text-red-600 mt-1" size={28} />
              ) : alert.type === "orange" ? (
                <CalendarClock className="text-orange-600 mt-1" size={28} />
              ) : (
                <Package className="text-green-600 mt-1" size={28} />
              )}

              <div>
                <h3 className="font-bold text-lg">{alert.title}</h3>
                <p className="text-gray-700 mt-1">{alert.message}</p>
              </div>
            </div>
          </div>
        ))
      )}

      {/* AI Suggestions */}
      <div className="mt-10 bg-cyan-50 rounded-2xl p-6 border-l-8 border-cyan-700">
        <h2 className="text-2xl font-bold text-cyan-800 mb-4">
          AI Suggestions
        </h2>

        <ul className="space-y-3 text-cyan-900">
          <li>✔ Reorder medicines marked as "Low Stock" immediately.</li>
          <li>✔ Review medicines expiring within 30 days.</li>
          <li>✔ Prioritize procurement from suppliers with reliability above 90%.</li>
          <li>✔ Run shortage prediction daily for proactive inventory planning.</li>
        </ul>
      </div>
    </div>
  );
}