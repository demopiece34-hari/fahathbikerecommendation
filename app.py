 import streamlit as st
import json, os, random
from datetime import date, datetime
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

DATA_FILE = "data.json"

# ------------------ AUTH ------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "9442176514":
            st.session_state.login = True
            st.success("Login Success")
        else:
            st.error("Wrong credentials")
    st.stop()

# ------------------ DATA ------------------
def load_data():
    default = {
        "points": 0,
        "xp": 0,
        "history": {},
        "badges": [],
        "reasons": {},
        "start_date": str(date.today()),
        "locked_days": [],
        "name": "Player",
        "avatar": "😎",
    }

    if not os.path.exists(DATA_FILE):
        return default

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        return default

    for k in default:
        if k not in data:
            data[k] = default[k]

    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


data = load_data()

today = date.today()
today_str = str(today)

# ------------------ LEVEL ------------------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))

# ------------------ TASKS ------------------
tasks = {
    "Morning": ["Wake 5:30", "Brush", "Bath", "Prayer"],
    "Workout": ["Walking", "Exercise", "Breathing"],
    "Learning": ["Python", "English", "Reading"],
    "Health": ["Water", "No Junk"]
}

TASK_XP = {
    "Wake 5:30": 10, "Brush": 5, "Bath": 5, "Prayer": 10,
    "Walking": 20, "Exercise": 25, "Breathing": 10,
    "Python": 20, "English": 15, "Reading": 15,
    "Water": 10, "No Junk": 20
}

# ------------------ NAV ------------------
menu = ["Dashboard", "Missions", "Stats", "Profile"]
choice = st.sidebar.radio("Menu", menu)

# ------------------ DASHBOARD ------------------
if choice == "Dashboard":
    st.title("🎯 LIFE GAME")
    st.subheader(f"{data['avatar']} {data['name']}")
    st.write(f"Level: {level}/100")
    st.write(f"XP: {data['xp']}")

# ------------------ MISSIONS ------------------
elif choice == "Missions":
    st.title("🎮 Missions")

    done = 0
    total = 0
    missed = []

    locked = today_str in data["locked_days"]

    for group, tlist in tasks.items():
        st.subheader(group)

        for t in tlist:
            total += 1
            checked = st.checkbox(t, key=f"{today_str}_{t}", disabled=locked)

            if checked:
                done += 1
            else:
                missed.append(t)

    score = int((done / total) * 100) if total else 0
    st.progress(score / 100)
    st.write(f"Score: {score}%")

    reasons = {}
    if missed:
        st.subheader("Missed Reasons")
        for t in missed:
            r = st.text_input(f"{t}")
            if r:
                reasons[t] = r

    if st.button("FINAL SAVE") and not locked:
        data["history"][today_str] = score
        data["xp"] += score
        data["points"] += score

        penalty = sum(TASK_XP.get(t, 5) for t in missed)
        data["xp"] -= penalty
        data["points"] -= penalty

        data["xp"] = max(0, data["xp"])
        data["points"] = max(0, data["points"])

        data["reasons"][today_str] = reasons
        data["locked_days"].append(today_str)

        save_data(data)
        st.success("Saved & Locked")
        st.rerun()

# ------------------ STATS ------------------
elif choice == "Stats":
    st.title("📊 Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())
        scores = list(history.values())

        st.plotly_chart(px.line(x=dates, y=scores, title="Progress"))

# ------------------ PROFILE ------------------
elif choice == "Profile":
    st.title("🧑 Profile")

    name = st.text_input("Name", value=data["name"])
    avatar = st.selectbox("Avatar", ["😎", "🔥", "👑", "💪"])

    if st.button("Save Profile"):
        data["name"] = name
        data["avatar"] = avatar
        save_data(data)
        st.success("Saved")

    st.write(f"XP: {data['xp']}")
    
