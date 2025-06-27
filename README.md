# 📊 Facebook Lead Scraper

**Automated Lead Generation from Facebook Ads Library using Apify and Streamlit**

---

## 🔍 Overview

`facebook-lead-scraper` is a powerful tool designed to automate the process of discovering and enriching Facebook business leads. It scrapes Facebook Ads Library using the [Apify platform](https://apify.com) and enhances the results with valuable contact details like email, phone number, and website. A Streamlit-powered UI is included for a smooth and simple user experience.

---

## 🚀 Features

* 🔎 **Phase 1**: Scrape active ads from Facebook Ads Library using a keyword and country.
* 🧹 **Phase 1 Cleaning**: Filters and cleans data to remove irrelevant or duplicate entries.
* 📬 **Phase 2**: Enriches Facebook pages with business contact information.
* 🖥️ **Streamlit App**: Complete visual interface to run the full pipeline or each phase separately.
* 💾 **Exportable Results**: Save cleaned and enriched leads as CSV files.

---

## 🧰 Technologies Used

* Python 3.9+
* [Apify SDK](https://docs.apify.com/) and `apify-client`
* Streamlit for interactive UI
* Pandas for data manipulation
* Dotenv for environment variable management

---

## 🏗️ Project Structure

```
facebook-lead-scraper/
├── results/                    # Auto-generated results
│   ├── ads_cleaned.csv         # Output from Phase 1
│   └── enriched_pages.csv      # Output from Phase 2
├── phase1_apify_client.py     # CLI script for scraping ads
├── phase2_enrich_pages.py     # CLI script for enriching pages
├── app.py                     # Combined Streamlit application
├── .env                       # Environment variable file (contains APIFY_API_TOKEN)
└── README.md                  # Project documentation
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/facebook-lead-scraper.git
cd facebook-lead-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
APIFY_API_TOKEN=your_apify_api_token_here
```

> 🔑 You can get your API token from [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)

---

## ▶️ How to Use

### Run via Streamlit

```bash
streamlit run app.py
```

### Run CLI Scripts Individually

* Phase 1: Scrape Facebook Ads

  ```bash
  python phase1_apify_client.py
  ```
* Phase 2: Enrich Facebook Pages

  ```bash
  python phase2_enrich_pages.py
  ```

---

## 📎 Example Use Case

Let’s say you want to generate leads for **digital marketing agencies** in the **United States**:

1. Run Phase 1 with keyword `digital marketing` and country code `US`.
2. The scraper fetches active Facebook ads and saves the advertiser info.
3. Run Phase 2 to fetch contact details from each page.
4. Export the enriched list for outreach campaigns.

---

## 📌 Notes

* Apify limits free tier executions. Use with appropriate delays or upgrade for high-volume scraping.
* Facebook sometimes blocks or throttles page data; results may vary by region and availability.

---

## 📫 Contact

If you have questions, feature requests, or would like to collaborate:

**👤 Ahmad Raza**
📧 [ranaahmadraza7863@gmail.com](mailto:ranaahmadraza7863@gmail.com) 
🌐 [LinkedIn](https://www.linkedin.com/in/ahmad-raza-403bbd0278/)

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

Made with ❤️ by Ahmad Raza
