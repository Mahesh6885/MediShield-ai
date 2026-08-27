import { useEffect, useState } from "react";
import api from "../services/api";

export default function Suppliers() {

  const [suppliers,setSuppliers]=useState<any[]>([]);
  const [best,setBest]=useState<any>(null);

  useEffect(()=>{

    api.get("/suppliers").then(res=>setSuppliers(res.data));

    api.get("/suppliers/best").then(res=>setBest(res.data));

  },[]);

  return(

    <div className="p-8 bg-slate-100 min-h-screen">

      <h1 className="text-4xl font-bold text-cyan-800">
        Supplier Recommendation
      </h1>

      <p className="text-gray-500 mt-2 mb-8">
        AI ranks suppliers based on reliability, quality, delivery time and procurement cost.
      </p>

      {/* Best Supplier Card */}

      {best && (

        <div className="bg-green-50 border-l-8 border-green-600 rounded-2xl p-6 shadow mb-8">

          <h2 className="text-2xl font-bold text-green-700 mb-3">
            Recommended Supplier
          </h2>

          <h3 className="text-3xl font-bold text-green-800">
            {best.name}
          </h3>

          <p className="mt-2">
            Overall AI Supplier Score :
            <span className="font-bold text-green-700"> {best.score}</span>
          </p>

          <p className="mt-3 text-green-800">
            This supplier has the highest combined reliability, product quality,
            delivery efficiency and procurement value.
          </p>

        </div>

      )}

      {/* Supplier Table */}

      <div className="bg-white rounded-2xl shadow overflow-auto">

        <table className="w-full text-center">

          <thead className="bg-cyan-700 text-white">

            <tr>
              <th className="p-4">Supplier</th>
              <th>Reliability</th>
              <th>Quality</th>
              <th>Delivery (Days)</th>
              <th>Cost</th>
              <th>Score</th>
              <th>Status</th>
            </tr>

          </thead>

          <tbody>

            {suppliers.map((s,index)=>(

              <tr key={s.id} className="border-b hover:bg-cyan-50">

                <td className="p-4 font-semibold">{s.name}</td>

                <td>{s.reliability}%</td>

                <td>{s.quality}%</td>

                <td>{s.delivery}</td>

                <td>₹{s.cost}</td>

                <td className="font-bold text-cyan-700">
                  {s.score}
                </td>

                <td>

                  {index===0 ? (

                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
                      Best Supplier
                    </span>

                  ) : s.score>=85 ? (

                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
                      Recommended
                    </span>

                  ) : (

                    <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm">
                      Standard
                    </span>

                  )}

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {/* Procurement Recommendations */}

      <div className="mt-10 bg-cyan-50 rounded-2xl p-6 border-l-8 border-cyan-700">

        <h2 className="text-2xl font-bold text-cyan-800 mb-5">
          Procurement Recommendations
        </h2>

        {suppliers.slice(0,3).map((s)=>(
          <div key={s.id} className="bg-white rounded-xl p-4 shadow mb-3">

            <h3 className="font-bold text-cyan-700">{s.name}</h3>

            <p>Supplier Score : {s.score}</p>

            <p>Reliability : {s.reliability}%</p>

            <p>Delivery Lead Time : {s.delivery} Days</p>

            <p className="mt-2 text-cyan-800 font-medium">
              AI Recommendation:
              Prioritize procurement from {s.name} for high-risk medicines.
            </p>

          </div>
        ))}

      </div>

    </div>

  );

}