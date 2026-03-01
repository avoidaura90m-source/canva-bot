"""
====================================
CANVA OTP BOT FOR TERMUX
====================================
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
        
    def create_driver(self):
        try:
            driver = webdriver.Chrome(options=self.options)
            return driver
        except:
            return None
            
    def send_otp(self, phone):
        driver = self.create_driver()
        if not driver:
            return False
            
        try:
            print(f"📱 Processing: {phone}")
            driver.get("https://www.canva.com")
            time.sleep(3)
            
            wait = WebDriverWait(driver, 10)
            
            # Click Sign Up
            signup = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up')]")))
            signup.click()
            time.sleep(2)
            
            # Click Phone
            phone_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'phone')]")))
            phone_btn.click()
            time.sleep(2)
            
            # Enter number
            clean = phone.replace("+263", "").replace(" ", "")
            if clean.startswith("0"):
                clean = clean[1:]
                
            phone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
            phone_input.send_keys(clean)
            time.sleep(1)
            
            # Continue
            continue_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_btn.click()
            
            time.sleep(5)
            
            print(f"✅ OTP Sent: {phone}")
            self.success += 1
            driver.quit()
            return True
            
        except:
            print(f"❌ Failed: {phone}")
            self.failed += 1
            driver.quit()
            return False
            
    def run(self, numbers):
        for i, num in enumerate(numbers[:10]):
            print(f"\n📌 [{i+1}/10]")
            self.send_otp(num)
            
            if i < 9:
                time.sleep(random.randint(30, 45))
                
        print(f"\n✅ Success: {self.success}")
        print(f"❌ Failed: {self.failed}")

if __name__ == "__main__":
    print("First connect VPN then run")
    numbers = ["71234567", "71234568", "71234569"]
    bot = CanvaBot()
    bot.run(numbers)
