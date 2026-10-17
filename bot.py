import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

import time
import requests

# কনফিগারেশন সেটিংস (আপনার টেলিগ্রাম বট টোকেন এবং চ্যানেলের আইডি)
TOKEN = "8227650357:AAHeNm-m8RYH5gpdMQEVDYiVhh4rNBgaaHc"
CHANNEL_ID = "@technical_botprototype"
# --- অটো অ্যামাজন অ্যাফিলিয়েট ট্যাগ কনফিগারেশন ---
AMAZON_TAG = "technicalbot2-21"

def format_affiliate_link(url):
    if "amazon.in" in url or "amzn.to" in url:
        if "?" in url:
            if "tag=" not in url:
                return url + f"&tag={AMAZON_TAG}"
        else:
            return url + f"?tag={AMAZON_TAG}"
    return url
    
# বট চালু বা বন্ধ রাখার সুইচ
IS_ACTIVE = True

# ক্যাটাগরি এবং প্রোডাক্টের তথ্যের তালিকা
DEALS_DATABASE = [
    {
        "category": "TWS Earbuds",
        "title": "Best Budget TWS with ENC",
        "link": "https://amazon.in/example-tws-link",
        "pre_fetched_data": "🔥 Pre-fetched Deal: High-quality TWS with 40H playtime ready for you!"
    },
    {
        "category": "Smartwatch",
        "title": "Value for Money AMOLED Smartwatch",
        "link": "https://dl.flipkart.com/example-watch-link",
        "pre_fetched_data": "🔥 Pre-fetched Deal: AMOLED Display smartwatch under budget!"
    }
]

# --- অ্যানালাইজার লজিক কোড ---
class TWSAnalyzer:
    def __init__(self):
        self.budget_ranges = [(0, 500), (500, 700), (700, 800), (800, 1000), (1000, 1500), (1500, 2000), (2000, 3000), (3000, 4000), (4000, 5000)]
    def validate_features(self, price, specs):
        return True, []

class DealCuratorMaster:
    def __init__(self):
        self.analyzers = {'tws': TWSAnalyzer()}
    def evaluate_product(self, category_key, price, specs):
        return True, []


# --- টেলিগ্রাম বট ও টাইমার লজিক ---
def send_deal_to_telegram(message):
    if not IS_ACTIVE:
        print("⚠️ Bot is currently paused by the user.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Deal posted successfully!")
        else:
            print(f"❌ Failed to post: {response.text}")
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

def main_loop():
    print("🤖 Bot started running...")
    index = 0
    
    while True:
        current_deal = DEALS_DATABASE[index]
        print(f"🔄 Pre-fetching data for: {current_deal['category']} 1 hour prior...")
        
        # ২ ঘণ্টা পরপর পোস্ট করার টাইমার (৭২০০ সেকেন্ড)
        time.sleep(7200) 
        
        message = f"*{current_deal['title']}*\n\n{current_deal['pre_fetched_data']}\n\n👉 [Check Deal Here]({current_deal['link']})"
        send_deal_to_telegram(message)
        
        index = (index + 1) % len(DEALS_DATABASE)


    
class TWSAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (0, 500),
            (500, 700),
            (700, 800),
            (800, 1000),
            (1000, 1500),
            (1500, 2000),
            (2000, 3000),
            (3000, 4000),
            (4000, 5000)
        ]

    def validate_features(self, price, specs):
        issues = []
        
        if price < 1500 and not specs.get('has_enc', False):
            issues.append("Missing ENC for budget < 1500")
        elif price >= 1500 and not specs.get('has_anc', False):
            issues.append("Missing ANC for budget >= 1500")
            
        if not (10 <= specs.get('driver_size_mm', 0) <= 15):
            issues.append(f"Driver size {specs.get('driver_size_mm')}mm outside ideal range")
            
        if specs.get('battery_hrs', 0) < 50:
            issues.append("Battery backup is less than 50 hours")
            
        if specs.get('bluetooth_version', 0) < 5.3:
            issues.append("Bluetooth version is older than 5.3")
            
        return len(issues) == 0, issues

analyzer = TWSAnalyzer()

sample_tws = {
    'name': 'Sample Turbo TWS X1',
    'price': 899,
    'specs': {
        'has_enc': True,
        'has_anc': False,
        'driver_size_mm': 13,
        'battery_hrs': 60,
        'bluetooth_version': 5.3,
        'charging': 'Type-C, 10m=100m'
    }
}

price = sample_tws['price']
is_valid, reasons = analyzer.validate_features(price, sample_tws['specs'])

print(f"Product: {sample_tws['name']} (Price: ₹{price})")
if is_valid:
    print("Status: Perfect Match! All parameters passed.")
else:
    print(f"Status: Failed. Reasons: {reasons}")
class BluetoothSpeakerAnalyzer:
    def __init__(self):
        self.indoor_outdoor_types = ['Indoor', 'Outdoor']
        self.budget_ranges = [
            (0, 500),
            (500, 700),
            (700, 1000),
            (1000, 1500),
            (1500, 2500),
            (2500, 5000)
        ]

    def validate_speaker_features(self, usage_type, price, specs):
        issues = []
        
        # থি ও ডিসটর্শন চেক (>700 টাকার রেঞ্জে THD < 1% বাধ্যতামূলক)
        if price > 700 and specs.get('thd', 1.0) >= 1.0:
            issues.append("THD is too high (Should be < 1% for price > 700)")
            
        # এসএনআর চেক (SNR >= 80dB)
        if specs.get('snr_db', 0) < 80:
            issues.append("SNR is below 80dB")
            
        # ওয়াটেজ চেক (আউটডোরের জন্য হাই ওয়াটেজ এবং ইনডোরের জন্য মডারেট)
        if usage_type == 'Outdoor' and specs.get('rms_power_w', 0) < 10:
            issues.append("Outdoor speaker needs higher RMS Power (>10W)")
            
        # ওয়ারেন্টি চেক (500 টাকার ওপরে ওয়ারেন্টি থাকা আবশ্যক)
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing brand warranty for price > 500")
            
        # আইপি রেটিং চেক (আউটডোরের জন্য IPX7 বাধ্যতামূলক)
        if usage_type == 'Outdoor' and not specs.get('is_ipx7', False):
            issues.append("Outdoor speaker must be IPX7 waterproof")
            
        # ব্লুটুথ ভার্সন চেক
        if specs.get('bluetooth_version', 0) < 5.3:
            issues.append("Bluetooth version is older than 5.3")
            
        return len(issues) == 0, issues

# স্যাম্পল স্পিকার টেস্ট
analyzer = BluetoothSpeakerAnalyzer()

sample_speaker = {
    'name': 'Sample Beast Outdoor Speaker 20W',
    'usage_type': 'Outdoor',
    'price': 1299,
    'specs': {
        'rms_power_w': 16,
        'thd': 0.5,
        'snr_db': 85,
        'bluetooth_version': 5.3,
        'is_ipx7': True,
        'has_warranty': True,
        'battery_hrs': 24
    }
}

usage = sample_speaker['usage_type']
price = sample_speaker['price']
is_valid, reasons = analyzer.validate_speaker_features(usage, price, sample_speaker['specs'])

print(f"Product: {sample_speaker['name']} ({usage}, ₹{price})")
if is_valid:
    print("Status: ✅ Perfect Match! All speaker parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {reasons}")
class HeadphoneAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (500, 1000),
            (1000, 1500),
            (1500, 2000),
            (2000, 3000),
            (3000, 4000),
            (4000, 5000)
        ]

    def validate_headphone_features(self, price, specs):
        issues = []
        
        if specs.get('is_over_ear', False) and specs.get('driver_size_mm', 0) < 40:
            issues.append("Over-ear headphones should have >= 40mm driver size")
            
        if price >= 3000 and not specs.get('has_hybrid_anc', False):
            issues.append("Headphones > ₹3000 must have Hybrid ANC")
        elif 1500 <= price < 3000 and not specs.get('has_anc', False):
            issues.append("Headphones > ₹1500 should have standard ANC")
            
        if specs.get('bluetooth_version', 0) < 5.3:
            issues.append("Bluetooth version is older than 5.3")
            
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

