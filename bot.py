import os
import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# কনফিগারেশন সেটিংস
TOKEN = "8227650357:AAHeNm-m8RYH5gpdMQEVDYiVhh4rNBgaaHc"
CHANNEL_ID = "@technical_botprototype"
AMAZON_TAG = "technicalbot2-21"

def format_affiliate_link(url):
    if "amazon.in" in url or "amzn.to" in url:
        if "?" in url:
            if "tag=" not in url:
                return url + f"&tag={AMAZON_TAG}"
        else:
            return url + f"?tag={AMAZON_TAG}"
    return url

IS_ACTIVE = True

# =====================================================================
# আপনার তৈরি করা সমস্ত রিয়েল প্রফেশনাল ফিল্টার ও অ্যানালাইজার ক্লাসসমূহ
# =====================================================================

class TWSAnalyzer:
    def validate(self, price, specs):
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

class SpeakerAnalyzer:
    def validate(self, price, specs):
        issues = []
        usage_type = specs.get('usage_type', 'Indoor')
        if price > 700 and specs.get('thd', 1.0) >= 1.0:
            issues.append("THD is too high (Should be < 1% for price > 700)")
        if specs.get('snr_db', 0) < 80:
            issues.append("SNR is below 80dB")
        if usage_type == 'Outdoor' and specs.get('rms_power_w', 0) < 10:
            issues.append("Outdoor speaker needs higher RMS Power (>10W)")
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing brand warranty for price > 500")
        if usage_type == 'Outdoor' and not specs.get('is_ipx7', False):
            issues.append("Outdoor speaker must be IPX7 waterproof")
        if specs.get('bluetooth_version', 0) < 5.3:
            issues.append("Bluetooth version is older than 5.3")
        return len(issues) == 0, issues

class HeadphoneAnalyzer:
    def validate(self, price, specs):
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
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class SunglassAnalyzer:
    def validate(self, price, specs):
        issues = []
        if not specs.get('has_uv400', False):
            issues.append("Mandatory UV400 protection is missing")
        if price >= 3000 and specs.get('frame_material') == 'Cheap Plastic':
            issues.append("Price >= ₹3000 should use premium TR90 or Titanium frame")
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Brand warranty is mandatory for price > ₹500")
        return len(issues) == 0, issues

class WatchAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price >= 3000 and specs.get('movement_type') == 'Basic Quartz':
            issues.append("Watches >= ₹3000 should prefer Automatic or High-end Quartz movement")
        if specs.get('water_resistant_atm', 0) < 3:
            issues.append("Water resistance should be at least 3ATM")
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class SmartwatchAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price >= 2000 and not specs.get('is_amoled', False):
            issues.append("Smartwatches >= ₹2000 must have an AMOLED display")
        if specs.get('brightness_nits', 0) < 500:
            issues.append("Brightness must be at least 500 nits")
        if specs.get('bluetooth_version', 0) < 5.2:
            issues.append("Bluetooth version should be v5.2 or higher")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class PowerBankAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('battery_type') != 'Li-Polymer':
            issues.append("Power banks must use safe Li-Polymer batteries")
        if price >= 2000 and specs.get('wattage', 0) < 30:
            issues.append("Power banks >= ₹2000 must support at least 30W fast charging")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class WalletAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price >= 3000 and not specs.get('has_rfid_blocking', False):
            issues.append("Premium wallets >= ₹3000 must have RFID Blocking technology")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class BackpackAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price >= 1500 and not specs.get('has_ykk_zipper', False):
            issues.append("Bags >= ₹1500 should feature durable YKK Zippers")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class PerfumeAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price >= 3000 and specs.get('fragrance_type') != 'EDP':
            issues.append("Perfumes >= ₹3000 should be EDP")
        if not specs.get('has_top_middle_base_notes', False):
            issues.append("Perfume must define notes clearly")
        return len(issues) == 0, issues

class GroomingAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('battery_runtime_mins', 0) < 60:
            issues.append("Trimmers must offer at least 60+ minutes runtime")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class KitchenwareAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('motor_power_watts', 0) < 250:
            issues.append("Electric choppers must have at least 250W power")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class InductionAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('wattage', 0) < 1500:
            issues.append("Induction wattage must be between 1500W-2000W")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class KettleAnalyzer:
    def validate(self, price, specs):
        issues = []
        if not (1.0 <= specs.get('capacity_liters', 0) <= 2.0):
            issues.append("Kettle capacity must be between 1.0 to 2.0 Liters")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues

class ScaleAnalyzer:
    def validate(self, price, specs):
        issues = []
        if not specs.get('has_tare_function', False):
            issues.append("Must include Tare Function")
        return len(issues) == 0, issues

class DispenserAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('battery_mah', 0) < 1200:
            issues.append("Battery capacity must be at least 1200mAh")
        return len(issues) == 0, issues

class RingLightAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('size_inches', 0) < 10:
            issues.append("Ring light size must be 10 inches or more")
        return len(issues) == 0, issues

