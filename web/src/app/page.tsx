"use client";

import React, { useState } from "react";

interface PriceItem {
  name: string;
  price: string;
  change: string;
  isPositive: boolean;
  image: string;
}

interface ListingItem {
  id: string;
  title: string;
  location: string;
  price: string;
  unit: string;
  badge: string;
  tonnage: string;
  image: string;
}

const MARKET_PRICES: PriceItem[] = [
  {
    name: "Pomidor",
    price: "6 200",
    change: "+4,2% kecha",
    isPositive: true,
    image: "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=240&auto=format&fit=crop&q=80",
  },
  {
    name: "Bodring",
    price: "5 400",
    change: "-1,8% kecha",
    isPositive: false,
    image: "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=240&auto=format&fit=crop&q=80",
  },
  {
    name: "Kartoshka",
    price: "4 100",
    change: "+0,9% kecha",
    isPositive: true,
    image: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=240&auto=format&fit=crop&q=80",
  },
  {
    name: "Piyoz",
    price: "3 300",
    change: "-2,5% kecha",
    isPositive: false,
    image: "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=240&auto=format&fit=crop&q=80",
  },
];

const RECENT_LISTINGS: ListingItem[] = [
  {
    id: "l-1",
    title: "Pomidor, 1-nav",
    location: "Qo'qon, Farg'ona",
    price: "5 800",
    unit: "so'm/kg",
    badge: "Tasdiqlangan",
    tonnage: "12 tonna mavjud",
    image: "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80",
  },
  {
    id: "l-2",
    title: "Bodring",
    location: "Zangiota, Toshkent",
    price: "4 900",
    unit: "so'm/kg",
    badge: "Tasdiqlangan",
    tonnage: "6 tonna mavjud",
    image: "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=600&auto=format&fit=crop&q=80",
  },
  {
    id: "l-3",
    title: "Kartoshka, 2-nav",
    location: "Bekobod, Toshkent",
    price: "3 700",
    unit: "so'm/kg",
    badge: "Yangi",
    tonnage: "25 tonna mavjud",
    image: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&auto=format&fit=crop&q=80",
  },
  {
    id: "l-4",
    title: "Uzum, Husayni",
    location: "Urgut, Samarqand",
    price: "9 500",
    unit: "so'm/kg",
    badge: "Tasdiqlangan",
    tonnage: "3 tonna, 15-avgust",
    image: "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=600&auto=format&fit=crop&q=80",
  },
];

