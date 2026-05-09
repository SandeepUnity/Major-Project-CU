import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EmpowerTech Support Chat",
  description: "RAG chatbot UI for EmpowerTech Solutions",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-zinc-50 text-zinc-900">
        {children}
      </body>
    </html>
  );
}
