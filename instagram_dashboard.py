import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Instagram AI Dashboard", layout="wide")
st.title("📸 Instagram Analytics Dashboard (AI Powered)")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("instagram_data.csv")
    except:
        # Demo dataset
        data = {
            "date": pd.date_range(start="2024-01-01", periods=120),
            "post_type": np.random.choice(["Reel", "Post", "Story"], 120),
            "caption": np.random.choice(["Travel", "Food", "Fitness", "Tech"], 120),
            "likes": np.random.randint(100, 5000, 120),
            "comments": np.random.randint(10, 500, 120),
            "shares": np.random.randint(5, 300, 120),
            "saves": np.random.randint(10, 500, 120),
            "reach": np.random.randint(1000, 20000, 120),
            "impressions": np.random.randint(2000, 30000, 120),
            "followers": np.random.randint(1000, 10000, 120),
            "profile_visits": np.random.randint(100, 3000, 120),
            "country": np.random.choice(["India", "USA", "UK"], 120),
            "upload_time": np.random.choice(["Morning", "Afternoon", "Evening", "Night"], 120),
        }
        df = pd.DataFrame(data)
    return df

df = load_data()
df["date"] = pd.to_datetime(df["date"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

date_range = st.sidebar.date_input("Date Range", [df["date"].min(), df["date"].max()])
if len(date_range) == 2:
    df = df[(df["date"] >= str(date_range[0])) & (df["date"] <= str(date_range[1]))]

post_type = st.sidebar.multiselect("Post Type", df["post_type"].unique())
if post_type:
    df = df[df["post_type"].isin(post_type)]

country = st.sidebar.selectbox("Country", ["All"] + list(df["country"].unique()))
if country != "All":
    df = df[df["country"] == country]

# -----------------------------
# KPI Metrics
# -----------------------------
st.subheader("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Likes", int(df["likes"].sum()))
col2.metric("Total Comments", int(df["comments"].sum()))
col3.metric("Total Reach", int(df["reach"].sum()))
col4.metric("Followers", int(df["followers"].iloc[-1]))

# -----------------------------
# Engagement Rate
# -----------------------------
df["engagement_rate"] = (
    df["likes"] + df["comments"] + df["shares"] + df["saves"]
) / df["reach"]

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Performance Trends")
col1, col2 = st.columns(2)

with col1:
    st.write("Reach Over Time")
    st.line_chart(df.groupby("date")["reach"].sum())

with col2:
    st.write("Engagement Rate Over Time")
    st.line_chart(df.groupby("date")["engagement_rate"].mean())

# -----------------------------
# Content Type Performance
# -----------------------------
st.subheader("🎬 Content Type Performance")
post_perf = df.groupby("post_type")["reach"].mean()
st.bar_chart(post_perf)

# -----------------------------
# Profile Visits
# -----------------------------
st.subheader("👤 Profile Visits")
st.line_chart(df.groupby("date")["profile_visits"].sum())

# -----------------------------
# Top Posts
# -----------------------------
st.subheader("🏆 Top Posts")
top_posts = df.sort_values(by="reach", ascending=False).head(5)
st.dataframe(top_posts[["caption", "post_type", "reach", "likes"]])

# -----------------------------
# AI Insights
# -----------------------------
st.subheader("🧠 AI Insights")

best_post = df.loc[df["reach"].idxmax()]
worst_post = df.loc[df["reach"].idxmin()]
best_type = df.groupby("post_type")["reach"].mean().idxmax()
best_time = df.groupby("upload_time")["reach"].mean().idxmax()
avg_engagement = df["engagement_rate"].mean()

col1, col2 = st.columns(2)

with col1:
    st.success(f"🔥 Best Post: {best_post['caption']}")
    st.info(f"🎬 Best Content Type: {best_type}")
    st.info(f"⏱ Best Upload Time: {best_time}")

with col2:
    st.warning(f"⚠ Worst Post: {worst_post['caption']}")
    st.write(f"📊 Avg Engagement Rate: {avg_engagement:.2%}")

# -----------------------------
# Growth Tracking
# -----------------------------
growth = df["followers"].pct_change().mean() * 100
st.metric("📈 Follower Growth Rate", f"{growth:.2f}%")

# -----------------------------
# 🔮 Viral Score (AI Simulation)
# -----------------------------
st.subheader("🔮 Viral Score Prediction")

df["viral_score"] = (
    df["engagement_rate"] * 0.5 +
    (df["shares"] / df["reach"]) * 0.3 +
    (df["saves"] / df["reach"]) * 0.2
)

top_viral = df.sort_values(by="viral_score", ascending=False).head(3)
st.dataframe(top_viral[["caption", "viral_score"]])

# -----------------------------
# 🤖 AI Suggestions
# -----------------------------
st.subheader("🤖 AI Content Suggestions")

if best_type == "Reel":
    st.write("👉 Focus more on Reels, they perform best 🚀")
elif best_type == "Post":
    st.write("👉 Static posts are working well 👍")
else:
    st.write("👉 Use Stories for engagement 💬")

if best_time == "Night":
    st.write("🌙 Post at night for maximum reach")
elif best_time == "Evening":
    st.write("🌆 Evening posts perform best")
else:
    st.write("☀ Try posting earlier in the day")

# -----------------------------
# 🏷 Hashtag Generator
# -----------------------------
st.subheader("🏷 Hashtag Generator")

keywords = st.text_input("Enter keyword (e.g., travel, fitness)")

if keywords:
    hashtags = [f"#{keywords}", f"#{keywords}life", f"#{keywords}daily",
                f"#{keywords}reels", f"#{keywords}india", "#viral", "#trending"]
    st.write("Suggested Hashtags:")
    st.write(" ".join(hashtags))

# -----------------------------
# Footer
# -----------------------------
st.write("---")
st.caption("🚀 AI Powered Instagram Analytics Dashboard")