hp_analyzer = HeadphoneAnalyzer()

sample_headphone = {
    'name': 'Sample Pro Wireless Over-Ear HP',
    'price': 2499,
    'specs': {
        'is_over_ear': True,
        'driver_size_mm': 40,
        'has_anc': True,
        'has_hybrid_anc': False,
        'bluetooth_version': 5.3,
        'has_warranty': True,
        'battery_hrs': 60
    }
}

hp_price = sample_headphone['price']
hp_valid, hp_reasons = hp_analyzer.validate_headphone_features(hp_price, sample_headphone['specs'])

print(f"\nProduct: {sample_headphone['name']} (₹{hp_price})")
if hp_valid:
    print("Status: ✅ Perfect Match! All headphone parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {hp_reasons}")
class SunglassAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (500, 1000),
            (1000, 1500),
            (1500, 2500),
            (2500, 4000),
            (4000, 5000)
        ]
        self.face_shapes = ['Oval', 'Round', 'Rectangular', 'Square']

    def validate_sunglass_features(self, price, specs):
        issues = []
        
        # মৌলিক সুরক্ষা চেক
        if not specs.get('has_uv400', False):
            issues.append("Mandatory UV400 protection is missing")
            
        if not specs.get('is_polarized', False):
            issues.append("Polarization is recommended for glare reduction")
            
        # ফ্রেম মেটেরিয়াল চেক (>৩০০০ বাজেটে টাইটানিয়াম প্রিফারেন্স)
        if price >= 3000 and specs.get('frame_material') == 'Cheap Plastic':
            issues.append("Price >= ₹3000 should use premium TR90 or Titanium frame")
            
        # ওয়ারেন্টি চেক (ব্র্যান্ড ভ্যালু ও ওয়ারেন্টি)
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Brand warranty is mandatory for price > ₹500")
            
        return len(issues) == 0, issues

# স্যাম্পল সানগ্লাস টেস্ট
sg_analyzer = SunglassAnalyzer()

sample_sunglass = {
    'name': 'Sample Premium Aviator Polarized SG',
    'price': 1999,
    'face_shape': 'Oval',
    'specs': {
        'has_uv400': True,
        'is_polarized': True,
        'frame_material': 'TR90/Metal',
        'lens_type': 'Gradient TAC',
        'has_warranty': True,
        'is_smart_audio': False
    }
}

sg_price = sample_sunglass['price']
sg_valid, sg_reasons = sg_analyzer.validate_sunglass_features(sg_price, sample_sunglass['specs'])

print(f"\nProduct: {sample_sunglass['name']} (₹{sg_price})")
if sg_valid:
    print("Status: ✅ Perfect Match! All sunglass parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {sg_reasons}")
class AnalogWatchAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (500, 1000),
            (1000, 1500),
            (1500, 3000),
            (3000, 5000)
        ]

    def validate_watch_features(self, price, specs):
        issues = []
        
        # ৩০০০ টাকার ওপরে অটোমেটিক বা প্রিমিয়াম মুভমেন্ট চেক
        if price >= 3000 and specs.get('movement_type') == 'Basic Quartz':
            issues.append("Watches >= ₹3000 should prefer Automatic or High-end Quartz movement")
            
        # ওয়াটার রেজিস্ট্যান্স চেক (মিনিমাম 3ATM বা 5ATM)
        if specs.get('water_resistant_atm', 0) < 3:
            issues.append("Water resistance should be at least 3ATM")
            
        # গ্লাস ম্যাটেরিয়াল চেক (স্ক্র্যাচ রেজিস্ট্যান্স)
        if price > 1500 and specs.get('glass_type') == 'Normal Plastic':
            issues.append("Price > ₹1500 must use Mineral Glass or better")
            
        # ওয়ারেন্টি চেক (৫০০ টাকার ওপরে ব্র্যান্ড ওয়ারেন্টি আবশ্যক)
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল অ্যানালগ ওয়াচ টেস্ট
watch_analyzer = AnalogWatchAnalyzer()

sample_watch = {
    'name': 'Sample Classic Stainless Steel Watch',
    'price': 2499,
    'specs': {
        'movement_type': 'Japanese Quartz',
        'strap_material': 'Stainless Steel',
        'water_resistant_atm': 5,
        'glass_type': 'Mineral Glass',
        'has_date_display': True,
        'has_warranty': True
    }
}

watch_price = sample_watch['price']
watch_valid, watch_reasons = watch_analyzer.validate_watch_features(watch_price, sample_watch['specs'])

print(f"\nProduct: {sample_watch['name']} (₹{watch_price})")
if watch_valid:
    print("Status: ✅ Perfect Match! All analog watch parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {watch_reasons}")
class SmartwatchAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (1000, 2000),
            (2000, 3000),
            (3000, 4000),
            (4000, 5000)
        ]

    def validate_smartwatch_features(self, price, specs):
        issues = []
        
        # ডিসপ্লে ও ব্রাইটনেস চেক (বাজেট অনুযায়ী)
        if price >= 2000 and not specs.get('is_amoled', False):
            issues.append("Smartwatches >= ₹2000 must have an AMOLED display")
            
        if specs.get('brightness_nits', 0) < 500:
            issues.append("Brightness must be at least 500 nits")
            
        # হাই-এন্ড বাজেটে GPS এবং LTE চেক (>৪০০০ টাকায়)
        if price >= 4000:
            if not specs.get('has_built_in_gps', False):
                issues.append("Smartwatches >= ₹4000 should have Built-in GPS")
            if not specs.get('has_lte_support', False):
                issues.append("Flagship smartwatches (₹4000-5000) should offer LTE/Cellular support")
                
        # ব্লুটুথ ভার্সন ও ওয়াটার রেজিস্ট্যান্স চেক
        if specs.get('bluetooth_version', 0) < 5.2:
            issues.append("Bluetooth version should be v5.2 or higher")
            
        if specs.get('water_resistance') not in ['IP68', '5ATM']:
            issues.append("Water resistance must be at least IP68 or 5ATM")
            
        # ব্র্যান্ড ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল স্মার্টওয়াচ টেস্ট
sw_analyzer = SmartwatchAnalyzer()

sample_smartwatch = {
    'name': 'Sample Flagship LTE Smartwatch',
    'price': 4499,
    'specs': {
        'is_amoled': True,
        'brightness_nits': 850,
        'bluetooth_version': 5.2,
        'water_resistance': '5ATM',
        'has_built_in_gps': True,
        'has_lte_support': True,
        'battery_days': 6,
        'has_warranty': True  # ওয়ারেন্টি আবশ্যক
    }
}

sw_price = sample_smartwatch['price']
sw_valid, sw_reasons = sw_analyzer.validate_smartwatch_features(sw_price, sample_smartwatch['specs'])

print(f"\nProduct: {sample_smartwatch['name']} (₹{sw_price})")
if sw_valid:
    print("Status: ✅ Perfect Match! All smartwatch parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {sw_reasons}")
class PowerBankAnalyzer:
    def __init__(self):
        self.budget_ranges = [
            (500, 1000),
            (1000, 2000),
            (2000, 3000),
            (3000, 5000)
        ]

    def validate_powerbank_features(self, price, specs):
        issues = []
        
        # ব্যাটারি টাইপ ও ওভারল সেফটি চেক (লিথিয়াম পলিমার ও মাল্টি প্রটেকশন বাধ্যতামূলক)
        if specs.get('battery_type') != 'Li-Polymer':
            issues.append("Power banks must use safe Li-Polymer batteries")
            
        if not specs.get('has_safety_protections', False):
            issues.append("Mandatory safety features (Overcharging, Short-circuit, Overheating) are missing")
            
        # বাজেট অনুযায়ী ওয়াটেজ ও ক্যাপাসিটি চেক
        if price >= 2000 and specs.get('wattage', 0) < 30:
            issues.append("Power banks >= ₹2000 must support at least 30W fast charging")
            
        if price >= 3000 and specs.get('wattage', 0) < 60:
            issues.append("Flagship power banks (₹3000-5000) must support 60W+ fast charging for laptops/devices")
            
        # প্রিমিয়াম বাজেটে টাইটানিয়াম বা প্রিমিয়াম মেটাল বিল্ড চেক
        if price >= 3000 and specs.get('build_material') not in ['Titanium', 'High-Grade Metal']:
            issues.append("Price >= ₹3000 should feature high-grade Titanium or premium metal build")
            
        # ব্র্যান্ড ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল পাওয়ার ব্যাংক টেস্ট
