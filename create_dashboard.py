
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

def generate_mock_data(player_name):
    """Generates a realistic mock dataset for a given cricket player."""
    
    # Player-specific details
    if player_name == "Tilak Varma":
        career_start_date = "2023-08-03"
        career_end_date = datetime.date.today().strftime("%Y-%m-%d")
        formats = ["T20I", "ODI"]
        playing_role = "Middle-order Batsman"
        batting_style = "Left-hand bat"
        bowling_style = "Right-arm off-break"
        nationality = "India"
        dob = "2002-11-08"
        bio = "Namboori Thakur Tilak Varma is an Indian international cricketer who plays for the Indian cricket team. A left-handed batsman and an occasional off-spin bowler, he plays for Hyderabad in domestic cricket and for Mumbai Indians in the Indian Premier League (IPL). He was a member of the Indian team that won the 2023 Asia Cup."

    else: # Generic fallback
        career_start_date = "2020-01-01"
        career_end_date = datetime.date.today().strftime("%Y-%m-%d")
        formats = ["T20I", "ODI", "Test"]
        playing_role = "Allrounder"
        batting_style = "Right-hand bat"
        bowling_style = "Right-arm fast-medium"
        nationality = "Unknown"
        dob = "2000-01-01"
        bio = "No biography available for this player."

    dates = pd.to_datetime(pd.date_range(start=career_start_date, end=career_end_date, periods=100).date)
    opposition_teams = ["Australia", "England", "South Africa", "New Zealand", "Pakistan", "Sri Lanka", "West Indies", "Bangladesh"]
    venues = ["Home", "Away"]
    
    data = []
    for date in dates:
        match_format = np.random.choice(formats)
        opposition = np.random.choice(opposition_teams)
        venue = np.random.choice(venues)
        
        # Batting Stats
        if np.random.rand() > 0.1: # 90% chance of batting
            balls_faced = np.random.randint(5, 60) if match_format != "Test" else np.random.randint(20, 150)
            if player_name == "Tilak Varma":
                runs = int(max(0, np.random.normal(loc=35, scale=25)))
                if runs > 50 and np.random.rand() > 0.3: # Make 50s more likely
                    runs = np.random.randint(50, 85)
            else:
                 runs = int(max(0, np.random.normal(loc=30, scale=20)))
            
            batting_sr = (runs / balls_faced * 100) if balls_faced > 0 else 0
        else:
            runs, balls_faced, batting_sr = 0, 0, 0

        # Bowling Stats (occasional bowler)
        if np.random.rand() > 0.7: # 30% chance of bowling
            overs_bowled = round(np.random.uniform(1, 4), 1) if match_format != "Test" else round(np.random.uniform(5, 15), 1)
            runs_conceded = np.random.randint(int(overs_bowled * 4), int(overs_bowled * 10))
            wickets = np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
            economy = runs_conceded / overs_bowled if overs_bowled > 0 else 0
            bowling_sr = (overs_bowled * 6) / wickets if wickets > 0 else 0
        else:
            overs_bowled, runs_conceded, wickets, economy, bowling_sr = 0, 0, 0, 0, 0
            
        result = np.random.choice(["Won", "Lost"])

        data.append({
            "Match Date": date,
            "Year": date.year,
            "Format": match_format,
            "Opposition": opposition,
            "Venue": venue,
            "Runs": runs,
            "Balls Faced": balls_faced,
            "Batting Strike Rate": batting_sr,
            "Wickets": wickets,
            "Overs Bowled": overs_bowled,
            "Runs Conceded": runs_conceded,
            "Economy": economy,
            "Bowling Strike Rate": bowling_sr,
            "Result": result,
            "Player Name": player_name,
            "DOB": dob,
            "Nationality": nationality,
            "Playing Role": playing_role,
            "Batting Style": batting_style,
            "Bowling Style": bowling_style,
            "Biography": bio
        })
        
    df = pd.DataFrame(data)
    # Ensure data types are correct
    for col in ['Runs', 'Balls Faced', 'Wickets', 'Runs Conceded']:
        df[col] = pd.to_numeric(df[col])
    for col in ['Batting Strike Rate', 'Economy', 'Bowling Strike Rate', 'Overs Bowled']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df

