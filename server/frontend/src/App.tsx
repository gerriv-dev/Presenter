import { useEffect, useRef, useState, type ChangeEvent } from "react";

export default function App() {
  const [showControls, setShowControls] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [files, setFiles] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const uploadFile = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await fetch("http://localhost:8000/pp/upload", {
      method: "POST",
      body: formData,
    });
    setFiles([]);
  };

  const startPresentation = async (file: string) => {
    const socket = new WebSocket("ws://localhost:8000/ws/controller");
    socket.onmessage = () => {
      stopPresentation();
    };
    setWs(socket);
    ws?.send(`start:${file}`);
    console.log("verbunden");
    setShowControls(true);
  };

  const stopPresentation = () => {
    if (ws) {
      ws.send("stop");
      ws.close();
      setWs(null);
      setShowControls(false);
      console.log("getrennt");
    }
  };

  useEffect(() => {
    const getFiles = async () => {
      const response = await fetch("http://localhost:8000/pp");
      const data: { files: string[] } = await response.json();
      setFiles(data.files);
    };
    getFiles();
  }, [files]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-between bg-white">
      <nav className="flex w-full items-center justify-between bg-gray-100 p-4">
        <h1>Presenter</h1>
        <input
          type="file"
          name="file"
          accept=".ppt,.pptx"
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
        {showControls ? (
          <div className="relative flex w-full flex-1 items-center justify-center gap-4">
            <button
              onClick={stopPresentation}
              className="absolute top-0 left-0 underline"
            >
              Zurück
            </button>
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