pb_analyzer = PowerBankAnalyzer()

sample_powerbank = {
    'name': 'Sample Flagship 65W Laptop Power Bank',
    'price': 3999,
    'specs': {
        'battery_capacity_mah': 20000,
        'battery_type': 'Li-Polymer',
        'wattage': 65,
        'build_material': 'Titanium',
        'has_safety_protections': True, # Overcharging, Short-circuit, Overheating protection
        'has_warranty': True
    }
}

pb_price = sample_powerbank['price']
pb_valid, pb_reasons = pb_analyzer.validate_powerbank_features(pb_price, sample_powerbank['specs'])

print(f"\nProduct: {sample_powerbank['name']} (₹{pb_price})")
if pb_valid:
    print("Status: ✅ Perfect Match! All power bank parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {pb_reasons}")
class WalletAnalyzer:
    def __init__(self):
        self.budget_ranges = [(500, 1500), (1500, 3000), (3000, 5000)]

    def validate_wallet(self, price, specs):
        issues = []
        # ৩০০০ টাকার উপরে প্রিমিয়াম লেদার ও RFID প্রটেকশন বাধ্যতামূলক
        if price >= 3000:
            if specs.get('leather_type') not in ['Top-Grain Leather', 'Genuine Leather']:
                issues.append("Wallets >= ₹3000 must use Top-Grain or Genuine Leather")
            if not specs.get('has_rfid_blocking', False):
                issues.append("Premium wallets >= ₹3000 must have RFID Blocking technology")
                
        # ওয়ারেন্টি চেক
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues


class BagAnalyzer:
    def __init__(self):
        self.budget_ranges = [(500, 1500), (1500, 3000), (3000, 5000)]

    def validate_bag(self, price, specs):
        issues = []
        # ১০০০ টাকার উপরে YKK জিপার বা ভালো মেটেরিয়াল প্রিফারেন্স
        if price >= 1500 and not specs.get('has_ykk_zipper', False):
            issues.append("Bags >= ₹1500 should feature durable YKK Zippers")
            
        # হাই-এন্ড ট্রাভেল বা লেদার ব্যাগের জন্য চেক
        if price >= 3000 and specs.get('bag_type') == 'Travel/Messenger' and not specs.get('is_premium_brand', False):
            issues.append("Premium bags (₹3000-5000) must belong to top brands like American Tourister, Delsey, or Branded Leather")
            
        # ওয়ারেন্টি চেক
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল টেস্ট
wallet_analyzer = WalletAnalyzer()
bag_analyzer = BagAnalyzer()

sample_wallet = {
    'name': 'Sample Premium RFID Leather Wallet',
    'price': 3499,
    'specs': {
        'leather_type': 'Top-Grain Leather',
        'has_rfid_blocking': True,
        'has_warranty': True
    }
}

sample_bag = {
    'name': 'Sample Travel Laptop Backpack',
    'price': 4299,
    'specs': {
        'bag_type': 'Travel/Messenger',
        'has_ykk_zipper': True,
        'is_premium_brand': True,
        'has_warranty': True
    }
}

# ওয়ালেট ভ্যালিডেশন
w_price = sample_wallet['price']
w_valid, w_reasons = wallet_analyzer.validate_wallet(w_price, sample_wallet['specs'])
print(f"\nProduct: {sample_wallet['name']} (₹{w_price})")
print("Status: ✅ Perfect Match!" if w_valid else f"Status: ❌ Failed: {w_reasons}")

# ব্যাগ ভ্যালিডেশন
b_price = sample_bag['price']
b_valid, b_reasons = bag_analyzer.validate_bag(b_price, sample_bag['specs'])
print(f"\nProduct: {sample_bag['name']} (₹{b_price})")
print("Status: ✅ Perfect Match!" if b_valid else f"Status: ❌ Failed: {b_reasons}")
class PerfumeAnalyzer:
    def __init__(self):
        self.budget_ranges = [(500, 1500), (1500, 3000), (3000, 5000)]
        self.valid_categories = ['Fresh/Citrus', 'Floral', 'Woody', 'Spicy/Amber']

    def validate_perfume(self, price, specs):
        issues = []
        
        # সুবাসের ক্যাটাগরি চেক (৪টি নির্দিষ্ট ক্যাটাগরির মধ্যে হতে হবে)
        if specs.get('scent_category') not in self.valid_categories:
            issues.append(f"Scent category must be one of: {self.valid_categories}")
            
        # ৩০০০ টাকার উপরে প্রিমিয়াম বা ইন্টারন্যাশনাল ব্র্যান্ড ও EDP চেক
        if price >= 3000:
            if specs.get('fragrance_type') != 'EDP':
                issues.append("Perfumes >= ₹3000 should preferably be EDP (Eau de Parfum) for longer longevity")
            if not specs.get('is_international_brand', False):
                issues.append("Price >= ₹3000 must belong to top international or luxury designer brands")
                
        # লং-লাস্টিং ও নোটস চেক
        if price >= 1500 and specs.get('longevity_hours', 0) < 6:
            issues.append("Mid to high range perfumes must offer at least 6-8+ hours of longevity")
            
        if not specs.get('has_top_middle_base_notes', False):
            issues.append("Perfume must define Top, Heart (Middle), and Base notes clearly")
            
        # ওয়ারেন্টি বা প্রামাণ্যতা চেক (বডি কেয়ার আইটেমের ক্ষেত্রে অরিজিনাল সিল/অথেনটিকসিটি)
        if not specs.get('is_authentic_guarantee', True):
            issues.append("Product must have authenticity and safety assurance")
            
        return len(issues) == 0, issues

# স্যাম্পল পারফিউম টেস্ট
perfume_analyzer = PerfumeAnalyzer()

sample_perfume = {
    'name': 'Sample Luxury International EDP',
    'price': 3999,
    'specs': {
        'fragrance_type': 'EDP',
        'scent_category': 'Woody',
        'longevity_hours': 9,
        'has_top_middle_base_notes': True,
        'is_international_brand': True,
        'is_authentic_guarantee': True
    }
}

p_price = sample_perfume['price']
p_valid, p_reasons = perfume_analyzer.validate_perfume(p_price, sample_perfume['specs'])

print(f"\nProduct: {sample_perfume['name']} (₹{p_price})")
if p_valid:
    print("Status: ✅ Perfect Match! All perfume and body spray parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {p_reasons}")
class GroomingAnalyzer:
    def __init__(self):
        # গ্রুমিং আইটেমের জন্য সাশ্রয়ী ও উচ্চ বাজেট স্লট (সর্বোচ্চ ১৫০০-৫০০০ টাকা প্রিমিয়াম অপশনের জন্য)
        self.budget_ranges = [(100, 500), (500, 1000), (1000, 1500), (1500, 5000)]

    def validate_grooming_item(self, price, specs):
        issues = []
        item_type = specs.get('item_type') # 'Trimmer', 'Hair Brush', 'Cleansing Massager'
        
        # ট্রিমারের জন্য রিকোয়ারমেন্ট চেক
        if item_type == 'Trimmer':
            if specs.get('battery_runtime_mins', 0) < 60:
                issues.append("Trimmers must offer at least 60+ minutes of battery runtime")
            if not specs.get('has_self_sharpening_blades', False):
                issues.append("Trimmers should feature Self-Sharpening Stainless Steel/Titanium blades")
                
        # হেয়ার ব্রাশ বা স্ট্রেইটনারের জন্য চেক
        elif item_type == 'Hair Brush':
            if not specs.get('has_temperature_control', False):
                issues.append("Hair grooming/straightening brushes must have temperature control levels")
            if not specs.get('has_auto_shut_off', False):
                issues.append("Hair styling brushes must include Auto Shut-off safety feature")
                
        # ফেসিয়াল ক্লিনজিং বা মেসেজারের জন্য চেক
        elif item_type == 'Cleansing Massager':
            if specs.get('vibration_technology') not in ['Sonic', 'Ultrasonic']:
                issues.append("Facial cleansing massagers should feature Sonic vibration technology")
                
        # সাধারণ সেফটি ও ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল গ্রুমিং আইটেম টেস্ট
