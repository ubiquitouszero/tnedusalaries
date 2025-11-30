import asyncio
from playwright.async_api import async_playwright
import sqlite3
import re
import time
import os

DB_PATH = "salary_db.sqlite"
URL = "https://data.tennessee.edu/"

async def scrape_ut_system():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Navigating to {URL}...")
        await page.goto(URL)
        
        try:
            await page.get_by_text("Explore Dashboards").click()
            print("Clicked 'Explore Dashboards'")
        except:
            print("Could not find 'Explore Dashboards'")
        
        try:
            await page.wait_for_timeout(5000)
            await page.get_by_text("Human Resources", exact=False).first.click()
            print("Clicked 'Human Resources'")
        except Exception as e:
            print(f"Error clicking HR: {e}")
            
        try:
            await page.wait_for_timeout(5000)
            await page.get_by_text("Salary", exact=False).first.click()
            print("Clicked 'Salary Dashboard'")
        except Exception as e:
            print(f"Error clicking Salary: {e}")

        await page.wait_for_timeout(10000)
        
        frames = page.frames
        powerbi_frame = None
        for frame in frames:
            if "powerbi" in frame.url or "app.powerbi.com" in frame.url:
                powerbi_frame = frame
                break
        
        if not powerbi_frame:
            iframe_element = await page.query_selector("iframe")
            if iframe_element:
                powerbi_frame = await iframe_element.content_frame()
        
        target_frame = powerbi_frame if powerbi_frame else page
        print(f"Using frame: {target_frame.url}")
        
        extracted_data = []
        
        for i in range(50): # Increased to 50
            print(f"Scraping page {i+1}...")
            await page.wait_for_timeout(3000)
            
            rows = await target_frame.get_by_role("row").all()
            if not rows:
                rows = await target_frame.locator(".row").all()
            
            print(f"Found {len(rows)} rows.")
            
            page_data = []
            for row in rows:
                text = await row.inner_text()
                parts = text.split('\n')
                if len(parts) >= 3:
                    salary_str = parts[-1]
                    if '$' in salary_str:
                        try:
                            salary = float(salary_str.replace('$', '').replace(',', ''))
                            name = parts[0]
                            rank = parts[1] if len(parts) > 1 else ""
                            dept = parts[2] if len(parts) > 2 else ""
                            page_data.append((name, rank, "UT System", dept, salary, 2024, "UT System Web"))
                        except:
                            pass
            
            extracted_data.extend(page_data)
            save_to_db(page_data)
            
            # Try to click Next
            next_clicked = False
            try:
                # Try aria-label
                next_btn = target_frame.get_by_label("Next", exact=False)
                if await next_btn.count() > 0:
                    await next_btn.first.click()
                    next_clicked = True
                    print("Clicked Next (aria-label)")
                else:
                    # Try class
                    chevrons = await target_frame.locator("i.glyphicon-chevron-right, .pbi-glyph-chevron-right").all()
                    if chevrons:
                        await chevrons[-1].click()
                        next_clicked = True
                        print("Clicked Next (chevron class)")
            except Exception as e:
                print(f"Error clicking next: {e}")
            
            if not next_clicked:
                print("Could not find Next button. Stopping.")
                break
                
        await browser.close()

def save_to_db(data):
    if not data: return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Use INSERT OR IGNORE if we had a unique constraint, but we don't.
    # We might duplicate data if we re-run.
    c.executemany('''
        INSERT INTO salaries (name, rank, organization, department, salary, year, source, original_source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(d[0], d[1], d[2], d[3], d[4], d[5], d[6], "Web Scrape") for d in data])
    conn.commit()
    conn.close()
    print(f"Saved {len(data)} records.")

if __name__ == "__main__":
    asyncio.run(scrape_ut_system())
