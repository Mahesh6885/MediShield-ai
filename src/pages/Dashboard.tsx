import { useEffect, useState } from "react";
import api from "../services/api";
import KPIcard from "../components/KPIcard";

export default function Dashboard(){

  const [data,setData]=useState<any>({});

  useEffect(()=>{

    api.get("/dashboard").then(res=>setData(res.data));

  },[]);

  return(

    <div className="p-8">

      <h1 className="text-4xl font-bold text-cyan-800 mb-2">
        Healthcare Inventory Intelligence
      </h1>

      <p className="text-gray-500 mb-8">
        AI-powered medicine shortage monitoring dashboard.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

        <KPIcard title="Total Medicines"
                 value={data.totalMedicines}
                 color="#0891B2"/>

        <KPIcard title="Low Stock Alerts"
                 value={data.lowStock}
                 color="#EA580C"/>

        <KPIcard title="Expiry Alerts"
                 value={data.expiryAlerts}
                 color="#DC2626"/>

        <KPIcard title="Suppliers"
                 value={data.suppliers}
                 color="#16A34A"/>

        <KPIcard title="Inventory Health"
                 value={`${data.inventoryHealth}%`}
                 color="#2563EB"/>

      </div>

    </div>

  );
}