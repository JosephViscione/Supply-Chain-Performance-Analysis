import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="📦",
    layout="wide"
)

@st.cache_data
def load_data():
    base = "outputs/"
    return {
        'kpi':      pd.read_csv(f"{base}kpi_summary.csv"),
        'cats':     pd.read_csv(f"{base}revenue_by_category_top10.csv"),
        'segment':  pd.read_csv(f"{base}revenue_by_segment.csv"),
        'abc':      pd.read_csv(f"{base}abc_summary.csv"),
        'trend':    pd.read_csv(f"{base}monthly_trend.csv", parse_dates=['date']),
        'shipping': pd.read_csv(f"{base}shipping_performance.csv"),
        'region':   pd.read_csv(f"{base}revenue_by_region.csv"),
    }

d = load_data()

NAVY  = '#1F3864'
BLUE  = '#2E75B6'
TEAL  = '#17A589'
AMBER = '#E67E22'
GRAY  = '#7F8C8D'
BG    = '#F8F9FA'

def clean_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(length=0, colors='#444444')
    ax.set_facecolor(BG)
    ax.xaxis.label.set_color('#444444')
    ax.yaxis.label.set_color('#444444')

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    f"<h1 style='color:{NAVY};margin-bottom:0;'>📦 Supply Chain Performance Dashboard</h1>",
    unsafe_allow_html=True
)
st.caption("DataCo Global · Pipeline: Python → MySQL → Streamlit")
st.divider()

# ── KPI Cards ──────────────────────────────────────────────────────────────────
kpi = d['kpi'].iloc[0]
c1, c2, c3, c4 = st.columns(4)

for col, label, value, color in [
    (c1, "Total Revenue",      f"${kpi['total_revenue']/1e6:.1f}M",  BLUE),
    (c2, "Total Orders",       f"{int(kpi['total_orders']):,}",       NAVY),
    (c3, "Avg Profit Margin",  f"{kpi['avg_profit_margin']:.1f}%",    TEAL),
    (c4, "Late Delivery Rate", f"{kpi['late_delivery_rate']:.1f}%",   "#C0392B"),
]:
    col.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E0E0E0;border-top:4px solid {color};
                border-radius:8px;padding:16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:{color};">{value}</div>
        <div style="font-size:11px;color:{GRAY};margin-top:4px;text-transform:uppercase;
                    letter-spacing:0.05em;">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Row 1: Categories + Segment & ABC ─────────────────────────────────────────
st.subheader("Product Performance")
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("**Top 10 Categories by Revenue**")
    cs = d['cats'].sort_values('total_revenue', ascending=True).copy()
    colors = [BLUE] * len(cs)
    colors[-1] = NAVY

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    ax.barh(cs['category_name'], cs['total_revenue'] / 1e6,
            color=colors, edgecolor='none', height=0.62)
    for i, val in enumerate(cs['total_revenue'] / 1e6):
        ax.text(val + 0.08, i, f'${val:.1f}M', va='center',
                fontsize=9.5, color='#2C3E50', fontweight='bold')
    ax.set_xlim(0, cs['total_revenue'].max() / 1e6 * 1.22)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}M'))
    plt.subplots_adjust(left=0.28)
    clean_ax(ax)
    st.pyplot(fig)
    plt.close()

with col_right:
    st.markdown("**Revenue by Customer Segment**")
    ss = d['segment'].sort_values('total_revenue', ascending=True).copy()
    ss['pct'] = ss['total_revenue'] / ss['total_revenue'].sum() * 100

    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    fig.patch.set_facecolor('white')
    ax.barh(ss['customer_segment'], ss['pct'],
            color=TEAL, edgecolor='none', height=0.5)
    for i, val in enumerate(ss['pct']):
        ax.text(val + 0.5, i, f'{val:.0f}%', va='center',
                fontsize=10, color='#2C3E50', fontweight='bold')
    ax.set_xlim(0, 100 * 1.18)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    clean_ax(ax)
    plt.tight_layout(pad=1.2)
    st.pyplot(fig)
    plt.close()

    # Change 2: ABC bar chart - clean labels, no duplication
    st.markdown("**ABC Inventory Classification**")
    abc_df = d['abc'].copy()
    abc_label_map = {
        'A': 'Class A (80% of revenue)',
        'B': 'Class B (15% of revenue)',
        'C': 'Class C (5% of revenue)',
    }
    abc_color_map = {'A': BLUE, 'B': TEAL, 'C': GRAY}
    abc_df['label'] = abc_df['abc_class'].map(abc_label_map)
    abc_df = abc_df.sort_values('product_count', ascending=True)

    fig, ax = plt.subplots(figsize=(5.5, 2.5))
    fig.patch.set_facecolor('white')
    bar_colors = [abc_color_map[c] for c in abc_df['abc_class']]
    ax.barh(abc_df['label'], abc_df['product_count'],
            color=bar_colors, edgecolor='none', height=0.45)
    for i, val in enumerate(abc_df['product_count']):
        ax.text(val + 0.5, i, f'{int(val)} products', va='center',
                fontsize=9, color='#2C3E50')
    ax.set_xlim(0, abc_df['product_count'].max() * 1.35)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x)}'))
    clean_ax(ax)
    plt.tight_layout(pad=1.0)
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Monthly Trend ──────────────────────────────────────────────────────────────
st.subheader("Monthly Revenue & Profit Trend (2016)")
t16 = d['trend'][d['trend']['order_year'] == 2016].copy()
t16['revenue_rolling_avg'] = t16['total_revenue'].rolling(window=3).mean()
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax = plt.subplots(figsize=(12, 4))
fig.patch.set_facecolor('white')
ax.plot(months, t16['total_revenue'] / 1e6, color=BLUE, linewidth=2.5,
        marker='o', markersize=6, markerfacecolor='white',
        markeredgecolor=BLUE, markeredgewidth=2, label='Revenue', zorder=3)
