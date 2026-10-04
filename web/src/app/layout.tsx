import React from "react";

export const metadata = {
  title: "HosilBozor — O'zbekiston Agrar Bozor Web Platformasi",
  description: "Fermer, ulgurji xaridor va haydovchini bog'lovchi shaffof agrar web-platforma.",
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
      </head>
      <body className="bg-gray-50 text-gray-900 min-h-screen flex flex-col font-sans">
        {/* Navigation Bar */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <a href="/" className="flex items-center space-x-2 text-xl font-bold text-emerald-700">
                <span>🌾</span>
                <span>HosilBozor</span>
              </a>
              <nav className="hidden md:flex space-x-6 text-sm font-medium text-gray-700">
                <a href="/listings" className="hover:text-emerald-600 transition">Hosil Bozori</a>
                <a href="/demand" className="hover:text-emerald-600 transition">Talab & Auksion</a>
                <a href="/admin" className="hover:text-emerald-600 transition">Admin Panel</a>
              </nav>
            </div>

            <div className="flex items-center space-x-4">
              <a
                href="https://t.me/HosilBozorBot"
                target="_blank"
                rel="noreferrer"
                className="hidden sm:inline-flex items-center px-3.5 py-1.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition"
              >
                <span>🤖 Telegram Bot</span>
              </a>
              <div className="text-xs font-semibold px-2.5 py-1 bg-gray-100 rounded text-gray-700">
                UZ (Lotin)
              </div>
            </div>
          </div>
        </header>

        {/* Main Body */}
        <main className="flex-1">{children}</main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 py-8 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
            <p className="font-semibold text-gray-700">🌾 HosilBozor — O'zbekiston Qishloq Xo'jaligi Raqamli Bozori</p>
            <p className="mt-1">Toshkent, O'zbekiston • Xavfsiz Escrow to'lovi va Logistika yechimlari</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
