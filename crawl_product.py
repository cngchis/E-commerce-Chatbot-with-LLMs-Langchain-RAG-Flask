import random
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

# declare browser driver
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)

# open URL
driver.get(
    "https://www.lazada.vn/catalog/?spm=a2o4n.tm80243110.cate_1.9.2e33XEXiXEXiS4&q=Monitors&from=hp_categories&src=all_channel"
)
sleep(random.randint(3, 6))

# Get product links
elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
title = [elem.text for elem in elems]
links = [elem.get_attribute("href") for elem in elems]
# Get Price
elms_price = driver.find_elements(By.CSS_SELECTOR, ".aBrP0")
price = [elm.text for elm in elms_price]
loc_elms = driver.find_elements(By.CSS_SELECTOR, ".oa6ri")
location = [loc.text for loc in loc_elms]


# loop through all pagination
def getCommentsItem(link):
    driver.get(link)
    page = 1
    all_stars, all_names, all_times, all_contents, all_sku = [], [], [], [], []
    while True:
        try:
            print(f"Crawling page" + str(page))
            # Find all comment items
            comments = driver.find_elements(By.CSS_SELECTOR, ".item")
            for item in comments:
                # Star rating
                stars = len(item.find_elements(By.CSS_SELECTOR, ".star"))
                all_stars.append(stars)
                # Reviewer name
                name = item.find_element(By.CSS_SELECTOR, ".reviewer").text.strip()
                all_names.append(name)

                # Time
                time_text = item.find_element(By.CSS_SELECTOR, ".time").text.strip()
                all_times.append(time_text)

                # Content
                content = item.find_element(
                    By.CSS_SELECTOR, ".item-content-main-content-reviews"
                ).text.strip()
                all_contents.append(content)

                # SKU Info
                sku = item.find_element(
                    By.CSS_SELECTOR, ".item-content-main-content-skuInfo"
                ).text.strip()
                all_sku.append(sku)

            # Click next page

            # Click next page
            try:
                # Wait for the next button to be present
                next_button = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.ant-pagination-next"))
                )

                # Check if it is disabled
                if "ant-pagination-disabled" in next_button.get_attribute("class"):
                    print("Pagination reached the end (disabled 'Next' button).")
                    break

                # Try to click the button or the link inside it
                try:
                    btn_to_click = next_button.find_element(By.TAG_NAME, "button")
                    btn_to_click.click()
                except:
                    next_button.click()

                sleep(random.randint(3, 5))

                # Handle potential popup
                try:
                    close_btn = driver.find_element(By.XPATH,
                                                    "//div[@class='next-dialog-close']")  # Example robust class, fallback to generic if needed
                    # If the specific class isn't known, we might keep the old xpath as a fallback or use a better one if we knew it.
                    # For now, let's keep a generic close attempt or the original if it was working for them (though it was absolute).
                    # The original was: "/html/body/div[7]/img". Let's try to be slightly smarter but keep it simple.
                    # close_btn = driver.find_element("xpath", "/html/body/div[7]/img")
                    # Better to use a try-except block with a short timeout if we want to be safe, but let's stick to the main task: pagination.
                except:
                    pass  # Popup handling is secondary to the crash

                # Re-add the popup closing logic from original code but safer
                try:
                    close_btn = driver.find_element(By.XPATH,
                                                    "//img[contains(@src, 'close') or contains(@class, 'close')]")
                    close_btn.click()
                    print("Closed a popup.")
                    sleep(random.randint(1, 3))
                except:
                    pass

                page += 1
            except (TimeoutException, ElementNotInteractableException):
                print("No more pages or cannot find next button. Ending pagination.")
                break
            except Exception as e:
                print(f"Error during pagination: {e}")
                break
        except Exception:
            break
    df = pd.DataFrame(
        {
            "Link_Item": link,
            "Star_Rating": all_stars,
            "User_Comment": all_names,
            "Time": all_times,
            "Content": all_contents,
            "SKU_Info": all_sku,
        }
    )
    return df


df_products = pd.DataFrame(
    list(zip(title, price, links, location)),
    columns=["Title", "Price", "Link_Item", "Location"],
)
df_products.to_csv("./data/csv/products.csv", index=False, encoding="utf-8-sig")
print("Product details saved to products.csv")

# Crawl all products
df_list = []
for link in links:
    df = getCommentsItem(link)
    df_list.append(df)

# Combine all products
df_all = pd.concat(df_list, ignore_index=True)
df_all.to_csv("./data/csv/summary.csv", index=False, encoding="utf-8-sig")
print("Crawling finished. Saved to reviews_all.csv")

driver.quit()
