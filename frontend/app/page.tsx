"use client";

import { useCallback, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Status = "idle" | "uploading" | "success" | "error";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [caption, setCaption] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);

  const reset = useCallback(() => {
    setFile(null);
    setPreview(null);
    setCaption(null);
    setStatus("idle");
    setError(null);
  }, []);

  const handleFile = useCallback((f: File | null) => {
    if (!f) {
      setFile(null);
      setPreview(null);
      return;
    }
    if (!f.type.startsWith("image/")) {
      setError("Please choose an image file (JPEG, PNG, WebP, or GIF).");
      return;
    }
    setError(null);
    setFile(f);
    setCaption(null);
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result as string);
    reader.readAsDataURL(f);
  }, []);

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const f = e.dataTransfer.files?.[0];
      handleFile(f || null);
    },
    [handleFile]
  );

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
  }, []);

  const onInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const f = e.target.files?.[0];
      handleFile(f || null);
    },
    [handleFile]
  );

  const generateCaption = useCallback(async () => {
    if (!file) return;
    setStatus("uploading");
    setError(null);
    setCaption(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API_URL}/caption`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setError(data.detail || `Request failed (${res.status})`);
        setStatus("error");
        return;
      }
      setCaption(data.caption ?? "");
      setStatus("success");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not reach the server. Is the backend running?"
      );
      setStatus("error");
    }
  }, [file]);

  return (
    <main className="min-h-screen bg-black flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl mx-auto space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Image Caption Generator
          </h1>
          <p className="text-gray-400 text-sm">
            Upload an image and get an AI-generated caption
          </p>
        </header>

        <div
          className={`upload-zone relative rounded-2xl border-2 border-dashed border-gray-700 min-h-[280px] flex flex-col items-center justify-center p-8 ${
            preview ? "has-image" : ""
          } ${dragging ? "dragging" : ""}`}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
        >
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp,image/gif"
            onChange={onInputChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-label="Choose image"
          />
          {preview ? (
            <div className="relative w-full max-h-[320px] flex items-center justify-center rounded-xl overflow-hidden bg-gray-900/50">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={preview}
                alt="Preview"
                className="max-h-[320px] w-auto object-contain rounded-xl"
              />
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  reset();
                }}
                className="absolute top-3 right-3 px-3 py-1.5 rounded-lg bg-black/70 text-gray-300 hover:bg-red-500/80 hover:text-white text-sm font-medium transition-colors"
              >
                Remove
              </button>
            </div>
          ) : (
            <>
              <div className="rounded-full bg-gray-800/80 p-4 mb-4">
                <svg
                  className="w-10 h-10 text-gray-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <p className="text-gray-400 text-center">
                Drag and drop an image here, or click to browse
              </p>
              <p className="text-gray-500 text-sm mt-1">
                JPEG, PNG, WebP, or GIF
              </p>
            </>
          )}
        </div>

        {error && (
          <div className="rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 text-sm">
            {error}
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            type="button"
            onClick={generateCaption}
            disabled={!file || status === "uploading"}
            className="btn-primary px-6 py-3 rounded-xl bg-indigo-600 text-white font-medium disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {status === "uploading" ? "Generating caption…" : "Generate caption"}
          </button>
          {file && status !== "uploading" && (
            <button
              type="button"
              onClick={() => {
                handleFile(null);
                setCaption(null);
                setError(null);
                setStatus("idle");
              }}
              className="px-6 py-3 rounded-xl border border-gray-600 text-gray-400 hover:border-gray-500 hover:text-gray-300 font-medium transition-colors"
            >
              Choose another image
            </button>
          )}
        </div>

        {caption !== null && (
          <div className="caption-box rounded-2xl p-6 space-y-2">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
              Caption
            </h2>
            <p className="text-lg text-white leading-relaxed">{caption}</p>
          </div>
        )}
      </div>

      <footer className="mt-12 text-center text-gray-500 text-xs">
        Backend: {API_URL}
      </footer>
    </main>
  );
}
