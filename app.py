import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import gsheet

# Simulated database of users (Replace with a real database in production)
USER_CREDENTIALS = {
    "admin": "fleet",
    "manager": "fleet"
}

# Function to check login credentials
def authenticate_user(username, password):
    return USER_CREDENTIALS.get(username.lower()) == password

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# 🚀 Login Page
def login_page():
    st.title("🔐 Fleet Management Login")

    username_input = st.text_input("Username", key="user_input")
    password_input = st.text_input("Password", type="password", key="pass_input")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username_input, password_input):
            st.session_state.logged_in = True
            st.session_state.current_user = username_input  # Update the session state variable
            st.success("✅ Login successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Incorrect username or password")


# 🚪 Logout Function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.rerun()

# Function to calculate driver score based on violations
def calculate_driver_score(violations_count):
    base_score = 100
    penalty_per_violation = 5  # Penalty for each violation
    final_score = base_score - (violations_count * penalty_per_violation)
    return max(final_score, 0)  # Ensure score doesn't go below 0


# 🚛 Fleet Management Dashboard (only accessible if logged in)
def dashboard():
    st.set_page_config(page_title="Fleet Driving Behavior Dashboard", layout="wide")

    # Navigation Bar
    st.sidebar.title("🔧 Dashboard Menu")
    #st.sidebar.button("Logout", on_click=logout)
    st.sidebar.text(f"Welcome 🙏 {st.session_state.current_user} ")
    if st.sidebar.button("Logout"):
        logout()
    
    url = "https://wokwi.com/projects/425977014448937985"
    st.sidebar.markdown(f"[Click here to visit Wokwi simulation!! ]({url})", unsafe_allow_html=True)

    st.title(f"🚛 Intelligent Fleet Management System")
    st.subheader("🔍 Unsafe Driving Detection Dashboard")


    # Load Data (Simulated for now)
    #df = generate_data()
    df=gsheet.read_gsheet()
    #st.dataframe(df)

    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🚨 Total Violations Today", len(df))
    col2.metric("🚦 High-Risk Driver", df["Driver Name"].value_counts().idxmax())
    col3.metric("🚗 Most Violated Vehicle", df["Vehicle Number"].value_counts().idxmax())

    # Unsafe Driving Events Table
    st.subheader("📋 Unsafe Driving Events Log")
    st.dataframe(df)

    # Violations Over Time (Line Chart)
    df["TimeStamp"] = pd.to_datetime(df["Time Stamp"], errors='coerce')
    df["Hour"] = df["TimeStamp"].dt.hour
    violation_counts = df.groupby(["Hour", "Violation"]).size().reset_index(name="Count")

    st.subheader("📊 Violations Trend Over Time")
    fig = px.line(violation_counts, x="Hour", y="Count", color="Violation", title="Violations per Hour")
    st.plotly_chart(fig, use_container_width=True)

    # Driver Performance Breakdown
    st.subheader("📌 Driver Performance")
    driver_violations = df["Driver Name"].value_counts().reset_index()
    driver_violations.columns = ["Driver Name", "Total Violations"]
    fig2 = px.bar(driver_violations, x="Driver Name", y="Total Violations", title="Driver Violation Breakdown", color="Total Violations")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Apply the scoring system to the driver violation data
    df["Driver Score"] = df.groupby("Driver Name")["Violation"].transform('count').apply(calculate_driver_score)

    # Displaying the Driver Performance with Scores
    #st.markdown("📊 Drivers Safety Scores")
    driver_scores = df.groupby("Driver Name")["Driver Score"].max().reset_index()
    fig2 = px.bar(driver_scores, x="Driver Name", y="Driver Score", title="📊 Drivers Safety Scores", color="Driver Score")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Add a status column to highlight unsafe drivers
    df["Driver Status"] = df["Driver Score"].apply(lambda x: "Unsafe" if x < 50 else "Safe")

    # Displaying the Driver Performance with Scores and Status
    #st.subheader("📊 Driver Performance with Scores")
    driver_scores = df.groupby("Driver Name")[["Driver Score", "Driver Status"]].max().reset_index()


    # Highlight and report unsafe drivers
    unsafe_drivers = driver_scores[driver_scores["Driver Status"] == "Unsafe"]
    if not unsafe_drivers.empty:
        st.markdown("### 🚨 Unsafe Drivers Report")
        st.write(unsafe_drivers)
        st.warning("⚠️ These drivers have a safety score below 50 and are considered unsafe!")


    # Refreshing data section
    refresh_button = st.button("🔄 Refresh Data", use_container_width=True)
    
    if refresh_button:
        with st.spinner("Refreshing data... Please wait."):
            time.sleep(2)  # Simulate some delay while loading data
            df = gsheet.read_gsheet()  # Replace with actual data refresh logic
            st.success("Data refreshed successfully!")

    # Refreshing Message
    if refresh_button:
        st.write("🔄 Data has been refreshed. You can see the updated information above!")

# 🛠 Run the login system first, then dashboard if authenticated
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()