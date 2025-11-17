import { useState } from "react";

export default function App() {
  const [securityType, setSecurityType] = useState("");

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-white">
      <form className="shadow-hard flex w-10/12 max-w-sm flex-col gap-2 rounded-xl border border-black p-8">
        <h1 className="text-xl font-bold">Quick Setup</h1>
        <p className="-mt-2 font-light">Gib hier deine WiFi-Zugangsdaten ein</p>
        <div className="my-4 h-px w-full bg-black" />
        <input type="text" name="ssid" placeholder="SSID" />
        <select
          name="security-type"
          onChange={(e) => setSecurityType(e.target.value)}
        >
          <option value="" hidden selected>
            Sicherheit
          </option>
          <option value="none">Keine</option>
          <option value="personal">Personal</option>
          <option value="enterprise">Enterprise</option>
        </select>
        {securityType != "" && securityType != "none" && (
          <>
            <div className="my-4 h-px w-full bg-black" />
            {securityType === "enterprise" && (
              <input type="text" name="account" placeholder="Account" />
            )}
            <input type="password" name="password" placeholder="Passwort" />
          </>
        )}
        <button
          type="submit"
          className="mt-4 w-full rounded-lg bg-black py-2 text-white"
        >
          Verbinden
        </button>
      </form>
    </div>
  );
}
