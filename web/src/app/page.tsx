"use client";

import React, { useState, useEffect } from "react";
import { getDailyPrices, MarketPrice } from "@/lib/api";

export default function HomePage() {
  const [prices, setPrices] = useState<MarketPrice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getDailyPrices();
        if (data && data.length > 0) {
          setPrices(data);
        } else {
          // Fallback realistic daily market benchmark prices
          setPrices([
            { id: "1", crop_id: "c1", market_name: "Qo'yliq ulgurji bozori (Toshkent)", min_price: 6500, max_price: 8500, avg_price: 7500, recorded_date: "2026-10-04", crop: { id: "c1", slug: "pomidor", name_uz: "Qizil Pomidor", name_ru: "Томаты", category: "vegetables", standard_unit: "kg" } },
            { id: "2", crop_id: "c2", market_name: "Parkent dehqon bozori", min_price: 4000, max_price: 5200, avg_price: 4600, recorded_date: "2026-10-04", crop: { id: "c2", slug: "bodring", name_uz: "Bodring (Orzu)", name_ru: "Огурцы", category: "vegetables", standard_unit: "kg" } },
            { id: "3", crop_id: "c3", market_name: "Samarqand Siyob bozori", min_price: 3200, max_price: 4100, avg_price: 3600, recorded_date: "2026-10-04", crop: { id: "c3", slug: "kartoshka", name_uz: "Qizil Kartoshka", name_ru: "Картофель", category: "vegetables", standard_unit: "kg" } },
            { id: "4", crop_id: "c4", market_name: "Farg'ona Markaziy dehqon bozori", min_price: 12000, max_price: 16000, avg_price: 14000, recorded_date: "2026-10-04", crop: { id: "c4", slug: "uzum", name_uz: "Qora Kishmish Uzum", name_ru: "Виноград Кишмиш", category: "fruits", standard_unit: "kg" } },
          ]);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-emerald-800 via-emerald-700 to-teal-900 rounded-3xl p-8 sm:p-14 text-white shadow-2xl relative overflow-hidden">
          <div className="relative z-10 max-w-3xl">
            <span className="inline-flex items-center px-3.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-200 border border-emerald-400/30 mb-6">
              🌾 O'zbekistonda 1-raqamli agrar birja va ekotizim
            </span>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              Fermer, Xaridor va Haydovchini bog'lovchi shaffof bozor
            </h1>
            <p className="mt-6 text-lg sm:text-xl text-emerald-100 font-normal leading-relaxed">
              O'rtakash dallollarsiz to'g'ridan-to'g'ri narxlar, xavfsiz escrow to'lovi hamda
              bo'sh qaytadigan yuk mashinalari logistikasini birlashtiruvchi zamonaviy agromarkaz.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href="/listings"
                className="px-6 py-3.5 rounded-xl bg-white text-emerald-800 font-bold hover:bg-emerald-50 transition shadow-lg text-sm sm:text-base flex items-center space-x-2"
              >
                <span>🛒 Hosil Sotib Olish</span>
              </a>
              <a
                href="/demand"
                className="px-6 py-3.5 rounded-xl bg-emerald-600/80 hover:bg-emerald-600 text-white font-bold transition border border-emerald-400/30 text-sm sm:text-base flex items-center space-x-2"
              >
                <span>📢 Talab E'lon Qilish (Auksion)</span>
              </a>
              <a
                href="https://t.me/HosilBozorBot"
                target="_blank"
                rel="noreferrer"
                className="px-6 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold transition shadow-lg text-sm sm:text-base flex items-center space-x-2"
              >
                <span>🤖 Fermer Boti (60 soniya)</span>
              </a>
            </div>
          </div>
          <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none text-9xl select-none pr-8 pb-4">
            🌾
          </div>
        </div>
      </section>

      {/* Live Market Price Intelligence Ticker */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center space-x-2">
              <span>📈</span>
              <span>Kunlik Bozor Narxlari Razvedkasi</span>
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              O'zbekiston yirik ulgurji bozorlaridagi real narxlar va "Bugun sotish foydalimi?" tahlili
            </p>
          </div>
          <a
            href="/listings"
            className="text-sm font-semibold text-emerald-700 hover:text-emerald-800"
          >
            Barchasini ko'rish &rarr;
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {prices.map((item) => {
            const spread = item.avg_price ? Math.round(((item.max_price - item.min_price) / item.avg_price) * 100) : 10;
            const isGoodToSell = spread < 25;

            return (
              <div
                key={item.id}
                className="bg-white border border-gray-200 rounded-2xl p-5 hover:border-emerald-300 transition hover:shadow-md"
              >
                <div className="flex items-start justify-between">
                  <div className="font-bold text-lg text-gray-900">
                    {item.crop?.name_uz || "Mahsulot"}
                  </div>
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                      isGoodToSell
                        ? "bg-emerald-100 text-emerald-800"
                        : "bg-amber-100 text-amber-800"
                    }`}
                  >
                    {isGoodToSell ? "🟢 Sotish foydali" : "🟡 Narx tebranmoqda"}
                  </span>
                </div>
                <div className="text-xs text-gray-500 mt-1 truncate">
                  📍 {item.market_name}
                </div>
                <div className="mt-4 pt-3 border-t border-gray-100 flex items-baseline justify-between">
                  <div>
                    <span className="text-xs text-gray-400">O'rtacha narx:</span>
                    <div className="text-xl font-extrabold text-emerald-700">
                      {Number(item.avg_price).toLocaleString()} <span className="text-xs font-normal">so'm/kg</span>
                    </div>
                  </div>
                  <div className="text-right text-xs text-gray-500">
                    <div>Min: {Number(item.min_price).toLocaleString()}</div>
                    <div>Maks: {Number(item.max_price).toLocaleString()}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 3 User Ecosystem Roles */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-2">
          HosilBozor Ekotizimi Qanday Ishlaydi?
        </h2>
        <p className="text-center text-gray-500 max-w-2xl mx-auto mb-10 text-sm">
          Har bir ishtirokchi uchun qulay kanallar va kafolatlangan manfaat
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Farmer Card */}
          <div className="bg-white rounded-2xl border border-gray-200 p-7 hover:border-emerald-500 transition shadow-sm">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-2xl mb-5">
              👨‍🌾
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Fermerlar Uchun</h3>
            <p className="text-gray-600 text-sm mb-4 leading-relaxed">
              Dallollarga arzon sotmang! Telegram bot orqali 60 soniyada hosilingizni e'lon qiling,
              kunlik bozor narxlarini kuzating va to'g'ridan-to'g'ri ulgurji xaridorlardan buyurtma oling.
            </p>
            <ul className="text-xs text-gray-500 space-y-2 mb-6">
              <li>✅ Telegram bot va Mini App (offline qo'llab-quvvatlash)</li>
              <li>✅ Rasmlarni avtomatik kichraytirish (kam trafik)</li>
              <li>✅ 100% kafolatlangan Escrow to'lovi</li>
            </ul>
            <a
              href="https://t.me/HosilBozorBot"
              target="_blank"
              rel="noreferrer"
              className="inline-block text-xs font-bold text-emerald-700 hover:underline"
            >
              Botda e'lon berish &rarr;
            </a>
          </div>

          {/* Buyer Card */}
          <div className="bg-white rounded-2xl border border-gray-200 p-7 hover:border-blue-500 transition shadow-sm">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-2xl mb-5">
              🏢
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Ulgurji Xaridorlar Uchun</h3>
            <p className="text-gray-600 text-sm mb-4 leading-relaxed">
              Restoran, supermarket yoki qayta ishlash korxonalari uchun to'g'ridan-to'g'ri daladan
              yangiligi va sifati kafolatlangan hosil. Yoki teskari auksionda talabingizni e'lon qiling!
            </p>
            <ul className="text-xs text-gray-500 space-y-2 mb-6">
              <li>✅ Qishloq va tumanlar bo'yicha geo-qidiruv</li>
              <li>✅ Teskari auksion (fermerlar narx taklif qiladi)</li>
              <li>✅ Nizo va sifat kafolati (Arbitraj himoyasi)</li>
            </ul>
            <a
              href="/listings"
              className="inline-block text-xs font-bold text-blue-700 hover:underline"
            >
              Hosil katalogini ochish &rarr;
            </a>
          </div>

          {/* Driver Card */}
          <div className="bg-white rounded-2xl border border-gray-200 p-7 hover:border-amber-500 transition shadow-sm">
            <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center text-2xl mb-5">
              🚛
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Haydovchilar Uchun</h3>
            <p className="text-gray-600 text-sm mb-4 leading-relaxed">
              Bo'sh qaytish safarlariga chek qo'ying! Mashinangiz turini (refrijerator, fura, gazel)
              ro'yxatdan o'tkazing va marshrutingiz bo'ylab yangi hosil yetkazib berish buyurtmalariga narx bering.
            </p>
            <ul className="text-xs text-gray-500 space-y-2 mb-6">
              <li>✅ Qaytish yo'lidagi yo'ldosh yuklarni birlashtirish</li>
              <li>✅ Masofa va narx hisoblagichi</li>
              <li>✅ Maxsus 6 raqamli topshirish kodi bilan xavfsiz to'lov</li>
            </ul>
            <a
              href="https://t.me/HosilBozorBot"
              target="_blank"
              rel="noreferrer"
              className="inline-block text-xs font-bold text-amber-700 hover:underline"
            >
              Haydovchi sifatida ulanish &rarr;
            </a>
          </div>
        </div>
      </section>

      {/* Escrow Guarantee Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-5">
            <div className="text-4xl">🛡️</div>
            <div>
              <h3 className="text-lg font-bold text-emerald-950">
                100% Xavfsiz Escrow Tranzaksiya Kafolati
              </h3>
              <p className="text-sm text-emerald-800 mt-1">
                Xaridor to'lagan pul HosilBozor platformasida xavfsiz muzlatiladi. Hosil yetib borgach
                va qabul qilingachgina fermer va haydovchiga to'liq o'tkaziladi. Sifat mos kelmasa — to'liq qaytariladi.
              </p>
            </div>
          </div>
          <a
            href="/listings"
            className="whitespace-nowrap px-6 py-3 rounded-xl bg-emerald-700 text-white font-bold hover:bg-emerald-800 transition text-sm"
          >
            Bozorga Kirish
          </a>
        </div>
      </section>
    </div>
  );
}
