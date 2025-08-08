
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path

def make_gantt(csv_in: str, png_out: str):
    df = pd.read_csv(csv_in)
    # Basic validation
    required = {"Task","Start","End"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    # Parse dates
    df["Start"] = pd.to_datetime(df["Start"]).dt.date
    df["End"]   = pd.to_datetime(df["End"]).dt.date
    # Sort by start date
    df = df.sort_values(by=["Start","End"]).reset_index(drop=True)

    # Prepare plotting
    fig, ax = plt.subplots(figsize=(10, 0.5*len(df)+2))
    # One row per task
    yticks = []
    ylabels = []
    for i, row in df.iterrows():
        start = mdates.date2num(row["Start"])
        end   = mdates.date2num(row["End"])
        width = max(end - start, 0.3)  # ensure visible even if same-day
        ax.barh(i, width, left=start, align="center")
        # Annotate with task name
        ax.text(start, i, f"  {row['Task']}", va="center", ha="left")
        yticks.append(i)
        owner = row.get("Owner", "")
        ylabels.append(owner if pd.notna(owner) else "")

    ax.set_yticks(yticks)
    if any(lbl != "" for lbl in ylabels):
        ax.set_yticklabels(ylabels)
        ax.set_ylabel("Owner")
    else:
        ax.set_yticklabels([str(i+1) for i in yticks])

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    ax.set_xlabel("Date")
    ax.set_title("Project Gantt Chart")

    fig.tight_layout()
    fig.savefig(png_out, dpi=150)
    plt.close(fig)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    csv_in = str(base / "tasks.csv")
    png_out = str(base / "gantt.png")
    make_gantt(csv_in, png_out)
    print(f"Saved {png_out}")
