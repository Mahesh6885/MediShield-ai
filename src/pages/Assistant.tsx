import { useState } from "react";
import api from "../services/api";

interface Chat {
  sender: "user" | "bot";
  text: string;
}

export default function Assistant() {

  const [message,setMessage]=useState("");
  const [loading,setLoading]=useState(false);

  const [chat,setChat]=useState<Chat[]>([
    {
      sender:"bot",
      text:"Hello! I'm MediShield AI Assistant. Ask me about medicines, suppliers, expiry alerts, inventory health, or shortage risks."
    }
  ]);

  const sendMessage = async()=>{

    if(!message.trim()) return;

    const userMessage = {
      sender:"user",
      text:message
    } as Chat;

    setChat(prev=>[...prev,userMessage]);

    setLoading(true);

    try{

      const res = await api.post("/assistant/chat",{
        message
      });

      setChat(prev=>[
        ...prev,
        {
          sender:"bot",
          text:res.data.assistant
        }
      ]);

    }catch{

      setChat(prev=>[
        ...prev,
        {
          sender:"bot",
          text:"Unable to connect to AI Assistant."
        }
      ]);

    }

    setLoading(false);
    setMessage("");
  };

  return(

    <div className="p-8 bg-slate-100 min-h-screen">

      <h1 className="text-4xl font-bold text-cyan-800 mb-2">
        MediShield AI Assistant
      </h1>

      <p className="text-gray-500 mb-8">
        Intelligent healthcare inventory chatbot powered by FastAPI and SQLite.
      </p>

      <div className="bg-white rounded-2xl shadow h-[550px] flex flex-col">

        <div className="flex-1 overflow-y-auto p-6 space-y-5">

          {chat.map((item,index)=>(

            <div
              key={index}
              className={`flex ${
                item.sender==="user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >

              <div
                className={`max-w-[75%] whitespace-pre-line rounded-2xl p-4 ${
                  item.sender==="user"
                    ? "bg-cyan-700 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
              >

                {item.text}

              </div>

            </div>

          ))}

          {loading && (
            <p className="text-gray-500">AI is typing...</p>
          )}

        </div>

        <div className="border-t p-4 flex gap-3">

          <input
            value={message}
            onChange={(e)=>setMessage(e.target.value)}
            onKeyDown={(e)=>e.key==="Enter" && sendMessage()}
            placeholder="Ask about inventory, suppliers, medicines..."
            className="flex-1 border rounded-xl px-4 py-3"
          />

          <button
            onClick={sendMessage}
            className="bg-cyan-700 text-white px-6 rounded-xl"
          >
            Send
          </button>

        </div>

      </div>

      {/* Quick Questions */}

      <div className="mt-8">

        <h2 className="text-xl font-bold text-cyan-700 mb-4">
          Quick Questions
        </h2>

        <div className="flex flex-wrap gap-3">

          {[
            "Show low stock medicines",
            "Which medicines expire soon?",
            "Best supplier",
            "Inventory health",
            "Show high risk medicines"
          ].map((q)=>(

            <button
              key={q}
              onClick={()=>setMessage(q)}
              className="bg-white border rounded-xl px-4 py-2 hover:bg-cyan-50"
            >
              {q}
            </button>

          ))}

        </div>

      </div>

    </div>

  );

}