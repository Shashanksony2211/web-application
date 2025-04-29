# import random
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import undetected_chromedriver as uc

# # Your target link
# link = "https://www.meesho.com/s/p/8r9kyb?utm_source=s_w"

# # Example proxy list (you need 1000 working proxies)
# proxies_list = [
#     "103.87.236.233:45557",
#     "194.233.65.205:443",
#     "47.242.225.165:999",
#     # Add up to 1000 proxies here
# ]


# def start_browser(proxy):
#     options = uc.ChromeOptions()
#     options.add_argument(f"--proxy-server=http://{proxy}")
#     options.add_argument("--headless")  # Run without opening a window
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = uc.Chrome(options=options)
#     return driver


# def visit_link_with_proxy(proxy):
#     try:
#         driver = start_browser(proxy)
#         driver.get(link)
#         time.sleep(3)  # wait for page to load

#         # Simulate a click on the page (if needed)
#         try:
#             # Example: click on the body
#             driver.find_element(By.TAG_NAME, "body").click()
#             print(f"Clicked on page using proxy {proxy}")
#         except Exception as e:
#             print(f"No clickable element found: {e}")

#         driver.quit()
#     except Exception as e:
#         print(f"Failed to open with proxy {proxy}: {e}")


# # Visit using 1000 proxies
# for i in range(1000):
#     proxy = random.choice(proxies_list)
#     print(f"[{i+1}] Using proxy: {proxy}")
#     visit_link_with_proxy(proxy)
#     time.sleep(5)  # wait 5 seconds before next click
