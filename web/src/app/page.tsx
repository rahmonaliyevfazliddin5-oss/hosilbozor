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

  // Demand offer modal state
  const [activeOfferDemand, setActiveOfferDemand] = useState<string | null>(null);
  const [offerPrice, setOfferPrice] = useState("6400");
  const [offerSent, setOfferSent] = useState(false);

  // Active region tab for Sourcing Map
  const [selectedRegion, setSelectedRegion] = useState("fargona");

  const filteredListings = RECENT_LISTINGS.filter(
    (item) =>
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-14 pb-6">
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
            className="bg-white border border-[#D5E4D8] hover:bg-[#F2F7F4] text-[#2F6B42] font-bold text-sm px-7 py-2.5 rounded-full transition shadow-sm"
          >
            Qidirish
          </button>
        </div>

        {/* Quick Telegram Bot CTA */}
        <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-[#5C5243]">
          <span className="font-medium text-[#7D7364]">Fermermisiz yoki haydovchi?</span>
          <a
            href="https://t.me/HosilBozorBot"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#EBF5FB] hover:bg-[#D9EAF5] text-[#1E7FA8] font-bold border border-[#C5DFEE] transition shadow-xs group"
            title="Telegram botimiz orqali tezkor e'lon bering"
          >
            <svg className="w-4 h-4 fill-[#2AABEE] group-hover:scale-110 transition-transform" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.37.74-.56 2.92-1.27 4.86-2.11 5.83-2.52 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06-.01.17-.02.27z"/>
            </svg>
            <span>@HosilBozorBot orqali 60 soniyada e'lon bering &rarr;</span>
          </a>
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

      {/* 4. SECTION 1 & 2: EXPANDED BUYER DEMANDS & LOGISTICS */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6" id="talablar">
        {/* SECTION 1: XARIDOR TALABLARI (Teskari auksion) */}
        <div className="bg-white border border-[#E8E4DB] rounded-3xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="text-xl font-extrabold text-[#1C1A17]">
                  Xaridor talablari (Teskari auksion)
                </h3>
                <p className="text-xs text-[#787165] mt-0.5">
                  Ulgurji xaridorlar talablari bo'yicha to'g'ridan-to'g'ri narx taklif qiling
                </p>
              </div>
              <span className="text-xs font-bold text-[#4F4638] bg-[#F1EDE6] px-3.5 py-1.5 rounded-full flex items-center space-x-1">
                <span>⚖️</span>
                <span>Teskari auksion</span>
              </span>
            </div>

            <div className="space-y-4">
              {/* Demand 1 */}
              <div className="border border-[#F0ECE4] bg-[#FAF8F5] rounded-2xl p-4.5 hover:border-[#D8CFBF] transition">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-extrabold text-base text-[#1C1A17] block">
                      100 tonna pomidor, Toshkent
                    </span>
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-[11px] font-bold bg-[#2F6B42] text-white px-2 py-0.5 rounded">
                        AKTV
                      </span>
                      <span className="text-xs text-[#5D5547] flex items-center space-x-1">
                        <span>⭐</span>
                        <span className="font-bold">4.9</span>
                        <span>&bull; Korzinka Ta'minot</span>
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold text-[#2F6B42] bg-[#EAF3ED] px-3 py-1 rounded-full">
                      14 taklif
                    </span>
                    <div className="text-[11px] text-[#8C8476] mt-2 font-medium">
                      ⏱️ 1 kun 4 soat qoldi
                    </div>
                  </div>
                </div>
                <div className="mt-3.5 pt-3 border-t border-[#EBE7DF] flex items-center justify-between">
                  <span className="text-xs text-[#5D5547]">Maks. narx: <strong>6 800 so'm/kg</strong></span>
                  <button
                    onClick={() => {
                      setActiveOfferDemand("100 tonna pomidor, Toshkent");
                      setOfferSent(false);
                    }}
                    className="px-4 py-1.5 rounded-xl bg-white border border-[#306C43] text-[#2F6B42] hover:bg-[#F2F7F4] font-bold text-xs transition shadow-sm"
                  >
                    Taklif yuborish
                  </button>
                </div>
              </div>

              {/* Demand 2 */}
              <div className="border border-[#F0ECE4] bg-[#FAF8F5] rounded-2xl p-4.5 hover:border-[#D8CFBF] transition">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-extrabold text-base text-[#1C1A17] block">
                      40 tonna kartoshka, Samarqand
                    </span>
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-[11px] font-bold bg-[#2F6B42] text-white px-2 py-0.5 rounded">
                        AKTV
                      </span>
                      <span className="text-xs text-[#5D5547] flex items-center space-x-1">
                        <span>⭐</span>
                        <span className="font-bold">4.8</span>
                        <span>&bull; Afrosiyob Agro MChJ</span>
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold text-[#2F6B42] bg-[#EAF3ED] px-3 py-1 rounded-full">
                      6 taklif
                    </span>
                    <div className="text-[11px] text-[#8C8476] mt-2 font-medium">
                      ⏱️ 3 kun qoldi
                    </div>
                  </div>
                </div>
                <div className="mt-3.5 pt-3 border-t border-[#EBE7DF] flex items-center justify-between">
                  <span className="text-xs text-[#5D5547]">Maks. narx: <strong>3 200 so'm/kg</strong></span>
                  <button
                    onClick={() => {
                      setActiveOfferDemand("40 tonna kartoshka, Samarqand");
                      setOfferSent(false);
                    }}
                    className="px-4 py-1.5 rounded-xl bg-white border border-[#306C43] text-[#2F6B42] hover:bg-[#F2F7F4] font-bold text-xs transition shadow-sm"
                  >
                    Taklif yuborish
                  </button>
                </div>
              </div>

              {/* Demand 3 */}
              <div className="border border-[#F0ECE4] bg-[#FAF8F5] rounded-2xl p-4.5 hover:border-[#D8CFBF] transition">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-extrabold text-base text-[#1C1A17] block">
                      20 tonna olma, Namangan
                    </span>
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-[11px] font-bold bg-[#8A7F6E] text-white px-2 py-0.5 rounded">
                        YANGI
                      </span>
                      <span className="text-xs text-[#5D5547] flex items-center space-x-1">
                        <span>⭐</span>
                        <span className="font-bold">5.0</span>
                        <span>&bull; Silk Road Fresh</span>
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-[#7E7465] bg-[#F3F0EA] px-3 py-1 rounded-full">
                      2 taklif
                    </span>
                    <div className="text-[11px] text-[#8C8476] mt-2 font-medium">
                      ⏱️ 5 kun qoldi
                    </div>
                  </div>
                </div>
                <div className="mt-3.5 pt-3 border-t border-[#EBE7DF] flex items-center justify-between">
                  <span className="text-xs text-[#5D5547]">Maks. narx: <strong>9 000 so'm/kg</strong></span>
                  <button
                    onClick={() => {
                      setActiveOfferDemand("20 tonna olma, Namangan");
                      setOfferSent(false);
                    }}
                    className="px-4 py-1.5 rounded-xl bg-white border border-[#306C43] text-[#2F6B42] hover:bg-[#F2F7F4] font-bold text-xs transition shadow-sm"
                  >
                    Taklif yuborish
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-5 pt-3 border-t border-[#F0ECE4] flex items-center justify-between text-xs text-[#736C61]">
            <span>Talablar bo'yicha g'olib xaridor tomonidan tanlanadi</span>
            <a href="/demand" className="font-bold text-[#2F6B42] hover:underline">
              Barcha talablar doskasi &rarr;
            </a>
          </div>
        </div>

        {/* SECTION 2: YETKAZIB BERISH XIZMATI (Logistics & Delivery) */}
        <div className="bg-white border border-[#E8E4DB] rounded-3xl p-6 shadow-sm flex flex-col justify-between" id="yetkazib-berish">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-xl font-extrabold text-[#1C1A17]">
                  Yetkazib berish xizmati
                </h3>
                <p className="text-xs text-[#787165] mt-0.5">
                  Hosilni sovitgichli mashinalarda daladan omborga xavfsiz yetkazish
                </p>
              </div>
              <span className="text-xs font-bold text-[#2F6B42] bg-[#EAF3ED] px-3 py-1 rounded-full">
                Real-vaqt marshrut
              </span>
            </div>

            {/* Logistics Grid: Route Preview + Vehicle Specs */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 mb-5">
              {/* Route Preview Graphic */}
              <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 flex flex-col justify-between relative overflow-hidden">
                <div className="flex items-center justify-between text-[11px] font-bold text-[#5A5245]">
                  <span>Marshrut: Toshkent ➔ Farg'ona</span>
                </div>
                <div className="my-3 flex items-center justify-center">
                  <div className="w-full h-12 bg-white rounded-xl border border-[#E5E0D5] flex items-center justify-around px-2 relative">
                    <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42]"></span>
                    <div className="h-0.5 flex-1 mx-2 bg-gradient-to-r from-[#2F6B42] via-amber-400 to-[#2F6B42]"></div>
                    <span className="text-base">🚚</span>
                    <div className="h-0.5 flex-1 mx-2 bg-gray-200"></div>
                    <span className="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                  </div>
                </div>
                <div className="text-[11px] text-[#7A7264] flex justify-between font-semibold">
                  <span>320 km</span>
                  <span className="text-[#2F6B42]">Yo'lda (Faol)</span>
                </div>
              </div>

              {/* Isuzu 5t Spec */}
              <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 text-center flex flex-col items-center justify-between">
                <div className="text-2xl filter drop-shadow">🚛</div>
                <div>
                  <div className="font-extrabold text-sm text-[#1C1A17]">Isuzu 5t (Ref)</div>
                  <div className="text-[11px] text-[#7A7264] mt-0.5 font-medium">Sovutgichli termoboks</div>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full">
                  🌡️ +2°C dan -18°C
                </span>
              </div>

              {/* Kamaz 20t Spec */}
              <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3.5 text-center flex flex-col items-center justify-between">
                <div className="text-2xl filter drop-shadow">🚚</div>
                <div>
                  <div className="font-extrabold text-sm text-[#1C1A17]">Kamaz 20t (Katta)</div>
                  <div className="text-[11px] text-[#7A7264] mt-0.5 font-medium">Uzoq viloyatlararo fura</div>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-amber-50 text-amber-800 rounded-full">
                  📦 20 tonna sig'im
                </span>
              </div>
            </div>

            {/* Drivers & Escrow Badges */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* Driver 1 */}
              <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3 flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-[#E5DFD3] flex items-center justify-center text-sm font-bold text-[#443B2E]">
                  DY
                </div>
                <div>
                  <div className="text-xs font-bold text-[#1C1A17]">Davron Haydovchi</div>
                  <div className="text-[11px] text-amber-600 font-semibold flex items-center space-x-0.5">
                    <span>★</span>
                    <span>4.9 (42 safar)</span>
                  </div>
                </div>
              </div>

              {/* Driver 2 */}
              <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-3 flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-[#E5DFD3] flex items-center justify-center text-sm font-bold text-[#443B2E]">
                  JK
                </div>
                <div>
                  <div className="text-xs font-bold text-[#1C1A17]">Jasur Karimov</div>
                  <div className="text-[11px] text-amber-600 font-semibold flex items-center space-x-0.5">
                    <span>★</span>
                    <span>4.8 (28 safar)</span>
                  </div>
                </div>
              </div>

              {/* Escrow Guarantee Badge */}
              <div className="bg-[#EBF3ED] border border-[#CDE3D3] rounded-2xl p-3 flex items-center space-x-2.5">
                <div className="w-8 h-8 rounded-full bg-[#2F6B42] text-white flex items-center justify-center text-sm">
                  🛡️
                </div>
                <div>
                  <div className="text-xs font-extrabold text-[#1B4D2C]">Xavfsiz to'lov</div>
                  <div className="text-[10px] text-[#2F6B42] font-semibold">100% Escrow kafolati</div>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-5 pt-3 border-t border-[#F0ECE4] flex items-center justify-between text-xs text-[#736C61]">
            <span>6 xonali topshirish kodi orqali pul haydovchiga beriladi</span>
            <a href="https://t.me/HosilBozorBot" target="_blank" rel="noreferrer" className="font-bold text-[#2F6B42] hover:underline">
              Haydovchi sifatida ulanish &rarr;
            </a>
          </div>
        </div>
      </section>

      {/* 5. SECTION 3: REGIONAL SOURCING MAP & ANALYTICS */}
      <section className="bg-white border border-[#E8E4DB] rounded-3xl p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-xl sm:text-2xl font-extrabold text-[#1C1A17]">
              Mintaqaviy manbalar va tahlillar (Sourcing Map)
            </h3>
            <p className="text-xs sm:text-sm text-[#787165] mt-1">
              O'zbekiston viloyatlari bo'yicha faol hosil yig'imi, ulgurji narxlar dinamikasi va haftalik hajm statistikasi
            </p>
          </div>

          {/* Region Tabs */}
          <div className="flex flex-wrap gap-2">
            {[
              { id: "fargona", label: "Farg'ona vodiysi" },
              { id: "toshkent", label: "Toshkent viloyati" },
              { id: "samarqand", label: "Samarqand" },
              { id: "surxondaryo", label: "Surxondaryo" },
            ].map((r) => (
              <button
                key={r.id}
                onClick={() => setSelectedRegion(r.id)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-bold transition ${
                  selectedRegion === r.id
                    ? "bg-[#2F6B42] text-white shadow-sm"
                    : "bg-[#F3EFE8] text-[#554D41] hover:bg-[#EAE4D9]"
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Interactive Uzbekistan Vector Sourcing Visual Map */}
          <div className="lg:col-span-2 bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-6 relative overflow-hidden flex flex-col justify-between min-h-[300px]">
            <div className="flex items-center justify-between text-xs text-[#736C61] font-semibold mb-4">
              <span>🗺️ O'zbekiston Qishloq Xo'jaligi Xaritasi</span>
              <span className="flex items-center space-x-3">
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42]"></span>
                  <span>Faol hududlar</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                  <span>Yuqori hosil</span>
                </span>
              </span>
            </div>

            {/* Stylized Uzbekistan Region Node Map */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 my-auto py-2">
              <div className={`p-4 rounded-xl border transition ${selectedRegion === "fargona" ? "bg-white border-[#2F6B42] shadow-md ring-2 ring-[#2F6B42]/20" : "bg-white/80 border-[#E5E0D5]"}`}>
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Farg'ona</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42] animate-pulse"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Uzum, Anor, Pomidor</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">12 400 t hosil</div>
              </div>

              <div className={`p-4 rounded-xl border transition ${selectedRegion === "toshkent" ? "bg-white border-[#2F6B42] shadow-md ring-2 ring-[#2F6B42]/20" : "bg-white/80 border-[#E5E0D5]"}`}>
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Toshkent vil.</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Bodring, Ko'katlar, Pomidor</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">18 200 t hosil</div>
              </div>

              <div className={`p-4 rounded-xl border transition ${selectedRegion === "samarqand" ? "bg-white border-[#2F6B42] shadow-md ring-2 ring-[#2F6B42]/20" : "bg-white/80 border-[#E5E0D5]"}`}>
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Samarqand</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42]"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Kartoshka, Piyoz, Olma</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">24 800 t hosil</div>
              </div>

              <div className={`p-4 rounded-xl border transition ${selectedRegion === "surxondaryo" ? "bg-white border-[#2F6B42] shadow-md ring-2 ring-[#2F6B42]/20" : "bg-white/80 border-[#E5E0D5]"}`}>
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Surxondaryo</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42]"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Erta pishar hosil, Anor</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">9 600 t hosil</div>
              </div>

              <div className="p-4 rounded-xl bg-white/80 border border-[#E5E0D5]">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Buxoro & Xorazm</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-gray-300"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Qovun, Tarvuz, Sabzi</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">15 100 t hosil</div>
              </div>

              <div className="p-4 rounded-xl bg-white/80 border border-[#E5E0D5]">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-[#1C1A17]">Andijon</span>
                  <span className="w-2.5 h-2.5 rounded-full bg-[#2F6B42]"></span>
                </div>
                <div className="text-xs text-[#736C61] mt-1">Gilos, O'rik, Shaftoli</div>
                <div className="text-sm font-black text-[#2F6B42] mt-2">8 900 t hosil</div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-[#EAE4D9] flex items-center justify-between text-xs text-[#787165]">
              <span>Viloyatlar bo'yicha to'g'ridan-to'g'ri fermerlar bazasi mavjud</span>
              <span className="font-bold text-[#2F6B42]">Jami: 89 000 tonna taklif</span>
            </div>
          </div>

          {/* Wholesale Prices & Weekly Volume Trend Charts */}
          <div className="space-y-4">
            {/* Price Chart Card */}
            <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-extrabold text-[#1C1A17]">
                  O'rtacha ulgurji narx dinamikasi
                </span>
                <span className="text-[11px] font-bold text-[#2F6B42] bg-[#EAF3ED] px-2 py-0.5 rounded">
                  Haftalik +3.4%
                </span>
              </div>
              <div className="text-2xl font-black text-[#1C1A17]">
                5 450 <span className="text-xs font-normal text-[#736C61]">so'm/kg indeks</span>
              </div>
              {/* Minimalist SVG Sparkline */}
              <div className="mt-3 h-14 w-full">
                <svg className="w-full h-full" viewBox="0 0 200 40" preserveAspectRatio="none">
                  <path
                    d="M 0 32 Q 30 18, 60 25 T 120 15 T 160 8 T 200 4"
                    fill="none"
                    stroke="#2F6B42"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  />
                  <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#2F6B42" stopOpacity="0.2" />
                    <stop offset="100%" stopColor="#2F6B42" stopOpacity="0" />
                  </linearGradient>
                  <path
                    d="M 0 32 Q 30 18, 60 25 T 120 15 T 160 8 T 200 4 L 200 40 L 0 40 Z"
                    fill="url(#grad)"
                  />
                </svg>
              </div>
              <div className="flex justify-between text-[10px] text-[#8C8476] mt-1 font-semibold">
                <span>Dush</span>
                <span>Sesh</span>
                <span>Chor</span>
                <span>Pay</span>
                <span>Jum</span>
                <span>Shan</span>
                <span>Yak</span>
              </div>
            </div>

            {/* Weekly Volume Bar Chart */}
            <div className="bg-[#FAF8F5] border border-[#EBE7DF] rounded-2xl p-5">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-extrabold text-[#1C1A17]">
                  Haftalik yetkazilgan hajm
                </span>
                <span className="text-xs font-bold text-[#2F6B42]">
                  1 700 t / hafta
                </span>
              </div>
              <div className="flex items-end justify-between h-16 pt-2 space-x-2">
                {[
                  { day: "D", val: 40 },
                  { day: "S", val: 65 },
                  { day: "C", val: 55 },
                  { day: "P", val: 80 },
                  { day: "J", val: 70 },
                  { day: "S", val: 95 },
                  { day: "Y", val: 50 },
                ].map((b, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1">
                    <div
                      className="w-full bg-[#2F6B42]/80 hover:bg-[#2F6B42] transition rounded-t-md"
                      style={{ height: `${b.val}%` }}
                    ></div>
                    <span className="text-[10px] text-[#8C8476] font-bold">{b.day}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. SECTION 4: PROFESSIONAL MODERN FOOTER */}
      <footer className="wooden-nav rounded-3xl p-8 sm:p-10 shadow-lg border border-[#D5CAB8] text-[#362D22]">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8 pb-8 border-b border-[#D8CEBE]">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-[#3F7C4E] flex items-center justify-center text-white text-base shadow-sm">
                🌿
              </div>
              <span className="font-extrabold text-2xl tracking-tight text-[#2B231A]">
                HosilBozor
              </span>
            </div>
            <p className="text-xs text-[#5C5243] max-w-sm leading-relaxed">
              O'zbekistonning birinchi raqamli agrar birjasi. Fermerlar, ulgurji xaridorlar va haydovchilarni to'g'ridan-to'g'ri bog'lovchi shaffof ekotizim.
            </p>
            {/* Telegram Bot & Mobile App Badges */}
            <div className="flex flex-wrap items-center gap-2.5 pt-2">
              <a
                href="https://t.me/HosilBozorBot"
                target="_blank"
                rel="noreferrer"
                className="bg-[#2AABEE] text-white px-4 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-[#229ED9] transition shadow-sm text-xs group"
                title="@HosilBozorBot Telegram boti"
              >
                <svg className="w-5 h-5 fill-white group-hover:scale-110 transition-transform" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.37.74-.56 2.92-1.27 4.86-2.11 5.83-2.52 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06-.01.17-.02.27z"/>
                </svg>
                <div>
                  <div className="text-[9px] uppercase tracking-wider text-blue-100">Telegram Bot</div>
                  <div className="font-extrabold text-[12px] leading-tight">@HosilBozorBot</div>
                </div>
              </a>
              <a
                href="#"
                className="bg-[#2B231A] text-white px-3.5 py-2 rounded-xl flex items-center space-x-2 hover:bg-black transition shadow-sm text-xs"
              >
                <span>🍏</span>
                <div>
                  <div className="text-[9px] uppercase tracking-wider text-gray-300">Yuklab oling</div>
                  <div className="font-bold text-[11px] leading-tight">App Store</div>
                </div>
              </a>
              <a
                href="#"
                className="bg-[#2B231A] text-white px-3.5 py-2 rounded-xl flex items-center space-x-2 hover:bg-black transition shadow-sm text-xs"
              >
                <span>🤖</span>
                <div>
                  <div className="text-[9px] uppercase tracking-wider text-gray-300">Yuklab oling</div>
                  <div className="font-bold text-[11px] leading-tight">Google Play</div>
                </div>
              </a>
            </div>
          </div>

          {/* Links Column 1: Fermerlarga */}
          <div className="space-y-3">
            <h4 className="font-extrabold text-sm text-[#241C13]">Fermerlarga</h4>
            <ul className="space-y-2 text-xs text-[#554B3E]">
              <li><a href="https://t.me/HosilBozorBot" target="_blank" rel="noreferrer" className="hover:text-black transition">Telegram Botda e'lon berish</a></li>
              <li><a href="/#narxlar" className="hover:text-black transition">Kunlik bozor narxlari</a></li>
              <li><a href="/listings" className="hover:text-black transition">Mavjud hosil monitoringi</a></li>
              <li><a href="/#talablar" className="hover:text-black transition">Teskari auksion takliflari</a></li>
            </ul>
          </div>

          {/* Links Column 2: Xaridorlarga */}
          <div className="space-y-3">
            <h4 className="font-extrabold text-sm text-[#241C13]">Xaridorlarga</h4>
            <ul className="space-y-2 text-xs text-[#554B3E]">
              <li><a href="/listings" className="hover:text-black transition">Ulgurji hosil xaridi</a></li>
              <li><a href="/demand" className="hover:text-black transition">Talab e'lon qilish</a></li>
              <li><a href="/#yetkazib-berish" className="hover:text-black transition">Escrow xavfsiz to'lov</a></li>
              <li><a href="/admin" className="hover:text-black transition">Tasdiqlangan fermerlar</a></li>
            </ul>
          </div>

          {/* Links Column 3: Logistika & Hujjatlar */}
          <div className="space-y-3">
            <h4 className="font-extrabold text-sm text-[#241C13]">Logistika & Huquqiy</h4>
            <ul className="space-y-2 text-xs text-[#554B3E]">
              <li><a href="/#yetkazib-berish" className="hover:text-black transition">Yo'ldosh yuklar logistikasi</a></li>
              <li><a href="https://t.me/HosilBozorBot" target="_blank" rel="noreferrer" className="hover:text-black transition">Haydovchilar reytingi</a></li>
              <li><a href="#" className="hover:text-black transition">Foydalanish shartlari</a></li>
              <li><a href="#" className="hover:text-black transition">Maxfiylik siyosati</a></li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom: Payment Icons, Language, Copyright */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[#5C5243]">
          <div className="flex items-center space-x-3">
            <span className="font-bold text-[#3B3224]">Xavfsiz To'lov Tizimlari:</span>
            <span className="px-2.5 py-1 bg-white/70 rounded-lg font-bold text-[#201A12] border border-[#DDD3C2]">
              UZCARD
            </span>
            <span className="px-2.5 py-1 bg-white/70 rounded-lg font-bold text-[#201A12] border border-[#DDD3C2]">
              HUMO
            </span>
            <span className="px-2.5 py-1 bg-white/70 rounded-lg font-bold text-[#201A12] border border-[#DDD3C2]">
              Payme
            </span>
            <span className="px-2.5 py-1 bg-white/70 rounded-lg font-bold text-[#201A12] border border-[#DDD3C2]">
              Click
            </span>
          </div>

          <div className="flex items-center space-x-4">
            <select className="bg-white/70 border border-[#D5CAB8] rounded-xl px-3 py-1.5 font-bold text-xs text-[#2F261B] outline-none">
              <option value="uz_latn">🇺🇿 O'zbekcha (Lotin)</option>
              <option value="uz_cyrl">🇺🇿 Ўзбекча (Кирилл)</option>
              <option value="ru">🇷🇺 Русский</option>
            </select>
            <span className="font-medium">
              &copy; 2026 HosilBozor. Barcha huquqlar himoyalangan.
            </span>
          </div>
        </div>
      </footer>

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

      {/* Demand Offer Modal */}
      {activeOfferDemand && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl relative border border-[#E8E4DB]">
            <button
              onClick={() => setActiveOfferDemand(null)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              &times;
            </button>

            {!offerSent ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-[#FAF8F5] flex items-center justify-center text-xl border border-[#EBE7DF]">
                    ⚖️
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-[#1C1A17]">
                      Fermer Narx Taklifi
                    </h3>
                    <p className="text-xs text-gray-500">{activeOfferDemand}</p>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-700 mb-1">
                    Taklif qilinadigan narx (so'm/kg):
                  </label>
                  <input
                    type="number"
                    value={offerPrice}
                    onChange={(e) => setOfferPrice(e.target.value)}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl font-bold text-base text-[#2F6B42] focus:ring-2 focus:ring-[#2F6B42] focus:outline-none"
                  />
                  <span className="text-[11px] text-gray-400 mt-1 block">
                    Xaridor auksion yakunida eng maqbul taklifni tanlaydi
                  </span>
                </div>

                <button
                  onClick={() => setOfferSent(true)}
                  className="w-full py-3 rounded-xl bg-[#2F6B42] hover:bg-[#285D39] text-white font-bold text-sm shadow-md transition"
                >
                  Taklifni Yuborish (Teskari Auksion)
                </button>
              </div>
            ) : (
              <div className="text-center py-4 space-y-3">
                <div className="w-14 h-14 bg-[#E8F2EC] text-[#2F6B42] rounded-full flex items-center justify-center mx-auto text-2xl font-black">
                  ✓
                </div>
                <h3 className="font-extrabold text-lg text-[#1C1A17]">
                  Taklif muvaffaqiyatli yuborildi!
                </h3>
                <p className="text-xs text-gray-500">
                  {offerPrice} so'm/kg taklifingiz xaridorga yetkazildi. Natija bot orqali bildiriladi.
                </p>
                <button
                  onClick={() => setActiveOfferDemand(null)}
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
