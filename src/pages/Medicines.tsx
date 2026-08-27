import { useEffect, useState } from "react";
import api from "../services/api";
import AddMedicineModal from "../components/AddMedicineModal";
import toast from "react-hot-toast";

export default function Medicines() {
  const [medicines, setMedicines] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [open, setOpen] = useState(false);

  const loadMedicines = async () => {
    const res = await api.get("/medicines", {
      params: { search, category },
    });

    setMedicines(res.data);
  };

  useEffect(() => {
    loadMedicines();
  }, [search, category]);

  const deleteMedicine = async (id: number) => {
    await api.delete(`/medicines/${id}`);
    toast.success("Medicine Deleted");
    loadMedicines();
  };

  return (
    <div className="p-8">

      <div className="flex justify-between mb-6">

        <div>
          <h1 className="text-4xl font-bold text-cyan-800">
            Medicine Inventory
          </h1>

          <p className="text-gray-500 mt-2">
            Manage hospital medicine inventory and stock.
          </p>
        </div>

        <button
          onClick={() => setOpen(true)}
          className="bg-cyan-700 text-white px-5 py-3 rounded-xl"
        >
          + Add Medicine
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow p-5 mb-5 flex gap-4">

        <input
          placeholder="Search medicine..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded-xl px-4 py-3 flex-1"
        />

        <select
          className="border rounded-xl px-4"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          <option>Analgesic</option>
          <option>Antibiotic</option>
          <option>Vitamin</option>
          <option>Vaccine</option>
          <option>Antidiabetic</option>
          <option>Cardiology</option>
        </select>
      </div>

      <div className="bg-white rounded-2xl shadow overflow-auto">

        <table className="w-full">

          <thead className="bg-cyan-700 text-white">
            <tr>
              <th className="p-4">Medicine</th>
              <th>Category</th>
              <th>Inventory</th>
              <th>Demand</th>
              <th>Supplier</th>
              <th>Expiry</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {medicines.map((m: any) => {
              const days =
                Math.floor(
                  (new Date(m.expiry_date).getTime() -
                    new Date().getTime()) /
                    (1000 * 3600 * 24)
                );

              return (
                <tr key={m.id} className="border-b hover:bg-cyan-50">

                  <td className="p-4 font-semibold">{m.name}</td>

                  <td>{m.category}</td>

                  <td>{m.inventory}</td>

                  <td>{m.demand}</td>

                  <td>{m.supplier}</td>

                  <td>{m.expiry_date}</td>

                  <td>
                    {m.inventory <= m.safety_stock ? (
                      <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm">
                        Low Stock
                      </span>
                    ) : days <= 30 ? (
                      <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm">
                        Expiring Soon
                      </span>
                    ) : (
                      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
                        Healthy
                      </span>
                    )}
                  </td>

                  <td>
                    <button
                      onClick={() => deleteMedicine(m.id)}
                      className="text-red-600"
                    >
                      Delete
                    </button>
                  </td>

                </tr>
              );
            })}

          </tbody>

        </table>

      </div>

      {open && (
        <AddMedicineModal
          close={() => setOpen(false)}
          refresh={loadMedicines}
        />
      )}

    </div>
  );
}