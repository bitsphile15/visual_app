import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="IPL Matches Dashboard", page_icon="🏏", layout="wide")
sns.set_style("whitegrid")


@st.cache_data
def load_data():
    df = pd.read_csv("clean_matches.csv")
    df["city"] = df["city"].fillna(df["city"].mode()[0])
    return df.dropna()


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
seasons = sorted(df["season"].unique())
season_range = st.sidebar.select_slider(
    "Season range", options=seasons, value=(seasons[0], seasons[-1])
)
toss_choice = st.sidebar.multiselect(
    "Toss decision",
    options=sorted(df["toss_decision"].unique()),
    default=sorted(df["toss_decision"].unique()),
)

data = df[
    (df["season"].between(season_range[0], season_range[1]))
    & (df["toss_decision"].isin(toss_choice))
]

# ---------- Title ----------
st.title("🏏 IPL Matches Dashboard (2008–2017)")
st.write("Explore how teams won, how the toss mattered, and how big the wins were.")

if data.empty:
    st.warning("No matches for these filters. Please widen your selection.")
    st.stop()

# ---------- Key numbers ----------
runs = data[data["win_by_runs"] > 0]
top_team = data["winner"].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches", len(data))
c2.metric("Most wins", top_team.index[0], f"{top_team.iloc[0]} wins")
c3.metric("Avg win margin (runs)", f"{runs['win_by_runs'].mean():.1f}" if len(runs) else "N/A")
c4.metric(
    "Toss winner won match",
    f"{(data['toss_winner'] == data['winner']).mean() * 100:.1f}%",
)

# ---------- Chart 1: wins per team ----------
st.subheader("1. Wins per team")
order = data["winner"].value_counts().index
fig1, ax1 = plt.subplots(figsize=(9, 5))
sns.countplot(data=data, y="winner", order=order, color="#4C72B0", ax=ax1)
ax1.set_xlabel("Number of wins")
ax1.set_ylabel("")
ax1.set_title("Mumbai Indians lead the table" if season_range == (seasons[0], seasons[-1]) else "Wins per team")
st.pyplot(fig1)

# ---------- Chart 2 and 3 side by side ----------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("2. Toss decision by season")
    toss_season = data.groupby(["season", "toss_decision"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    toss_season.plot(kind="bar", stacked=True, ax=ax2, color=["#DD8452", "#4C72B0"][: len(toss_season.columns)])
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Matches")
    ax2.set_title("Captains increasingly choose to field")
    ax2.legend(title="Toss decision")
    plt.xticks(rotation=0)
    st.pyplot(fig2)

with col_b:
    st.subheader("3. Win margin (runs) by toss decision")
    if len(runs):
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=runs, x="toss_decision", y="win_by_runs", hue="toss_decision", palette="Set2", legend=False, ax=ax3)
        ax3.set_xlabel("Toss decision")
        ax3.set_ylabel("Win by runs")
        ax3.set_title("Margin of victory when batting first")
        st.pyplot(fig3)
    else:
        st.info("No run-margin wins in this selection.")

# ---------- Bonus: download ----------
st.download_button(
    "⬇️ Download clean data (CSV)",
    data=data.to_csv(index=False).encode("utf-8"),
    file_name="clean_matches_filtered.csv",
    mime="text/csv",
)
