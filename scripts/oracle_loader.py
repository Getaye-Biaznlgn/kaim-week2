import pandas as pd
import oracledb

class OracleReviewLoader:
    def __init__(self, user, password, dsn, df:pd.DataFrame):
        self.user=user
        self.password=password
        self.df=df
        self.dsn=dsn
        self.connection=None
        self.bank_map = {}

    def connect(self):
        self.connection =oracledb.connect(user=self.user, password= self.password,dsn=self.dsn)

    def insert_banks(self):
        print(self.df.columns)
        cursor = self.connection.cursor()
        banks = self.df['bank'].unique()
#    
        for name in banks:
            id_var = cursor.var(int)
            cursor.execute(
            "INSERT INTO banks (name) VALUES (:1) RETURNING id INTO :2",
            [name, id_var]
        )
        self.bank_map[name] = id_var.getvalue()[0]

        self.connection.commit()
        print(f"✅ Inserted {self.bank_map} banks.")

    
    def insert_reviews(self):
        cursor = self.connection.cursor()
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        for _, row in self.df.iterrows():
            cursor.execute("""
                INSERT INTO reviews 
                (review, processed_review, sentiment, rating, review_date, bank_id)
                VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6)
            """, (
                row['review'],
                row['processed_review'],
                row['textblob_sentiment'],
                row['rating'] if 'rating' in row else None,
                str(row['date']),
                self.bank_map.get(row['bank'])
            ))

        self.connection.commit()
        print("✅ All reviews inserted into database.")

    def fetch_banks(self):
     if self.connection is None:
        print("❌ No database connection.")
        return

        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM banks ORDER BY id")
        
        rows = cursor.fetchall()
        print("\n📋 Bank Table Records:${rows} ")
        print("-" * 30)
        for row in rows:
          print(f"ID: {row[0]}, Name: {row[1]}")
          print("-" * 30)

        return rows
     
    def close(self):
        if self.connection:
            self.connection.close()
            print("🔒 Oracle connection closed.")