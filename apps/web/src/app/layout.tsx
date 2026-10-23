import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "CI × Nasara | Risk Intelligence", description: "Read-only trading risk intelligence and portfolio monitoring." };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html>; }
