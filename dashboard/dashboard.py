"""
Bike Sharing Data Dashboard
Capital Bikeshare Washington D.C. (2011–2012)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
)

sns.set_theme(style="whitegrid", palette="muted")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    day  = pd.read_csv("main_data.csv",  parse_dates=["dteday"])
    hour = pd.read_csv("hour_data.csv",  parse_dates=["dteday"])
    return day, hour

df_day, df_hour = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/color/96/bicycle.png",
    width=80,
)
st.sidebar.title("Filter Data")

year_options = sorted(df_day["year"].unique())
sel_years = st.sidebar.multiselect("Tahun", year_options, default=year_options)

season_options = ["Spring", "Summer", "Fall", "Winter"]
sel_seasons = st.sidebar.multiselect("Musim", season_options, default=season_options)

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=[df_day["dteday"].min(), df_day["dteday"].max()],
    min_value=df_day["dteday"].min(),
    max_value=df_day["dteday"].max(),
)

# Apply filters
mask = (
    df_day["year"].isin(sel_years) &
    df_day["season_label"].isin(sel_seasons) &
    (df_day["dteday"] >= pd.Timestamp(date_range[0])) &
    (df_day["dteday"] <= pd.Timestamp(date_range[1]))
)
df_filtered = df_day[mask]

mask_h = (
    df_hour["year"].isin(sel_years) &
    df_hour["season_label"].isin(sel_seasons)
)
df_hour_f = df_hour[mask_h]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown(
    "**Dataset:** Capital Bikeshare Washington D.C. (2011–2012)  "
    "| Analisis pola permintaan dan faktor lingkungan yang memengaruhi penyewaan sepeda."
)
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{df_filtered['cnt'].sum():,.0f}")
col2.metric("Rata-rata / Hari", f"{df_filtered['cnt'].mean():,.0f}")
col3.metric("Hari Tertinggi",   f"{df_filtered['cnt'].max():,.0f}")
col4.metric("Penyewa Terdaftar (%)",
            f"{(df_filtered['registered'].sum() / df_filtered['cnt'].sum() * 100):.1f}%")

st.divider()

# ── Tab layout ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pola Per Jam",
    "🌤️ Faktor Lingkungan",
    "📅 Tren Bulanan",
    "🗂️ Kluster Permintaan",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 – Hourly pattern
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Pola Rata-rata Penyewaan Per Jam")
    st.markdown(
        "Visualisasi ini menjawab **Pertanyaan Bisnis 1**: "
        "_Bagaimana pola penyewaan per jam antara hari kerja dan hari libur?_"
    )

    hourly_wd  = df_hour_f[df_hour_f["workingday"] == 1].groupby("hr")["cnt"].mean()
    hourly_nwd = df_hour_f[df_hour_f["workingday"] == 0].groupby("hr")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(hourly_wd.index,  hourly_wd.values,  marker="o", lw=2.2,
            color="#2196F3", label="Hari Kerja", ms=5)
    ax.plot(hourly_nwd.index, hourly_nwd.values, marker="s", lw=2.2,
            color="#FF9800", label="Hari Libur / Akhir Pekan", ms=5, ls="--")

    if not hourly_wd.empty:
        ax.annotate(
            f"Puncak\nJam {hourly_wd.idxmax()}:00\n({hourly_wd.max():.0f})",
            xy=(hourly_wd.idxmax(), hourly_wd.max()),
            xytext=(hourly_wd.idxmax() - 3.5, hourly_wd.max() + 18),
            arrowprops=dict(arrowstyle="->", color="#2196F3"),
            color="#2196F3", fontsize=8.5,
        )
    if not hourly_nwd.empty:
        ax.annotate(
            f"Puncak\nJam {hourly_nwd.idxmax()}:00\n({hourly_nwd.max():.0f})",
            xy=(hourly_nwd.idxmax(), hourly_nwd.max()),
            xytext=(hourly_nwd.idxmax() + 1, hourly_nwd.max() + 18),
            arrowprops=dict(arrowstyle="->", color="#FF9800"),
            color="#FF9800", fontsize=8.5,
        )

    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam (0–23)", fontsize=10)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=10)
    ax.set_title("Pola Penyewaan Sepeda Per Jam: Hari Kerja vs. Hari Libur",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    c1, c2 = st.columns(2)
    if not hourly_wd.empty:
        c1.info(f"🕗 **Jam puncak hari kerja:** {hourly_wd.idxmax()}:00 "
                f"(rata-rata {hourly_wd.max():.0f} sewa)")
    if not hourly_nwd.empty:
        c2.info(f"🕛 **Jam puncak hari libur:** {hourly_nwd.idxmax()}:00 "
                f"(rata-rata {hourly_nwd.max():.0f} sewa)")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 – Environmental factors
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Pengaruh Faktor Lingkungan terhadap Penyewaan Harian")
    st.markdown(
        "Visualisasi ini menjawab **Pertanyaan Bisnis 2**: "
        "_Faktor lingkungan apa yang paling berpengaruh terhadap penyewaan harian?_"
    )

    c_left, c_right = st.columns(2)

    # Season bar chart
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_avg = (
        df_filtered.groupby("season_label")["cnt"]
        .mean()
        .reindex(season_order)
        .dropna()
    )
    with c_left:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        colors = ["#81C784", "#FFB74D", "#FF7043", "#64B5F6"]
        bars = ax2.bar(season_avg.index, season_avg.values,
                       color=colors[: len(season_avg)], edgecolor="white", width=0.55)
        for bar, val in zip(bars, season_avg.values):
            ax2.text(bar.get_x() + bar.get_width() / 2, val + 30, f"{val:,.0f}",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax2.set_ylabel("Rata-rata Penyewaan / Hari", fontsize=10)
        ax2.set_title("Rata-rata Sewa per Musim", fontsize=11, fontweight="bold")
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax2.set_ylim(0, season_avg.max() * 1.18 if not season_avg.empty else 10)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # Weather bar chart
    weather_avg = (
        df_filtered.groupby("weather_label")["cnt"]
        .mean()
        .sort_values(ascending=False)
    )
    with c_right:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        wcolors = ["#29B6F6", "#78909C", "#90A4AE", "#546E7A"]
        bars3 = ax3.barh(weather_avg.index, weather_avg.values,
                          color=wcolors[: len(weather_avg)], edgecolor="white", height=0.5)
        for bar, val in zip(bars3, weather_avg.values):
            ax3.text(val + 30, bar.get_y() + bar.get_height() / 2, f"{val:,.0f}",
                     va="center", fontsize=9, fontweight="bold")
        ax3.set_xlabel("Rata-rata Penyewaan / Hari", fontsize=10)
        ax3.set_title("Rata-rata Sewa per Kondisi Cuaca", fontsize=11, fontweight="bold")
        ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax3.set_xlim(0, weather_avg.max() * 1.22 if not weather_avg.empty else 10)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    # Temperature cluster
    st.markdown("#### Rata-rata Sewa berdasarkan Kluster Suhu (Binning)")
    temp_avg = (
        df_filtered.groupby("temp_cluster", observed=True)["cnt"]
        .mean()
        .dropna()
    )
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    tcolors = ["#90CAF9", "#42A5F5", "#FF8A65", "#EF5350"]
    bars4 = ax4.bar(range(len(temp_avg)), temp_avg.values,
                    color=tcolors[: len(temp_avg)], edgecolor="white", width=0.55)
    ax4.set_xticks(range(len(temp_avg)))
    ax4.set_xticklabels(temp_avg.index, fontsize=9, rotation=10, ha="right")
    for bar, val in zip(bars4, temp_avg.values):
        ax4.text(bar.get_x() + bar.get_width() / 2, val + 30, f"{val:,.0f}",
                 ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax4.set_ylabel("Rata-rata Penyewaan / Hari", fontsize=10)
    ax4.set_title("Rata-rata Sewa per Kluster Suhu", fontsize=11, fontweight="bold")
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax4.set_ylim(0, temp_avg.max() * 1.15 if not temp_avg.empty else 10)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close()


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 – Monthly trend
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Tren Penyewaan Bulanan per Tahun")

    monthly = (
        df_filtered
        .groupby(["year", "mnth"])["cnt"]
        .mean()
        .reset_index()
    )
    bulan_label = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    palette = {2011: "#1565C0", 2012: "#E53935"}

    fig5, ax5 = plt.subplots(figsize=(12, 5))
    for yr in sorted(monthly["year"].unique()):
        d = monthly[monthly["year"] == yr].set_index("mnth")["cnt"]
        ax5.plot(d.index, d.values, marker="o", lw=2.2,
                 label=str(yr), color=palette.get(yr, "#888"), ms=6)

    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels(bulan_label, fontsize=10)
    ax5.set_xlabel("Bulan", fontsize=11)
    ax5.set_ylabel("Rata-rata Penyewaan / Hari", fontsize=11)
    ax5.set_title("Tren Penyewaan Sepeda Bulanan: 2011 vs. 2012",
                  fontsize=12, fontweight="bold")
    ax5.legend(title="Tahun", fontsize=10)
    ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close()

    yearly = df_filtered.groupby("year")["cnt"].agg(["sum", "mean"]).round(0)
    yearly.columns = ["Total Sewa", "Rata-rata / Hari"]
    st.dataframe(yearly, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 – Demand clustering
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Kluster Permintaan Harian (Binning)")
    st.markdown(
        "Hari-hari dikelompokkan ke dalam **4 kluster permintaan** "
        "berdasarkan volume penyewaan (Rendah / Sedang / Tinggi / Sangat Tinggi)."
    )

    cluster_summary = (
        df_filtered
        .groupby("demand_cluster", observed=True)
        .agg(
            Jumlah_Hari=("cnt", "count"),
            Min_Sewa=("cnt", "min"),
            Max_Sewa=("cnt", "max"),
            Mean_Sewa=("cnt", "mean"),
            Pct_Workingday=("workingday", "mean"),
        )
        .round(1)
    )
    cluster_summary["Pct_Workingday"] = (cluster_summary["Pct_Workingday"] * 100).round(1)
    st.dataframe(
        cluster_summary.reindex(["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]),
        use_container_width=True,
    )

    # Stacked bar: cluster × season
    cluster_season = (
        df_filtered
        .groupby(["demand_cluster", "season_label"], observed=True)
        .size()
        .unstack(fill_value=0)
    )
    fig6, ax6 = plt.subplots(figsize=(10, 4.5))
    cluster_season.reindex(
        ["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
    ).plot(
        kind="bar", stacked=True, ax=ax6,
        color=["#81C784", "#FFB74D", "#FF7043", "#64B5F6"],
        edgecolor="white", linewidth=0.8,
    )
    ax6.set_xlabel("Kluster Permintaan", fontsize=11)
    ax6.set_ylabel("Jumlah Hari", fontsize=11)
    ax6.set_title("Distribusi Kluster Permintaan Harian berdasarkan Musim",
                  fontsize=12, fontweight="bold")
    ax6.legend(title="Musim", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax6.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close()

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:#888; font-size:12px;'>"
    "Bike Sharing Dataset · Capital Bikeshare Washington D.C. (2011–2012) · "
    "Dashboard dibuat dengan Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