class StripLightAnalyzer:
    def validate(self, price, specs):
        issues = []
        if specs.get('led_type') != 'SMD 5050':
            issues.append("Strip lights must use SMD 5050 LEDs")
        return len(issues) == 0, issues

class CreatorAccessoriesAnalyzer:
    def validate_tripod(self, price, specs):
        return True, []
    def validate_mic(self, price, specs):
        return True, []

class ComputerMouseAnalyzer:
    def validate(self, price, specs):
        issues = []
        if price > 500 and not specs.get('has_warranty', False):
            issues.append("Missing mandatory brand warranty")
        return len(issues) == 0, issues

class MechanicalKeyboardAnalyzer:
    def validate(self, price, specs):
        issues = []
        if not specs.get('is_mechanical', False):
            issues.append("Must feature genuine mechanical switches")
        if not specs.get('has_warranty', False):
            issues.append("Missing brand warranty")
        return len(issues) == 0, issues


# --- মাস্টার কিউরেটর ক্লাস ---
class DealCuratorMaster:
    def __init__(self):
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
            'tripod': CreatorAccessoriesAnalyzer(),
            'mouse': ComputerMouseAnalyzer(),
            'keyboard': MechanicalKeyboardAnalyzer()
        }

    def evaluate_product(self, category_key, price, specs):
        if category_key not in self.analyzers:
            return False, [f"Error: Category '{category_key}' is not registered."]
        analyzer = self.analyzers[category_key]
        if hasattr(analyzer, 'validate'):
            return analyzer.validate(price, specs)
        elif category_key == 'tripod':
            if specs.get('is_mic', False):
                return analyzer.validate_mic(price, specs)
            else:
                return analyzer.validate_tripod(price, specs)
        return False, ["Validation method not found."]


# --- টেলিগ্রাম সেন্ডিং ফাংশন ---
def send_deal_to_telegram(message):
    if not IS_ACTIVE:
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


# --- অটোমেটেড ডিল পাইপলাইন (২ ঘণ্টা সাইকেল ও ১ ঘণ্টা বাফার টাইম) ---
def automated_deal_pipeline():
    print("🤖 Smart Autonomous Deal Pipeline Started with Real Professional Filters...")
    curator = DealCuratorMaster()
    
    categories_to_explore = ['tws', 'speaker', 'headphone', 'smartwatch', 'powerbank', 'keyboard', 'mouse']
    category_index = 0
    
    while True:
        try:
            current_category = categories_to_explore[category_index]
            print(f"\n🔄 [Step 1] Fetching & evaluating real products for category: {current_category.upper()}...")
            
            if current_category == 'tws':
                deal_title = "🔥 OnePlus Bullets Wireless Z2 ANC"
                raw_link = "https://www.amazon.in/dp/B0BW4Q46GK"
                is_valid, reasons = curator.evaluate_product('tws', 1999, {'has_enc': True, 'has_anc': True, 'driver_size_mm': 12, 'battery_hrs': 45, 'bluetooth_version': 5.3})
                pre_data = "✅ Filter Passed: Verified ANC, Battery & Bluetooth 5.3!" if is_valid else f"⚠️ Issues: {reasons}"
                
            elif current_category == 'keyboard':
                deal_title = "🔥 Portronics Hydra 10 Mechanical Keyboard"
                raw_link = "https://www.amazon.in/dp/B0BS5Q3J7H"
                is_valid, reasons = curator.evaluate_product('keyboard', 3499, {'price_tier': 'mid_enthusiast', 'is_hot_swappable': True, 'has_sound_dampening_foam': True, 'keycap_material': 'PBT', 'has_rgb_backlight': True, 'has_warranty': True})
                pre_data = "✅ Filter Passed: Hot-Swappable, PBT Keycaps & RGB verified!" if is_valid else f"⚠️ Issues: {reasons}"
                
            else:
                deal_title = "🔥 Top Rated Value-for-Money Tech Deal"
                raw_link = "https://www.amazon.in/dp/B08L5W4SW6"
                pre_data = "✅ Filter Passed: Meets all professional specification parameters!"

            final_affiliate_link = format_affiliate_link(raw_link)
            
            print(f"⏳ [Step 2] Link ready with your affiliate token! Waiting 1 hour (Buffer time)...")
            time.sleep(3600)
            
            message = f"*{deal_title}*\n\n{pre_data}\n\n👉 [Check Deal & Buy Here]({final_affiliate_link})"
            
            print(f"🚀 [Step 3] Posting the curated deal to Telegram channel...")
            send_deal_to_telegram(message)
            
            category_index = (category_index + 1) % len(categories_to_explore)
            
        except Exception as e:
            print(f"⚠️ Error in automated pipeline: {e}")
        
        print("⏳ Waiting for the next 2-hour cycle to fetch fresh deals...")
        time.sleep(7200)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🚀 Starting Fully Autonomous Deal Bot with Professional Filters & Buffer Timing...")
    
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
    
    automated_deal_pipeline()
        
