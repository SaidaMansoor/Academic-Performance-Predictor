import streamlit as st
import numpy as np
import pickle
import joblib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Academic Performance Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Improved CSS with enhanced visibility for both light and dark themes
st.markdown("""
<style>
    /* Base styles */
.stApp {
    max-width: 1200px;
    margin: 0 auto;
}

/* Typography */
h1, h2, h3 {
    font-weight: 600;
}

/* Button styling */
.stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: bold;
    border: none;
}
.stButton>button:hover {
    background-color: #4338ca;
}

/* Cards - borders removed */
.card {
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: rgba(255, 255, 255, 0.1);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Reduced shadow */
}

/* Score display - improved contrast */
.score-display {
    text-align: center;
    padding: 20px 0;
}
.score-value {
    font-size: 48px;
    font-weight: bold;
    line-height: 1.2;
    background: linear-gradient(45deg, #4f46e5, #818cf8);
    -webkit-background-clip: text;
    color: #4f46e5; /* Fallback color */
    margin: 10px 0;
}

/* Status boxes - improved contrast, reduced borders */
.status-improved {
    background-color: rgba(16, 185, 129, 0.2);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0;
}
.status-improved p {
    color: #10b981;
    font-weight: 600;
    margin: 0;
}

.status-decreased {
    background-color: rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0;
}
.status-decreased p {
    color: #ef4444;
    font-weight: 600;
    margin: 0;
}

.status-same {
    background-color: rgba(59, 130, 246, 0.2);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0;
}
.status-same p {
    color: #3b82f6;
    font-weight: 600;
    margin: 0;
}

/* Tab styling - reduced borders */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 4px 4px 0 0;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(79, 70, 229, 0.2);
}

/* Leaderboard card - No borders */
.leaderboard-card {
    border-radius: 10px;
    padding: 15px;
    background-color: rgba(79, 70, 229, 0.1);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Minimal shadow */
}

/* Leaderboard title styling - IMPROVED for both themes */
.leaderboard-title {
    margin-top: 0; /* Remove extra space at the top */
    padding-top: 0; /* Remove extra padding at the top */
}

/* Leaderboard items - IMPROVED HIGH CONTRAST for both themes */
.leaderboard-item {
    display: flex;
    align-items: center;
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
    background-color: rgba(100, 100, 100, 0.25);
    border: 1px solid rgba(0, 0, 0, 0.1); /* Border for better visibility */
}

/* Gold medal - ENHANCED for both themes */
.leaderboard-item-gold {
    background-color: rgba(255, 215, 0, 0.5);
}
.leaderboard-item-gold .rank-num,
.leaderboard-item-gold .user-name,
.leaderboard-item-gold .user-score {
    font-weight: bold;
}

/* Silver medal - ENHANCED for both themes */
.leaderboard-item-silver {
    background-color: rgba(192, 192, 192, 0.5);
}
.leaderboard-item-silver .rank-num,
.leaderboard-item-silver .user-name,
.leaderboard-item-silver .user-score {
    font-weight: bold;
}

/* Bronze medal - ENHANCED for both themes */
.leaderboard-item-bronze {
    background-color: rgba(205, 127, 50, 0.5);
}
.leaderboard-item-bronze .rank-num,
.leaderboard-item-bronze .user-name,
.leaderboard-item-bronze .user-score {
    font-weight: bold;
}

/* Regular entries - ENHANCED contrast for both themes */
.leaderboard-item-normal {
    background-color: rgba(100, 100, 100, 0.3);
}
.leaderboard-item-normal .rank-num,
.leaderboard-item-normal .user-name,
.leaderboard-item-normal .user-score {
    font-weight: bold;
}

/* Current user - ENHANCED contrast for both themes */
.leaderboard-item-current {
    background-color: rgba(59, 130, 246, 0.5);
}
.leaderboard-item-current .rank-num,
.leaderboard-item-current .user-name,
.leaderboard-item-current .user-score {
    font-weight: bold;
}

.rank-num {
    font-size: 18px;
    margin-right: 10px;
    min-width: 30px;
    text-align: center;
}

.user-name {
    flex-grow: 1;
    font-weight: bold;
}

.user-score {
    font-weight: bold;
    font-size: 18px;
}

/* Top performer message - IMPROVED VISIBILITY */
.top-performer-message {
    text-align: center;
    margin-top: 10px;
    padding: 8px;
    background-color: rgba(16, 185, 129, 0.2);
    border-radius: 8px;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.top-performer-message p {
    font-weight: bold;
    color: #10b981; /* Bright green that works in both themes */
    margin: 0;
    font-size: 16px;
}

/* Total users display - IMPROVED VISIBILITY */
.total-users {
    text-align: center;
    margin-top: 20px;
}

/* Expander styling */
.expander-card {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
}

.expander-title {
    font-weight: 600;
    color: #4f46e5;
}

.tip-card {
    background-color: rgba(79, 70, 229, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
}

.tip-title {
    font-weight: 600;
    margin-bottom: 5px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(100, 100, 100, 0.1); /* Lighter border */
}
</style>
""", unsafe_allow_html=True)