ax.plot(months, t16['total_profit'] / 1e6, color=TEAL, linewidth=2,
        marker='s', markersize=5, markerfacecolor='white',
        markeredgecolor=TEAL, markeredgewidth=1.5, label='Profit', zorder=3)
ax.fill_between(months, t16['total_revenue'] / 1e6, alpha=0.07, color=BLUE)
ax.plot(months, t16['revenue_rolling_avg'] / 1e6, color=AMBER, linewidth=2,
        linestyle='--', label='Revenue (3-Month Rolling Avg)', zorder=3)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.2f}M'))
ax.legend(frameon=False, fontsize=10)
ax.grid(axis='y', alpha=0.2, color='#CCCCCC')
clean_ax(ax)
plt.tight_layout(pad=1.2)
st.pyplot(fig)
plt.close()

st.divider()

# ── Operations & Regional Performance ─────────────────────────────────────────
st.subheader("Operations & Regional Performance")
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("**Delivery Performance by Shipping Mode**")
    ship = d['shipping'][['shipping_mode', 'total_orders', 'total_revenue', 'avg_actual_days', 'late_delivery_pct']].copy()
    ship['total_revenue']     = ship['total_revenue'].apply(lambda x: f'${x/1e6:.1f}M')
    ship['avg_actual_days']   = ship['avg_actual_days'].apply(lambda x: f'{x:.1f} days')
    ship['late_delivery_pct'] = ship['late_delivery_pct'].apply(lambda x: f'{x:.1f}%')
    ship['total_orders']      = ship['total_orders'].apply(lambda x: f'{int(x):,}')
    ship.columns = ['Shipping Mode', 'Total Orders', 'Revenue', 'Avg Days', 'Late %']
    st.dataframe(ship, hide_index=True, use_container_width=True)

with col_right:
    st.markdown("**Revenue by Market**")
    rm = (d['region'].groupby('market')['total_revenue']
          .sum().reset_index()
          .sort_values('total_revenue', ascending=True))

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor('white')
    ax.barh(rm['market'], rm['total_revenue'] / 1e6,
            color=AMBER, edgecolor='none', height=0.5)
    for i, val in enumerate(rm['total_revenue'] / 1e6):
        ax.text(val + 0.1, i, f'${val:.1f}M', va='center',
                fontsize=9.5, color='#2C3E50', fontweight='bold')
    ax.set_xlim(0, rm['total_revenue'].max() / 1e6 * 1.28)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}M'))
    clean_ax(ax)
    plt.tight_layout(pad=1.2)
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.subheader("Key Insights")
st.markdown("""
- **ABC Classification:** 7 products (Class A) drive 80% of total revenue, while 95 products (Class C) contribute just 5%. Inventory and forecasting efforts should prioritize the Class A group.
- **Shipping Performance:** Second Class shipping has the highest late delivery rate at 76.6%, despite handling significantly fewer orders than Standard Class. This represents a clear operational bottleneck.
- **Customer Segments:** Consumer customers generate 52% of total revenue, followed by Corporate at 30% and Home Office at 18%. Marketing and retention efforts are best focused on the Consumer segment.
- **Revenue Trend:** Monthly revenue shows consistent growth through 2016, with seasonal peaks suggesting opportunity for targeted promotional planning during high-volume periods.
""")
