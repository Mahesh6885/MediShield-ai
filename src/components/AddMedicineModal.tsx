import { useState } from "react";
import api from "../services/api";
import toast from "react-hot-toast";

export default function AddMedicineModal({ close, refresh }: any) {
  const [medicine, setMedicine] = useState({
    name: "",
    category: "Analgesic",
    inventory: 50,
    demand: 80,
    lead_time: 3,
    supplier: "Sun Pharma",
    supplier_reliability: 95,
    expiry_date: "",
    safety_stock: 10,
  });

  const saveMedicine = async () => {
    await api.post("/medicines", medicine);
    toast.success("Medicine Added Successfully");
    refresh();
    close();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white rounded-3xl p-6 w-[550px]">
        <h2 className="text-2xl font-bold mb-5 text-cyan-700">
          Add Medicine
        </h2>

        <div className="grid grid-cols-2 gap-3">
          {Object.keys(medicine).map((field) => (
            <input
              key={field}
              placeholder={field.replace("_", " ")}
              value={(medicine as any)[field]}
              onChange={(e) =>
                setMedicine({
                  ...medicine,
                  [field]: e.target.value,
                })
              }
              className="border rounded-xl p-3"
            />
          ))}
        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={close}
            className="px-5 py-2 rounded-xl bg-gray-200"
          >
            Cancel
          </button>

          <button
            onClick={saveMedicine}
            className="px-5 py-2 rounded-xl bg-cyan-700 text-white"
          >
            Save Medicine
          </button>
        </div>
      </div>
    </div>
  );
}