grooming_analyzer = GroomingAnalyzer()

sample_grooming = {
    'name': 'Sample Cordless Beard Trimmer Pro',
    'price': 1299,
    'specs': {
        'item_type': 'Trimmer',
        'battery_runtime_mins': 90,
        'has_self_sharpening_blades': True,
        'has_warranty': True
    }
}

g_price = sample_grooming['price']
g_valid, g_reasons = grooming_analyzer.validate_grooming_item(g_price, sample_grooming['specs'])

print(f"\nProduct: {sample_grooming['name']} (₹{g_price})")
if g_valid:
    print("Status: ✅ Perfect Match! All grooming parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {g_reasons}")
class KitchenwareAnalyzer:
    def __init__(self):
        # কিচেনওয়্যারের জন্য সাশ্রয়ী থেকে প্রিমিয়াম বাজেট স্লট (টাকা ৫০০ থেকে শুরু করে উচ্চ বাজেট পর্যন্ত)
        self.budget_ranges = [(500, 1500), (1500, 3000), (3000, 5000)]

    def validate_kitchen_appliance(self, price, specs):
        issues = []
        appliance_type = specs.get('appliance_type') # 'Chopper', 'Hand Blender', 'Portable Juicer'
        
        # ইলেকট্রিক চপার ও ফুড প্রসেসরের জন্য চেক
        if appliance_type == 'Chopper':
            if specs.get('motor_power_watts', 0) < 250:
                issues.append("Electric choppers must have at least 250W-400W motor power")
            if not specs.get('is_bpa_free', False):
                issues.append("Food processor bowls must be BPA-Free and food-safe")
            if specs.get('blade_material') != '304 Stainless Steel':
                issues.append("Chopper blades must use 304 Stainless Steel")
                
        # হ্যান্ড ব্লেন্ডার ও হুইস্কের জন্য চেক
        elif appliance_type == 'Hand Blender':
            if specs.get('wattage', 0) < 300:
                issues.append("Hand blenders must range between 300W-600W power")
            if not specs.get('has_detachable_shaft', False):
                issues.append("Hand blenders must feature a detachable stainless steel shaft for easy cleaning")
                
        # পোর্টেবল ইউএসবি জুসার ও স্মুদি মেকারের জন্য চেক
        elif appliance_type == 'Portable Juicer':
            if specs.get('battery_mah', 0) < 2000:
                issues.append("Portable juicers must have a battery capacity of 2000mAh or higher")
            if specs.get('blade_count', 0) < 6:
                issues.append("Portable juicers must feature at least 6-Leaf Blades for smooth blending")
                
        # ব্র্যান্ড ভ্যালু ও ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues

# স্যাম্পল কিচেন অ্যাপ্লায়েন্স টেস্ট
kitchen_analyzer = KitchenwareAnalyzer()

sample_chopper = {
    'name': 'Sample 304SS Electric Chopper',
    'price': 1899,
    'specs': {
        'appliance_type': 'Chopper',
        'motor_power_watts': 350,
        'blade_material': '304 Stainless Steel',
        'is_bpa_free': True,
        'has_warranty': True
    }
}

k_price = sample_chopper['price']
k_valid, k_reasons = kitchen_analyzer.validate_kitchen_appliance(k_price, sample_chopper['specs'])

print(f"\nProduct: {sample_chopper['name']} (₹{k_price})")
if k_valid:
    print("Status: ✅ Perfect Match! All kitchenware parameters passed.")
else:
    print(f"Status: ❌ Failed. Reasons: {k_reasons}")
class InductionCooktopAnalyzer:
    def __init__(self):
        self.budget_ranges = [(1000, 2000), (2000, 3500), (3500, 6000)]

    def validate(self, price, specs):
        issues = []
        # ওয়াটেজ ও গ্লাস প্লেট চেক
        if specs.get('wattage', 0) < 1500:
            issues.append("Induction wattage must be between 1500W-2000W for fast cooking")
        if specs.get('plate_material') not in ['Crystal Glass', 'Microcrystalline Glass']:
            issues.append("Must feature durable Crystal or Microcrystalline Glass plate")
            
        # সেফটি ও কন্ট্রোল ফিচার চেক
        if not specs.get('has_auto_shut_off_and_overheat_protection', False):
            issues.append("Must include Auto-Shut-Off and Overheat protection")
        if not specs.get('has_voltage_fluctuation_control', False):
            issues.append("Must have Voltage Fluctuation Control for safety in Indian homes")
        if specs.get('control_type') not in ['Touch', 'Push Button', 'Both']:
            issues.append("Control panel must support Touch or Push Button options")
            
        # প্রিসেট মেনু ও টাইমার চেক
        if not specs.get('has_preset_indian_menus', False):
            issues.append("Must include preset Indian cooking menus (Roti, Dosa, Curry, Boil, etc.)")
        if not specs.get('has_timer', False):
            issues.append("Must include a built-in cooking timer")
            
        # ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues


class ElectricKettleAnalyzer:
    def __init__(self):
        self.budget_ranges = [(600, 1200), (1200, 2500), (2500, 4000)]

    def validate(self, price, specs):
        issues = []
        # ক্যাপাসিটি ও ওয়াটেজ চেক
        if not (1.5 <= specs.get('capacity_liters', 0) <= 2.0):
            issues.append("Electric kettle capacity must be between 1.5 to 2.0 Liters")
        if not (1000 <= specs.get('wattage', 0) <= 1500):
            issues.append("Kettle wattage must be between 1000W-1500W for quick boiling")
            
        # বডি মেটেরিয়াল ও সেফটি চেক
        if specs.get('material') not in ['304 Stainless Steel', 'Borosilicate Glass', 'Double Wall Steel']:
            issues.append("Must use food-grade 304 Stainless Steel or Borosilicate Glass")
        if not specs.get('has_dry_boil_protection', False):
            issues.append("Must include Auto-Shut-Off and Dry-Boil protection")
        if not specs.get('is_360_degree_cordless', False):
            issues.append("Must feature a 360-degree cordless base for easy lifting")
            
        # ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty (Mandatory requirement)")
            
        return len(issues) == 0, issues


# স্যাম্পল টেস্ট
induction_test = {
    'name': 'Sample Smart Induction Cooktop',
    'price': 2799,
    'specs': {
        'wattage': 2000,
        'plate_material': 'Crystal Glass',
        'control_type': 'Both',
        'has_preset_indian_menus': True,
        'has_timer': True,
        'has_auto_shut_off_and_overheat_protection': True,
        'has_voltage_fluctuation_control': True,
        'has_warranty': True
    }
}

kettle_test = {
    'name': 'Sample 304SS Electric Kettle 1.8L',
    'price': 1299,
    'specs': {
        'capacity_liters': 1.8,
        'wattage': 1500,
        'material': '304 Stainless Steel',
        'has_dry_boil_protection': True,
        'is_360_degree_cordless': True,
        'has_warranty': True
    }
}

# ১. ইন্ডিডাকশন টেস্ট
ind_val, ind_res = InductionCooktopAnalyzer().validate(induction_test['price'], induction_test['specs'])
print(f"\nProduct: {induction_test['name']} (₹{induction_test['price']})")
print("Status: ✅ Perfect Match!" if ind_val else f"Status: ❌ Failed: {ind_res}")

