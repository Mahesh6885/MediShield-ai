import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import InventoryHealthChart from "../components/InventoryHealthChart";

interface Medicine {
  id: number;
  name: string;
  inventory: number;
  demand: number;
  safety_stock: number;
  reorder_point: number;
  eoq: number;
  expiry_days: number;
  status: string;
}

export default function Inventory() {
  const [inventory, setInventory] = useState<Medicine[]>([]);
  const [filter, setFilter] = useState("ALL");

  useEffect(() => {
    loadInventory();
  }, []);

  const loadInventory = async () => {
    try {
      const res = await api.get("/inventory");
      setInventory(res.data);
    } catch (err) {
      console.error("Inventory API Error:", err);
    }
  };

  const filteredInventory = useMemo(() => {
    if (filter === "ALL") return inventory;
    return inventory.filter((m) => m.status === filter);
  }, [inventory, filter]);

  const totalMedicines = inventory.length;
  const lowStock = inventory.filter((m) => m.status === "LOW STOCK").length;
  const reorder = inventory.filter((m) => m.status === "REORDER").length;
  const healthy = inventory.filter((m) => m.status === "HEALTHY").length;

  const inventoryHealth =
    totalMedicines === 0
      ? 0
      : Math.round((healthy / totalMedicines) * 100);

  return (
    <div className="p-8 bg-slate-100 min-h-screen">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-cyan-800">
          Inventory Optimization
        </h1>

        <p className="text-gray-500 mt-2">
          AI-powered inventory monitoring with EOQ, Reorder Point and Expiry
          Tracking.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-cyan-600">
          <p className="text-gray-500">Total Medicines</p>
          <h2 className="text-3xl font-bold text-cyan-700">
            {totalMedicines}
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-red-500">
          <p className="text-gray-500">Low Stock</p>
          <h2 className="text-3xl font-bold text-red-600">{lowStock}</h2>
        </div>

        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-orange-500">
          <p className="text-gray-500">Need Reorder</p>
          <h2 className="text-3xl font-bold text-orange-500">{reorder}</h2>
        </div>

        <div className="bg-white rounded-2xl shadow p-5 border-l-8 border-green-600">
          <p className="text-gray-500">Inventory Health</p>
          <h2 className="text-3xl font-bold text-green-600">
            {inventoryHealth}%
          </h2>
        </div>
      </div>

      {/* Pie Chart */}
      <div className="mb-8">
        <InventoryHealthChart inventory={inventory} />
      </div>

      {/* Filter Buttons */}
      <div className="flex flex-wrap gap-3 mb-6">
        {["ALL", "HEALTHY", "REORDER", "LOW STOCK"].map((item) => (
          <button
            key={item}
            onClick={() => setFilter(item)}
            className={`px-4 py-2 rounded-xl font-medium transition ${
              filter === item
                ? "bg-cyan-700 text-white"
                : "bg-white border border-gray-300 hover:bg-cyan-50"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      {/* Inventory Table */}
      <div className="bg-white rounded-2xl shadow overflow-x-auto">
        <table className="w-full text-center">
          <thead className="bg-cyan-700 text-white">
            <tr>
              <th className="p-4">Medicine</th>
              <th>Inventory</th>
              <th>Demand</th>
              <th>Safety Stock</th>
              <th>ROP</th>
              <th>EOQ</th>
              <th>Expiry</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {filteredInventory.map((m) => (
              <tr
                key={m.id}
                className="border-b hover:bg-cyan-50 transition"
              >
                <td className="p-4 font-semibold text-left pl-6">{m.name}</td>

                <td>{m.inventory}</td>

                <td>{m.demand}</td>

                <td>{m.safety_stock}</td>

                <td className="font-semibold text-cyan-700">
                  {m.reorder_point}
                </td>

                <td className="font-semibold text-green-700">{m.eoq}</td>

                <td>
                  {m.expiry_days <= 30 ? (
                    <span className="text-red-600 font-semibold">
                      {m.expiry_days} Days
                    </span>
                  ) : m.expiry_days <= 60 ? (
                    <span className="text-orange-500 font-semibold">
                      {m.expiry_days} Days
                    </span>
                  ) : (
                    <span className="text-green-600">
                      {m.expiry_days} Days
                    </span>
                  )}
                </td>

                <td>
                  {m.status === "LOW STOCK" && (
                    <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-semibold">
                      Low Stock
                    </span>
                  )}

                  {m.status === "REORDER" && (
                    <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm font-semibold">
                      Reorder
                    </span>
                  )}

                  {m.status === "HEALTHY" && (
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
                      Healthy
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Expiry Alerts */}
      <div className="mt-10">
        <h2 className="text-2xl font-bold text-orange-600 mb-5">
          Medicines Expiring Within 60 Days
        </h2>

        {inventory.filter((m) => m.expiry_days <= 60).length === 0 ? (
          <div className="bg-white rounded-xl p-5 shadow text-gray-500">
            No medicines are expiring within the next 60 days.
          </div>
        ) : (
          inventory
            .filter((m) => m.expiry_days <= 60)
            .slice(0, 8)
            .map((m) => (
              <div
                key={m.id}
                className="bg-orange-50 border-l-8 border-orange-500 rounded-xl p-4 mb-3 shadow"
              >
                <h3 className="font-bold text-orange-700 text-lg">{m.name}</h3>

                <p className="mt-1">
                  Expires in{" "}
                  <span className="font-bold">{m.expiry_days} Days</span>
                </p>

                <p>Current Inventory: {m.inventory}</p>

                <p>Reorder Point: {m.reorder_point}</p>
              </div>
            ))
        )}
      </div>

      {/* AI Reorder Recommendation */}
      <div className="mt-10 bg-cyan-50 rounded-2xl p-6 border-l-8 border-cyan-700">
        <h2 className="text-2xl font-bold text-cyan-800 mb-5">
          AI Reorder Recommendations
        </h2>

        {inventory
          .filter((m) => m.status !== "HEALTHY")
          .slice(0, 5)
          .map((m) => (
            <div
              key={m.id}
              className="bg-white rounded-xl p-5 mb-4 shadow"
            >
              <h3 className="text-lg font-bold text-cyan-700">{m.name}</h3>

              <div className="grid grid-cols-2 gap-3 mt-3 text-sm">
                <p>
                  <strong>Current Stock:</strong> {m.inventory}
                </p>

                <p>
                  <strong>Demand:</strong> {m.demand}
                </p>

                <p>
                  <strong>Reorder Point:</strong> {m.reorder_point}
                </p>

                <p>
                  <strong>Recommended EOQ:</strong> {m.eoq}
                </p>
              </div>

              <div className="mt-4 bg-cyan-100 p-3 rounded-lg">
                <p className="text-cyan-900 font-semibold">
                  Recommendation:
                </p>

                <p className="text-cyan-800">
                  Place an order for approximately{" "}
                  <strong>{m.eoq} units</strong> to maintain optimal inventory
                  levels.
                </p>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}