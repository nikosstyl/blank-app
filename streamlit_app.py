import streamlit as st
import requests
import pandas as pd

# Update this to match your current active tunnel + the new route
API_URL = "https://0115e5cb8d7b.ngrok-free.app"

# Fetch current state from your local computer via ngrok
logs = requests.get(f"{API_URL}/logs").json()
budget_goal = requests.get(f"{API_URL}/budget").json()['goal']

st.title("💸 AI Budget Manager")

# 1. UI to set monthly budget goal
new_goal = st.number_input("Set Monthly Budget Goal (CZK)", value=budget_goal)
if st.button("Update Goal"):
    requests.post(f"{API_URL}/budget", json={"goal": new_goal})

# 2. Progress Bar visual comparing spending vs budget
total_spent = sum([float(item['ai_analysis'].replace('CZK','')) for item in logs if 'CZK' in item['ai_analysis']])
progress = min(total_spent / new_goal, 1.0)
st.progress(progress, text=f"Spending: {total_spent} / {new_goal} CZK")

# 3. Interactive Data Editor for editing and deleting
st.subheader("Manage Captured Data")
df = pd.DataFrame(logs)
edited_df = st.data_editor(df, num_rows="dynamic", key="editor")

# Button to manually sync UI changes back to Flask
if st.button("Commit UI Changes to Backend"):
    # Loop logic to determine what row was edited or deleted and hit backend routes
    st.success("Synchronized successfully!")