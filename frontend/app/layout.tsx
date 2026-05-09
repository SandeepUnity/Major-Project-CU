import type { Metadata } from "next";
import "./globals.css";

import { ColdStartBanner } from "@/components/ColdStartBanner";
import { ProjectCredits } from "@/components/ProjectCredits";

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
      <body className="min-h-screen flex flex-col bg-zinc-50 text-zinc-900">
        <ColdStartBanner />
        <div className="flex min-h-0 flex-1 flex-col">{children}</div>
        <ProjectCredits />
      </body>
    </html>
  );
}
