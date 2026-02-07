import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image Caption Generator",
  description: "Generate captions for your images using AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-black text-gray-100 antialiased">
        {children}
      </body>
    </html>
  );
}
