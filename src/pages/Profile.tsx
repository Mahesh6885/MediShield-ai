import { useEffect, useState } from "react";
import api from "../services/api";
import {
  User,
  Mail,
  Phone,
  Building2,
  Stethoscope,
  Camera,
  Save,
  ShieldCheck,
  KeyRound,
} from "lucide-react";

export default function Profile() {
  const [profile, setProfile] = useState({
    full_name: "",
    email: "",
    phone: "",
    department: "",
    hospital: "",
    role: "Hospital Administrator",
  });

  const [password, setPassword] = useState({
    current_password: "",
    new_password: "",
  });

  const [message, setMessage] = useState("");

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const res = await api.get("/profile/");
      setProfile(res.data);
    } catch (err) {
      console.log(err);
    }
  }

  async function saveProfile() {
    try {
      await api.put("/profile/", profile);
      setMessage("Profile updated successfully.");
    } catch {
      setMessage("Failed to update profile.");
    }
  }

  async function changePassword() {
    try {
      await api.put("/profile/password", password);

      setPassword({
        current_password: "",
        new_password: "",
      });

      alert("Password changed successfully.");
    } catch {
      alert("Wrong current password.");
    }
  }

  return (
    <div className="p-8 bg-slate-100 dark:bg-slate-900 min-h-screen">

      <h1 className="text-4xl font-bold text-cyan-700 dark:text-cyan-400 mb-8">
        My Profile
      </h1>

      <div className="grid lg:grid-cols-3 gap-8">

        {/* LEFT CARD */}

        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl p-6 text-center">

          <div className="relative inline-block">

            <img
              src="https://i.pravatar.cc/200?img=12"
              className="w-40 h-40 rounded-full object-cover mx-auto border-4 border-cyan-600"
            />

            <button className="absolute bottom-1 right-2 bg-cyan-600 text-white p-2 rounded-full">
              <Camera size={18}/>
            </button>

          </div>

          <h2 className="text-2xl font-bold mt-5 dark:text-white">
            {profile.full_name}
          </h2>

          <p className="text-gray-500 mt-1">{profile.role}</p>

          <p className="text-cyan-700 font-semibold mt-2">
            {profile.hospital}
          </p>

          <div className="mt-8 space-y-3 text-left">

            <div className="flex gap-3 items-center">
              <ShieldCheck className="text-green-600"/>
              Verified Hospital Admin
            </div>

            <div className="flex gap-3 items-center">
              <Building2 className="text-cyan-700"/>
              Inventory Department
            </div>

            <div className="flex gap-3 items-center">
              <Stethoscope className="text-cyan-700"/>
              AI Decision Support
            </div>

          </div>

        </div>

        {/* RIGHT */}

        <div className="lg:col-span-2 space-y-6">

          <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl p-6">

            <h2 className="font-bold text-xl mb-6 dark:text-white">
              Personal Information
            </h2>

            <div className="grid md:grid-cols-2 gap-5">

              <div>
                <label>Full Name</label>
                <div className="flex items-center gap-3 mt-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-3">
                  <User/>
                  <input
                    value={profile.full_name}
                    onChange={(e)=>setProfile({...profile,full_name:e.target.value})}
                    className="bg-transparent w-full py-3 outline-none dark:text-white"
                  />
                </div>
              </div>

              <div>
                <label>Email</label>
                <div className="flex items-center gap-3 mt-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-3">
                  <Mail/>
                  <input
                    value={profile.email}
                    onChange={(e)=>setProfile({...profile,email:e.target.value})}
                    className="bg-transparent w-full py-3 outline-none dark:text-white"
                  />
                </div>
              </div>

              <div>
                <label>Phone</label>
                <div className="flex items-center gap-3 mt-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-3">
                  <Phone/>
                  <input
                    value={profile.phone}
                    onChange={(e)=>setProfile({...profile,phone:e.target.value})}
                    className="bg-transparent w-full py-3 outline-none dark:text-white"
                  />
                </div>
              </div>

              <div>
                <label>Department</label>
                <div className="flex items-center gap-3 mt-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-3">
                  <Building2/>
                  <input
                    value={profile.department}
                    onChange={(e)=>setProfile({...profile,department:e.target.value})}
                    className="bg-transparent w-full py-3 outline-none dark:text-white"
                  />
                </div>
              </div>

              <div className="md:col-span-2">
                <label>Hospital</label>
                <div className="flex items-center gap-3 mt-2 bg-slate-100 dark:bg-slate-700 rounded-xl px-3">
                  <Building2/>
                  <input
                    value={profile.hospital}
                    onChange={(e)=>setProfile({...profile,hospital:e.target.value})}
                    className="bg-transparent w-full py-3 outline-none dark:text-white"
                  />
                </div>
              </div>

            </div>

            <button
              onClick={saveProfile}
              className="mt-6 bg-cyan-700 text-white rounded-xl px-6 py-3 flex items-center gap-2 hover:bg-cyan-800"
            >
              <Save size={18}/>
              Save Profile
            </button>

            {message && (
              <p className="text-green-600 mt-4">{message}</p>
            )}

          </div>

          {/* PASSWORD */}

          <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl p-6">

            <h2 className="font-bold text-xl mb-6 dark:text-white flex items-center gap-2">
              <KeyRound/>
              Change Password
            </h2>

            <div className="space-y-4">

              <input
                type="password"
                placeholder="Current Password"
                value={password.current_password}
                onChange={(e)=>setPassword({...password,current_password:e.target.value})}
                className="w-full bg-slate-100 dark:bg-slate-700 rounded-xl px-4 py-3 outline-none dark:text-white"
              />

              <input
                type="password"
                placeholder="New Password"
                value={password.new_password}
                onChange={(e)=>setPassword({...password,new_password:e.target.value})}
                className="w-full bg-slate-100 dark:bg-slate-700 rounded-xl px-4 py-3 outline-none dark:text-white"
              />

              <button
                onClick={changePassword}
                className="bg-green-600 hover:bg-green-700 text-white rounded-xl px-6 py-3"
              >
                Update Password
              </button>

            </div>

          </div>

          {/* ACTIVITY */}

          <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl p-6">

            <h2 className="font-bold text-xl mb-6 dark:text-white">
              Account Activity
            </h2>

            <div className="space-y-4">

              <div className="border-l-4 border-cyan-600 pl-4">
                <p className="font-semibold dark:text-white">
                  Last Login
                </p>
                <p className="text-gray-500">Today • 08:15 AM</p>
              </div>

              <div className="border-l-4 border-green-600 pl-4">
                <p className="font-semibold dark:text-white">
                  Inventory Updated
                </p>
                <p className="text-gray-500">Added 12 medicines yesterday.</p>
              </div>

              <div className="border-l-4 border-orange-500 pl-4">
                <p className="font-semibold dark:text-white">
                  AI Prediction Executed
                </p>
                <p className="text-gray-500">
                  Predicted shortage for Paracetamol.
                </p>
              </div>

              <div className="border-l-4 border-purple-600 pl-4">
                <p className="font-semibold dark:text-white">
                  PDF Report Downloaded
                </p>
                <p className="text-gray-500">Inventory Report generated.</p>
              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}