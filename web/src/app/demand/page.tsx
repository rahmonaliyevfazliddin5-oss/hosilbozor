"use client";

import React, { useState, useEffect } from "react";
import { getDemands, DemandRequest } from "@/lib/api";

const SAMPLE_DEMANDS: DemandRequest[] = [
  {
    id: "d-201",
    buyer_id: "b-1",
    crop_id: "c-1",
    target_quantity: 50000,
    max_price_per_unit: 6800,
    status: "active",
    description: "Toshkent supermarketlar tarmog'i uchun sifatli issiqxona pushti pomidori. Har haftada 10 tonnadan yetkazib berish sharti bilan.",
    crop: { id: "c-1", slug: "pomidor", name_uz: "Pushti Pomidor", name_ru: "Томаты", category: "vegetables", standard_unit: "kg" },
    buyer: { full_name: "Aziz Rahimov", company_name: "Oazis Fresh Ulgurji Savdo" },
    offers_count: 4,
  },
  {
    id: "d-202",
    buyer_id: "b-2",
    crop_id: "c-2",
    target_quantity: 30000,
    max_price_per_unit: 3800,
    status: "active",
    description: "Konserva va tuzlama ishlab chiqaruvchi korxona uchun bir xil o'lchamdagi bodring zarur. Shartnoma asosida.",
    crop: { id: "c-2", slug: "bodring", name_uz: "Bodring (Tuzlamabop)", name_ru: "Огурцы", category: "vegetables", standard_unit: "kg" },
    buyer: { full_name: "Farrux Saidov", company_name: "Afrosiyob Konserva MChJ" },
    offers_count: 6,
  },
  {
    id: "d-203",
    buyer_id: "b-3",
    crop_id: "c-3",
    target_quantity: 80000,
    max_price_per_unit: 3200,
    status: "active",
    description: "Qishki zaxira ombori uchun quruq qizil kartoshka. Minimal partiya 20 tonna.",
    crop: { id: "c-3", slug: "kartoshka", name_uz: "Kartoshka (Qishki saqlash)", name_ru: "Картофель", category: "vegetables", standard_unit: "kg" },
    buyer: { full_name: "Jahongir Aliyev", company_name: "Zarafshon Logistika Markazi" },
    offers_count: 8,
  },
  {
    id: "d-204",
    buyer_id: "b-4",
    crop_id: "c-4",
    target_quantity: 15000,
    max_price_per_unit: 13000,
    status: "active",
    description: "Eksport uchun tayyorlangan saralangan qora kishmish uzumi. Maxsus sovutgichli mashinada yetkazish zarur.",
    crop: { id: "c-4", slug: "uzum", name_uz: "Qora Kishmish Uzum", name_ru: "Виноград", category: "fruits", standard_unit: "kg" },
    buyer: { full_name: "Temur Mahmudov", company_name: "SilkRoad Agro Export" },
    offers_count: 2,
  },
];