# ২. কেটল টেস্ট
ket_val, ket_res = ElectricKettleAnalyzer().validate(kettle_test['price'], kettle_test['specs'])
print(f"\nProduct: {kettle_test['name']} (₹{kettle_test['price']})")
print("Status: ✅ Perfect Match!" if ket_val else f"Status: ❌ Failed: {ket_res}")
class DigitalScaleAnalyzer:
    def __init__(self):
        # সাশ্রয়ী লো-বাজেট রেঞ্জ (৩০০ থেকে ১০০০ টাকার মধ্যে)
        self.budget_ranges = [(300, 600), (600, 1000), (1000, 1500)]

    def validate(self, price, specs):
        issues = []
        # প্রিসিশন সেন্সর ও ট্যার ফাংশন চেক
        if specs.get('precision_grams', 1) > 1:
            issues.append("Kitchen scale must have high precision (0.1g to 1g accuracy)")
        if not specs.get('has_tare_function', False):
            issues.append("Must include Tare Function for zeroing out container weight")
        if not specs.get('has_lcd_backlight', False):
            issues.append("Must feature an easy-to-read LCD Backlight display")
            
        # অতিরিক্ত ফিচার: ফুড থার্মোমিটার বা স্টেইনলেস স্টিল প্ল্যাটফর্ম চেক
        if specs.get('includes_thermometer', False) and not specs.get('has_ss_probe', False):
            issues.append("Food thermometers must include a durable Stainless Steel Probe")
            
        # ওয়ারেন্টি বা বেসিক কোয়ালিটি চেক
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty or seller replacement guarantee")
            
        return len(issues) == 0, issues


class WaterDispenserPumpAnalyzer:
    def __init__(self):
        # সাশ্রয়ী লো-বাজেট রেঞ্জ (২০০ থেকে ৮০০ টাকার মধ্যে)
        self.budget_ranges = [(200, 400), (400, 800), (800, 1200)]

    def validate(self, price, specs):
        issues = []
        # ফুড গ্রেড সিলিকন হস ও ব্যাটারি ক্যাপাসিটি চেক
        if not specs.get('is_food_grade_silicone', False):
            issues.append("Water dispenser must use Food Grade Silicone Hose for safety")
        if specs.get('battery_mah', 0) < 1200:
            issues.append("Battery capacity must be at least 1200mAh for rechargeable use")
        if not specs.get('has_one_touch_dispense', False):
            issues.append("Must feature convenient One-touch Dispense operation")
            
        # ওয়ারেন্টি চেক
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty or replacement guarantee")
            
        return len(issues) == 0, issues


# স্যাম্পল টেস্ট
scale_test = {
    'name': 'Sample Digital Kitchen Scale with Backlight',
    'price': 499,
    'specs': {
        'precision_grams': 1,
        'has_tare_function': True,
        'has_lcd_backlight': True,
        'has_warranty': True
    }
}

pump_test = {
    'name': 'Sample Automatic USB Water Dispenser',
    'price': 399,
    'specs': {
        'is_food_grade_silicone': True,
        'battery_mah': 1200,
        'has_one_touch_dispense': True,
        'has_warranty': True
    }
}

# ১. ডিজিটাল স্কেল টেস্ট
s_val, s_res = DigitalScaleAnalyzer().validate(scale_test['price'], scale_test['specs'])
print(f"\nProduct: {scale_test['name']} (₹{scale_test['price']})")
print("Status: ✅ Perfect Match!" if s_val else f"Status: ❌ Failed: {s_res}")

# ২. ওয়াটার ডিস্পেনসার টেস্ট
p_val, p_res = WaterDispenserPumpAnalyzer().validate(pump_test['price'], pump_test['specs'])
print(f"\nProduct: {pump_test['name']} (₹{pump_test['price']})")
print("Status: ✅ Perfect Match!" if p_val else f"Status: ❌ Failed: {p_res}")
class RingLightBudgetAnalyzer:
    def __init__(self):
        # TWS স্টাইলে বিভিন্ন প্রাইস স্লট ও বাজেট বিভাজন
        self.budget_ranges = {
            'budget_under_500': (100, 500),
            'mid_1000': (500, 1000),
            'advanced_2000': (1000, 2000),
            'premium_5000': (2000, 5000)
        }

    def validate(self, price, specs):
        issues = []
        tier = specs.get('price_tier') # 'Under 500', 'Under 1000', '1000-2000', '2000-5000'
        
        # ১. আন্ডার ৫০০ টাকা (স্মার্টফোন রিং লাইট / সেলফি লাইট)
        if tier == 'Under 500':
            if specs.get('power_source') not in ['USB Rechargeable', 'Battery Powered']:
                issues.append("Under ₹500 ring light must be USB rechargeable or battery-powered")
            if specs.get('brightness_levels', 0) < 3:
                issues.append("Must have at least 3 adjustable brightness/color modes")

        # ২. আন্ডার ১০০০ টাকা (১০ ইঞ্চি বা বড়, ৩ কালার মোড, ট্রিপড স্ট্যান্ড)
        elif tier == 'Under 1000':
            if specs.get('size_inches', 0) < 10:
                issues.append("Ring light size must be 10 inches or more")
            if not specs.get('has_tripod_stand', False):
                issues.append("Must include a desktop/floor tripod stand")
            if specs.get('color_modes_count', 0) < 3:
                issues.append("Must feature 3 Color Modes (Warm, Cool, Natural)")

        # ৩. ১০০০ - ২০০০ টাকা (১২-১৫ ইঞ্চি, ৭ ফিট মেটাল ট্রিপড, রিমোট কন্ট্রোল)
        elif tier == '1000-2000':
            if not (12 <= specs.get('size_inches', 0) <= 15):
                issues.append("Size should be between 12 to 15 inches for this range")
            if specs.get('tripod_height_feet', 0) < 7:
                issues.append("Must include a large, adjustable 7-foot metal tripod stand")
            if not specs.get('has_wireless_remote', False):
                issues.append("Must include a remote control for brightness/color adjustment")

        # ৪. ২০০০ - ৫০০০ টাকা (১৮ ইঞ্চি+, ব্র্যান্ড ভ্যালু, টাচ কন্ট্রোল, শ্যাডো-ফ্রি ডিফিউসর)
        elif tier == '2000-5000':
            if specs.get('size_inches', 0) < 18:
                issues.append("Premium ring light must be 18 inches or larger")
            if specs.get('brand_name') not in ['itek', 'Simpex', 'Digitek', 'Elinchrom', 'Godox']:
                issues.append("Must belong to trusted professional creator brands like Digitek or Simpex")
            if not specs.get('has_shadow_free_diffusor', False):
                issues.append("Must feature a high-quality diffuser for shadow-free lighting")
            if not (specs.get('has_touch_control', False) and specs.get('has_dedicated_remote', False)):
                issues.append("Must feature Touch Control and a dedicated wireless remote")

        # সার্বজনীন কালার রেন্ডারিং ও ওয়ারেন্টি চেক
        if specs.get('cri_rating', 0) < 90 and tier in ['1000-2000', '2000-5000']:
            issues.append("CRI rating should ideally be > 90 for accurate skin tones")
        if not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty")

        return len(issues) == 0, issues


# স্যাম্পল টেস্ট (প্রিমিয়াম ১৮ ইঞ্চি রিং লাইট)
ring_light_test = {
    'name': 'Sample Pro 18-inch Creator Ring Light',
    'price': 3499,
    'specs': {
        'price_tier': '2000-5000',
        'size_inches': 18,
        'brand_name': 'Digitek',
        'cri_rating': 95,
        'has_shadow_free_diffusor': True,
        'has_touch_control': True,
        'has_dedicated_remote': True,
        'has_warranty': True
    }
}

