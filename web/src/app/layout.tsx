import React from "react";

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
    <html lang="uz">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
        <style>{`
          body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #F8F6F0;
            color: #1A1A1A;
          }
          .wooden-nav {
            background: linear-gradient(135deg, #E6DDD0 0%, #DFD5C5 50%, #D8CDBC 100%);
            box-shadow: 0 4px 20px -2px rgba(160, 140, 110, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.45);
            border: 1px solid rgba(210, 195, 175, 0.5);
          }
        `}</style>
      </head>
      <body className="min-h-screen flex flex-col font-sans px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pt-4">
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

        {/* Minimal Footer */}
        <footer className="py-10 mt-12 border-t border-[#EBE6DC] text-center text-xs text-[#7A7265] space-y-1">
          <p className="font-bold text-[#3B342A]">🌾 HosilBozor — O'zbekiston Qishloq Xo'jaligi Raqamli Bozori</p>
          <p>Vositachisiz narx, tasdiqlangan fermerlar, xavfsiz to'lov va yetkazib berish.</p>
        </footer>
      </body>
    </html>
  );
}
