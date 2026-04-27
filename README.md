# Airbnb Data Analytics

Data analysis project focused on **Airbnb Cairo rentals**. The repository explores rental pricing, review sentiment, and other signals to better understand guest experience and market behavior.

## Project Overview
This project contains notebooks and scripts that:
- Load and explore Airbnb rentals and reviews datasets.
- Perform **NLP / sentiment analysis** on guest reviews.
- Visualize sentiment distribution and insights that may relate to rental pricing.

## Repository Structure
- `Data/` — datasets used in the analysis (raw/processed depending on your setup).
- `nlp/` — NLP notebooks (e.g., review analysis).
- `*.ipynb` — Jupyter notebooks for exploration and reporting.

## Reviews Sentiment Analysis (NLP)
The notebook `nlp/Reviews_Analysis.ipynb` performs:
- Loading the reviews dataset.
- Computing sentiment scores (e.g., using TextBlob polarity).
- Classifying reviews into **Positive / Neutral / Negative**.
- Plotting the distribution of sentiment.

### Output 
Below is the sentiment distribution chart generated in the notebook:

![Guest Satisfaction Level](files/nlp/chart.png)


## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Mennaa-Ayman/Airbnb-Data-Analytics.git
   cd Airbnb-Data-Analytics
   ```
2. (Recommended) Create and activate a virtual environment.
3. Install dependencies (example):
   ```bash
   pip install pandas numpy matplotlib textblob
   ```
4. Open and run notebooks:
   ```bash
   jupyter notebook
   ```

## Notes
- File paths in notebooks may assume a specific folder layout. Adjust paths if your data is stored elsewhere.
- Some notebooks may have been authored in Google Colab; local execution may require small path changes.
