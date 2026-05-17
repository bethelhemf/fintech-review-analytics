from src.db_manager import DBManager
def main():
    db = DBManager()
    db.setup_database()
    db.upload_reviews('data/final_analytics_results.csv')

if __name__ == "__main__":
    main()