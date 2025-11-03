Mochi Mood Log App
This is a tool allows users to log the emotional state of the ticket queue throughout the day and visualize trends. The backend mood entry record is stored in Google Sheets.

Features
1. Log a mood with one click and optional comment 
2. Mood trend visualization in bar charts
3. Filter mood history by custom date range
4. Auto refresh after 1 minute

Fully cloud-hosted using Streamlit Cloud

Project Structure
app.py           # Streamlit UI, auto refresh, graphs
main.py          # Google Sheets mood log, read, and data select methods 
requirements.txt # Dependencies

Deployment (Streamlit Cloud)

Run the app locally:
streamlit run app.py (uncomment the get service method)


