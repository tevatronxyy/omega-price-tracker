import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def get_jomashop_price(reference):
    url = f"https://www.jomashop.com/search?q={reference}"
    
    # Cloud/CI environment tweaks
    options = uc.ChromeOptions()
    options.add_argument('--headless=new') # Updated headless mode
    options.add_argument('--no-sandbox') # Required for GitHub Actions
    options.add_argument('--disable-dev-shm-usage') # Prevents memory limits
    options.add_argument('--window-size=1920,1080') # Helps avoid some bot detection
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(5) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        price_elements = soup.find_all(string=lambda t: t and '$' in t)
        
        for element in price_elements:
            text = element.strip()
            if len(text) > 4 and text.startswith('$') and any(c.isdigit() for c in text):
                return text
                
        return "Price not found (may be out of stock)."
        
    except Exception as e:
        return f"Error: {e}"
        
    finally:
        driver.quit()

if __name__ == "__main__":
    speedmasters = {
        "Hesalite": "310.30.42.50.01.001",
        "Sapphire Sandwich": "310.30.42.50.01.002"
    }
    
    print("Scouting Jomashop for Omega Speedmaster deals...\n")
    
    for model, ref in speedmasters.items():
        print(f"Searching for {model} (Ref. {ref})...")
        price = get_jomashop_price(ref)
        print(f"Best Price Found: {price}\n")
