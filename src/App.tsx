import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import Medicines from "./pages/Medicines";
import Prediction from "./pages/Prediction";
import Inventory from "./pages/Inventory";
import Suppliers from "./pages/Suppliers";
import Assistant from "./pages/Assistant";
import Reports from "./pages/Report";
import Notification from "./pages/Notification";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

export default function App() {

  return (

    <BrowserRouter>

      <Layout>

        <Routes>

          <Route path="/" element={<Dashboard />} />

          <Route path="/medicines" element={<Medicines />} />

          <Route path="/prediction" element={<Prediction />} />

          <Route path="/inventory" element={<Inventory />} />

          <Route path="/suppliers" element={<Suppliers />} />

          <Route path="/assistant" element={<Assistant />} />

          <Route path="/reports" element={<Reports />} />

          <Route path="/notifications" element={<Notification />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>

      </Layout>

    </BrowserRouter>

  );

}