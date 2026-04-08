import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Academic Writing Copilot",
  description: "Human-in-the-Loop academic writing workspace"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
