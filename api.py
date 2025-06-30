from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests

# Promoted teams context
PROMOTED_TEAMS_NOTE = """
Note:
- Sunderland, Leeds United, and Burnley have been promoted to the Premier League for the 2025/26 season.
- Treat all three as active Premier League teams.
- Do NOT say they are in lower divisions or refer to them as hypothetical.
"""

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load match data
df = pd.read_csv("epl_matches_2017_2023.csv", low_memory=False)

# Gemini API Config
GEMINI_API_KEY = "AIzaSyBw6_T1YGWDJYKFfqSsrqjroTm8qaa3o3w"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Summarize team form
def summarize_form(matches, team_name):
    wins = (matches['Result'] == 'W').sum()
    draws = (matches['Result'] == 'D').sum()
    losses = (matches['Result'] == 'L').sum()
    avg_goals_for = matches['GF'].mean()
    avg_goals_against = matches['GA'].mean()

    return f"""{team_name} - Last 10 Matches:
- Wins: {wins}, Draws: {draws}, Losses: {losses}
- Avg Goals Scored: {avg_goals_for:.2f}, Avg Goals Conceded: {avg_goals_against:.2f}
"""

# Summarize head-to-head
def summarize_h2h(matches, home, away):
    if matches.empty:
        return "No recent head-to-head match data available."

    total = len(matches)
    home_wins = ((matches['Team'] == home) & (matches['Result'] == 'W')).sum()
    away_wins = ((matches['Team'] == away) & (matches['Result'] == 'W')).sum()
    draws = (matches['Result'] == 'D').sum()

    return f"""Head-to-Head ({home} vs {away}) - Last {total} Matches:
- {home} Wins: {home_wins}, {away} Wins: {away_wins}, Draws: {draws}
"""

# Prompt builder
def build_prompt(home_team: str, away_team: str) -> str:
    home_recent = df[df['Team'] == home_team].sort_values(by='date', ascending=False).head(10)
    away_recent = df[df['Team'] == away_team].sort_values(by='date', ascending=False).head(10)

    h2h_matches = df[
        ((df['Team'] == home_team) & (df['Opponent'] == away_team)) |
        ((df['Team'] == away_team) & (df['Opponent'] == home_team))
    ].sort_values(by='date', ascending=False).head(10)

    home_summary = summarize_form(home_recent, home_team)
    away_summary = summarize_form(away_recent, away_team)
    h2h_summary = summarize_h2h(h2h_matches, home_team, away_team)

    return f"""
You are a football analyst AI. Predict the outcome of the upcoming Premier League match between {home_team} and {away_team}. Follow this structured format:

Match prediction: [e.g., Arsenal to win, Draw, etc.]
Match stats:
- Summarized form and performance data for both teams
- Head-to-head stats
Discussion:
- Provide a brief (under 100 words) analysis based on the stats and football knowledge. Be realistic and analytical, like a football pundit.

Match Data:
{home_summary}
{away_summary}
{h2h_summary}

{PROMOTED_TEAMS_NOTE}
"""

# Prediction endpoint
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    home_team = data.get("home_team")
    away_team = data.get("away_team")

    if not home_team or not away_team:
        return {"error": "Missing team names."}

    prompt = build_prompt(home_team, away_team)

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return {"error": f"Gemini API error {response.status_code}: {response.text}"}

        res_json = response.json()

        # Debug print
        print("🧠 Gemini API Response:", res_json)

        ai_reply = (
            res_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        lines = [line.strip() for line in ai_reply.strip().split("\n") if line.strip()]
        prediction, stats, discussion = "No prediction available", [], ""
        reading_stats = False
        reading_discussion = False

        for line in lines:
            lower = line.lower()

            if lower.startswith("match prediction"):
                prediction_part = line.split(":", 1)
                if len(prediction_part) > 1:
                    prediction = prediction_part[1].strip()
                reading_stats = False
                reading_discussion = False

            elif lower.startswith("match stats"):
                reading_stats = True
                reading_discussion = False

            elif lower.startswith("discussion"):
                reading_stats = False
                reading_discussion = True
                discussion_part = line.split(":", 1)
                if len(discussion_part) > 1:
                    discussion += discussion_part[1].strip() + " "

            elif reading_stats and (line.startswith("-") or line.startswith("*")):
                stats.append(line.lstrip("-* ").strip())

            elif reading_discussion:
                discussion += line.strip() + " "

        return {
            "prediction": prediction,
            "stats": stats,
            "discussion": discussion.strip()
        }

    except Exception as e:
        return {"error": str(e)}
