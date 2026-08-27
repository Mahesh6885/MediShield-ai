import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Pill,
  Activity,
  Boxes,
  Truck,
  Bot,
  FileText
} from "lucide-react";

const menus=[
  {name:"Dashboard",icon:LayoutDashboard,path:"/"},
  {name:"Medicines",icon:Pill,path:"/medicines"},
  {name:"Prediction",icon:Activity,path:"/prediction"},
  {name:"Inventory",icon:Boxes,path:"/inventory"},
  {name:"Suppliers",icon:Truck,path:"/suppliers"},
  {name:"AI Assistant",icon:Bot,path:"/assistant"},
  {name:"Reports",icon:FileText,path:"/reports"},
];

export default function Sidebar(){

  return(

    <aside className="w-64 min-h-screen bg-cyan-900 text-white">

      <div className="p-6 border-b border-cyan-700">

        <h2 className="text-3xl font-bold">MediShield AI</h2>

        <p className="text-cyan-300 text-sm mt-1">
          Decision Support System
        </p>

      </div>

      <nav className="mt-5">

        {menus.map(menu=>{

          const Icon=menu.icon;

          return(

            <NavLink key={menu.path}
                     to={menu.path}
                     className={({isActive})=>
                       `flex items-center gap-3 px-6 py-4 transition ${
                         isActive
                         ? "bg-cyan-700"
                         : "hover:bg-cyan-800"
                       }`
                     }>

              <Icon size={20}/>

              {menu.name}

            </NavLink>

          );

        })}

      </nav>

    </aside>

  );

}