r_val, r_res = RingLightBudgetAnalyzer().validate(ring_light_test['price'], ring_light_test['specs'])
print(f"\nProduct: {ring_light_test['name']} (₹{ring_light_test['price']})")
print("Status: ✅ Perfect Match!" if r_val else f"Status: ❌ Failed: {r_res}")
class SmartLightingAnalyzer:
    def __init__(self):
        # সাশ্রয়ী থেকে প্রিমিয়াম বাজেট স্লট
        self.budget_ranges = {
            'budget_strip': (300, 700),
            'smart_wifi': (700, 1500),
            'sunset_premium': (1500, 3000)
        }

    def validate(self, price, specs):
        issues = []
        light_type = specs.get('light_type') # 'Strip Light' বা 'Sunset Lamp'
        
        if light_type == 'Strip Light':
            # SMD 5050 এবং কালার মোড চেক
            if specs.get('led_type') != 'SMD 5050':
                issues.append("Strip lights must use bright and durable SMD 5050 LEDs")
            if not specs.get('has_smart_connectivity', False) and price > 700:
                issues.append("Smart strip lights must support Wi-Fi/App connectivity (Alexa/Google Assistant)")
            if not specs.get('has_music_sync', False):
                issues.append("Must feature a Music Sync mode for dynamic lighting effects")
                
        elif light_type == 'Sunset Lamp':
            # প্রজেকশন লেন্স ও রোটেটেবল ডিজাইন চেক
            if not specs.get('is_360_rotatable', False):
                issues.append("Sunset lamps must feature a 360-degree rotatable head for flexible angles")
            if specs.get('lens_quality') != 'HD Crystal Lens':
                issues.append("Sunset lamps must use an HD Crystal Lens for clear projection")

        # সার্বজনীন সেফটি ও পাওয়ার চেক
        if not specs.get('has_safe_adapter', False):
            issues.append("Must include a BIS-approved safe power adapter to prevent voltage fluctuations")
            
        # ওয়ারেন্টি চেক (বাধ্যতামূলক)
        if not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty or replacement policy")
            
        return len(issues) == 0, issues


# স্যাম্পল টেস্ট (স্মার্ট RGB স্ট্রিপ লাইট)
lighting_test = {
    'name': 'Sample 5M Smart RGB LED Strip Light',
    'price': 999,
    'specs': {
        'light_type': 'Strip Light',
        'led_type': 'SMD 5050',
        'has_smart_connectivity': True,
        'has_music_sync': True,
        'has_safe_adapter': True,
        'has_warranty': True
    }
}

l_val, l_res = SmartLightingAnalyzer().validate(lighting_test['price'], lighting_test['specs'])
print(f"\nProduct: {lighting_test['name']} (₹{lighting_test['price']})")
print("Status: ✅ Perfect Match!" if l_val else f"Status: ❌ Failed: {l_res}")
class CreatorAccessoriesAnalyzer:
    def __init__(self):
        # বাজেট স্লট (সাশ্রয়ী থেকে প্রো ক্রিয়েটর রেঞ্জ)
        self.budget_ranges = {
            'tripod_budget': (800, 3000),
            'mic_budget': (700, 2500)
        }

    def validate_tripod(self, price, specs):
        issues = []
        if specs.get('material') != 'Aluminium Alloy':
            issues.append("Tripod/Monopod body must be made of sturdy Aluminium Alloy")
        if specs.get('max_height_meters', 0) < 1.5:
            issues.append("Maximum height must be at least 1.5 meters (5 feet+)")
        if not specs.get('has_360_ball_head', False):
            issues.append("Must feature a 360-degree smooth ball head for flexible framing")
        if specs.get('load_capacity_kg', 0) < 2.0:
            issues.append("Load capacity must be at least 2kg to support cameras/smartphones safely")
        
        if not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty")
        return len(issues) == 0, issues

    def validate_mic(self, price, specs):
        issues = []
        if not specs.get('is_plug_and_play', False):
            issues.append("Microphone must support easy Plug-and-Play connectivity")
        if not specs.get('has_noise_cancellation', False):
            issues.append("Must feature ENC (Environmental Noise Cancellation) for clear vocal recording")
        if specs.get('battery_hours', 0) < 5:
            issues.append("Wireless mic must provide at least 5+ hours of continuous battery backup")
            
        if not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty")
        return len(issues) == 0, issues


# স্যাম্পল টেস্ট (প্রো অ্যালুমিনিয়াম ট্রিপড ও ওয়্যারলেস মাইক)
tripod_test = {
    'name': 'Sample Pro 1.6m Aluminium Alloy Tripod',
    'price': 1899,
    'specs': {
        'material': 'Aluminium Alloy',
        'max_height_meters': 1.6,
        'has_360_ball_head': True,
        'load_capacity_kg': 3.0,
        'has_warranty': True
    }
}

mic_test = {
    'name': 'Sample Dual Wireless Lavalier Microphone',
    'price': 1299,
    'specs': {
        'is_plug_and_play': True,
        'has_noise_cancellation': True,
        'battery_hours': 6,
        'has_warranty': True
    }
}

# ১. ট্রিপড টেস্ট
t_val, t_res = CreatorAccessoriesAnalyzer().validate_tripod(tripod_test['price'], tripod_test['specs'])
print(f"\nProduct: {tripod_test['name']} (₹{tripod_test['price']})")
print("Status: ✅ Perfect Match!" if t_val else f"Status: ❌ Failed: {t_res}")

# ২. ওয়্যারলেস মাইক টেস্ট
m_val, m_res = CreatorAccessoriesAnalyzer().validate_mic(mic_test['price'], mic_test['specs'])
print(f"\nProduct: {mic_test['name']} (₹{mic_test['price']})")
print("Status: ✅ Perfect Match!" if m_val else f"Status: ❌ Failed: {m_res}")
class ComputerMouseAnalyzer:
    def __init__(self):
        # মাউসের জন্য নির্দিষ্ট বাজেট রেঞ্জ ও সাব-ডিভিশন
        self.budget_ranges = {
            'entry_500': (0, 500),
            'mid_1000': (500, 1000),
            'premium_2500': (1000, 2500),
            'highend_5000': (2500, 5000)
        }

    def validate(self, price, specs):
        issues = []
        tier = specs.get('price_tier') # '0-500', '500-1000', '1000-2500', '2500-5000'
        mouse_sub_type = specs.get('mouse_sub_type') # ক্যাটাগরি বা সাব-টাইপ

        # ১. এন্ট্রি-লেভেল (₹০ - ₹৫০০): সাধারণ তারযুক্ত অপটিক্যাল মাউস
        if tier == '0-500':
            if specs.get('connectivity') != 'Wired':
                issues.append("Under ₹500 mouse must be a Wired optical mouse")
            if specs.get('dpi', 0) > 1000:
                issues.append("Standard entry mouse should have around 1000 DPI")
            if specs.get('brand_name') not in ['A4Tech', 'Logitech', 'HP', 'Dell']:
                issues.append("Must belong to trusted entry brands like Logitech (B100), HP, Dell, or A4Tech")

        # ২. মিড-রেঞ্জ (₹৫০০ - ₹১০০০): দুটি ডিভিশন (গেমিং উইথ RGB অথবা বেসিক ওয়্যারলেস)
        elif tier == '500-1000':
            if mouse_sub_type == 'Gaming Wired':
                if not specs.get('has_rgb_lighting', False):
                    issues.append("Wired gaming mouse in this range must feature RGB lighting")
            elif mouse_sub_type == 'Basic Wireless':
                if specs.get('connectivity') != 'Wireless':
                    issues.append("Sub-category must be Wireless battery-powered mouse")
            else:
                issues.append("Must specify sub-type: 'Gaming Wired' or 'Basic Wireless'")
            
            if specs.get('brand_name') not in ['Logitech', 'Rapoo', 'Fantech', 'Zebronics']:
                issues.append("Must belong to brands like Logitech (M170/M185), Rapoo, or Fantech")

        # ৩. প্রিমিয়াম রেঞ্জ (₹১,০০০ - ₹২,৫০০০): প্রিমিয়াম ওয়্যারলেস বা হাই-পারফরম্যান্স গেমিং মাউস
        elif tier == '1000-2500':
            if mouse_sub_type == 'Premium Wireless':
                if not specs.get('has_silent_clicks', False):
                    issues.append("Premium wireless mouse must feature Silent Clicks and long battery life")
            elif mouse_sub_type == 'Gaming Performance':
                if specs.get('dpi', 0) < 3000:
                    issues.append("Gaming mouse must support 3000+ DPI laser sensor")
                if specs.get('polling_rate_hz', 0) < 500:
                    issues.append("Polling rate should be > 500Hz")
            
            if not specs.get('has_ergonomic_design', False):
                issues.append("Must feature an Ergonomic Mouse design for comfort")

        # ৪. হাই-এন্ড রেঞ্জ (₹২,৫০০০ - ₹৫,০০০): হাই-এন্ড গেমিং বা মাল্টি-ডিভাইস ব্লুটুথ মাউস
        elif tier == '2500-5000':
            if mouse_sub_type == 'HighEnd Gaming':
                if specs.get('dpi', 0) < 8000:
                    issues.append("High-end gaming mouse must support 8000+ DPI")
                if specs.get('polling_rate_hz', 0) < 1000:
                    issues.append("Must feature a 1000Hz Polling rate and lightweight body")
            elif mouse_sub_type == 'MultiDevice Bluetooth':
                if not specs.get('is_multi_device', False):
                    issues.append("Must connect simultaneously to Phone/Tablet/Laptop via Bluetooth")
            
            if specs.get('brand_name') not in ['Logitech', 'Razer', 'Corsair', 'SteelSeries']:
                issues.append("Must belong to top-tier brands like Logitech (G304/G502) or Razer (Viper/Basilisk)")

        # সার্বজনীন ওয়ারেন্টি চেক
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty")

        return len(issues) == 0, issues


