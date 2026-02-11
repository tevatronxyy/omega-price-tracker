import time
import subprocess
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def get_chrome_major_version():
    """Detects the installed Chrome major version on the Linux runner."""
    try:
        # Asks the OS for the Chrome version (e.g., "Google Chrome 144.0.7559.0")
        output = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        version_str = output.strip().split()[-1]
        major_version = int(version_str.split('.')[0])
        return major_version
    except Exception:
        return None

def get_jomashop_price(reference):
    url = f"https://www.jomashop.com/search?q={reference}"
    
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Grab the exact version installed on the GitHub server
    chrome_version = get_chrome_major_version()
    
    # Pass the version_main argument so it doesn't download the wrong driver
    if chrome_version:
        driver = uc.Chrome(options=options, version_main=chrome_version)
    else:
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
