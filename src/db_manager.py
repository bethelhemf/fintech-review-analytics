import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load credentials from a .env file
load_dotenv()

class DBManager:
    def __init__(self):
        # Database credentials from environment variables
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASS", "your_password_here")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "omega_banking")
        
        # Create connection string
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(self.connection_string)

    def upload_data(self, csv_path):
        """Reads CSV and pushes to PostgreSQL."""
        try:
            df = pd.read_csv(csv_path)
            
            # We use 'append' so you can add new reviews every month
            df.to_sql('processed_reviews', self.engine, if_exists='append', index=False)
            print(f"Successfully uploaded {len(df)} records to PostgreSQL!")
            
        except Exception as e:
            print(f"Error uploading to database: {e}")