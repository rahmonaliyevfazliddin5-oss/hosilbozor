import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from datetime import date, datetime, timedelta
from decimal import Decimal

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.region import Region, District
from app.models.crop import Crop
from app.models.user import User, UserRole
from app.models.profile import FarmerProfile, BuyerProfile, DriverProfile, Vehicle
from app.models.listing import Listing, ListingStatus
from app.models.market_price import MarketPrice
from app.models.demand import DemandRequest, Offer, DemandStatus, OfferStatus


def seed():
    print("🌱 HosilBozor ma'lumotlar bazasini to'ldirish boshlanmoqda...")
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. REGIONS & DISTRICTS
        print("📍 Viloyatlar va tumanlar kiritilmoqda...")
        regions_data = [
            ("toshkent_sh", "Toshkent shahri", "г. Ташкент", [
                ("chilonzor", "Chilonzor tumani", "Чиланзарский район"),
                ("sergeli", "Sergeli tumani", "Сергелийский район"),
                ("bektemir", "Bektemir tumani", "Бектемирский район"),
            ]),
            ("toshkent_vil", "Toshkent viloyati", "Ташкентская область", [
                ("yangiyol", "Yangiyo'l tumani", "Янгиюльский район"),
                ("chinoz", "Chinoz tumani", "Чиназский район"),
                ("parkent", "Parkent tumani", "Паркентский район"),
            ]),
            ("samarqand", "Samarqand viloyati", "Самаркандская область", [
                ("urgut", "Urgut tumani", "Ургутский район"),
                ("pastdargom", "Pastdarg'om tumani", "Пастдаргомский район"),
                ("samarqand_t", "Samarqand tumani", "Самаркандский район"),
            ]),
            ("fargona", "Farg'ona viloyati", "Ферганская область", [
                ("quva", "Quva tumani", "Кувинский район"),
                ("oltiariq", "Oltiariq tumani", "Алтыарыкский район"),
                ("rishton", "Rishton tumani", "Риштанский район"),
            ]),
            ("andijon", "Andijon viloyati", "Андижанская область", [
                ("asaka", "Asaka tumani", "Асакинский район"),
                ("shahrixon", "Shahrixon tumani", "Шахриханский район"),
            ]),
            ("xorazm", "Xorazm viloyati", "Хорезмская область", [
                ("xonqa", "Xonqa tumani", "Ханкинский район"),
                ("urganch_t", "Urganch tumani", "Урганчский район"),
            ]),
            ("qashqadaryo", "Qashqadaryo viloyati", "Кашкадарьинская область", [
                ("shahrisabz", "Shahrisabz tumani", "Шахрисабзский район"),
                ("kitob", "Kitob tumani", "Китабский район"),
            ]),
        ]

        districts_map = {}
        for r_code, r_uz, r_ru, dists in regions_data:
            region = db.query(Region).filter(Region.code == r_code).first()
            if not region:
                region = Region(code=r_code, name_uz=r_uz, name_ru=r_ru)
                db.add(region)
                db.flush()

            for d_code, d_uz, d_ru in dists:
                dist = db.query(District).filter(District.region_id == region.id, District.name_uz == d_uz).first()
                if not dist:
                    dist = District(region_id=region.id, name_uz=d_uz, name_ru=d_ru)
                    db.add(dist)
                    db.flush()
                districts_map[d_code] = dist

        db.commit()

        # 2. CROPS (O'zbekiston agrar mahsulotlari)
        print("🌾 Qishloq xo'jaligi ekinlari kiritilmoqda...")
        crops_data = [
            ("pomidor", "Pomidor (Qizil & Pushti)", "Помидоры", "vegetables", "kg"),
            ("bodring", "Bodring (Orzu / Yangiyo'l)", "Огурцы", "vegetables", "kg"),
            ("kartoshka", "Qizil Kartoshka (Gala)", "Картофель", "vegetables", "kg"),
            ("piyoz", "Sariq Piyoz (Eksportbop)", "Лук репчатый", "vegetables", "kg"),
            ("sabzi", "Qizil Sabzi (Shirin)", "Морковь", "vegetables", "kg"),
            ("uzum", "Qora Kishmish Uzum", "Виноград Кишмиш", "fruits", "kg"),
            ("anor", "Quva Qizil Anori", "Гранат Кувинский", "fruits", "kg"),
            ("olma", "Besh Yulduz Olma", "Яблоки Пять Звезд", "fruits", "kg"),
            ("tarvuz", "Jondor Shirin Tarvuzi", "Арбуз", "melons", "kg"),
            ("qovun", "Mirzacho'l Qovuni", "Дыня Мирзачульская", "melons", "kg"),
        ]

        crops_map = {}
        for slug, name_uz, name_ru, cat, unit in crops_data:
            crop = db.query(Crop).filter(Crop.slug == slug).first()
            if not crop:
                crop = Crop(slug=slug, name_uz=name_uz, name_ru=name_ru, category=cat, standard_unit=unit)
                db.add(crop)
                db.flush()
            crops_map[slug] = crop

        db.commit()

        # 3. USERS & PROFILES
        print("👥 Foydalanuvchilar (Admin, Fermerlar, Xaridorlar, Haydovchilar) yaratilmoqda...")
        default_pwd_hash = hash_password("HosilBozor2026!")

        # A. Admin
        admin_user = db.query(User).filter(User.phone == "+998900000001").first()
        if not admin_user:
            admin_user = User(
                phone="+998900000001",
                full_name="Bosh Nazoratchi (Admin)",
                password_hash=default_pwd_hash,
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True,
                language="uz_latn"
            )
            db.add(admin_user)
            db.flush()

        # B. Farmers
        farmers_data = [
            ("+998901112233", "Rustam Yoqubov", "Chinoz Agrogurux", "chinoz", 4.9, 34),
            ("+998902223344", "Bahodir Mirzayev", "Zarafshon Agro MChJ", "urgut", 5.0, 52),
            ("+998903334455", "Akmal Qosimov", "Quva Anorzorlari", "quva", 4.8, 19),
        ]
        farmers_map = {}
        for phone, name, farm_name, dist_key, rating, deals in farmers_data:
            u = db.query(User).filter(User.phone == phone).first()
            if not u:
                u = User(
                    phone=phone,
                    full_name=name,
                    password_hash=default_pwd_hash,
                    role=UserRole.FARMER,
                    is_active=True,
                    is_verified=True,
                    language="uz_latn"
                )
                db.add(u)
                db.flush()
                prof = FarmerProfile(
                    user_id=u.id,
                    district_id=districts_map[dist_key].id,
                    farm_name=farm_name,
                    rating=rating,
                    total_deals=deals
                )
                db.add(prof)
                db.flush()
            farmers_map[phone] = u

        # C. Buyers
        buyers_data = [
            ("+998904445566", "Bobur Savdogar", "Korzinka Logistika Markazi", "wholesale"),
            ("+998905556677", "Aziz Rahimov", "Safia Restoranlar Tarmog'i", "restaurant"),
        ]
        buyers_map = {}
        for phone, name, comp, btype in buyers_data:
            u = db.query(User).filter(User.phone == phone).first()
            if not u:
                u = User(
                    phone=phone,
                    full_name=name,
                    password_hash=default_pwd_hash,
                    role=UserRole.BUYER,
                    is_active=True,
                    is_verified=True,
                    language="uz_latn"
                )
                db.add(u)
                db.flush()
                bprof = BuyerProfile(
                    user_id=u.id,
                    company_name=comp,
                    buyer_type=btype,
                    rating=4.9
                )
                db.add(bprof)
                db.flush()
            buyers_map[phone] = u

        # D. Drivers
        drivers_data = [
            ("+998907778899", "Davron Haydovchi", "AB1234567", "Isuzu Sovutgichli (Ref)", "01 A 777 AA", 5.0, True),
            ("+998908889900", "Jasur Karimov", "AB7654321", "Gazel Next Tentli", "10 B 234 BB", 2.5, False),
        ]
        for phone, name, lic, vtype, plate, tons, is_ref in drivers_data:
            u = db.query(User).filter(User.phone == phone).first()
            if not u:
                u = User(
                    phone=phone,
                    full_name=name,
                    password_hash=default_pwd_hash,
                    role=UserRole.DRIVER,
                    is_active=True,
                    is_verified=True,
                    language="uz_latn"
                )
                db.add(u)
                db.flush()
                dprof = DriverProfile(
                    user_id=u.id,
                    license_number=lic,
                    rating=4.9,
                    total_trips=28
                )
                db.add(dprof)
                db.flush()
                veh = Vehicle(
                    driver_id=dprof.id,
                    vehicle_type=vtype,
                    plate_number=plate,
                    capacity_tons=tons,
                    is_refrigerated=is_ref
                )
                db.add(veh)
                db.flush()

        db.commit()

        # 4. ACTIVE HARVEST LISTINGS
        print("📦 Hosil e'lonlari kiritilmoqda...")
        f1 = farmers_map["+998901112233"]
        f2 = farmers_map["+998902223344"]
        f3 = farmers_map["+998903334455"]

        listings_sample = [
            (f1.id, crops_map["pomidor"].id, districts_map["chinoz"].id, 12000.0, 500.0, 7200.0, "premium", "Issiqxonada yetishtirilgan sifatli pushti pomidor. Qutilarga terilgan, eksportbop.", 40.9412, 68.7584),
            (f1.id, crops_map["bodring"].id, districts_map["yangiyol"].id, 8500.0, 300.0, 4400.0, "standard", "Yangiyo'l shirin bodringi. Yangi uzilgan, do'kon va restoranlar uchun qulay narx.", 41.1167, 69.0500),
            (f2.id, crops_map["kartoshka"].id, districts_map["urgut"].id, 25000.0, 1000.0, 3400.0, "standard", "Samarqand qizil kartoshkasi. Qishki saqlash uchun juda mos, quruq ombordan.", 39.4033, 67.2417),
            (f2.id, crops_map["piyoz"].id, districts_map["pastdargom"].id, 40000.0, 2000.0, 2100.0, "standard", "Zarafshon sariq piyozi. Quruq, qobig'i butun, uzoq masofaga tashishga chidamli.", 39.6700, 66.7000),
            (f3.id, crops_map["uzum"].id, districts_map["quva"].id, 5000.0, 200.0, 14500.0, "premium", "Farg'ona vodiysining shirin qora kishmish uzumi. Maxsus qutilarda saqlangan.", 40.5217, 72.0083),
            (f3.id, crops_map["anor"].id, districts_map["quva"].id, 8000.0, 200.0, 18000.0, "premium", "Mashhur Quva qizil anori. To'q qizil donali, sersuv, eksport uchun saralangan.", 40.5217, 72.0083),
        ]

        for farmer_id, crop_id, dist_id, qty, min_qty, price, grade, desc, lat, lon in listings_sample:
            existing = db.query(Listing).filter(Listing.farmer_id == farmer_id, Listing.crop_id == crop_id).first()
            if not existing:
                l = Listing(
                    farmer_id=farmer_id,
                    crop_id=crop_id,
                    district_id=dist_id,
                    quantity=Decimal(str(qty)),
                    min_order_quantity=Decimal(str(min_qty)),
                    price_per_unit=Decimal(str(price)),
                    quality_grade=grade,
                    description=desc,
                    latitude=lat,
                    longitude=lon,
                    status=ListingStatus.ACTIVE
                )
                db.add(l)

        db.commit()

        # 5. WHOLESALE MARKET PRICES
        print("📈 Ulgurji bozor narxlari kiritilmoqda...")
        today_str = date.today()
        reg_toshkent = db.query(Region).filter(Region.code == "toshkent_sh").first()
        reg_samarqand = db.query(Region).filter(Region.code == "samarqand").first()
        reg_fargona = db.query(Region).filter(Region.code == "fargona").first()

        prices_sample = [
            (crops_map["pomidor"].id, reg_toshkent.id, "Qo'yliq ulgurji dehqon bozori", 6500.0, 8500.0, 7500.0),
            (crops_map["bodring"].id, reg_toshkent.id, "Parkent dehqon bozori", 4000.0, 5200.0, 4600.0),
            (crops_map["kartoshka"].id, reg_samarqand.id, "Samarqand Siyob bozori", 3200.0, 4100.0, 3600.0),
            (crops_map["uzum"].id, reg_fargona.id, "Farg'ona Markaziy dehqon bozori", 12000.0, 16000.0, 14000.0),
            (crops_map["anor"].id, reg_fargona.id, "Quva ulgurji meva bozori", 15000.0, 20000.0, 17500.0),
            (crops_map["piyoz"].id, reg_toshkent.id, "Qo'yliq ulgurji dehqon bozori", 1800.0, 2400.0, 2100.0),
        ]

        for cid, rid, market, pmin, pmax, pavg in prices_sample:
            mp = db.query(MarketPrice).filter(MarketPrice.crop_id == cid, MarketPrice.market_name == market).first()
            if not mp:
                mp = MarketPrice(
                    crop_id=cid,
                    region_id=rid,
                    market_name=market,
                    min_price=Decimal(str(pmin)),
                    max_price=Decimal(str(pmax)),
                    avg_price=Decimal(str(pavg)),
                    recorded_date=today_str
                )
                db.add(mp)

        db.commit()

        # 6. DEMAND REQUESTS (Reverse auctions)
        print("📢 Talablar va teskari auksionlar kiritilmoqda...")
        b1 = buyers_map["+998904445566"]
        b2 = buyers_map["+998905556677"]

        d1 = db.query(DemandRequest).filter(DemandRequest.buyer_id == b1.id).first()
        if not d1:
            d1 = DemandRequest(
                buyer_id=b1.id,
                crop_id=crops_map["pomidor"].id,
                destination_district_id=districts_map["sergeli"].id,
                target_quantity=Decimal("50000.0"),
                max_price_per_unit=Decimal("6800.0"),
                description="Toshkent supermarketlar tarmog'i uchun sifatli issiqxona pushti pomidori. Har haftada 10 tonnadan yetkazib berish sharti bilan.",
                status=DemandStatus.ACTIVE,
                expires_at=datetime.utcnow() + timedelta(days=14)
            )
            db.add(d1)
            db.flush()

            # Farmer offer
            offer1 = Offer(
                demand_id=d1.id,
                farmer_id=f1.id,
                offered_quantity=Decimal("20000.0"),
                offered_price_per_unit=Decimal("6500.0"),
                notes="Chinoz issiqxonalaridan to'g'ridan-to'g'ri saralangan mahsulot.",
                status=OfferStatus.PENDING
            )
            db.add(offer1)

        d2 = db.query(DemandRequest).filter(DemandRequest.buyer_id == b2.id).first()
        if not d2:
            d2 = DemandRequest(
                buyer_id=b2.id,
                crop_id=crops_map["kartoshka"].id,
                destination_district_id=districts_map["chilonzor"].id,
                target_quantity=Decimal("80000.0"),
                max_price_per_unit=Decimal("3200.0"),
                description="Qishki zaxira ombori uchun quruq qizil kartoshka. Minimal partiya 20 tonna.",
                status=DemandStatus.ACTIVE,
                expires_at=datetime.utcnow() + timedelta(days=21)
            )
            db.add(d2)
            db.flush()

            offer2 = Offer(
                demand_id=d2.id,
                farmer_id=f2.id,
                offered_quantity=Decimal("40000.0"),
                offered_price_per_unit=Decimal("3000.0"),
                notes="Urgut omborlaridan qadoqlangan holda yetkazib beriladi.",
                status=OfferStatus.PENDING
            )
            db.add(offer2)

        db.commit()

        print("\n✨ BARCHA REAL MA'LUMOTLAR MUVAFFAQIYATLI YARATILDI!")
        print("-------------------------------------------------------------")
        print("🔑 Test Hisoblari (Parol barchasi uchun: HosilBozor2026!):")
        print("  1. Admin:   +998900000001 (Bosh Nazoratchi)")
        print("  2. Fermer:  +998901112233 (Rustam Yoqubov, Chinoz Agrogurux)")
        print("  3. Fermer:  +998902223344 (Bahodir Mirzayev, Samarqand)")
        print("  4. Xaridor: +998904445566 (Bobur Savdogar, Korzinka)")
        print("  5. Haydovchi:+998907778899 (Davron Haydovchi, Isuzu 5t Ref)")
        print("-------------------------------------------------------------")

    except Exception as e:
        db.rollback()
        print(f"❌ Xatolik yuz berdi: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
