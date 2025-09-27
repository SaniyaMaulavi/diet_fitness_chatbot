import streamlit as st
import pandas as pd
import os  # for building relative paths

# -----------------------------
# Paths for CSV files (Cloud-friendly)
# -----------------------------
current_dir = os.path.dirname(__file__)  # folder jahan app.py hai

diet_csv_path = os.path.join(current_dir, "data", "diet_tips.csv")
exercise_csv_path = os.path.join(current_dir, "data", "exercises.csv")

# -----------------------------
# Load CSV data
# -----------------------------
diet_data = pd.read_csv(diet_csv_path)
exercise_data = pd.read_csv(exercise_csv_path)

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Diet & Fitness Chatbot", page_icon="🍎", layout="wide")
st.markdown("<h1 style='text-align: center; color: darkgreen;'>🍎 Diet & Fitness Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Ask anything about your diet or exercise!</h4>", unsafe_allow_html=True)
st.write("---")

# -----------------------------
# User Input
# -----------------------------
user_input = st.text_input("Type your question here:")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Your Age:", min_value=5, max_value=120, value=25)
with col2:
    weight = st.number_input("Your Weight (kg):", min_value=10, max_value=200, value=60)
with col3:
    goal = st.selectbox("Your Goal:", ["Maintain Weight", "Lose Weight", "Gain Muscle", "Stay Fit"])

# -----------------------------
# Personalized Notes
# -----------------------------
goal_notes = {
    "Lose Weight": "Try to keep portions small and focus on high-protein, low-calorie foods.",
    "Gain Muscle": "Include protein-rich meals and strength exercises.",
    "Maintain Weight": "Balanced diet and regular exercise will help maintain your weight.",
    "Stay Fit": "Stay active daily and eat a variety of healthy foods."
}

# -----------------------------
# Suggestion Logic
# -----------------------------
if st.button("Get Suggestions"):
    if user_input.strip() == "":
        st.warning("⚠️ Please type your question first!")
    else:
        user_input_lower = user_input.lower()

        # Diet matches
        diet_matches = diet_data[diet_data['Keyword'].apply(lambda x: x.lower() in user_input_lower)]
        # Exercise matches
        exercise_matches = exercise_data[exercise_data['Keyword'].apply(lambda x: x.lower() in user_input_lower)]

        # -----------------------------
        # Display Diet Suggestions
        # -----------------------------
        if not diet_matches.empty:
            st.markdown("<h3 style='color: darkblue;'>🍽️ Diet Suggestions</h3>", unsafe_allow_html=True)
            for tip in diet_matches['Tip'].tolist():
                st.info(f"{tip}\nGoal Tip: {goal_notes[goal]}")

        # -----------------------------
        # Display Exercise Suggestions
        # -----------------------------
        if not exercise_matches.empty:
            st.markdown("<h3 style='color: darkred;'>🏋️ Exercise Suggestions</h3>", unsafe_allow_html=True)
            for ex in exercise_matches['Exercise'].tolist():
                st.success(f"{ex}\nGoal Tip: {goal_notes[goal]}")

        # -----------------------------
        # Fallback generic tips
        # -----------------------------
        if diet_matches.empty and exercise_matches.empty:
            st.warning("⚠️ No exact match found. Here are some general tips:")
            st.write("- **Diet:** Eat a balanced mix of proteins, carbs, and vegetables.")
            st.write("- **Exercise:** Include at least 30 minutes of walking or light cardio daily.")
