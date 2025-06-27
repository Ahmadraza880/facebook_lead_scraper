import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
import re

# Load environment variables
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_TOKEN:
    st.error("Missing APIFY_API_TOKEN in .env")
    st.stop()

client = ApifyClient(APIFY_TOKEN)

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# --- Phase 1: Scrape Meta Ads ---
def scrape_meta_ads(keyword, country, max_results=50):
    search_url = (
        f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country}"
        f"&q={keyword}&search_type=keyword_unordered&media_type=all"
    )
    run_input = {
        "urls": [{"url": search_url}],
        "count": max_results,
        "scrapePageAds.activeStatus": "active"
    }
    try:
        run = client.actor("curious_coder/facebook-ads-library-scraper").call(run_input=run_input)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            st.error("No dataset ID returned from Apify actor.")
            return pd.DataFrame()

        items = list(client.dataset(dataset_id).iterate_items())
    except Exception as e:
        st.error(f"Failed to scrape Meta ads: {e}")
        return pd.DataFrame()

    seen = set()
    clean = []

    for ad in items:
        page = ad.get("pageName") or ad.get("page_name")
        url = ad.get("pageUrl")
        if not url and page:
            url = f"https://www.facebook.com/{page.replace(' ', '')}"

        ad_text = ad.get("adText", "")
        if not ad_text:
            snapshot = ad.get("snapshot") or {}
            body = snapshot.get("body") or {}
            ad_text = body.get("text", "")

        ad_text = (ad_text or "").strip()

        if (
            not page or
            not ad_text or
            len(ad_text) < 20 or
            "{{" in ad_text or
            re.match(r"^[\W_]+$", ad_text)
        ):
            continue

        if page not in seen:
            clean.append({
                "page_name": page,
                "page_url": url,
                "ad_text": ad_text
            })
            seen.add(page)

    df = pd.DataFrame(clean)
    if not df.empty:
        df.to_csv("results/ads_cleaned.csv", index=False)
    return df

# --- Phase 2: Enrich Facebook Pages ---
def enrich_facebook_pages(df):
    enriched = []
    seen = set()
    for _, row in df.iterrows():
        page_url = row.get("page_url", "").strip()
        if not page_url or page_url in seen:
            continue
        seen.add(page_url)

        try:
            run = client.actor("apify/facebook-pages-scraper").call(
                run_input={
                    "startUrls": [{"url": page_url, "method": "GET"}],
                    "scrapePosts": False,
                    "scrapeReviews": False,
                    "scrapeAbout": True
                }
            )
            dataset_id = run.get("defaultDatasetId")
            if not dataset_id:
                continue
            items = list(client.dataset(dataset_id).iterate_items())
            if items:
                data = items[0]
                enriched.append({
                    **row,
                    "phone": data.get("phone", ""),
                    "email": data.get("email", ""),
                    "website": data.get("website", "")
                })
        except Exception as e:
            st.warning(f"Failed to enrich {page_url}: {e}")

    enriched_df = pd.DataFrame(enriched)
    if not enriched_df.empty:
        enriched_df.to_csv("results/enriched_pages.csv", index=False)
    return enriched_df

# --- Streamlit UI ---
st.set_page_config(page_title="Lead Gen Scraper", layout="centered")
st.title("📊 Lead Generation Automation Tool")

st.header("🔍 Scraper Settings")
keyword = st.text_input("Enter keyword", "marketing")
country = st.text_input("2-letter country code", "US")
max_ads = st.slider("Number of ads to fetch", 10, 100, 50)

st.header("🚀 Run Full Pipeline")
if st.button("▶️ Run Full Pipeline"):
    with st.spinner("Running Phase 1: Scraping Meta Ads..."):
        ads_df = scrape_meta_ads(keyword, country, max_ads)
        if ads_df.empty:
            st.error("Phase 1 failed: No ads scraped. Stopping pipeline.")
            st.stop()
        st.success(f"Phase 1: Scraped {len(ads_df)} ads")
        st.dataframe(ads_df)
        st.download_button("⬇️ Download ads_cleaned.csv", ads_df.to_csv(index=False), file_name="ads_cleaned.csv")

    with st.spinner("Running Phase 2: Enriching Facebook Pages..."):
        enriched_df = enrich_facebook_pages(ads_df)
        st.success(f"Phase 2: Enriched {len(enriched_df)} pages")
        st.dataframe(enriched_df)
        st.download_button("⬇️ Download enriched_pages.csv", enriched_df.to_csv(index=False), file_name="enriched_pages.csv")

st.header("🔍 Phase 1: Scrape Meta Ads")
if st.button("▶️ Run Meta Ads Scraper"):
    with st.spinner("Scraping Meta Ads..."):
        ads_df = scrape_meta_ads(keyword, country, max_ads)
        if not ads_df.empty:
            st.success(f"Scraped {len(ads_df)} ads")
            st.dataframe(ads_df)
            st.download_button("⬇️ Download ads_cleaned.csv", ads_df.to_csv(index=False), file_name="ads_cleaned.csv")
        else:
            st.error("No ads scraped.")

st.header("📥 Phase 2: Enrich Facebook Pages")
uploaded_file = st.file_uploader("Upload ads_cleaned.csv (or use above results)", type=["csv"])

if st.button("🚀 Enrich Pages"):
    if uploaded_file:
        df_to_enrich = pd.read_csv(uploaded_file)
    elif os.path.exists("results/ads_cleaned.csv"):
        df_to_enrich = pd.read_csv("results/ads_cleaned.csv")
    else:
        st.error("❌ Please upload a CSV or run Phase 1 first.")
        st.stop()

    with st.spinner("Running enrichment via Facebook page scraper..."):
        enriched_df = enrich_facebook_pages(df_to_enrich)
        if not enriched_df.empty:
            st.success(f"Enriched {len(enriched_df)} pages")
            st.dataframe(enriched_df)
            st.download_button("⬇️ Download enriched_pages.csv", enriched_df.to_csv(index=False), file_name="enriched_pages.csv")
        else:
            st.error("No pages enriched.")