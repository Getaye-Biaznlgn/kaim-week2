from google_play_scraper import reviews, Sort
import pandas as pd
import time
from typing import List, Dict


class BankReviewScraper:
    def __init__(self, apps: List[Dict[str, str]], limit_per_bank: int = 400):
        self.apps = apps
        self.limit = limit_per_bank
        self.lang = 'en'
        self.country = 'us'
        self.all_data = []

    def scrape_reviews_for_app(self, app_id: str, bank_name: str) -> pd.DataFrame:
    
        all_reviews = []
        next_token = None

        while len(all_reviews) < self.limit:
            count = min(200, self.limit - len(all_reviews))
            try:
                result, next_token = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count,
                    continuation_token=next_token
                )
                all_reviews.extend(result)

                if not next_token:
                    break
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error scraping {bank_name}: {e}")
                break

        df = pd.DataFrame(all_reviews)
        if df.empty:
            print(f"⚠️ No reviews found for {bank_name}.")
            return df
      
        df = df[['userName', 'content', 'score', 'at',]]
        df.columns = ['user', 'review', 'rating', 'date']
        df['bank'] = bank_name
        df['source'] = 'Google Play'
        return df

    def scrape_all_banks(self):
        for app in self.apps:
            df = self.scrape_reviews_for_app(app["app_id"], app["bank"])
            if not df.empty:
                self.all_data.append(df)
            

    def save_to_csv(self, filename: str = "bank_reviews_raw.csv")-> pd.DataFrame:
        if self.all_data:
         try:
           final_df = pd.concat(self.all_data, ignore_index=True)
           final_df.to_csv(filename, index=False)
           print(f"Length from save_to_csv = {len(final_df)}")
           print(f"✅ Merged data saved to {filename} with {len(final_df)} total reviews.")
         except Exception as e:
            print(f"❌ Error saving to CSV: {e}")

        else:
            print("❌ No data to save.")
        return final_df;  

    def preprocess_reviews_and_save(self, df: pd.DataFrame, filename: str = "bank_reviews_clean.csv") -> pd.DataFrame:
        # Drop duplicates based on review content
        df.drop_duplicates(subset='review', inplace=True)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Normalize date to YYYY-MM-DD
        df['date'] = pd.to_datetime(df['date']).dt.date
        df.to_csv(filename, index=False)
        return df
       