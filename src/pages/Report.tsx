import { useEffect, useState } from "react";
import api from "../services/api";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import {
  FileText,
  Download,
  AlertTriangle,
  CalendarClock,
  CheckCircle,
} from "lucide-react";

interface MedicineReport {
  name: string;
  inventory: number;
  risk: string;
  expiry: string;
}

export default function Reports() {
  const [medicines, setMedicines] = useState<MedicineReport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const res = await api.get("/reports/");
      setMedicines(res.data);
    } catch (error) {
      console.error("Report Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFontSize(20);
    doc.setTextColor(0, 102, 153);
    doc.text("MediShield AI Inventory Report", 14, 20);

    doc.setFontSize(11);
    doc.setTextColor(80);
    doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30);

    autoTable(doc, {
      startY: 40,
      head: [["Medicine", "Inventory", "Risk Level", "Expiry Date"]],
      body: medicines.map((m) => [
        m.name,
        m.inventory,
        m.risk,
        m.expiry,
      ]),
      theme: "grid",
      headStyles: {
        fillColor: [8, 145, 178],
      },
    });

    doc.save("MediShield_AI_Report.pdf");
  };

  const highRisk = medicines.filter((m) => m.risk === "High").length;
  const mediumRisk = medicines.filter((m) => m.risk === "Medium").length;
  const lowRisk = medicines.filter((m) => m.risk === "Low").length;

  return (
    <div className="bg-slate-100 min-h-screen p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-cyan-800">
            Inventory Reports
          </h1>
          <p className="text-gray-600 mt-2">
            AI-generated inventory analytics and downloadable reports.
          </p>
        </div>

        <button
          onClick={downloadPDF}
          className="bg-cyan-700 text-white px-5 py-3 rounded-xl flex items-center gap-2 hover:bg-cyan-800"
        >
          <Download size={18} />
          Download PDF
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid md:grid-cols-4 gap-5 mb-8">
        <SummaryCard
          title="Total Medicines"
          value={medicines.length}
          icon={<FileText className="text-cyan-700" />}
          color="border-cyan-600"
        />

        <SummaryCard
          title="High Risk"
          value={highRisk}
          icon={<AlertTriangle className="text-red-600" />}
          color="border-red-600"
        />

        <SummaryCard
          title="Medium Risk"
          value={mediumRisk}
          icon={<CalendarClock className="text-orange-500" />}
          color="border-orange-500"
        />

        <SummaryCard
          title="Low Risk"
          value={lowRisk}
          icon={<CheckCircle className="text-green-600" />}
          color="border-green-600"
        />
      </div>

      {/* Table */}
      <div className="bg-white rounded-3xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-cyan-800 mb-5">
          Medicine Inventory Report
        </h2>

        {loading ? (
          <p className="text-gray-500">Loading report...</p>
        ) : medicines.length === 0 ? (
          <p className="text-red-500">No report data available.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-cyan-700 text-white">
                <tr>
                  <th className="p-3 text-left">Medicine</th>
                  <th className="p-3 text-center">Inventory</th>
                  <th className="p-3 text-center">Risk Level</th>
                  <th className="p-3 text-center">Expiry Date</th>
                </tr>
              </thead>

              <tbody>
                {medicines.map((m, index) => (
                  <tr
                    key={index}
                    className="border-b hover:bg-cyan-50 transition"
                  >
                    <td className="p-3 font-medium">{m.name}</td>

                    <td className="p-3 text-center">{m.inventory}</td>

                    <td className="p-3 text-center">
                      <span
                        className={`px-3 py-1 rounded-full text-white text-sm ${
                          m.risk === "High"
                            ? "bg-red-600"
                            : m.risk === "Medium"
                            ? "bg-orange-500"
                            : "bg-green-600"
                        }`}
                      >
                        {m.risk}
                      </span>
                    </td>

                    <td className="p-3 text-center">{m.expiry}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* AI Recommendation */}
      <div className="bg-cyan-50 border-l-8 border-cyan-700 rounded-2xl p-6 mt-8">
        <h2 className="text-2xl font-bold text-cyan-800 mb-3">
          AI Report Summary
        </h2>

        <ul className="space-y-2 text-gray-700">
          <li>✔ {highRisk} medicines require urgent monitoring.</li>
          <li>✔ {mediumRisk} medicines should be reviewed this week.</li>
          <li>✔ Inventory data is synchronized with the SQLite database.</li>
          <li>✔ PDF reports can be generated for hospital administration.</li>
        </ul>
      </div>
    </div>
  );
}

function SummaryCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <div className={`bg-white rounded-2xl shadow p-5 border-l-8 ${color}`}>
      <div className="flex justify-between items-center mb-3">{icon}</div>

      <p className="text-gray-500">{title}</p>

      <h2 className="text-3xl font-bold text-slate-800 mt-2">{value}</h2>
    </div>
  );
}