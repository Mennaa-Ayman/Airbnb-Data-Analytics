# Airbnb Data Analytics

Data analysis project for **Airbnb Cairo rentals**. The repository explores rental features, ratings, review sentiment, and pricing to better understand **guest experience**, **market behavior** and **optimize rental pricing strategies**.

## Features
- Loading rentals records using **Apify Airbnb Scrapper**, then using **Selenium** for extracting reviews and more rental features
- Data cleaning — handling missing values, formatting inconsistencies, and filtering irrelevant features
- Features Extraction from rental description and title using **ollama** and boolean features extraction using **`Spacy`**
- Generate **charts** and **heatmaps** to visualize sentiment, pricing, and feature distributions
- Perform **sentiment analysis** on guest reviews
- **Regression model** to predict rental prices

## Repository Structure
- `Data/` — datasets used in the analysis (raw/cleaned).
- `Scrapper/` — Using selenium to extract rental features and user reviews.
- `Cleaning/` — cleaning scrabbed data (e.g., handling nulls, filtering columns, handling datatypes)
- `nlp/` — NLP notebooks (e.g., features extraction from rental description text, reviews analysis).
- `Analysis/` — Prices analysis with location, ratings and rental features.
- `Plots/`  — Analysis outputs
- `Models/` — Regression models for predicting price based on rental features.
- `Streamlit_Gui/` — Dashboard for presenting the data cleaning and using the model

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Mennaa-Ayman/Airbnb-Data-Analytics.git
   cd Airbnb-Data-Analytics
   ```
2. (Recommended) Create and activate a virtual environment.

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the gui:

   ```bash
   python .\streamlit_gui\main.py
   streamlit run .\streamlit_gui\main.py
   ```

