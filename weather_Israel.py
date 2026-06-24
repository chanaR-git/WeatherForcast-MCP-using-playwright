import re

from mcp.server.fastmcp import FastMCP
from playwright.async_api import TimeoutError as PlaywrightTimeout
from playwright.async_api import async_playwright, Browser, Page


mcp = FastMCP("weather-Israel")

FORECAST_URL = "https://www.weather2day.co.il/forecast"

# Global variables to maintain browser session across tool calls
browser_instance: Browser | None = None
page_instance: Page | None = None


@mcp.tool()
async def open_weather_forecast_israel() -> dict:
    """Open browser and navigate to Israel weather forecast page.
    
    Returns:
        dict: Operation result with open and ready page for further queries
    """
    global browser_instance, page_instance
    
    try:
        playwright = await async_playwright().start()
        browser_instance = await playwright.chromium.launch()
        page_instance = await browser_instance.new_page()
        
        # Navigate to weather forecast website
        await page_instance.goto(FORECAST_URL, wait_until="networkidle")
        
        # Wait for page load
        await page_instance.wait_for_load_state("networkidle")
        
        return {
            "status": "success",
            "message": f"Browser opened successfully and navigated to {FORECAST_URL}",
            "url": FORECAST_URL,
            "page_loaded": True
        }
            
    except PlaywrightTimeout as e:
        return {
            "status": "error",
            "message": f"Timeout error: {str(e)}",
            "error_type": "timeout"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error opening browser: {str(e)}",
            "error_type": "general"
        }


@mcp.tool()
async def enter_weather_forecast_city_israel(city_name: str) -> dict:
    """Enter city name in the weather forecast search field.
    
    Args:
        city_name: Name of the city to search for weather forecast
        
    Returns:
        dict: Operation result with city entered and search ready
    """
    global page_instance
    
    if page_instance is None:
        return {
            "status": "error",
            "message": "Page not initialized. Call open_weather_forecast_israel first.",
            "error_type": "page_not_initialized"
        }
    
    try:
        # Find and fill the city search input field
        # Common selectors for search inputs on weather websites
        search_selectors = [
            "input[placeholder*='עיר']",  # Hebrew: city
            "input[placeholder*='City']",
            "input[type='text'][placeholder*='search']",
            "input[name='city']",
            "input[id='city']",
            "input[id*='search']",
            "#searchInput",
            ".search-input",
            "input[autocomplete='off']"
        ]
        
        input_field = None
        for selector in search_selectors:
            try:
                input_field = page_instance.locator(selector).first
                # Check if element exists
                if await input_field.is_visible():
                    break
            except:
                continue
        
        if input_field is None:
            return {
                "status": "error",
                "message": f"Could not find search input field on the page",
                "error_type": "selector_not_found"
            }
        
        # Clear any existing text and enter the city name
        await input_field.fill("")
        await input_field.fill(city_name)
        
        # Wait a bit for autocomplete suggestions to appear if any
        await page_instance.wait_for_timeout(1000)
        
        return {
            "status": "success",
            "message": f"City '{city_name}' entered successfully in search field",
            "city_name": city_name,
            "ready_for_search": True
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error entering city name: {str(e)}",
            "error_type": "general",
            "city_name": city_name
        }


@mcp.tool()
async def select_weather_forecast_city_israel() -> dict:
    """Select the first item from the city suggestions list.
    
    Returns:
        dict: Operation result with selected city
    """
    global page_instance
    
    if page_instance is None:
        return {
            "status": "error",
            "message": "Page not initialized. Call open_weather_forecast_israel first.",
            "error_type": "page_not_initialized"
        }
    
    try:
        # Common selectors for dropdown/suggestion items
        dropdown_selectors = [
            "ul li",  # Generic unordered list item
            ".dropdown-item",
            ".suggestion-item",
            "[role='option']",
            ".autocomplete-item",
            "div[class*='suggestion']",
            "div[class*='dropdown']",
            ".city-item",
            "a[class*='city']"
        ]
        
        first_item = None
        for selector in dropdown_selectors:
            try:
                items = page_instance.locator(selector)
                count = await items.count()
                if count > 0:
                    first_item = items.first
                    # Check if element is visible
                    if await first_item.is_visible():
                        break
            except:
                continue
        
        if first_item is None:
            return {
                "status": "error",
                "message": "Could not find city suggestions dropdown",
                "error_type": "dropdown_not_found"
            }
        
        # Get the text of the first item before selecting it
        item_text = await first_item.text_content()
        
        # Click on the first item
        await first_item.click()
        
        # Wait for selection to process
        await page_instance.wait_for_timeout(1000)
        
        return {
            "status": "success",
            "message": f"First city item selected: '{item_text.strip()}'",
            "selected_city": item_text.strip(),
            "ready_for_forecast": True
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error selecting city from list: {str(e)}",
            "error_type": "general"
        }


def clean_text(raw_text: str) -> str:
    """Clean page text by removing scripts, styles, extra whitespace, and non-content characters."""
    text = re.sub(r"<script.*?>.*?</script>", "", raw_text, flags=re.S | re.I)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


@mcp.tool()
async def extract_page_context_for_llm() -> dict:
    """Extract page content, clean it, and return context-ready text for an LLM."""
    global page_instance

    if page_instance is None:
        return {
            "status": "error",
            "message": "Page not initialized. Call open_weather_forecast_israel first.",
            "error_type": "page_not_initialized"
        }

    try:
        raw_html = await page_instance.content()
        cleaned_text = clean_text(raw_html)

        # Truncate if extremely long, but keep enough content for LLM context
        snippet = cleaned_text[:32000]

        return {
            "status": "success",
            "message": "Page content extracted and cleaned for LLM context.",
            "context_text": snippet,
            "text_length": len(snippet)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting page content: {str(e)}",
            "error_type": "general"
        }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
