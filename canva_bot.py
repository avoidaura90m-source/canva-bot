"""
FIXED CANVA BOT FOR TERMUX
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

class CanvaBot:
    def __init__(self):
        print("🚀 Canva Bot Starting...")
        
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--headless=new')
        self.options.binary_location = '/data/data/com.termux/files/usr/bin/chromium'
        
        self.success = 0
        self.failed = 0
        
        # Numbers file path
        self.numbers_file = '/sdcard/Download/numbers.txt'
        
    def check_vpn(self):
        """VPN check with user input"""
        print("\n" + "="*60)
        print("🔴 STEP 1: VPN CONNECT KARO!")
        print("="*60)
        print("🌍 South Africa (ZA) connect karo")
        print("📱 Proton VPN ya koi bhi VPN app use karo")
        print("\n⚠️  BINA VPN KE BOT KAAM NAHI KAREGA!")
        print("="*60)
        input("\n✅ VPN ready? Press Enter to continue...")
        print("👍 Great! Continuing...\n")
        time.sleep(2)
        
    def load_numbers(self):
        """Load numbers from file"""
        if not os.path.exists(self.numbers_file):
            print(f"\n❌ Numbers file nahi mili: {self.numbers_file}")
            print("\n📝 File bana rahe hain...")
            
            # Create numbers file
            with open(self.numbers_file, 'w') as f:
                f.write("71234567\n71234568\n71234569\n")
            print(f"✅ File ban gayi: {self.numbers_file}")
            print("✏️  Edit karo: nano /sdcard/Download/numbers.txt")
            
        # Read numbers
        with open(self.numbers_file, 'r') as f:
            numbers = f.read().strip().split('\n')
            numbers = [n.strip() for n in numbers if n.strip() and not n.startswith('#')]
        
        print(f"\n📊 Total numbers: {len(numbers)}")
        return numbers
        
    def create_driver(self):
        """Create browser driver"""
        try:
            driver = webdriver.Chrome(options=self.options)
            return driver
        except Exception as e:
            print(f"❌ Browser error: {e}")
            return None
            
    def send_otp(self, phone):
        """Send OTP to phone number"""
        driver = self.create_driver()
        if not driver:
            self.failed += 1
            return False
            
        try:
            print(f"   🌐 Opening Canva...")
            driver.get("https://www.canva.com")
            time.sleep(3)
            
            wait = WebDriverWait(driver, 10)
            
            # Click Sign Up
            print("   📍 Clicking Sign Up...")
            signup = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up')]")))
            signup.click()
            time.sleep(2)
            
            # Click Phone
            print("   📍 Selecting Phone...")
            phone_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'phone')]")))
            phone_btn.click()
            time.sleep(2)
            
            # Clean number
            clean = phone.replace("+263", "").replace(" ", "")
            if clean.startswith("0"):
                clean = clean[1:]
                
            # Enter number
            print(f"   📍 Entering: {clean}")
            phone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
            phone_input.send_keys(clean)
            time.sleep(1)
            
            # Click Continue
            print("   📍 Clicking Continue...")
            continue_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_btn.click()
            
            # Wait for OTP
            time.sleep(5)
            
            # Check result
            page = driver.page_source
            if "OTP" in page or "code" in page:
                print(f"   ✅ OTP Sent: {phone}")
                self.success += 1
                result = True
            else:
                print(f"   ❌ Failed: {phone}")
                self.failed += 1
                result = False
                
            driver.quit()
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}")
            self.failed += 1
            driver.quit()
            return False
            
    def run(self):
        """Main function"""
        
        # Step 1: VPN check
        self.check_vpn()
        
        # Step 2: Load numbers
        numbers = self.load_numbers()
        if not numbers:
            print("❌ No numbers to process")
            return
            
        # Step 3: How many to process
        print(f"\n📊 Total numbers available: {len(numbers)}")
        try:
            max_num = input("📈 Kitne process karein? (Enter for 5): ").strip()
            if max_num:
                max_num = int(max_num)
            else:
                max_num = 5
            numbers = numbers[:max_num]
        except:
            numbers = numbers[:5]
            
        print(f"\n🚀 Processing {len(numbers)} numbers...")
        time.sleep(2)
        
        # Step 4: Process each number
        for i, num in enumerate(numbers):
            print(f"\n{'='*50}")
            print(f"📌 [{i+1}/{len(numbers)}] {num}")
            
            # VPN reminder every 3 attempts
            if i > 0 and i % 3 == 0:
                print("\n⏸️ 3 numbers done! VPN change karo?")
                change = input("VPN change kiya? (y/n): ").lower()
                if change == 'y':
                    print("👍 Continuing...")
                else:
                    print("⚠️ Continuing with same VPN")
                    
            # Send OTP
            self.send_otp(num)
            
            # Wait between attempts
            if i < len(numbers) - 1:
                wait = random.randint(30, 45)
                print(f"⏱️ Waiting {wait} seconds...")
                time.sleep(wait)
                
        # Final report
        self.show_report()
        
    def show_report(self):
        """Show final results"""
        print("\n" + "="*50)
        print("📈 FINAL REPORT")
        print("="*50)
        total = self.success + self.failed
        if total > 0:
            print(f"✅ Successful: {self.success}")
            print(f"❌ Failed: {self.failed}")
            print(f"📊 Success Rate: {(self.success/total)*100:.1f}%")
        else:
            print("No attempts made")
            
        # Save results
        try:
            with open("/sdcard/Download/canva_results.txt", "w") as f:
                f.write(f"Success: {self.success}\nFailed: {self.failed}")
            print(f"✅ Results saved")
        except:
            pass

# ============================================
# START
# ============================================

if __name__ == "__main__":
    bot = CanvaBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Bot stopped")
        bot.show_report()
