from src.db_manager import DBManager
import os

def main():
    # Path to the file created by your NLP pipeline
    final_csv = 'data/final_analytics_results.csv'
    
    if os.path.exists(final_csv):
        db = DBManager()
        db.upload_data(final_csv)
    else:
        print("Final CSV not found. Please wait for the NLP pipeline to finish.")

if __name__ == "__main__":
    main()