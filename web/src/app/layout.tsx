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
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#2AABEE] text-white hover:bg-[#229ED9] shadow-sm hover:shadow transition"
              title="@HosilBozorBot Telegram boti"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.37.74-.56 2.92-1.27 4.86-2.11 5.83-2.52 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06-.01.17-.02.27z"/>
              </svg>
              <span>@HosilBozorBot</span>
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

        {/* Floating Telegram Bot Widget */}
        <aside className="fixed bottom-6 right-6 z-50">
          <a
            href="https://t.me/HosilBozorBot"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-2.5 bg-[#2AABEE] hover:bg-[#229ED9] text-white px-4 py-3 rounded-full shadow-2xl hover:shadow-cyan-500/40 transition-all transform hover:-translate-y-1 group"
            title="Telegram botimiz orqali tezkor bog'lanish: @HosilBozorBot"
          >
            <div className="w-8 h-8 bg-white text-[#2AABEE] rounded-full flex items-center justify-center shadow-inner">
              <svg className="w-4 h-4 fill-current ml-0.5" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.37.74-.56 2.92-1.27 4.86-2.11 5.83-2.52 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06-.01.17-.02.27z"/>
              </svg>
            </div>
            <div className="flex flex-col text-left pr-1">
              <span className="text-[10px] font-medium leading-none opacity-90">Telegram Bot</span>
              <span className="text-xs font-extrabold leading-tight">@HosilBozorBot</span>
            </div>
          </a>
        </aside>
      </body>
    </html>
  );
}
