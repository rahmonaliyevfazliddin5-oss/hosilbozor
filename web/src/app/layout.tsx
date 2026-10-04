import React from "react";
import "./globals.css";

export const metadata = {
  title: "HosilBozor — O'zbekiston Agrar Bozor Web Platformasi",
  description: "Hosilni to'g'ridan-to'g'ri fermerdan oling. Vositachisiz narx, tasdiqlangan fermerlar, xavfsiz to'lov va yetkazib berish.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="uz" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col font-sans px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pt-4" suppressHydrationWarning>
        {/* Floating Top Wooden Navbar */}
        <header className="wooden-nav rounded-2xl h-14 px-5 flex items-center justify-between sticky top-4 z-50 mb-8 transition">
          <div className="flex items-center space-x-8">
            <a href="/" className="flex items-center space-x-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-[#3F7C4E] flex items-center justify-center text-white shadow-sm font-black text-sm">
                🌿
              </div>
              <span className="font-extrabold text-lg tracking-tight text-[#2B231A]">HosilBozor</span>
            </a>
            <nav className="hidden md:flex items-center space-x-7 text-sm font-semibold text-[#44382C]">
              <a href="/listings" className="hover:text-[#1F1812] transition">E'lonlar</a>
              <a href="/#narxlar" className="hover:text-[#1F1812] transition">Narxlar</a>
              <a href="/demand" className="hover:text-[#1F1812] transition">Talablar</a>
              <a href="/#yetkazib-berish" className="hover:text-[#1F1812] transition">Yetkazib berish</a>
              <a href="/admin" className="hover:text-[#1F1812] transition text-xs opacity-75">Admin Panel</a>
            </nav>
          </div>

          <div className="flex items-center space-x-3">
            <a
              href="https://t.me/HosilBozorBot"
              target="_blank"
              rel="noreferrer"
              className="hidden sm:inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-[#EFE9DF] text-[#42372A] hover:bg-[#E8DFD0] transition"
            >
              🤖 Bot
            </a>
            <a
              href="/admin"
              className="text-sm font-semibold text-[#3D3226] hover:text-black transition px-3 py-1.5"
            >
              Kirish
            </a>
          </div>
        </header>

        {/* Main Body */}
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}
