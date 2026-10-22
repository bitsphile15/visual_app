# 🏏 IPL Matches Dashboard (2008–2017)

An interactive Streamlit dashboard that explores 10 seasons of Indian Premier League (IPL) cricket matches: which teams won the most, how the toss decision has changed, and how big the winning margins were.

**Live app:** [https://visualapp-pseb.streamlit.app/](https://visualapp-pseb.streamlit.app/)

**Author:** Qadeer Ahmed

---

## 📊 What the app shows

| Section | What it answers |
|---|---|
| **Key numbers** | Total matches, team with most wins, average win margin (runs), % of matches won by the toss winner |
| **1. Wins per team** | Which team won the most matches? |
| **2. Toss decision by season** | Do captains prefer to bat or field, and has that changed over time? |
| **3. Win margin by toss decision** | How big are wins by runs, and does the toss decision matter? |

Every chart has a **"What this chart says"** box with bullet-point insights that update automatically when you change the filters.

## 🎛️ Features

- **Season range filter** (slider)
- **Toss decision filter** (multi-select)
- **Download clean data** button (CSV of the currently filtered matches)
- Insights that recalculate for the selected filters

## 🔍 Key findings

1. **Mumbai Indians won the most matches**: 92 of 632, ahead of Chennai Super Kings (79) and Kolkata Knight Riders (77).
2. **Captains now prefer to field**: 57% overall chose to field, rising from 55% in 2008 to about 83% in 2017.
3. **Chasing teams win slightly more often**: 54% of matches were won by wickets and 45% by runs (7 ties).
4. **The toss is only a small advantage**: toss winners won 51.3% of matches. Those who chose to field won 55.7%, against 45.4% for those who chose to bat.
5. **Most wins by runs are narrow**: the median margin is 22.5 runs, but the average is 30.4 because a few huge wins pull it up. The biggest win was 146 runs (Mumbai Indians, 2017).

## 🧹 Data cleaning

The dataset is `clean_matches.csv` (636 matches, 17 columns). The app applies the same cleaning as the analysis notebook:

- Missing `city` values are filled with the most common city (mode).
- Rows with other missing values are dropped (632 matches remain).
- No duplicate rows were found.
- Zero values in both `win_by_runs` and `win_by_wickets` are valid, because they are tied matches.

## 📁 Project files

```
├── app.py               # Streamlit app
├── clean_matches.csv    # Dataset
├── requirements.txt     # Python dependencies
├── Qadeer_Ahmed.ipynb   # Analysis notebook (Parts A–C)
└── README.md
```

## 🚀 Run it locally

```bash
# 1. Install the dependencies
pip install -r requirements.txt

# 2. Start the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repository to GitHub (make sure `clean_matches.csv` is in the root folder).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, select this repository, and set the main file to `app.py`.
4. Click **Deploy**.

## 🛠️ Built with

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/) and [Matplotlib](https://matplotlib.org/)
- [Streamlit](https://streamlit.io/)