export default function DemandPage() {
  const [demands, setDemands] = useState<DemandRequest[]>([]);
  const [loading, setLoading] = useState(true);

  // New Demand Modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [cropName, setCropName] = useState("Pomidor");
  const [targetQuantity, setTargetQuantity] = useState(10000);
  const [maxPrice, setMaxPrice] = useState(6500);
  const [demandDesc, setDemandDesc] = useState("");

  // Submit Offer Modal
  const [selectedDemand, setSelectedDemand] = useState<DemandRequest | null>(null);
  const [offerPrice, setOfferPrice] = useState<number>(6200);
  const [offerQuantity, setOfferQuantity] = useState<number>(5000);
  const [offerSubmitted, setOfferSubmitted] = useState(false);

  useEffect(() => {
    async function fetchDemands() {
      try {
        const res = await getDemands();
        if (res.items && res.items.length > 0) {
          setDemands(res.items);
        } else {
          setDemands(SAMPLE_DEMANDS);
        }
      } catch {
        setDemands(SAMPLE_DEMANDS);
      } finally {
        setLoading(false);
      }
    }
    fetchDemands();
  }, []);

  const handleCreateDemand = (e: React.FormEvent) => {
    e.preventDefault();
    const newDemand: DemandRequest = {
      id: `d-${Date.now()}`,
      buyer_id: "current-user",
      crop_id: "c-new",
      target_quantity: targetQuantity,
      max_price_per_unit: maxPrice,
      status: "active",
      description: demandDesc,
      crop: { id: "c-new", slug: "crop", name_uz: cropName, name_ru: cropName, category: "vegetables", standard_unit: "kg" },
      buyer: { full_name: "Mening Kompaniyam", company_name: "Ulgurji Xaridor" },
      offers_count: 0,
    };
    setDemands([newDemand, ...demands]);
    setShowCreateModal(false);
    setDemandDesc("");
  };

  const handleSubmitOffer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDemand) return;
    setOfferSubmitted(true);
    setTimeout(() => {
      // Increment offer count
      setDemands(demands.map(d => d.id === selectedDemand.id ? { ...d, offers_count: d.offers_count + 1 } : d));
      setSelectedDemand(null);
      setOfferSubmitted(false);
    }, 1000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header & CTA */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 flex items-center space-x-2">
            <span>📢</span>
            <span>Talablar & Teskari Auksion Doskasi</span>
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Ulgurji xaridorlar va korxonalar talab qo'yadi — fermerlar o'z hosiliga eng qulay narx taklif qiladi
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm transition shadow-md flex items-center space-x-2 self-start md:self-auto"
        >
          <span>➕ Talab E'lon Qilish (Xaridor)</span>
        </button>
      </div>

      {/* Explainer card */}
      <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="text-3xl">⚖️</div>
          <div>
            <h4 className="font-bold text-blue-900 text-sm sm:text-base">
              Teskari auksion qanday ishlaydi?
            </h4>
            <p className="text-xs text-blue-700 mt-0.5">
              Xaridor hosil miqdori va eng yuqori sotib olish narxini belgilaydi. Fermerlar raqobatlashib
              arzonroq yoki sifatliroq taklif beradi. Xaridor eng ma'qul taklifni qabul qilib, escrowga to'laydi.
            </p>
          </div>
        </div>
      </div>

      {/* Demands List */}
      <div className="space-y-4">
        {demands.map((demand) => (
          <div
            key={demand.id}
            className="bg-white border border-gray-200 rounded-2xl p-6 hover:border-blue-400 transition shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6"
          >
            <div className="space-y-3 flex-1">
              <div className="flex items-center space-x-3">
                <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800">
                  {demand.crop?.name_uz}
                </span>
                <span className="text-xs font-semibold text-gray-500">
                  🏢 {demand.buyer?.company_name || demand.buyer?.full_name}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600 font-medium">
                  {demand.offers_count} ta taklif kelgan
                </span>
              </div>

              <h3 className="text-lg font-bold text-gray-900">
                Kerak: {Number(demand.target_quantity).toLocaleString()} kg ({(demand.target_quantity / 1000).toFixed(0)} tonna)
              </h3>

              <p className="text-sm text-gray-600">
                {demand.description}
              </p>
            </div>

            <div className="flex md:flex-col items-end justify-between md:justify-center border-t md:border-t-0 pt-4 md:pt-0 border-gray-100 gap-3">
              <div className="text-right">
                <span className="text-xs text-gray-400">Maksimal xarid narxi:</span>
                <div className="text-2xl font-extrabold text-blue-700">
                  {Number(demand.max_price_per_unit).toLocaleString()} <span className="text-xs font-normal">so'm/kg</span>
                </div>
              </div>

              <button
                onClick={() => {
                  setSelectedDemand(demand);
                  setOfferPrice(Math.round(demand.max_price_per_unit * 0.95));
                  setOfferQuantity(Math.min(5000, demand.target_quantity));
                }}
                className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition shadow-sm whitespace-nowrap"
              >
                🌾 Fermer sifatida taklif berish
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Create Demand Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl relative">
            <button
              onClick={() => setShowCreateModal(false)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              &times;
            </button>

            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Yangi Talab E'lon Qilish
            </h3>
            <p className="text-xs text-gray-500 mb-6">
              Fermerlar sizning talabingizni ko'rib, o'z narxlarini taklif qilishadi
            </p>

            <form onSubmit={handleCreateDemand} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Ekin turi:
                </label>
                <input
                  type="text"
                  value={cropName}
                  onChange={(e) => setCropName(e.target.value)}
                  required
                  placeholder="Masalan: Pomidor, Bodring, Olma..."
                  className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Zarur hajm (kg):
                </label>
                <input
                  type="number"
                  value={targetQuantity}
                  onChange={(e) => setTargetQuantity(Number(e.target.value))}
                  required
                  min={100}
                  className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Maksimal qabul qilinadigan narx (so'm/kg):
                </label>
                <input
                  type="number"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(Number(e.target.value))}
                  required
                  min={500}
                  className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Talab tavsifi va shartlar:
                </label>
                <textarea
                  value={demandDesc}
                  onChange={(e) => setDemandDesc(e.target.value)}
                  rows={3}
                  required
                  placeholder="Hosil navi, qadoqlash turi, yetkazib berish manzili..."
                  className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm transition shadow-md"
              >
                E'lonni chop etish
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Submit Farmer Offer Modal */}
      {selectedDemand && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl relative">
            <button
              onClick={() => setSelectedDemand(null)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              &times;
            </button>

            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Fermer Narx Taklifi
            </h3>
            <p className="text-xs text-gray-500 mb-6">
              Xaridor: <span className="font-semibold text-gray-700">{selectedDemand.buyer?.company_name}</span> (Kerak: {selectedDemand.target_quantity.toLocaleString()} kg)
            </p>

            {offerSubmitted ? (
              <div className="text-center py-6">
                <div className="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto text-2xl mb-3">
                  ✓
                </div>
                <h4 className="font-bold text-gray-900">Taklif yuborildi!</h4>
                <p className="text-xs text-gray-500 mt-1">
                  Xaridor taklifingizni qabul qilsa, buyurtma avtomatik rasmiylashtiriladi.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmitOffer} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Siz taklif qiladigan narx (so'm/kg):
                  </label>
                  <input
                    type="number"
                    value={offerPrice}
                    onChange={(e) => setOfferPrice(Number(e.target.value))}
                    max={selectedDemand.max_price_per_unit}
                    required
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-base font-bold text-emerald-700 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                  <div className="text-xs text-gray-400 mt-1">
                    Maksimal chegara: {selectedDemand.max_price_per_unit.toLocaleString()} so'm
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Yetkazib bera oladigan hajm (kg):
                  </label>
                  <input
                    type="number"
                    value={offerQuantity}
                    onChange={(e) => setOfferQuantity(Number(e.target.value))}
                    max={selectedDemand.target_quantity}
                    required
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div className="bg-emerald-50 p-3 rounded-xl text-xs text-emerald-800">
                  💡 Jami taklif qiymati: {(offerPrice * offerQuantity).toLocaleString()} so'm
                </div>

                <button
                  type="submit"
                  className="w-full py-3 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm transition shadow-md"
                >
                  Taklifni Yuborish
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
