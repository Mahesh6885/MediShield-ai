import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function InventoryHealthChart({inventory}:any){

  const data=[
    {
      name:"Healthy",
      value:inventory.filter((m:any)=>m.status==="HEALTHY").length
    },
    {
      name:"Reorder",
      value:inventory.filter((m:any)=>m.status==="REORDER").length
    },
    {
      name:"Low Stock",
      value:inventory.filter((m:any)=>m.status==="LOW STOCK").length
    }
  ];

  return(

    <div className="bg-white rounded-2xl p-5 shadow h-[350px]">

      <h2 className="text-xl font-bold text-cyan-800 mb-4">
        Inventory Health Distribution
      </h2>

      <ResponsiveContainer width="100%" height="90%">

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            outerRadius={110}
            label
          >

            <Cell fill="#16A34A"/>
            <Cell fill="#F59E0B"/>
            <Cell fill="#DC2626"/>

          </Pie>

          <Tooltip/>

        </PieChart>

      </ResponsiveContainer>

    </div>

  );

}