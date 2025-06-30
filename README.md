# Football_Prediction_Website
# ⚽ EPL Predictor Guru

Welcome to **EPL Predictor Guru** – a web-based Premier League match prediction platform powered by machine learning, AI insights, and live football APIs.

This project brings together real-time match data, AI-generated predictions, league standings, latest football news, and betting site links to create a dynamic matchweek dashboard for English Premier League fans.

![screenshot](preview.png) <!-- Add an image to your repo for visual reference -->

---

## 🔮 Features

- **Upcoming Matchweek Predictions**  
  Get AI-powered predictions for upcoming EPL matches using recent form, head-to-head history, and team stats.

- **Premier League Table**  
  See the latest standings using data from the Football Data API.

- **Live Betting Odds**  
  View head-to-head betting odds from The Odds API (Home Win, Draw, Away Win).

- **Natural Language AI Analysis**  
  Uses Gemini AI (fallback to DeepSeek AI) to summarize trends and provide a short match analysis.

- **Latest EPL News**  
  Aggregated football news stories from NewsAPI, complete with titles, thumbnails, and links.

- **Quick Access to Betting Sites**  
  Direct links to popular Kenyan betting platforms (Betika, SportPesa, Betway, etc.).

---

## 🛠 Tech Stack

- **Frontend:** HTML, Tailwind CSS, Vanilla JavaScript  
- **Backend:** FastAPI (Python)  
- **Machine Learning Models:** Gemini AI (Google), DeepSeek AI  
- **APIs Used:**
  - [Football-Data.org](https://www.football-data.org/)
  - [The Odds API](https://the-odds-api.com/)
  - [NewsAPI.org](https://newsapi.org/)
  - [Gemini (Google AI)](https://ai.google.dev/)
  - [DeepSeek AI](https://deepseek.com/)

---

## 🚀 Setup Instructions

1. Clone the Repository:
  git clone https://github.com/yourusername/epl-predictor-guru.git
  cd epl-predictor-guru
  
2. Install Backend Dependencies:
  pip install -r requirements.txt

3. Create .env File and Add API Keys
  GEMINI_API_KEY=your_gemini_key
  DEEPSEEK_API_KEY=your_deepseek_key
  ODDS_API_KEY=your_odds_api_key
  FOOTBALL_API_KEY=your_football_data_key
  NEWS_API_KEY=your_news_api_key

4. Run the FastAPI Backend:
  uvicorn api:app --reload
  Open epl.html in your browser

📁 Project Structure
    .
    ├── api.py                  # FastAPI backend
    ├── index.html              # Main frontend file
    ├── epl_matches_2017_2023.csv  # Match history dataset
    ├── .env                    # API keys and secrets
    ├── static/                 # (Optional) for logos or styles
    └── README.md               # Project documentation


📌 Current Limitations
Predictions are only as good as the available historical and statistical data.

Not optimized for mobile devices yet.

Requires reliable API quotas – fallback to DeepSeek is used when Gemini quota is exceeded.

Currently limited to the English Premier League.


🌱 Future Improvements
✅ Add support for other leagues like La Liga, Serie A, Bundesliga.

🔄 Allow users to input their own match predictions and compare with AI.

📊 Integrate visual stats and charts using Chart.js or Recharts.

🧠 Train a custom machine learning model for score prediction.

🔔 Add user login and notifications (e.g., prediction success rate, favorites).

📱 Build a mobile-first UI or convert to PWA (Progressive Web App).

💬 Add a comment or community section for user match discussions.

🌐 Deploy backend (Render) and frontend (Vercel/Netlify) for public access.


🙌 Acknowledgements
Special thanks to:

Google for Gemini AI

Football-Data.org, NewsAPI.org, and The Odds API for making this project possible

📬 Contact
Built by Peter Sankale Kopejo
For collaboration, email: kopejopeter@gmail.com

⭐ License
MIT License – free to use, share, and contribute.
