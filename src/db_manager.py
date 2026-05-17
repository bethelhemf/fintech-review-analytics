import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
class DBManager:
    def __init__(self):
        self.engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}")
    def upload_reviews(self, csv_path):
        df = pd.read_csv(csv_path)
        df.to_sql('reviews', self.engine, if_exists='append', index=False)
        print("🚀 Data uploaded to PostgreSQL")
