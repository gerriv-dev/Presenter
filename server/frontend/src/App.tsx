import { useEffect, useRef, useState, type ChangeEvent } from "react";

export default function App() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [files, setFiles] = useState<string[]>([]);
  const [file, setFile] = useState("");
  const [updateFiles, setUpdateFiles] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const uploadFile = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await fetch("/pp/upload", {
      method: "POST",
      body: formData,
    });
    setFiles([]);
    setUpdateFiles(!updateFiles);
  };

  const startPresentation = async (file: string) => {
    const socket = new WebSocket(`ws://${location.host}/ws`);
    socket.onmessage = () => {
      stopPresentation();
    };
    setWs(socket);
    console.log("verbunden");
    setFile(file);
  };

  const stopPresentation = () => {
    if (ws) {
      ws.send("stop");
      ws.close();
      setWs(null);
      setFile("");
      console.log("getrennt");
    }
  };

  useEffect(() => {
    const getFiles = async () => {
      const response = await fetch("/pp");
      const data: { files: string[] } = await response.json();
      setFiles(data.files);
    };
    getFiles();
  }, [updateFiles]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-between bg-white">
      <nav className="flex w-full items-center justify-between bg-gray-100 p-4">
        <h1>Presenter</h1>
        <input
          type="file"
          name="file"
          accept=".png,.jpg"
          ref={fileInputRef}
          onChange={uploadFile}
          hidden
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          className="size-8 rounded bg-black text-white"
        >
          +
        </button>
      </nav>
      <main className="flex w-full flex-1 flex-col items-center justify-start p-4">
        {file ? (
          <div className="relative flex w-full flex-1 items-center justify-center gap-4">
            <div className="absolute top-0 left-0 flex gap-4">
              <button onClick={stopPresentation} className="underline">
                Zurück
              </button>
              <button
                onClick={() => ws?.send(`start:${file}`)}
                className="underline"
              >
                Starten
              </button>
            </div>
            <button onClick={() => ws?.send("back")} className="control">
              &lt;
            </button>
            <button onClick={() => ws?.send("next")} className="control">
              &gt;
            </button>
          </div>
        ) : (
          <div className="flex w-full flex-col items-center justify-center gap-4">
            <ul className="shadow-hard flex w-full flex-col gap-4 rounded-xl border border-black p-4">
              {files.map((file) => (
                <li key={file} onClick={() => startPresentation(file)}>
                  <button>{file}</button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