def create_dashboard(df, player_name):
    """Creates a creative, high-impact dashboard with a black and red theme."""

    # --- Player Image ---
    player_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Tilak_Varma_in_2023.jpg/330px-Tilak_Varma_in_2023.jpg"

    # --- Color Theme (Black & Red) ---
    theme_colors = {
        'background': '#000000',
        'text': '#FFFFFF',
        'grid': '#333333',
        'accent': '#E50914', # Bold Red
        'accent_light': '#F5575E'
    }

    # --- Data Aggregation ---
    total_runs = df['Runs'].sum()
    total_wickets = df['Wickets'].sum()
    matches_played = len(df)
    highest_score = df['Runs'].max()
    batting_avg = total_runs / len(df[df['Balls Faced'] > 0]) if len(df[df['Balls Faced'] > 0]) > 0 else 0
    strike_rate = (total_runs / df['Balls Faced'].sum()) * 100 if df['Balls Faced'].sum() > 0 else 0
    half_centuries = len(df[(df['Runs'] >= 50) & (df['Runs'] < 100)])
    centuries = len(df[df['Runs'] >= 100])
    yearly_perf = df.groupby('Year').agg(Total_Runs=('Runs', 'sum'), Total_Wickets=('Wickets', 'sum')).reset_index()

    # --- Dashboard Layout ---
    fig = make_subplots(
        rows=3, cols=4,
        specs=[
            [{"type": "domain", "rowspan": 2, "colspan": 1}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
            [None, {"type": "gauge"}, {"type": "gauge"}, {"type": "gauge"}],
            [{"type": "bar", "colspan": 4}, None, None, None]
        ],
        vertical_spacing=0.15, horizontal_spacing=0.1,
        subplot_titles=("", "Total Runs", "Highest Score", "Matches Played", "", "", "", "", "Yearly Performance")
    )

    # --- Row 1 & 2: Profile & KPIs ---
    player_info = df.iloc[0]
    info_text = (
        f"<img src='{player_image_url}' width='130' style='border-radius: 50%;'><br><br>"
        f"<b style='font-size: 1.5em; color:white;'>{player_info['Player Name']}</b><br>"
        f"<span style='font-size: 1.1em; color: {theme_colors['accent']};'>{player_info['Playing Role']}</span>"
    )
    fig.add_annotation(text=info_text, align='center', showarrow=False, xref='paper', yref='paper', x=0.12, y=0.78)

    # Main KPIs
    fig.add_trace(go.Indicator(mode="number", value=total_runs, number={'font':{'color':theme_colors['accent'], 'size':50}}), row=1, col=2)
    fig.add_trace(go.Indicator(mode="number", value=highest_score, number={'font':{'color':theme_colors['accent'], 'size':50}}), row=1, col=3)
    fig.add_trace(go.Indicator(mode="number", value=matches_played, number={'font':{'color':theme_colors['accent'], 'size':50}}), row=1, col=4)

    # Gauge KPIs
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=batting_avg, domain={'x': [0.27, 0.47], 'y': [0.38, 0.62]},
        title={'text': "Batting Avg", 'font': {'size': 18}},
        gauge={'axis': {'range': [0, 60]}, 'bar': {'color': theme_colors['accent']}}
    ), row=2, col=2)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=strike_rate, domain={'x': [0.53, 0.73], 'y': [0.38, 0.62]},
        title={'text': "Strike Rate", 'font': {'size': 18}},
        gauge={'axis': {'range': [50, 200]}, 'bar': {'color': theme_colors['accent']}}
    ), row=2, col=3)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=half_centuries, domain={'x': [0.79, 0.99], 'y': [0.38, 0.62]},
        title={'text': "50s", 'font': {'size': 18}},
        gauge={'axis': {'range': [0, 20]}, 'bar': {'color': theme_colors['accent']}}
    ), row=2, col=4)

    # --- Row 3: Bar Chart ---
    fig.add_trace(go.Bar(
        x=yearly_perf['Year'], y=yearly_perf['Total_Runs'], name='Runs',
        marker=dict(color=yearly_perf['Total_Runs'], colorscale=[[0, theme_colors['grid']], [1, theme_colors['accent']]]),
        text=yearly_perf['Total_Runs'], textposition='outside', textfont_color=theme_colors['text']
    ), row=3, col=1)

    # --- Layout Update ---
    fig.update_layout(
        title_text=f"PROFESSIONAL CAREER OVERVIEW", title_x=0.5, title_y=0.97,
        height=800,
        showlegend=False,
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        font=dict(family="Segoe UI, Helvetica, Arial, sans-serif", color=theme_colors['text']),
        margin=dict(l=40, r=40, t=80, b=40),
        annotations=[dict(font=dict(size=16)) for _ in fig.layout.annotations] # Update subplot title font size
    )
    fig.update_yaxes(showgrid=True, gridcolor=theme_colors['grid'])

    # --- Save to HTML ---
    output_path = 'dashboard.html'
    fig.write_html(output_path, auto_open=False)
    print(f"Dashboard saved to {os.path.abspath(output_path)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        player_name = sys.argv[1]
    else:
        player_name = "Tilak Varma" # Default player

    print("Generating mock data...")
    player_df = generate_mock_data(player_name)
    
    csv_path = 'player_data.csv'
    player_df.to_csv(csv_path, index=False)
    print(f"Player data saved to {os.path.abspath(csv_path)}")
    
    print("Creating interactive dashboard...")
    create_dashboard(player_df, player_name)