export default function HomePage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedListing, setSelectedListing] = useState<ListingItem | null>(null);
  const [orderKg, setOrderKg] = useState(1000);
  const [isOrdered, setIsOrdered] = useState(false);

  const filteredListings = RECENT_LISTINGS.filter(
    (item) =>
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-12 pb-10">
      {/* 1. HERO SECTION */}
      <section className="max-w-4xl pt-2">
        <h1 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold tracking-tight text-[#1C1A17] leading-tight">
          Hosilni to'g'ridan-to'g'ri fermerdan oling
        </h1>
        <p className="mt-2 text-base text-[#686258] font-normal leading-relaxed">
          Vositachisiz narx, tasdiqlangan fermerlar, xavfsiz to'lov va yetkazib berish.
        </p>

        {/* Sleek Search Pill Container */}
        <div className="mt-6 flex items-center bg-white border border-[#E8E4DB] rounded-full p-1.5 pl-5 pr-2 w-full max-w-3xl shadow-sm focus-within:border-[#387C4C] transition">
          <div className="flex items-center flex-1 space-x-3">
            <svg
              className="w-5 h-5 text-gray-400 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Mahsulot turi yoki hududni qidiring"
              className="w-full text-sm text-gray-800 placeholder-gray-400 bg-transparent border-none outline-none font-medium"
            />
          </div>
          <button
            onClick={() => {}}
            className="bg-white border border-[#D5E4D8] hover:bg-[#F2F7F4] text-[#2F6B42] font-bold text-sm px-7 py-2.5 rounded-full transition shadow-sm"
          >
            Qidirish
          </button>
        </div>
      </section>

      {/* 2. BUGUNGI BOZOR NARXLARI */}
      <section id="narxlar">
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="text-xl sm:text-2xl font-extrabold text-[#1C1A17]">
            Bugungi bozor narxlari
          </h2>
          <span className="text-xs sm:text-sm text-[#736C61] font-medium">
            Parkent bozori, kg uchun
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {MARKET_PRICES.map((item, idx) => (
            <div
              key={idx}
              className="bg-white border border-[#E8E4DB] rounded-2xl p-4 flex items-center justify-between hover:shadow-md transition cursor-pointer"
            >
              <div>
                <div className="text-sm font-semibold text-[#5A544A]">{item.name}</div>
                <div className="text-2xl font-black text-[#1F1D19] tracking-tight mt-0.5">
                  {item.price}
                </div>
                <div
                  className={`text-xs font-bold mt-1 flex items-center space-x-0.5 ${
                    item.isPositive ? "text-[#2A8248]" : "text-[#C6473D]"
                  }`}
                >
                  <span>{item.isPositive ? "↑" : "↓"}</span>
                  <span>{item.change}</span>
                </div>
              </div>
              <div className="w-20 h-20 rounded-xl overflow-hidden flex items-center justify-center p-1">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover rounded-lg"
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. YANGI E'LONLAR */}
      <section id="elonlar">
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="text-xl sm:text-2xl font-extrabold text-[#1C1A17]">
            Yangi e'lonlar
          </h2>
          <a
            href="/listings"
            className="text-xs sm:text-sm font-bold text-[#2F6B42] hover:underline"
          >
            Barchasini ko'rish
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {filteredListings.map((item) => (
            <div
              key={item.id}
              onClick={() => {
                setSelectedListing(item);
                setIsOrdered(false);
              }}
              className="bg-white border border-[#E8E4DB] rounded-2xl overflow-hidden flex flex-col justify-between hover:shadow-lg transition cursor-pointer"
            >
              <div>
                {/* Photo with Overlay Badge */}
                <div className="h-44 w-full relative overflow-hidden bg-gray-100">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover hover:scale-105 transition duration-300"
                  />
                  <span className="absolute top-3 right-3 bg-[#2E7D4B]/90 backdrop-blur-md text-white text-[11px] font-bold px-2.5 py-1 rounded-full flex items-center space-x-1 shadow-sm">
                    <svg className="w-3 h-3 fill-current" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>TASDIQLANGAN</span>
                  </span>
                </div>

                {/* Details */}
                <div className="p-4 space-y-1.5">
                  <h3 className="font-extrabold text-base text-[#1C1A17]">{item.title}</h3>
                  <div className="text-xs text-[#736C61] flex items-center space-x-1">
                    <svg
                      className="w-3.5 h-3.5 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                    <span>{item.location}</span>
                  </div>

                  {/* Price & Tag */}
                  <div className="pt-2 flex items-baseline space-x-2">
                    <span className="text-lg font-black text-[#1C1A17]">{item.price}</span>
                    <span className="text-xs font-semibold text-[#736C61]">{item.unit}</span>
                    {item.badge === "Tasdiqlangan" ? (
                      <span className="text-[11px] font-bold text-[#2F6B42] bg-[#E8F2EC] px-2 py-0.5 rounded-full flex items-center space-x-0.5">
                        <span>✓</span>
                        <span>Tasdiqlangan</span>
                      </span>
                    ) : (
                      <span className="text-[11px] font-bold text-[#555047] bg-[#EFECE6] px-2 py-0.5 rounded-full">
                        Yangi
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Stock Footer */}
              <div className="px-4 pb-4 pt-1 text-xs text-[#736C61] font-semibold flex items-center space-x-1.5">
                <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                <span>{item.tonnage}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4. BOTTOM TWO-COLUMN SECTION */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-5" id="yetkazib-berish">
        {/* Left: Xaridor talablari (Teskari auksion) */}
        <div className="bg-white border border-[#E8E4DB] rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-5">
            <h3 className="text-lg font-extrabold text-[#1C1A17]">Xaridor talablari</h3>
            <a
              href="/demand"
              className="text-xs font-bold text-[#6D6558] bg-[#F1EDE6] px-3 py-1 rounded-full flex items-center space-x-1 hover:bg-[#EAE4DC] transition"
            >
              <span>⚖️</span>
              <span>Teskari auksion</span>
            </a>
          </div>

          <div className="space-y-3.5 divide-y divide-[#F1EFEA]">
            <div className="pt-1 flex items-center justify-between">
              <div className="text-sm font-semibold text-[#2C2720]">
                100 tonna pomidor, Toshkent
              </div>
              <div className="text-sm font-bold text-[#2F6B42] bg-[#EAF3ED] px-3 py-1 rounded-lg">
                14 taklif
              </div>
            </div>

            <div className="pt-3.5 flex items-center justify-between">
              <div className="text-sm font-semibold text-[#2C2720]">
                20 tonna olma, Samarqand
              </div>
              <div className="text-sm font-bold text-[#7E7465] bg-[#F3F0EA] px-3 py-1 rounded-lg">
                X taklif
              </div>
            </div>

            <div className="pt-3.5 flex items-center justify-between">
              <div className="text-sm font-semibold text-[#2C2720]">
                50 tonna qizil kartoshka, Andijon
              </div>
              <div className="text-sm font-bold text-[#2F6B42] bg-[#EAF3ED] px-3 py-1 rounded-lg">
                8 taklif
              </div>
            </div>
          </div>
        </div>

        {/* Right: Yetkazib berish (Logistika & 3D Icons) */}
        <div className="bg-white border border-[#E8E4DB] rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-extrabold text-[#1C1A17]">Yetkazib berish</h3>
            <span className="text-xs text-[#736C61] font-semibold">
              Kafolatlangan logistika
            </span>
          </div>

          {/* 3D Elements Row */}
          <div className="grid grid-cols-3 gap-4 my-2">
            <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 text-center flex flex-col items-center justify-center space-y-1.5">
              <div className="text-3xl filter drop-shadow">🚚</div>
              <div className="text-xs font-bold text-[#3B342A]">Yo'ldosh Yuklar</div>
              <div className="text-[11px] text-[#7E7567]">Bo'sh qaytmaydi</div>
            </div>

            <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 text-center flex flex-col items-center justify-center space-y-1.5">
              <div className="text-3xl filter drop-shadow">🛡️</div>
              <div className="text-xs font-bold text-[#3B342A]">Escrow To'lov</div>
              <div className="text-[11px] text-[#7E7567]">100% himoyalangan</div>
            </div>

            <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 text-center flex flex-col items-center justify-center space-y-1.5">
              <div className="text-3xl filter drop-shadow">⭐</div>
              <div className="text-xs font-bold text-[#3B342A]">Tasdiqlangan</div>
              <div className="text-[11px] text-[#7E7567]">Ishonchli haydovchi</div>
            </div>
          </div>

          <div className="pt-2 text-xs text-[#736C61] flex items-center justify-between border-t border-[#F1EFEA]">
            <span>6 xonali topshirish kodi bilan xavfsiz to'lov</span>
            <a
              href="https://t.me/HosilBozorBot"
              target="_blank"
              rel="noreferrer"
              className="font-bold text-[#2F6B42] hover:underline"
            >
              Haydovchi bo'lish &rarr;
            </a>
          </div>
        </div>
      </section>

      {/* Escrow Purchase Modal */}
      {selectedListing && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl relative border border-[#E8E4DB]">
            <button
              onClick={() => setSelectedListing(null)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              &times;
            </button>

            {!isOrdered ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-[#E8F2EC] flex items-center justify-center text-lg">
                    🌾
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-[#1C1A17]">
                      {selectedListing.title}
                    </h3>
                    <p className="text-xs text-gray-500">{selectedListing.location}</p>
                  </div>
                </div>

                <div className="bg-[#FAF8F5] border border-[#EBE7DF] p-4 rounded-2xl space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Birlik narxi:</span>
                    <span className="font-bold text-[#1C1A17]">
                      {selectedListing.price} {selectedListing.unit}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Mavjud hajm:</span>
                    <span className="font-semibold text-gray-800">
                      {selectedListing.tonnage}
                    </span>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-700 mb-1">
                    Buyurtma hajmi (kg):
                  </label>
                  <input
                    type="number"
                    value={orderKg}
                    onChange={(e) => setOrderKg(Number(e.target.value))}
                    min={100}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl font-bold text-base focus:ring-2 focus:ring-[#2F6B42] focus:outline-none"
                  />
                </div>

                <div className="border-t border-gray-100 pt-3 space-y-1.5 text-xs text-gray-600">
                  <div className="flex justify-between">
                    <span>Hosil qiymati:</span>
                    <span>
                      {(
                        orderKg * parseInt(selectedListing.price.replace(/\s/g, ""))
                      ).toLocaleString()}{" "}
                      so'm
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Escrow kafolat (2%):</span>
                    <span>
                      {Math.round(
                        orderKg *
                          parseInt(selectedListing.price.replace(/\s/g, "")) *
                          0.02
                      ).toLocaleString()}{" "}
                      so'm
                    </span>
                  </div>
                  <div className="flex justify-between text-sm font-black text-[#1C1A17] pt-1">
                    <span>Jami to'lov:</span>
                    <span className="text-[#2F6B42]">
                      {Math.round(
                        orderKg *
                          parseInt(selectedListing.price.replace(/\s/g, "")) *
                          1.02
                      ).toLocaleString()}{" "}
                      so'm
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => setIsOrdered(true)}
                  className="w-full py-3 rounded-xl bg-[#2F6B42] hover:bg-[#285D39] text-white font-bold text-sm shadow-md transition"
                >
                  🛡️ Escrow orqali buyurtma berish
                </button>
              </div>
            ) : (
              <div className="text-center py-4 space-y-3">
                <div className="w-14 h-14 bg-[#E8F2EC] text-[#2F6B42] rounded-full flex items-center justify-center mx-auto text-2xl font-black">
                  ✓
                </div>
                <h3 className="font-extrabold text-lg text-[#1C1A17]">
                  Buyurtma Escrowda Muzlatildi!
                </h3>
                <p className="text-xs text-gray-500">
                  Topshirish kodi xaridorga yetkazildi. Hosil yetib borgach, kod orqali pul
                  fermerga o'tkaziladi.
                </p>
                <div className="bg-[#FAF8F5] p-3 rounded-xl font-mono text-xs font-bold text-[#8A5A2B]">
                  Topshirish Kodi: 719342
                </div>
                <button
                  onClick={() => setSelectedListing(null)}
                  className="w-full py-2.5 rounded-xl bg-[#1C1A17] text-white font-bold text-xs"
                >
                  Yopish
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
