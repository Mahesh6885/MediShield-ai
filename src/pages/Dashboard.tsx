import { useEffect, useState } from "react";
import api from "../services/api";
import {
  Pill,
  AlertTriangle,
  CalendarClock,
  Truck,
  Activity,
  BrainCircuit,
  Download,
  Plus,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

interface DashboardStats {
  totalMedicines: number;
  lowStock: number;
  expiryAlerts: number;
  suppliers: number;
  inventoryHealth: number;
  highRisk: number;
}

interface Medicine {
  id: number;
  name: string;
  inventory: number;
  demand: number;
  risk_level: string;
  expiry_days: number;
  status: string;
}

const COLORS = ["#16a34a", "#f59e0b", "#dc2626"];

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalMedicines: 0,
    lowStock: 0,
    expiryAlerts: 0,
    suppliers: 0,
    inventoryHealth: 0,
    highRisk: 0,
  });

  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const dashboardRes = await api.get("/dashboard/");
      const inventoryRes = await api.get("/inventory/");

      setStats({
        totalMedicines: dashboardRes.data.total_medicines,
        lowStock: dashboardRes.data.low_stock,
        expiryAlerts: dashboardRes.data.expiring,
        suppliers: dashboardRes.data.suppliers,
        inventoryHealth: dashboardRes.data.inventory_health,
        highRisk: dashboardRes.data.high_risk,
      });

      setMedicines(inventoryRes.data);
    } catch (error) {
      console.error("Dashboard Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const demandChart = medicines.slice(0, 8).map((m) => ({
    name: m.name.length > 10 ? m.name.substring(0, 10) + "..." : m.name,
    demand: m.demand,
    inventory: m.inventory,
  }));

  const riskChart = [
    {
      name: "High",
      value: medicines.filter((m) => m.risk_level === "High").length,
    },
    {
      name: "Medium",
      value: medicines.filter((m) => m.risk_level === "Medium").length,
    },
    {
      name: "Low",
      value: medicines.filter((m) => m.risk_level === "Low").length,
    },
  ];

  const lowStockMedicines = medicines.filter(
    (m) => m.status === "LOW STOCK"
  );

  const expiryMedicines = medicines.filter(
    (m) => m.expiry_days <= 30
  );

  return (
    <div className="bg-slate-100 min-h-screen p-8">
      {/* ---------------- Header ---------------- */}

      <div className="mb-8">
        <h1 className="text-5xl font-bold text-cyan-800">
          Healthcare Inventory Intelligence
        </h1>

        <p className="text-gray-600 mt-2 text-lg">
          AI-powered medicine shortage monitoring dashboard.
        </p>
        {loading && (
          <p className="text-xs text-cyan-700 animate-pulse mt-1 font-medium">
            Syncing real-time inventory telemetry...
          </p>
        )}
      </div>

      {/* ---------------- KPI Cards ---------------- */}

      <div className="grid md:grid-cols-3 xl:grid-cols-6 gap-5 mb-8">
        <Card
          title="Total Medicines"
          value={stats.totalMedicines}
          icon={<Pill size={28} className="text-cyan-700" />}
          color="border-cyan-600"
        />

        <Card
          title="Low Stock Alerts"
          value={stats.lowStock}
          icon={<AlertTriangle size={28} className="text-orange-600" />}
          color="border-orange-500"
        />

        <Card
          title="Expiry Alerts"
          value={stats.expiryAlerts}
          icon={<CalendarClock size={28} className="text-red-600" />}
          color="border-red-600"
        />

        <Card
          title="Suppliers"
          value={stats.suppliers}
          icon={<Truck size={28} className="text-green-600" />}
          color="border-green-600"
        />

        <Card
          title="Inventory Health"
          value={`${stats.inventoryHealth}%`}
          icon={<Activity size={28} className="text-blue-600" />}
          color="border-blue-600"
        />

        <Card
          title="High Risk Medicines"
          value={stats.highRisk}
          icon={<BrainCircuit size={28} className="text-purple-700" />}
          color="border-purple-600"
        />
      </div>

      {/* ---------------- AI Insight ---------------- */}

      <div className="bg-gradient-to-r from-cyan-700 to-blue-700 rounded-3xl text-white p-6 shadow-lg mb-8">
        <h2 className="text-2xl font-bold mb-3 flex items-center gap-2">
          <BrainCircuit />
          AI Insights
        </h2>

        <ul className="space-y-2 text-cyan-50">
          <li>
            • {stats.lowStock} medicines require immediate replenishment.
          </li>

          <li>
            • {stats.expiryAlerts} medicines expire within the next 60 days.
          </li>

          <li>
            • Inventory health is currently {stats.inventoryHealth}%.
          </li>

          <li>
            • {stats.highRisk} medicines have a high predicted shortage risk.
          </li>
        </ul>
      </div>

      {/* ---------------- Charts ---------------- */}

      <div className="grid xl:grid-cols-2 gap-6 mb-8">
        {/* Demand Chart */}

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="font-bold text-xl text-cyan-800 mb-4">
            Medicine Demand vs Inventory
          </h2>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={demandChart}>
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="name" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="demand" fill="#0891B2" radius={[8, 8, 0, 0]} />

              <Bar dataKey="inventory" fill="#16A34A" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="font-bold text-xl text-cyan-800 mb-4">
            AI Risk Distribution
          </h2>

          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={riskChart}
                dataKey="value"
                outerRadius={95}
                label
              >
                {riskChart.map((_, index) => (
                  <Cell key={index} fill={COLORS[index]} />
                ))}
              </Pie>

              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ---------------- Inventory Trend ---------------- */}

      <div className="bg-white rounded-3xl shadow p-6 mb-8">
        <h2 className="font-bold text-xl text-cyan-800 mb-4">
          Inventory Trend
        </h2>

        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={demandChart}>
            <CartesianGrid strokeDasharray="4 4" />

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="inventory"
              stroke="#2563EB"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* ---------------- Alerts ---------------- */}

      <div className="grid xl:grid-cols-2 gap-6 mb-8">
        {/* Low Stock */}

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="font-bold text-xl text-red-700 mb-5">
            Low Stock Medicines
          </h2>

          {lowStockMedicines.length === 0 ? (
            <p className="text-green-600">No low stock medicines.</p>
          ) : (
            lowStockMedicines.slice(0, 6).map((m) => (
              <div
                key={m.id}
                className="flex justify-between items-center border-b py-3"
              >
                <div>
                  <p className="font-semibold">{m.name}</p>

                  <p className="text-sm text-gray-500">
                    Demand : {m.demand}
                  </p>
                </div>

                <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-semibold">
                  {m.inventory} Units
                </span>
              </div>
            ))
          )}
        </div>

        {/* Expiry */}

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="font-bold text-xl text-orange-600 mb-5">
            Medicines Expiring Soon
          </h2>

          {expiryMedicines.length === 0 ? (
            <p className="text-green-600">No medicines expiring soon.</p>
          ) : (
            expiryMedicines.slice(0, 6).map((m) => (
              <div
                key={m.id}
                className="flex justify-between items-center border-b py-3"
              >
                <div>
                  <p className="font-semibold">{m.name}</p>

                  <p className="text-sm text-gray-500">
                    Inventory : {m.inventory}
                  </p>
                </div>

                <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full font-semibold">
                  {m.expiry_days} Days
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* ---------------- AI Recommendation ---------------- */}

      <div className="bg-white rounded-3xl shadow p-6 mb-8">
        <h2 className="font-bold text-xl text-cyan-800 mb-4">
          AI Procurement Recommendation
        </h2>

        <div className="space-y-4 text-gray-700">
          <div className="flex items-start gap-3">
            <AlertTriangle className="text-red-600 mt-1" />

            <p>
              Immediately reorder all medicines marked as{" "}
              <span className="font-semibold text-red-600">
                LOW STOCK
              </span>
              .
            </p>
          </div>

          <div className="flex items-start gap-3">
            <CalendarClock className="text-orange-500 mt-1" />

            <p>
              Prioritize distribution of medicines expiring within{" "}
              <span className="font-semibold">30 days</span>.
            </p>
          </div>

          <div className="flex items-start gap-3">
            <Truck className="text-green-600 mt-1" />

            <p>
              Preferred supplier reliability should remain above{" "}
              <span className="font-semibold">90%</span> for critical medicines.
            </p>
          </div>

          <div className="flex items-start gap-3">
            <BrainCircuit className="text-purple-600 mt-1" />

            <p>
              High-risk medicines should be monitored daily using the AI
              prediction module.
            </p>
          </div>
        </div>
      </div>

      {/* ---------------- Quick Actions ---------------- */}

      <div className="grid md:grid-cols-3 gap-5">
        <ActionButton
          icon={<Plus size={22} />}
          title="Add Medicine"
          description="Register new medicine inventory."
          color="bg-cyan-700"
        />

        <ActionButton
          icon={<BrainCircuit size={22} />}
          title="Run AI Prediction"
          description="Predict shortage probability using XGBoost."
          color="bg-purple-700"
        />

        <ActionButton
          icon={<Download size={22} />}
          title="Download Report"
          description="Generate PDF inventory report."
          color="bg-green-700"
        />
      </div>

      {/* ---------------- Footer ---------------- */}

      <div className="mt-10 text-center text-gray-500">
        MediShield AI • Healthcare Decision Support System • IEEE Conference
        Version 2.0
      </div>
    </div>
  );
}

/* ---------------- KPI Card ---------------- */

function Card({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <div
      className={`bg-white rounded-2xl shadow-lg border-l-8 ${color} p-5`}
    >
      <div className="flex justify-between items-center mb-3">
        {icon}
      </div>

      <p className="text-gray-500 text-sm">{title}</p>

      <h2 className="text-3xl font-bold text-slate-800 mt-2">{value}</h2>
    </div>
  );
}

/* ---------------- Action Button ---------------- */

function ActionButton({
  icon,
  title,
  description,
  color,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}) {
  return (
    <button
      className={`${color} text-white rounded-2xl p-6 shadow-lg hover:scale-[1.02] transition text-left`}
    >
      <div className="mb-4">{icon}</div>

      <h3 className="font-bold text-xl">{title}</h3>

      <p className="text-sm text-white/80 mt-2">{description}</p>
    </button>
  );
}