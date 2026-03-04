import urllib.request
import xml.etree.ElementTree as ET

def fetch_daily_trends() -> str:
    """Fetches current trending topics from a permissionless RSS feed (Google Trends)."""
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    try:
        # User-Agent is required to prevent basic bot blocking
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        # Grab the top 5 trending items
        trends = [item.find('title').text for item in root.findall('.//item')[:5]]
        return ", ".join(trends)
    except Exception as e:
        print(f"Trend fetch failed: {e}")
        return "Dark mysterious horror story." # Fallback trends