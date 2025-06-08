# Google Play Store Bank Reviews Scraper

A Python-based tool for scraping and analyzing bank app reviews from the Google Play Store. This project helps collect and process user reviews for banking applications, enabling data-driven insights into user experiences and feedback.

## Features

- Scrapes reviews from multiple banking apps simultaneously
- Configurable review limits per bank
- Handles pagination and rate limiting
- Exports data in CSV format
- Includes data preprocessing capabilities
- Supports both raw and cleaned data exports

## Project Structure

```
.
├── data/               # Directory for storing scraped data
├── notebooks/         # Jupyter notebooks for analysis
├── scripts/          # Python scripts for scraping
├── tests/            # Test files
└── requirements.txt  # Project dependencies
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .scraper
   ```
3. Activate the virtual environment:
   - Windows: `.scraper\Scripts\activate`
   - Unix/MacOS: `source .scraper/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure the bank apps to scrape in your script:
   ```python
   app_configs = [
       {"bank": "Bank Name", "app_id": "com.bank.appid"},
       # Add more banks as needed
   ]
   ```

2. Initialize and run the scraper:
   ```python
   from scripts.bank_review_scraper import BankReviewScraper
   
   scraper = BankReviewScraper(apps=app_configs, limit_per_bank=400)
   scraper.scrape_all_banks()
   scraper.save_to_csv("data/bank_reviews_raw.csv")
   ```

3. For cleaned data:
   ```python
   df = scraper.preprocess_reviews_and_save(df, "data/bank_reviews_clean.csv")
   ```

## Data Format

The scraper collects the following information for each review:
- User name
- Review content
- Rating (1-5 stars)
- Date
- Bank name
- Source (Google Play)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