# Google Sheets API setup using Streamlit secrets
def authenticate_gspread():
    try:
        # Get credentials from Streamlit secrets
        credentials_dict = st.secrets["gcp_service_account"]
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Authentication error: {e}")
        st.error("Make sure your Streamlit secrets are properly configured with GCP service account credentials.")
        return None

def append_to_google_sheet(sheet_name, data):
    client = authenticate_gspread()
    if client:
        try:
            # Open your Google Sheet
            sheet = client.open(sheet_name).sheet1
            sheet.append_row(data)
            return True
        except Exception as e:
            st.error(f"Error accessing Google Sheet: {e}")
            return False
    return False

# App header with new title
st.markdown("<h1 style='text-align: center;'>📚 Academic Performance Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Analyze your study habits and predict your academic performance</p>", unsafe_allow_html=True)      

st.markdown('<div class="card">', unsafe_allow_html=True)

# Add a separate "How to use" expander at the top (but after study tips)
with st.expander("ℹ️ How to Use This Tool"):
    st.markdown("<h4 class='expander-title'>📋 Instructions</h4>", unsafe_allow_html=True)
    st.markdown("""
    1. **Enter your details** in the form on the left side of the screen.
    2. **Fill in all required fields** including your name, study hours, previous score, sleep hours, and sample papers solved.
    3. **Select whether you participate** in extracurricular activities.
    4. **Click "Predict My Performance"** to see your predicted academic score.
    5. **Track your progress** over time in the "Your History" tab.
    6. **Compare your performance** with others in the "Leaderboard" tab.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([3, 2])

# Load model
try:
    file = open('performance.pkl', 'rb')
    model = joblib.load(file)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Input form in a card
with col1:
    st.subheader("📋 Enter Your Details")

    name = st.text_input("Full Name")

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        hr_std = st.number_input("Study Hours Daily", min_value=0.0, max_value=24.0, step=0.5, help="How many hours do you study each day?")
        pr_scr = st.number_input("Previous Test Score", min_value=0.0, max_value=100.0, step=1.0, help="What was your score in the last test?")

    with input_col2:
        hr_slp = st.number_input("Sleep Hours Daily", min_value=0.0, max_value=24.0, step=0.5, help="How many hours do you sleep each day?")
        sp_ppr = st.number_input("Sample Papers Solved", min_value=0, step=1, help="How many practice papers have you completed?")

    activi = st.radio('Do you participate in extracurricular activities?', ['Yes', 'No'], horizontal=True)

    act_num_1 = 1 if activi == "Yes" else 0
    act_num_0 = 1 - act_num_1

    input_data = np.array([hr_std, pr_scr, hr_slp, sp_ppr, act_num_0, act_num_1])

    submit_button = st.button("Predict My Performance", use_container_width=True)
    
# Results and history
with col2:
    st.subheader("🔍 Prediction Results")
    
    if submit_button:
        if name.strip() == "":
            st.error("⚠️ Please enter your name before proceeding.")
        else:
            prediction = model.predict([input_data])
            predicted_score = round(prediction[0], 2)
            
            # Display prediction with theme-friendly styling
            st.markdown(f"""
            <div class='score-display'>
                <p>Your Predicted Score</p>
                <h2 class='score-value'>{predicted_score}</h2>
                <p>out of 100</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get current date and time
            current_datetime = datetime.now()
            current_date = current_datetime.strftime('%Y-%m-%d')
            current_time = current_datetime.strftime('%H:%M:%S')
            
            # Save to Google Sheet with "Current" status and SEPARATE date/time columns
            new_entry = ["Current", name, hr_std, pr_scr, hr_slp, sp_ppr, activi, predicted_score, current_date, current_time]
            
            try:
                # First, update any existing entries for this user to "Previous"
                client = authenticate_gspread()
                if client:
                    sheet = client.open('User History').sheet1
                    all_rows = sheet.get_all_values()
                    
                    # Get the header row and find column indices
                    headers = all_rows[0]
                    status_idx = headers.index("Status")
                    name_idx = headers.index("Name")
                    
                    # Update previous entries for this user to "Previous"
                    for i, row in enumerate(all_rows[1:], start=2):  # Start from 2 because sheet rows are 1-indexed and we skip header
                        if row[name_idx].lower() == name.lower() and row[status_idx] == "Current":
                            sheet.update_cell(i, status_idx + 1, "Previous")  # +1 because gspread is 1-indexed
                    
                    # Now append the new entry
                    if append_to_google_sheet('User History', new_entry):
                        st.success("✅ Your data has been saved successfully!")
                    
                    # Reload the data to show updated history
                    history_data = sheet.get_all_records()
                    history = pd.DataFrame(history_data)
                    
                    # Ensure all columns are properly typed
                    if 'Name' in history.columns:
                        history['Name'] = history['Name'].astype(str)
                    
                    # Filter for this user's history
                    user_history = history[history['Name'].str.lower() == name.lower()]
                    
                    if not user_history.empty:
                        # Show improvement if multiple entries exist
                        if len(user_history) > 1:
                            current_score = user_history[user_history['Status'] == 'Current']['Predicted Score'].values[0]
                            previous_scores = user_history[user_history['Status'] == 'Previous']['Predicted Score'].values
                            if len(previous_scores) > 0:
                                latest_previous = previous_scores[-1]
                                improvement = current_score - latest_previous
                                
                                if improvement > 0:
                                    st.markdown(f"""
                                    <div class='status-improved'>
                                        <p>📈 You've improved by {improvement:.2f} points!</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                elif improvement < 0:
                                    st.markdown(f"""
                                    <div class='status-decreased'>
                                        <p>📉 Your score decreased by {abs(improvement):.2f} points.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class='status-same'>
                                        <p>Your score remains the same.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
                st.error("Check that your Google Sheet has the correct columns")
    else:
        st.info("Fill in your details and click 'Predict My Performance' to see your results.")

# Show history and leaderboard in a new row if data exists
if submit_button and name.strip() != "":
    try:
        client = authenticate_gspread()
        if client:
            sheet = client.open('User History').sheet1
            history_data = sheet.get_all_records()
            history = pd.DataFrame(history_data)
            
            if 'Name' in history.columns:
                history['Name'] = history['Name'].astype(str)
            
            # Filter for this user's history
            user_history = history[history['Name'].str.lower() == name.lower()]
            
            # Show history and leaderboard in different tabs
            tab1, tab2 = st.tabs(["📊 Your History", "🏆 Leaderboard"])
            
            with tab1:
                if not user_history.empty:
                    st.subheader("Your Performance History")
                    
                    # Process Date and Time columns (now separate)
                    if 'Date' in user_history.columns and 'Time' in user_history.columns:
                        # Keep them as separate columns
                        pass
                    elif 'DateTime' in user_history.columns:
                        # For backward compatibility, split the datetime
                        user_history['Date'] = pd.to_datetime(user_history['DateTime']).dt.date
                        user_history['Time'] = pd.to_datetime(user_history['DateTime']).dt.time
                    
                    # Display user history as a styled table
                    display_columns = ['Status', 'Date', 'Time', 'Predicted Score', 'Studied Hours', 'Sleep Hours', 'Sample Papers', 'Activity']
                    
                    # Only include columns that actually exist
                    existing_columns = [col for col in display_columns if col in user_history.columns]
                    
                    history_display = user_history[existing_columns]
                    history_display = history_display.rename(columns={
                        'Predicted Score': 'Score',
                        'Studied Hours': 'Study Hrs',
                        'Sleep Hours': 'Sleep Hrs',
                        'Sample Papers': 'Practice'
                    })
                    
                    st.dataframe(
                        history_display,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No previous records found for you.")
            
            with tab2:
                if not history.empty:
                    st.markdown("<div class='leaderboard-card'>", unsafe_allow_html=True)
                    st.markdown("<h3 class='leaderboard-title'>🏆 Top Performers</h3>", unsafe_allow_html=True)
                    
                    # 1. Find the best score for each student
                    best_scores = history.groupby('Name')['Predicted Score'].max().reset_index()
                    
                    # 2. Sort them by score in descending order
                    best_scores = best_scores.sort_values(by='Predicted Score', ascending=False).reset_index(drop=True)
                    
                    # 3. Assign Rank
                    best_scores['Rank'] = best_scores.index + 1
                    
                    # Create a styled leaderboard
                    leaderboard = best_scores.head(5)
                    
                    # Display the leaderboard with improved visibility for both themes
                    for i, row in leaderboard.iterrows():
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
                        item_class = "leaderboard-item-gold" if i == 0 else "leaderboard-item-silver" if i == 1 else "leaderboard-item-bronze" if i == 2 else "leaderboard-item-normal"
                        
                        st.markdown(f"""
                        <div class='leaderboard-item {item_class}'>
                            <div class='rank-num'>{medal}</div>
                            <div class='user-name'>{row['Name']}</div>
                            <div class='user-score'>{row['Predicted Score']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Find the rank of the current user
                    user_rank = best_scores[best_scores['Name'].str.lower() == name.lower()]
                    
                    if not user_rank.empty:
                        rank = int(user_rank['Rank'].values[0])
                        your_best = user_rank['Predicted Score'].values[0]
                        
                        st.markdown("<div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.2);'>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-weight: bold;'>Your Best Performance:</p>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class='leaderboard-item leaderboard-item-current'>
                            <div class='rank-num'>#{rank}</div>
                            <div class='user-name'>{name}</div>
                            <div class='user-score'>{your_best}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Check how much more to reach #1
                        if rank > 1:
                            top_score = best_scores['Predicted Score'].iloc[0]
                            diff = top_score - your_best
                            st.markdown(f"""
                            <div style='text-align: center; margin-top: 10px;'>
                                <p>Just <strong style='color: #4f46e5;'>{diff:.2f}</strong> more points to reach the top!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.balloons()
                            # IMPROVED TOP PERFORMER VISIBILITY with new class
                            st.markdown("""
                            <div class='top-performer-message'>
                                <p>🚀 Congratulations! You are the Top Performer!</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Add back the total user count with improved visibility
                    total_users = len(history['Name'].unique())
                    st.markdown(f"""
                    <div class='total-users'>
                        <p>👥 Total unique users: {total_users}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

# MOVED: Study tips to the bottom as requested
with st.expander("📝 Study Tips for Academic Success"):
    
    st.markdown("<div class='tip-card'>", unsafe_allow_html=True)
    st.markdown("<p class='tip-title'>⏰ Optimize Your Study Time</p>", unsafe_allow_html=True)
    st.markdown("""
    * Quality over quantity: 2 focused hours are better than 4 distracted hours
    * Use the Pomodoro Technique: 25 minutes of focused study, followed by a 5-minute break
    * Study at the time of day when your mind is most alert
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='tip-card'>", unsafe_allow_html=True)
    st.markdown("<p class='tip-title'>😴 Prioritize Sleep</p>", unsafe_allow_html=True)
    st.markdown("""
    * Aim for 7-9 hours of quality sleep per night
    * Avoid screens one hour before bedtime
    * Consistent sleep schedule improves memory consolidation
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='tip-card'>", unsafe_allow_html=True)
    st.markdown("<p class='tip-title'>📝 Practice with Sample Papers</p>", unsafe_allow_html=True)
    st.markdown("""
    * Solve past papers under timed conditions
    * Review mistakes and understand correct solutions
    * Identify patterns in questions and topics
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='tip-card'>", unsafe_allow_html=True)
    st.markdown("<p class='tip-title'>🏃‍♂️ Balance Activities</p>", unsafe_allow_html=True)
    st.markdown("""
    * Physical activities can improve cognitive function
    * Extracurricular activities build important soft skills
    * Find a healthy balance between studies and other activities
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='tip-card'>", unsafe_allow_html=True)
    st.markdown("<p class='tip-title'>🧠 Effective Study Strategies</p>", unsafe_allow_html=True)
    st.markdown("""
    * Spaced repetition: Review material at increasing intervals
    * Active recall: Test yourself rather than re-reading
    * Teach concepts to others to solidify understanding
    * Use mind maps and flashcards for visual learning
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# Add footer
st.markdown("""
<div class='footer'>
    <p>Academic Performance Predictor © 2025</p>
</div>
""", unsafe_allow_html=True)