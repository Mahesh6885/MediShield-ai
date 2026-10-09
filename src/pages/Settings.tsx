import { useState } from "react";

export default function Settings() {
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [smsAlerts, setSmsAlerts] = useState(false);

  return (
    <div className="p-8 bg-slate-100 min-h-screen">
      <h1 className="text-4xl font-bold text-cyan-800 mb-6">
        Settings
      </h1>

      <div className="bg-white rounded-2xl shadow p-6 space-y-5">
        <div className="flex justify-between">
          <span>Email Alerts</span>

          <input
            type="checkbox"
            checked={emailAlerts}
            onChange={() => setEmailAlerts(!emailAlerts)}
          />
        </div>

        <div className="flex justify-between">
          <span>SMS Alerts</span>

          <input
            type="checkbox"
            checked={smsAlerts}
            onChange={() => setSmsAlerts(!smsAlerts)}
          />
        </div>

        <div>
          <button className="bg-cyan-700 text-white px-5 py-2 rounded-xl">
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  );
}