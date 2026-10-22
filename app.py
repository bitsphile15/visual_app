import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="IPL Matches Dashboard", page_icon="🏏", layout="wide")

# ---------- Look & feel ----------
BLUE, ORANGE, RED, GREY = "#1F4E79", "#E8833A", "#C0392B", "#9DB4C0"
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.size": 13, "axes.titlesize": 16, "axes.titleweight": "bold",
    "axes.labelsize": 13, "xtick.labelsize": 12, "ytick.labelsize": 12,
    "axes.spines.top": False, "axes.spines.right": False,
})

st.markdown(
    f"""
<style>
.block-container {{ padding-top: 2rem; max-width: 1250px; }}
.hero {{
    background: linear-gradient(120deg, {BLUE}, #2E86AB 60%, {ORANGE});
    padding: 2rem 2.2rem; border-radius: 18px; color: white; margin-bottom: 1.5rem;
}}
.hero h1 {{ color: white; font-size: 2.8rem; margin: 0; }}
.hero p  {{ font-size: 1.3rem; margin: .4rem 0 0 0; opacity: .95; }}
div[data-testid="stMetric"] {{
    background: rgba(46,134,171,0.10); border: 1px solid rgba(46,134,171,0.35);
    border-radius: 14px; padding: 1rem 1.2rem;
}}
div[data-testid="stMetricLabel"] p {{ font-size: 1.1rem; }}
div[data-testid="stMetricValue"]   {{ font-size: 2.1rem; font-weight: 700; }}
h2, h3 {{ font-size: 1.9rem !important; margin-top: 1.5rem !important; }}
.insight {{
    background: rgba(232,131,58,0.12); border-left: 7px solid {ORANGE};
    border-radius: 12px; padding: 1.1rem 1.6rem; margin: .8rem 0 2rem 0;
}}
.insight h4 {{ font-size: 1.5rem; margin: 0 0 .5rem 0; }}
.insight ul {{ margin: 0; padding-left: 1.4rem; }}
.insight li {{ font-size: 1.3rem; line-height: 1.75; margin-bottom: .3rem; }}
</style>
""",
    unsafe_allow_html=True,
)


def insight(bullets):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    st.markdown(
        f'<div class="insight"><h4>💡 What this chart says</h4><ul>{items}</ul></div>',
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data():
    df = pd.read_csv("clean_matches.csv")
    df["city"] = df["city"].fillna(df["city"].mode()[0])
    return df.dropna()


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("🎛️ Filters")
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
    df["season"].between(season_range[0], season_range[1])
    & df["toss_decision"].isin(toss_choice)
]

# ---------- Header ----------
st.markdown(
    """<div class="hero"><h1>🏏 IPL Matches Dashboard</h1>
<p>Seasons 2008–2017: who won, how the toss mattered, and how big the wins were.</p></div>""",
    unsafe_allow_html=True,
)

if data.empty:
    st.warning("No matches for these filters. Please widen your selection.")
    st.stop()

# ---------- Key numbers ----------
runs = data[data["win_by_runs"] > 0]
wins = data["winner"].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches", len(data))
c2.metric("Most wins", wins.index[0], f"{wins.iloc[0]} wins")
c3.metric("Avg win margin (runs)", f"{runs['win_by_runs'].mean():.1f}" if len(runs) else "N/A")
c4.metric("Toss winner won match", f"{(data['toss_winner'] == data['winner']).mean() * 100:.1f}%")

# ---------- Chart 1 ----------
st.subheader("1️⃣ Wins per team")
colors = [RED if t == wins.index[0] else GREY for t in wins.index]
fig1, ax1 = plt.subplots(figsize=(10, 5.5))
sns.countplot(data=data, y="winner", order=wins.index, hue="winner",
              palette=colors, legend=False, ax=ax1)
for cont in ax1.containers:
    ax1.bar_label(cont, padding=4, fontsize=12)
ax1.set_xlabel("Number of wins")
ax1.set_ylabel("")
ax1.set_title(f"{wins.index[0]} won the most matches")
sns.despine(left=True)
st.pyplot(fig1)

insight([
    f"<b>{wins.index[0]}</b> won the most matches: <b>{wins.iloc[0]}</b> out of {len(data)} ({wins.iloc[0] / len(data) * 100:.1f}%).",
    f"<b>{wins.index[-1]}</b> won the fewest: only <b>{wins.iloc[-1]}</b> matches.",
    f"The top 3 teams ({', '.join(wins.index[:3])}) together won <b>{wins.iloc[:3].sum() / len(data) * 100:.0f}%</b> of all matches.",
])

# ---------- Chart 2 ----------
st.subheader("2️⃣ Toss decision by season")
toss_season = data.groupby(["season", "toss_decision"]).size().unstack(fill_value=0)
palette = {"bat": ORANGE, "field": BLUE}
fig2, ax2 = plt.subplots(figsize=(10, 5))
toss_season.plot(kind="bar", stacked=True, ax=ax2,
                 color=[palette[c] for c in toss_season.columns], width=0.75)
ax2.set_xlabel("Season")
ax2.set_ylabel("Matches")
ax2.set_title("Captains increasingly choose to field")
ax2.legend(title="Toss decision", fontsize=12, title_fontsize=12)
plt.xticks(rotation=0)
st.pyplot(fig2)

field_share = (toss_season.get("field", 0) / toss_season.sum(axis=1) * 100).round(0)
insight([
    f"Overall, captains chose to <b>field in {(data['toss_decision'] == 'field').mean() * 100:.0f}%</b> of matches.",
    f"In {field_share.index[0]}, <b>{field_share.iloc[0]:.0f}%</b> chose to field; in {field_share.index[-1]}, it was <b>{field_share.iloc[-1]:.0f}%</b>.",
    f"Season with the most fielding choices: <b>{field_share.idxmax()}</b> ({field_share.max():.0f}%).",
])

# ---------- Chart 3 ----------
st.subheader("3️⃣ Win margin (runs) by toss decision")
if len(runs):
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=runs, x="toss_decision", y="win_by_runs", hue="toss_decision",
                palette=palette, legend=False, width=0.5, ax=ax3)
    ax3.set_xlabel("Toss decision")
    ax3.set_ylabel("Win by runs")
    ax3.set_title("Margin of victory when winning by runs")
    st.pyplot(fig3)

    med = runs.groupby("toss_decision")["win_by_runs"].median()
    big = runs.loc[runs["win_by_runs"].idxmax()]
    insight([
        "Median win margin: " + ", ".join(f"<b>{k}</b> = {v:.1f} runs" for k, v in med.items()) + ".",
        f"The average ({runs['win_by_runs'].mean():.1f}) is higher than the median ({runs['win_by_runs'].median():.1f}), so a few huge wins pull it up.",
        f"Biggest win: <b>{big['winner']}</b> by <b>{int(big['win_by_runs'])} runs</b> in {int(big['season'])}.",
    ])
else:
    st.info("No run-margin wins in this selection.")

# ---------- Download ----------
st.download_button(
    "⬇️ Download clean data (CSV)",
    data=data.to_csv(index=False).encode("utf-8"),
    file_name="clean_matches_filtered.csv",
    mime="text/csv",
)