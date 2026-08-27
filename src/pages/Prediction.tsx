import { useEffect, useState } from "react";
import api from "../services/api";

export default function Prediction(){

    const [medicines,setMedicines]=useState<any[]>([]);
    const [selected,setSelected]=useState("");
    const [result,setResult]=useState<any>(null);

    useEffect(()=>{
        api.get("/medicines").then(res=>setMedicines(res.data));
    },[]);

    const predict=async()=>{
        if(!selected) return;

        const res=await api.post(`/prediction/${selected}`);
        setResult(res.data);
    };

    return(

        <div className="p-8">

            <h1 className="text-4xl font-bold text-cyan-800">
                AI Medicine Shortage Prediction
            </h1>

            <p className="text-gray-500 mt-2 mb-8">
                Select a medicine and let AI predict shortage probability.
            </p>

            <div className="bg-white p-6 rounded-2xl shadow">

                <select
                    value={selected}
                    onChange={(e)=>setSelected(e.target.value)}
                    className="border rounded-xl p-4 w-full"
                >

                    <option value="">Choose Medicine</option>

                    {medicines.map((m:any)=>(
                        <option key={m.id} value={m.id}>
                            {m.name}
                        </option>
                    ))}

                </select>

                <button
                    onClick={predict}
                    className="bg-cyan-700 text-white mt-5 px-6 py-3 rounded-xl w-full"
                >
                    Predict Medicine Shortage
                </button>

            </div>

            {result && (

                <div className="bg-white mt-8 rounded-2xl shadow p-6">

                    <h2 className="text-2xl font-bold text-cyan-800 mb-6">
                        Prediction Result
                    </h2>

                    <div className="text-center mb-8">

                        <p className="text-gray-500">Shortage Probability</p>

                        <h1 className="text-6xl font-bold text-cyan-700">
                            {result.probability}%
                        </h1>

                        <span
                            className={`mt-4 inline-block px-5 py-2 rounded-full text-white ${
                                result.risk==="High"
                                    ? "bg-red-600"
                                    : result.risk==="Medium"
                                    ? "bg-orange-500"
                                    : "bg-green-600"
                            }`}
                        >
                            {result.risk} Risk
                        </span>

                    </div>

                    <div className="mb-6">

                        <div className="w-full bg-gray-200 rounded-full h-4">

                            <div
                                className={`h-4 rounded-full ${
                                    result.risk==="High"
                                        ? "bg-red-600"
                                        : result.risk==="Medium"
                                        ? "bg-orange-500"
                                        : "bg-green-600"
                                }`}
                                style={{width:`${result.probability}%`}}
                            />

                        </div>

                    </div>

                    <h3 className="text-xl font-bold text-cyan-700 mb-4">
                        Explainable AI (SHAP)
                    </h3>

                    {result.explanation.map((item:any,index:number)=>(

                        <div key={index} className="mb-4">

                            <div className="flex justify-between">

                                <span>{item.feature}</span>

                                <span>{item.impact}</span>

                            </div>

                            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">

                                <div
                                    className={`h-2 rounded-full ${
                                        item.impact>0
                                            ? "bg-red-500"
                                            : "bg-green-500"
                                    }`}
                                    style={{
                                        width:`${Math.min(Math.abs(item.impact)*20,100)}%`
                                    }}
                                />

                            </div>

                        </div>

                    ))}

                    <div className="mt-8 p-5 rounded-xl bg-cyan-50 border-l-8 border-cyan-700">

                        <h3 className="font-bold text-cyan-800">
                            AI Recommendation
                        </h3>

                        {result.risk==="High" && (
                            <p className="mt-2">
                                Immediately reorder medicine, notify procurement team,
                                and prioritize suppliers with reliability above 90%.
                            </p>
                        )}

                        {result.risk==="Medium" && (
                            <p className="mt-2">
                                Increase monitoring frequency and prepare reorder within
                                the next procurement cycle.
                            </p>
                        )}

                        {result.risk==="Low" && (
                            <p className="mt-2">
                                Current inventory is sufficient. Continue routine monitoring.
                            </p>
                        )}

                    </div>

                </div>

            )}

        </div>

    );

}