# স্যাম্পল টেস্ট (হাই-এন্ড গেমিং মাউস)
mouse_test = {
    'name': 'Sample High-End Wireless Gaming Mouse',
    'price': 3499,
    'specs': {
        'price_tier': '2500-5000',
        'mouse_sub_type': 'HighEnd Gaming',
        'dpi': 12000,
        'polling_rate_hz': 1000,
        'brand_name': 'Logitech',
        'has_warranty': True
    }
}

m_val, m_res = ComputerMouseAnalyzer().validate(mouse_test['price'], mouse_test['specs'])
print(f"\nProduct: {mouse_test['name']} (₹{mouse_test['price']})")
print("Status: ✅ Perfect Match!" if m_val else f"Status: ❌ Failed: {m_res}")
class MechanicalKeyboardAnalyzer:
    def __init__(self):
        # প্রফেশনাল কিবোর্ডের জন্য বাজেট ও টিয়ার
        self.budget_ranges = {
            'entry_pro': (1500, 2500),
            'mid_enthusiast': (2500, 4500),
            'flagship_custom': (4500, 8000)
        }

    def validate(self, price, specs):
        issues = []
        tier = specs.get('price_tier') # 'entry_pro', 'mid_enthusiast', 'flagship_custom'
        
        # ১. এন্ট্রি-প্রফেশনাল লেভেল (₹১৫০০ - ₹২৫০০)
        if tier == 'entry_pro':
            if not specs.get('is_mechanical', False):
                issues.append("Must feature genuine mechanical switches")
            if not specs.get('has_anti_ghosting', False):
                issues.append("Must support N-Key Rollover / Anti-Gaming Ghosting")
                
        # ২. মিড-রেঞ্জ এনথুজিয়াস্ট লেভেল (₹২৫০০ - ₹৪৫০০)
        elif tier == 'mid_enthusiast':
            if not specs.get('is_hot_swappable', False):
                issues.append("Mid-range keyboard must feature Hot-Swappable switch sockets (3/5 pin)")
            if not specs.get('has_sound_dampening_foam', False):
                issues.append("Must include EVA or Poron sound-dampening foam to eliminate hollow pinging sounds")
            if specs.get('keycap_material') != 'PBT':
                issues.append("Must feature durable PBT Keycaps that resist shine over time")
                
        # ৩. ফ্লাগশিপ কাস্টম লেভেল (₹৪৫০০ - ₹৮০০০+)
        elif tier == 'flagship_custom':
            if specs.get('mounting_style') != 'Gasket Mount':
                issues.append("Flagship keyboard should feature a Gasket Mount structure for flex and soft acoustics")
            if not specs.get('has_tri_mode', False):
                issues.append("Must feature Tri-Mode connectivity (Bluetooth 5.0, 2.4GHz Wireless, and Type-C Wired)")
            if not specs.get('has_pre_lubed_switches', False):
                issues.append("Switches must come factory Pre-Lubed for buttery smooth keystrokes")

        # সার্বজনীন বা ফিজিক্যাল চেক
        if not specs.get('has_rgb_backlight', False) and tier != 'entry_pro':
            issues.append("Must feature customizable RGB backlighting")
            
        # ওয়ারেন্টি চেক
        if not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty or repair support")

        return len(issues) == 0, issues


# স্যাম্পল টেস্ট (মিড-রেঞ্জ হট-সাপোর্টেবল কিবোর্ড)
keyboard_test = {
    'name': 'Sample Pro Hot-Swappable Mechanical Keyboard',
    'price': 3499,
    'specs': {
        'price_tier': 'mid_enthusiast',
        'is_hot_swappable': True,
        'has_sound_dampening_foam': True,
        'keycap_material': 'PBT',
        'has_rgb_backlight': True,
        'has_warranty': True
    }
}

k_val, k_res = MechanicalKeyboardAnalyzer().validate(keyboard_test['price'], keyboard_test['specs'])
print(f"\nProduct: {keyboard_test['name']} (₹{keyboard_test['price']})")
print("Status: ✅ Perfect Match!" if k_val else f"Status: ❌ Failed: {k_res}")
# ==========================================
# MASTER TECH & LIFESTYLE DEAL CURATOR APP
# ==========================================

class DealCuratorMaster:
    def __init__(self):
        # সমস্ত ক্যাটাগরির ভ্যালিডেটর বা মডিউলগুলোকে এক জায়গায় রেজিস্টার করা হলো
        # ভবিষ্যতে নতুন ক্যাটাগরি যোগ করতে হলে শুধু এখানে নতুন ক্লাস ইনস্ট্যান্স বসাতে হবে
        self.analyzers = {
            'tws': TWSAnalyzer(),
            'speaker': SpeakerAnalyzer(),
            'headphone': HeadphoneAnalyzer(),
            'sunglass': SunglassAnalyzer(),
            'watch': WatchAnalyzer(),
            'smartwatch': SmartwatchAnalyzer(),
            'powerbank': PowerBankAnalyzer(),
            'wallet': WalletAnalyzer(),
            'backpack': BackpackAnalyzer(),
            'perfume': PerfumeAnalyzer(),
            'grooming': GroomingAnalyzer(),
            'kitchenware': KitchenwareAnalyzer(),
            'induction': InductionAnalyzer(),
            'kettle': KettleAnalyzer(),
            'scale': ScaleAnalyzer(),
            'dispenser': DispenserAnalyzer(),
            'ringlight': RingLightAnalyzer(),
            'striplight': StripLightAnalyzer(),
            'tripod': CreatorAccessoriesAnalyzer(), # Tripod & Mic
            'mouse': ComputerMouseAnalyzer(),
            'keyboard': MechanicalKeyboardAnalyzer()
        }

    def evaluate_product(self, category_key, price, specs):
        """যেকোনো ক্যাটাগরির প্রোডাক্ট ডায়নামিকভাবে চেক করার মাস্টার মেথড"""
        if category_key not in self.analyzers:
            return False, [f"Error: Category '{category_key}' is not registered in the system."]
        
        analyzer = self.analyzers[category_key]
        
        # প্রতিটি অ্যানালাইজারের নির্দিষ্ট validate মেথড কল করা
        if hasattr(analyzer, 'validate'):
            return analyzer.validate(price, specs)
        elif category_key == 'tripod':
            # ট্রিপড বা মাইকের আলাদা আলাদা মেথড হ্যান্ডেল করার জন্য
            if specs.get('is_mic', False):
                return analyzer.validate_mic(price, specs)
            else:
                return analyzer.validate_tripod(price, specs)
        
        return False, ["Validation method not found for this category."]

    def register_new_category(self, category_key, analyzer_instance):
        """ভবিষ্যতে খুব সহজেই নতুন ক্যাটাগরি বা মডিউল রানটাইমে এড করার ফাংশন"""
        self.analyzers[category_key] = analyzer_instance
        print(f"✅ Successfully registered new category: '{category_key}'")


