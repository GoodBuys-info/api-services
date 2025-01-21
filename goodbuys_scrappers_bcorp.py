import csv
import asyncio
from playwright.async_api import async_playwright

async def fetch_all_b_corp_companies(max_pages=20, csv_filename="bcorporation_companies.csv"):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            base_url = "https://www.bcorporation.net/en-us/find-a-b-corp/?page="

            with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['bcorporation'])

                page_num = 1
                while page_num <= max_pages:
                    print(f"Scraping page {page_num}...")
                    await page.goto(f"{base_url}{page_num}")

                    try:
                        await page.wait_for_selector(".ais-Hits-item", timeout=10000)
                    except:
                        print("No more pages or page load failed.")
                        break

                    companies_on_page = await page.eval_on_selector_all(
                        ".ais-Hits-item span[data-testid='company-name-desktop']",
                        "elements => elements.map(el => el.textContent.trim())"
                    )

                    if not companies_on_page:
                        print("No more companies found.")
                        break

                    for company in companies_on_page:
                        writer.writerow([company])

                    page_num += 1

            await browser.close()
            print(f"Data successfully saved to {csv_filename}.")
    except Exception as e:
        print("An error occurred:", e)

def main():
    max_pages = 20
    csv_filename = "bcorporation_companies.csv"
    asyncio.run(fetch_all_b_corp_companies(max_pages=max_pages, csv_filename=csv_filename))

if __name__ == "__main__":
    main()
