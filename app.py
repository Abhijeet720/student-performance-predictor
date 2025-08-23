import streamlit as st
import numpy as np
import joblib
import warnings

warnings.filterwarnings("ignore")


try:
    model = joblib.load("best_model.pkl")
except FileNotFoundError:
    st.error("❌ Error: 'best_model.pkl' not found. Please ensure the model file is in the same directory.")
    st.stop()


st.set_page_config(page_title="🎓 Student Exam Score Predictor", layout="centered")
st.title("📊 Student Performance Predictor")
st.markdown("#### Predict your expected exam score based on daily habits")

st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider("📚 Study Hours Per Day", 0.0, 12.0, 2.0)
    attendance = st.slider("🏫 Attendance Percentage", 0.0, 100.0, 80.0)
    sleep_hours = st.slider("😴 Sleep Hours Per Night", 0.0, 12.0, 7.0)
    screen_time = st.slider("📱 Screen Time Per Day", 0.0, 12.0, 4.0)
with col2:
    mental_health = st.slider("🧠 Mental Health (1 - Poor, 10 - Excellent)", 1, 10, 5)
    internet_quality = st.selectbox("🌐 Internet Quality", ["Low", "Fair", "Good"])
    diet_quality = st.selectbox("🥗 Diet Quality", ["Bad", "Average", "Good"])
    part_time_job = st.radio("💼 Part-time Job", ["Yes", "No"])


ptj_encoded = 1 if part_time_job == "Yes" else 0
internet_quality_map = {"low": 0, "fair": 1, "good": 2}
diet_quality_map = {"bad": 0, "average": 1, "good": 2}
internet_quality_encoded = internet_quality_map[internet_quality]
diet_quality_encoded = diet_quality_map[diet_quality]

st.markdown("---")

if st.button("🔍 Predict Exam Score"):
    input_data = np.array([[study_hours, attendance,mental_health, sleep_hours, ptj_encoded]])
    
    
    prediction = model.predict(input_data)[0]
    prediction = max(0, min(100, prediction))

    
    st.success(f"🎯 *Predicted Exam Score: {prediction:.2f} / 100*")

    
    if prediction >= 85:
        remark = "🌟 Excellent! Keep up the great work!"
    elif prediction >= 70:
        remark = "👍 Good job! A little push and you'll be on top!"
    elif prediction >= 50:
        remark = "📈 Fair! You can improve with better habits."
    else:
        remark = "⚠ Needs Improvement. Consider working more on study hours, sleep, and mental health."

    st.markdown(f"*Performance Remark:* {remark}")


    st.markdown("#### 📌 Suggestions to Improve:")
    suggestions = []

    if study_hours < 3:
        suggestions.append("➡ Try to study at least 3 hours a day.")
    if sleep_hours < 6:
        suggestions.append("➡ Ensure at least 6-8 hours of sleep for better focus.")
    if mental_health < 5:
        suggestions.append("➡ Take care of your mental health. Consider mindfulness or talking to someone.")
    if diet_quality == "bad":
        suggestions.append("➡ Improve your diet. A healthy body fuels a healthy mind.")
    if internet_quality == "low":
        suggestions.append("➡ Stable internet can help with better learning resources.")
    if screen_time > 4:
        st.warning("⚠ Your screen time is quite high. Consider reducing it for better focus and sleep quality")    

    if suggestions:
        for tip in suggestions:
            st.markdown(tip)
    else:
        st.markdown("✅ Your habits are on point! Maintain consistency.")

    st.balloons()
    