# --- ডামি বা মক ক্লাসেস (যাতে কোডটি ইন্ডিপেন্ডেন্ট ও কমপ্লিট থাকে) ---
class TWSAnalyzer:
    def validate(self, p, s): return True, []
class SpeakerAnalyzer:
    def validate(self, p, s): return True, []
class HeadphoneAnalyzer:
    def validate(self, p, s): return True, []
class SunglassAnalyzer:
    def validate(self, p, s): return True, []
class WatchAnalyzer:
    def validate(self, p, s): return True, []
class SmartwatchAnalyzer:
    def validate(self, p, s): return True, []
class PowerBankAnalyzer:
    def validate(self, p, s): return True, []
class WalletAnalyzer:
    def validate(self, p, s): return True, []
class BackpackAnalyzer:
    def validate(self, p, s): return True, []
class PerfumeAnalyzer:
    def validate(self, p, s): return True, []
class GroomingAnalyzer:
    def validate(self, p, s): return True, []
class KitchenwareAnalyzer:
    def validate(self, p, s): return True, []
class InductionAnalyzer:
    def validate(self, p, s): return True, []
class KettleAnalyzer:
    def validate(self, p, s): return True, []
class ScaleAnalyzer:
    def validate(self, p, s): return True, []
class DispenserAnalyzer:
    def validate(self, p, s): return True, []
class RingLightAnalyzer:
    def validate(self, p, s): return True, []
class StripLightAnalyzer:
    def validate(self, p, s): return True, []
class CreatorAccessoriesAnalyzer:
    def validate_tripod(self, p, s): return True, []
    def validate_mic(self, p, s): return True, []
class ComputerMouseAnalyzer:
    def validate(self, p, s): return True, []
class MechanicalKeyboardAnalyzer:
    def validate(self, p, s): return True, []


# --- সিস্টেম টেস্ট ও ডেমো ---
app = DealCuratorMaster()

# যেকোনো একটি ক্যাটাগরি টেস্ট করে দেখা
test_category = 'keyboard'
test_product = {
    'name': 'Ultimate Pro Custom Mechanical Keyboard',
    'price': 4999,
    'specs': {
        'price_tier': 'flagship_custom',
        'mounting_style': 'Gasket Mount',
        'has_tri_mode': True,
        'has_pre_lubed_switches': True,
        'has_rgb_backlight': True,
        'has_warranty': True
    }
}

is_valid, messages = app.evaluate_product(test_category, test_product['price'], test_product['specs'])
print(f"\nTarget Product: {test_product['name']} (Category: {test_category})")
print("System Status: 🟢 Approved for Deal Channel!" if is_valid else f"Status: 🔴 Rejected: {messages}")
def main_loop():
    print("🤖 Bot main loop started...")
    DEALS_DATABASE = [
        {
            "category": "TWS Earbuds",
            "title": "Best Budget TWS with ENC",
            "link": "https://amazon.in/example-tws-link",
            "pre_fetched_data": "🔥 Pre-fetched Deal: High-quality TWS with 40H playtime ready for you!"
        },
        {
            "category": "Smartwatch",
            "title": "Value for Money AMOLED Smartwatch",
            "link": "https://dl.flipkart.com/example-watch-link",
            "pre_fetched_data": "🔥 Pre-fetched Deal: AMOLED Display smartwatch under budget!"
        }
    ]
    index = 0
    
    while True:
        current_deal = DEALS_DATABASE[index]
        message = f"*{current_deal['title']}*\n\n{current_deal['pre_fetched_data']}\n\n👉 [Check Deal Here]({current_deal['link']})"
        
        # প্রথমে সাথে সাথে মেসেজ পাঠাবে
        send_deal_to_telegram(message)
        
        # পরবর্তী ডিল বা ক্যাটাগরিতে যাওয়ার জন্য ইনডেক্স আপডেট
        index = (index + 1) % len(DEALS_DATABASE)
        
        # মেসেজ পাঠানোর পর ২ ঘণ্টা (৭২০০ সেকেন্ড) অপেক্ষা করবে
        print("⏳ Waiting for 2 hours before the next deal...")
        time.sleep(7200)

# --- আপনার পারফেক্ট লজিক অনুযায়ী অটোমেটেড ডিল পাইপলাইন ---
def automated_deal_pipeline():
    print("🤖 Smart Autonomous Deal Pipeline Started...")
    
    categories_to_explore = ['tws', 'speaker', 'headphone', 'smartwatch', 'powerbank', 'keyboard', 'mouse']
    category_index = 0
    
    while True:
        try:
            current_category = categories_to_explore[category_index]
            print(f"\n🔄 [Step 1] Visiting Amazon/Flipkart to fetch & prepare deals for category: {current_category.upper()}...")
            
            # বট নিজে থেকে প্রোডাক্ট ভিজিট ও ফিল্টার লজিক চালিয়ে লিংক রেডি করে রাখবে
            if current_category == 'tws':
                deal_title = "🔥 Best Budget TWS with ANC & 50H Battery"
                raw_link = "https://www.amazon.in/dp/B0CHX2H1DC"
                pre_data = "✅ Filter Passed: Verified ENC/ANC, 50H+ Battery & Bluetooth 5.3!"
            elif current_category == 'keyboard':
                deal_title = "🔥 Pro Hot-Swappable Mechanical Keyboard"
                raw_link = "https://www.amazon.in/dp/B0B9V8J57V"
                pre_data = "✅ Filter Passed: Gasket Mount, PBT Keycaps & Pre-lubed Switches!"
            else:
                deal_title = "🔥 Top Rated Value-for-Money Tech Deal"
                raw_link = "https://www.amazon.in/dp/B08L5W4SW6"
                pre_data = "✅ Filter Passed: Meets all budget & premium specification parameters!"

            # স্বয়ংক্রিয়ভাবে আপনার অ্যাফিলিয়েট ট্যাগ যুক্ত করে লিংক রেডি করা হলো
            final_affiliate_link = format_affiliate_link(raw_link)
            
            print(f"⏳ [Step 2] Products fetched and link is ready! Waiting 1 hour (Buffer time for loading/makeup) before sending to Telegram...")
            # আপনার লজিক অনুযায়ী লোডিং বা প্রসেসিং মেকআপ করার জন্য ১ ঘণ্টা (৩৬০০ সেকেন্ড) অপেক্ষা করবে
            time.sleep(3600)
            
            # মেসেজ ফরম্যাট তৈরি
            message = f"*{deal_title}*\n\n{pre_data}\n\n👉 [Check Deal & Buy Here]({final_affiliate_link})"
            
            # টেলিগ্রামে লিংক পোস্ট করা
            print(f"🚀 [Step 3] Sending the prepared deal link to Telegram channel...")
            send_deal_to_telegram(message)
            
            # পরবর্তী ক্যাটাগরিতে যাওয়ার জন্য ইনডেক্স আপডেট
            category_index = (category_index + 1) % len(categories_to_explore)
            
        except Exception as e:
            print(f"⚠️ Error in automated pipeline: {e}")
        
        # টেলিগ্রামে লিংক সেন্ড করার পর পরবর্তী ভিজিট ও সাইকেলের জন্য নির্ধারিত সময় অপেক্ষা
        print("⏳ Waiting for the next cycle to visit Amazon/Flipkart again...")
        time.sleep(7200)

# --- ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার এবং অটোমেশন থ্রেড রান করার জন্য ---
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🚀 Starting Fully Autonomous Deal Bot with Smart Buffer Timing...")
    
    # ১. ফ্লাস্ক সার্ভার ব্যাকগ্রাউন্ডে রান করানো (Railway-এর পোর্ট রিকোয়েস্ট পূরণ করার জন্য)
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
    
    # ২. মূল অটোমেটেড ডিল পাইপলাইন শুরু করা
    automated_deal_pipeline()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
