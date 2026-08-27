import Sidebar from "./Sidebar";
import Header from "./Header";

export default function Layout({children}:any){

  return(

    <div className="flex">

      <Sidebar/>

      <div className="flex-1 bg-slate-100 min-h-screen">

        <Header/>

        {children}

      </div>

    </div>

  );

}