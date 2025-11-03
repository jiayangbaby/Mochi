import streamlit as st
import plotly.express as px
from main import log_mood, get_moods_by_date
from streamlit_autorefresh import st_autorefresh
import datetime

#name of the app
st.set_page_config(page_title=" Mochi Mood Tracker", layout="wide")
# set up left and right sections
left, right = st.columns([1, 1.4])  

#left side, the log mood section
with left:
    st.subheader("Select Your Mood")
    note = st.text_input("Optional note (How are you today?)")
    st.text("Log your Mood by clicking it. Wait for few seconds, and a confirmation message will show up.")

    mood_emojis = [
        "😊", "😄", "🤩", "🙌", "🎉", "👍",
        "🙂", "😐", "🤔", "🤨", "🫤",
        "😠", "😡", "😤", "😕", "😢", "😭", "😫", "😩", "😵‍💫",
        "🕒", "⏳", "🏃‍♀️", "🔥", "📞", "💊", "✅", "❌",
        "🚨", "🆘"
    ]

    #emojis as clickable buttons
    num_cols = 6
    mood = None
    emoji_cols = st.columns(num_cols)
    for i, emoji in enumerate(mood_emojis):
        if emoji_cols[i % num_cols].button(emoji, key=emoji):
            mood = emoji

    #if select a emoji, print a success message
    if mood:
        result = log_mood(mood, note)
        st.success(f"Logged successfully: {mood} {note}")


#right side, visual sections
with right:
    st.subheader("Mood Visualization")
    # refresh 60 sec
    st_autorefresh(interval=60000, key="mood_refresh")

    today = datetime.date.today()
    #date filter, bonus
    colA, colB = st.columns(2)
    start = colA.date_input("Start Date", value=today)
    end = colB.date_input("End Date", value=today)

    if start > end:
        st.warning("Error: Start date is after end date")
        start, end = end, start

    df = get_moods_by_date(start, end)

    #graphs
    if df.empty:
        st.info("No moods record in the selected range.")
    else:
        mood_counts = df["mood"].value_counts().reset_index()
        mood_counts.columns = ["mood", "count"]

        fig = px.bar(
            mood_counts,
            x="mood",
            y="count",
            text="count",
            title=f"Mood Counts ({start} → {end})"
        )
        st.plotly_chart(fig, use_container_width=True)
