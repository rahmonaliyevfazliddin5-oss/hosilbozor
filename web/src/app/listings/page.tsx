"use client";

import React, { useState, useEffect } from "react";
import { getListings, Listing } from "@/lib/api";

const SAMPLE_LISTINGS: Listing[] = [
  {
    id: "l-101",
    farmer_id: "f-1",
    crop_id: "c-1",
    quantity: 12000,
    min_order_quantity: 500,
    price_per_unit: 7200,
    quality_grade: "premium",
    status: "active",
    description: "Issiqxonada yetishtirilgan sifatli pushti pomidor. Qutilarga terilgan, eksportbop.",
    crop: { id: "c-1", slug: "pomidor", name_uz: "Pushti Pomidor", name_ru: "Розовые томаты", category: "vegetables", standard_unit: "kg" },
    farmer: { id: "f-1", full_name: "Rustam Yoqubov", farm_name: "Chinoz Agrogurux", rating: 4.9 },
    distance_km: 18,
  },
  {
    id: "l-102",
    farmer_id: "f-2",
    crop_id: "c-2",
    quantity: 8500,
    min_order_quantity: 300,
    price_per_unit: 4400,
    quality_grade: "standard",
    status: "active",
    description: "Yangiyo'l shirin bodringi. Yangi uzilgan, do'kon va restoranlar uchun qulay narx.",
    crop: { id: "c-2", slug: "bodring", name_uz: "Yangiyo'l Bodringi", name_ru: "Огурцы Янгиюль", category: "vegetables", standard_unit: "kg" },
    farmer: { id: "f-2", full_name: "Sardor Ikromov", farm_name: "Yangiyo'l Hosili", rating: 4.8 },
    distance_km: 25,
  },
  {
    id: "l-103",
    farmer_id: "f-3",
    crop_id: "c-3",
    quantity: 25000,
    min_order_quantity: 1000,
    price_per_unit: 3400,
    quality_grade: "standard",
    status: "active",
    description: "Samarqand qizil kartoshkasi. Qishki saqlash uchun juda mos, quruq ombordan.",
    crop: { id: "c-3", slug: "kartoshka", name_uz: "Qizil Kartoshka (Gala)", name_ru: "Картофель Гала", category: "vegetables", standard_unit: "kg" },
    farmer: { id: "f-3", full_name: "Bahodir Mirzayev", farm_name: "Zarafshon Agro", rating: 5.0 },
    distance_km: 260,
  },
  {
    id: "l-104",
    farmer_id: "f-4",
    crop_id: "c-4",
    quantity: 5000,
    min_order_quantity: 200,
    price_per_unit: 14500,
    quality_grade: "premium",
    status: "active",
    description: "Farg'ona vodiysining shirin qora kishmish uzumi. Maxsus qutilarda saqlangan.",
    crop: { id: "c-4", slug: "uzum", name_uz: "Qora Kishmish Uzum", name_ru: "Виноград Кишмиш", category: "fruits", standard_unit: "kg" },
    farmer: { id: "f-4", full_name: "Akmal Qosimov", farm_name: "Quva Bog'lari", rating: 4.9 },
    distance_km: 310,
  },
  {
    id: "l-105",
    farmer_id: "f-5",
    crop_id: "c-5",
    quantity: 40000,
    min_order_quantity: 2000,
    price_per_unit: 2100,
    quality_grade: "standard",
    status: "active",
    description: "Zarafshon sariq piyozi. Quruq, qobig'i butun, uzoq masofaga tashishga chidamli.",
    crop: { id: "c-5", slug: "piyoz", name_uz: "Sariq Piyoz (Eksportbop)", name_ru: "Лук репчатый", category: "vegetables", standard_unit: "kg" },
    farmer: { id: "f-5", full_name: "Nodir Xoliqov", farm_name: "Nurota Dalalari", rating: 4.7 },
    distance_km: 380,
  },
  {
    id: "l-106",
    farmer_id: "f-6",
    crop_id: "c-6",
    quantity: 15000,
    min_order_quantity: 500,
    price_per_unit: 9500,
    quality_grade: "premium",
    status: "active",
    description: "Namangan qizil olmasi (Simirenko va Besh yulduz). Shirin, sersuv, tozalangan.",
    crop: { id: "c-6", slug: "olma", name_uz: "Qizil Bog' Olmasi", name_ru: "Яблоки сортовые", category: "fruits", standard_unit: "kg" },
    farmer: { id: "f-6", full_name: "Shavkat To'rayev", farm_name: "Chortoq Mevazori", rating: 4.8 },
    distance_km: 290,
  },
];

