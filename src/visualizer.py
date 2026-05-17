import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    def __init__(self, data_path='data/final_analytics_results.csv'):
        self.df = pd.read_csv(data_path)
        # Set a professional style
        sns.set_theme(style="whitegrid")
        os.makedirs('reports/figures', exist_ok=True)

    def plot_sentiment_distribution(self):
        """Stacked Bar Chart of Sentiment by Bank."""
        plt.figure(figsize=(10, 6))
        # Group data
        sent_counts = self.df.groupby(['bank', 'sentiment_label']).size().unstack().fillna(0)
        sent_pct = sent_counts.div(sent_counts.sum(axis=1), axis=0) * 100
        
        sent_pct.plot(kind='bar', stacked=True, color=['#e74c3c', '#95a5a6', '#2ecc71'])
        plt.title('Sentiment Distribution Across Ethiopian Banks', fontsize=14)
        plt.ylabel('Percentage (%)')
        plt.legend(title='Sentiment')
        plt.savefig('reports/figures/sentiment_dist.png')
        print("✅ Saved Sentiment Distribution Chart")

    def plot_theme_frequency(self):
        """Horizontal Bar Chart of dominant themes."""
        plt.figure(figsize=(12, 7))
        theme_counts = self.df.groupby(['bank', 'identified_theme']).size().reset_index(name='count')
        
        sns.barplot(data=theme_counts, x='count', y='identified_theme', hue='bank', palette='viridis')
        plt.title('Dominant Feedback Themes by Bank', fontsize=14)
        plt.xlabel('Number of Reviews')
        plt.savefig('reports/figures/theme_frequency.png')
        print("✅ Saved Theme Frequency Chart")

    def plot_rating_boxplots(self):
        """Rating Distribution Boxplot."""
        plt.figure(figsize=(10, 5))
        sns.boxplot(data=self.df, x='bank', y='rating', palette='Set2')
        plt.title('User Rating Distribution (1-5 Stars)', fontsize=14)
        plt.savefig('reports/figures/rating_boxplot.png')
        print("✅ Saved Rating Distribution Chart")
    def plot_sentiment_trend(self):
        """Line chart showing sentiment trend over time."""
        plt.figure(figsize=(12, 6))
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Resample to monthly and calculate mean sentiment
        # Map: POSITIVE=1, NEUTRAL=0, NEGATIVE=-1
        mapping = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
        self.df['sent_val'] = self.df['sentiment_label'].map(mapping)
        
        trend = self.df.groupby([pd.Grouper(key='date', freq='ME'), 'bank'])['sent_val'].mean().unstack()
        
        trend.plot(marker='o', linewidth=2)
        plt.title('Monthly Sentiment Trend (Average Score)', fontsize=14)
        plt.ylabel('Mean Sentiment (-1 to 1)')
        plt.axhline(0, color='black', linestyle='--', alpha=0.3)
        plt.savefig('reports/figures/sentiment_trend.png')
        print("✅ Saved Sentiment Trend Chart")