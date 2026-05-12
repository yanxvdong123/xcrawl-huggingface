"""
XCrawl Scraper — Hugging Face Space Demo

A Streamlit demo app that shows XCrawl's web scraping capabilities.
"""

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="XCrawl Web Scraper Demo",
    page_icon="🕷️",
    layout="centered",
)

st.title("🕷️ XCrawl Web Scraper Demo")
st.markdown("Enter a URL to scrape it using XCrawl Proxy API.")

# API Key
api_key = st.text_input(
    "XCrawl API Key",
    type="password",
    help="Get your API key at https://dash.xcrawl.com",
)

# URL input
url = st.text_input("URL to scrape", placeholder="https://example.com")

# Options
col1, col2 = st.columns(2)
with col1:
    format = st.selectbox("Output format", ["markdown", "json", "text", "html"])
with col2:
    wait_for = st.number_input("Wait (ms)", min_value=0, max_value=10000, value=0)

if st.button("🚀 Scrape", type="primary") and url and api_key:
    with st.spinner(f"Scraping {url}..."):
        try:
            response = requests.post(
                "https://api.xcrawl.com/v1/scrape",
                json={"url": url, "format": format, "waitFor": wait_for},
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            st.success("✅ Scrape successful!")

            content = data.get("content", json.dumps(data, indent=2))

            if format == "json":
                st.json(data)
            else:
                st.text_area("Content", content, height=400)

            # Show metadata
            with st.expander("📊 Metadata"):
                meta = data.get("metadata", {})
                st.json(meta)

        except Exception as e:
            st.error(f"❌ Error: {e}")

elif st.button("🚀 Scrape"):
    if not api_key:
        st.warning("Please enter your API key")
    if not url:
        st.warning("Please enter a URL to scrape")

st.markdown("---")
st.markdown("Powered by [XCrawl Proxy](https://xcrawl.com)")