export default function ListingsPage() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [gradeFilter, setGradeFilter] = useState("all");
  const [sortBy, setSortBy] = useState("price_asc");

  // Purchase Escrow Modal state
  const [selectedListing, setSelectedListing] = useState<Listing | null>(null);
  const [orderQuantity, setOrderQuantity] = useState<number>(500);
  const [isOrdering, setIsOrdering] = useState(false);
  const [orderSuccess, setOrderSuccess] = useState<any | null>(null);

  useEffect(() => {
    async function fetchListings() {
      try {
        const res = await getListings();
        if (res.items && res.items.length > 0) {
          setListings(res.items);
        } else {
          setListings(SAMPLE_LISTINGS);
        }
      } catch {
        setListings(SAMPLE_LISTINGS);
      } finally {
        setLoading(false);
      }
    }
    fetchListings();
  }, []);

  // Filter and sort listings
  const filteredListings = listings
    .filter((item) => {
      const matchSearch =
        item.crop?.name_uz.toLowerCase().includes(search.toLowerCase()) ||
        item.description?.toLowerCase().includes(search.toLowerCase()) ||
        item.farmer?.full_name.toLowerCase().includes(search.toLowerCase());

      const matchGrade = gradeFilter === "all" || item.quality_grade === gradeFilter;
      return matchSearch && matchGrade;
    })
    .sort((a, b) => {
      if (sortBy === "price_asc") return a.price_per_unit - b.price_per_unit;
      if (sortBy === "price_desc") return b.price_per_unit - a.price_per_unit;
      if (sortBy === "qty_desc") return b.quantity - a.quantity;
      return 0;
    });

  const handleOpenOrder = (item: Listing) => {
    setSelectedListing(item);
    setOrderQuantity(item.min_order_quantity || 100);
    setOrderSuccess(null);
  };

  const handleExecuteEscrowOrder = async () => {
    if (!selectedListing) return;
    setIsOrdering(true);

    // Simulate real order checkout and escrow holding
    setTimeout(() => {
      const productTotal = orderQuantity * selectedListing.price_per_unit;
      const escrowFee = Math.round(productTotal * 0.02);
      const totalAmount = productTotal + escrowFee;

      setOrderSuccess({
        order_id: `ORD-${Math.floor(100000 + Math.random() * 900000)}`,
        crop_name: selectedListing.crop?.name_uz,
        farmer_name: selectedListing.farmer?.full_name,
        quantity: orderQuantity,
        total_amount: totalAmount,
        escrow_status: "PAID_ESCROW",
        pickup_code: "482910",
        delivery_code: "719342",
      });
      setIsOrdering(false);
    }, 1200);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Title & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 flex items-center space-x-2">
            <span>🛒</span>
            <span>Ulgurji Hosil Bozori</span>
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Fermerlar dalasidan to'g'ridan-to'g'ri yangi va saralangan agrar mahsulotlar
          </p>
        </div>

        {/* Telegram Farmer CTA */}
        <a
          href="https://t.me/HosilBozorBot"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center px-4 py-2.5 rounded-xl bg-emerald-600 text-white text-sm font-bold hover:bg-emerald-700 shadow-sm transition"
        >
          <span>👨‍🌾 Fermermisiz? Botda e'lon berish</span>
        </a>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div className="lg:col-span-2">
          <label className="block text-xs font-semibold text-gray-600 mb-1">
            Qidiruv (Mahsulot yoki fermer):
          </label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Masalan: pomidor, bodring, Toshkent..."
            className="w-full px-3.5 py-2 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
        </div>

        {/* Quality Grade Filter */}
        <div>
          <label className="block text-xs font-semibold text-gray-600 mb-1">
            Navi (Sifati):
          </label>
          <select
            value={gradeFilter}
            onChange={(e) => setGradeFilter(e.target.value)}
            className="w-full px-3.5 py-2 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
          >
            <option value="all">Barcha navlar</option>
            <option value="premium">Birinchi nav (Premium)</option>
            <option value="standard">Standart</option>
            <option value="processing">Qayta ishlashga</option>
          </select>
        </div>

        {/* Sort */}
        <div>
          <label className="block text-xs font-semibold text-gray-600 mb-1">
            Saralash:
          </label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="w-full px-3.5 py-2 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
          >
            <option value="price_asc">Narx: Arzondan qimmatga</option>
            <option value="price_desc">Narx: Qimmatdan arzonga</option>
            <option value="qty_desc">Hosil miqdori bo'yicha</option>
          </select>
        </div>
      </div>

      {/* Listings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredListings.map((item) => (
          <div
            key={item.id}
            className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg transition-all flex flex-col justify-between"
          >
            <div>
              {/* Header */}
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700">
                    {item.quality_grade === "premium" ? "🌟 Birinchi nav" : "Standart"}
                  </span>
                  <h3 className="text-xl font-bold text-gray-900 mt-2">
                    {item.crop?.name_uz || "Hosil"}
                  </h3>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-extrabold text-emerald-700">
                    {Number(item.price_per_unit).toLocaleString()}
                  </div>
                  <div className="text-xs text-gray-400">so'm / kg</div>
                </div>
              </div>

              {/* Description */}
              <p className="text-sm text-gray-600 mt-3 line-clamp-2">
                {item.description || "Yangi pishgan saralangan hosil."}
              </p>

              {/* Quantities */}
              <div className="mt-4 pt-4 border-t border-gray-100 grid grid-cols-2 gap-2 text-xs text-gray-500">
                <div>
                  <span className="text-gray-400">Mavjud hajm:</span>
                  <div className="font-bold text-gray-800 text-sm">
                    {Number(item.quantity).toLocaleString()} kg ({(item.quantity / 1000).toFixed(1)} t)
                  </div>
                </div>
                <div>
                  <span className="text-gray-400">Min. buyurtma:</span>
                  <div className="font-bold text-gray-800 text-sm">
                    {Number(item.min_order_quantity).toLocaleString()} kg
                  </div>
                </div>
              </div>

              {/* Farmer Info */}
              <div className="mt-4 p-3 bg-gray-50 rounded-xl flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-gray-800 flex items-center space-x-1">
                    <span>{item.farmer?.full_name}</span>
                    <span className="text-emerald-600" title="Tasdiqlangan fermer">✓</span>
                  </div>
                  <div className="text-gray-500">{item.farmer?.farm_name || "Fermer xo'jaligi"}</div>
                </div>
                <div className="text-amber-500 font-bold flex items-center space-x-1">
                  <span>★</span>
                  <span>{item.farmer?.rating || 4.9}</span>
                </div>
              </div>
            </div>

            {/* Escrow Buy CTA */}
            <div className="mt-6">
              <button
                onClick={() => handleOpenOrder(item)}
                className="w-full py-3 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm transition shadow-sm flex items-center justify-center space-x-2"
              >
                <span>🛡️ Escrow orqali buyurtma berish</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Escrow Purchase Modal */}
      {selectedListing && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl relative">
            <button
              onClick={() => setSelectedListing(null)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              &times;
            </button>

            {!orderSuccess ? (
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center text-xl">
                    🌾
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">
                      Escrow Xavfsiz Buyurtmasi
                    </h3>
                    <p className="text-xs text-gray-500">
                      Mablag' hosil qabul qilinmaguncha platformada muzlatiladi
                    </p>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-2xl space-y-2 text-sm mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Mahsulot:</span>
                    <span className="font-bold text-gray-900">
                      {selectedListing.crop?.name_uz}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Fermer:</span>
                    <span className="font-semibold text-gray-800">
                      {selectedListing.farmer?.full_name} (✓ Tasdiqlangan)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Birlik narxi:</span>
                    <span className="font-bold text-emerald-700">
                      {Number(selectedListing.price_per_unit).toLocaleString()} so'm / kg
                    </span>
                  </div>
                </div>

                {/* Desired quantity input */}
                <div className="mb-6">
                  <label className="block text-xs font-semibold text-gray-700 mb-2">
                    Xarid hajmi (kg):
                  </label>
                  <input
                    type="number"
                    min={selectedListing.min_order_quantity}
                    max={selectedListing.quantity}
                    value={orderQuantity}
                    onChange={(e) => setOrderQuantity(Number(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl text-base font-bold focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                  <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>Min: {selectedListing.min_order_quantity} kg</span>
                    <span>Mavjud: {Number(selectedListing.quantity).toLocaleString()} kg</span>
                  </div>
                </div>

                {/* Calculation summary */}
                <div className="border-t border-gray-200 pt-4 space-y-2 text-sm mb-6">
                  <div className="flex justify-between text-gray-600">
                    <span>Hosil qiymati:</span>
                    <span>{(orderQuantity * selectedListing.price_per_unit).toLocaleString()} so'm</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Escrow kafolat to'lovi (2%):</span>
                    <span>{(Math.round(orderQuantity * selectedListing.price_per_unit * 0.02)).toLocaleString()} so'm</span>
                  </div>
                  <div className="flex justify-between text-base font-extrabold text-gray-900 pt-2 border-t border-gray-100">
                    <span>Jami to'lov (Escrow ushlovi):</span>
                    <span className="text-emerald-700">
                      {(Math.round(orderQuantity * selectedListing.price_per_unit * 1.02)).toLocaleString()} so'm
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleExecuteEscrowOrder}
                  disabled={isOrdering || orderQuantity < selectedListing.min_order_quantity}
                  className="w-full py-3.5 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white font-bold text-sm transition shadow-md flex items-center justify-center space-x-2"
                >
                  {isOrdering ? (
                    <span>Qayta ishlanmoqda...</span>
                  ) : (
                    <span>💳 To'lovni amalga oshirish (Mock Escrow)</span>
                  )}
                </button>
              </div>
            ) : (
              /* Success screen */
              <div className="text-center py-4 space-y-4">
                <div className="w-16 h-16 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto text-3xl">
                  ✓
                </div>
                <h3 className="text-xl font-bold text-gray-900">
                  Escrow To'lovi Muvaffaqiyatli O'tkazildi!
                </h3>
                <p className="text-xs text-gray-500 max-w-sm mx-auto">
                  {orderSuccess.total_amount.toLocaleString()} so'm platforma hisobida muzlatildi.
                  Hosil yuklangach va yetib borgachgina pul fermerga beriladi.
                </p>

                <div className="bg-gray-50 p-4 rounded-2xl text-left text-xs space-y-2 mt-4">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Buyurtma raqami:</span>
                    <span className="font-mono font-bold text-gray-800">{orderSuccess.order_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Holat:</span>
                    <span className="font-bold text-emerald-700">PAID_ESCROW (Muzlatilgan)</span>
                  </div>
                  <div className="flex justify-between pt-2 border-t border-gray-200">
                    <span className="text-gray-600">Topshirish kodi (Haydovchi uchun):</span>
                    <span className="font-mono font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">
                      {orderSuccess.delivery_code}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => setSelectedListing(null)}
                  className="w-full mt-4 py-3 rounded-xl bg-gray-900 text-white font-bold text-xs hover:bg-gray-800 transition"
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
