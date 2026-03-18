import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 페이지 설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="BIZ Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 커스텀 CSS (프리미엄 다크 테마)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── 메트릭 카드 ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1A1F2E 0%, #252B3B 100%);
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(108, 99, 255, 0.25);
    border-color: rgba(108, 99, 255, 0.5);
}
div[data-testid="stMetric"] label {
    color: #8B8FA3 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0E1117 0%, #151929 100%);
    border-right: 1px solid rgba(108, 99, 255, 0.15);
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(26, 31, 46, 0.5);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(108, 99, 255, 0.2) !important;
    border-color: transparent !important;
}

/* ── 차트 컨테이너 ── */
div[data-testid="stPlotlyChart"] {
    background: rgba(26, 31, 46, 0.4);
    border-radius: 12px;
    padding: 8px;
    border: 1px solid rgba(108, 99, 255, 0.1);
    transition: border-color 0.3s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(108, 99, 255, 0.3);
}

/* ── 데이터프레임 ── */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(108, 99, 255, 0.15);
}

/* ── 버튼 ── */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 1px solid rgba(108, 99, 255, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #6C63FF 0%, #5A52E0 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 28px;
    transition: all 0.3s ease;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
}

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0E1117; }
::-webkit-scrollbar-thumb { background: #6C63FF; border-radius: 3px; }

/* ── Divider ── */
hr { border-color: rgba(108, 99, 255, 0.15) !important; }
.block-container { padding-top: 2rem; }

/* ── 커스텀 HTML 컴포넌트 ── */
.gradient-title {
    background: linear-gradient(120deg, #6C63FF 0%, #00D2FF 50%, #6C63FF 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 3s ease infinite;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
@keyframes gradient-shift {
    0% { background-position: 0% center; }
    50% { background-position: 100% center; }
    100% { background-position: 0% center; }
}
.page-subtitle {
    color: #8B8FA3;
    font-size: 1rem;
    margin-bottom: 2rem;
}
.section-header {
    color: #C8C8FF;
    font-size: 1.15rem;
    font-weight: 600;
    margin: 1.5rem 0 1rem 0;
    padding-left: 12px;
    border-left: 3px solid #6C63FF;
}
.kpi-card {
    background: linear-gradient(135deg, #1A1F2E 0%, #252B3B 100%);
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6C63FF, #00D2FF);
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(108, 99, 255, 0.2);
}
.kpi-icon { font-size: 2rem; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #FFFFFF; margin: 4px 0; }
.kpi-label { font-size: 0.85rem; color: #8B8FA3; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.kpi-delta { font-size: 0.85rem; font-weight: 600; padding: 4px 12px; border-radius: 20px; display: inline-block; }
.kpi-delta.positive { color: #00E676; background: rgba(0, 230, 118, 0.1); }
.kpi-delta.negative { color: #FF5252; background: rgba(255, 82, 82, 0.1); }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 차트 설정 (공통 다크 테마)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COLORS = ["#6C63FF", "#00D2FF", "#FF6B6B", "#FFD93D", "#6BCB77", "#EE82EE", "#FFA07A"]
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#E0E0E0", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0)", font=dict(size=11),
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
    ),
    xaxis=dict(gridcolor="rgba(108,99,255,0.08)", zerolinecolor="rgba(108,99,255,0.1)"),
    yaxis=dict(gridcolor="rgba(108,99,255,0.08)", zerolinecolor="rgba(108,99,255,0.1)"),
    hoverlabel=dict(bgcolor="#1A1F2E", font_size=12, font_color="#E0E0E0"),
)


def apply_dark(fig, title=""):
    """Plotly Figure에 다크 테마를 적용합니다."""
    fig.update_layout(**DARK_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=16, color="#C8C8FF")))
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 데이터 생성 (캐싱)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def generate_sales_data():
    """계절성과 트렌드를 반영한 다차원 비즈니스 가상 데이터를 생성합니다."""
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    categories = ["전자제품", "의류", "식품", "뷰티", "가구"]
    regions = ["서울", "부산", "대구", "제주"]
    base_sales = {"전자제품": 3500000, "의류": 2200000,
                  "식품": 1800000, "뷰티": 1500000, "가구": 2800000}
    region_weights = {"서울": 1.3, "부산": 1.0, "대구": 0.85, "제주": 0.65}
    seasonal = {
        "전자제품": [0.8, 0.7, 0.9, 0.85, 0.9, 1.0, 0.95, 0.9, 1.1, 1.0, 1.3, 1.5],
        "의류":     [1.2, 1.1, 1.3, 1.0, 0.9, 0.8, 0.7, 0.8, 1.1, 1.2, 1.3, 1.4],
        "식품":     [1.0, 0.95, 1.0, 1.0, 1.05, 1.1, 1.15, 1.1, 1.05, 1.0, 1.0, 1.1],
        "뷰티":    [0.9, 1.0, 1.1, 1.0, 1.2, 1.1, 1.0, 1.0, 1.1, 1.0, 1.15, 1.3],
        "가구":     [0.7, 0.8, 1.1, 1.2, 1.0, 0.9, 0.8, 0.9, 1.0, 1.1, 1.0, 0.9],
    }
    records = []
    for date in dates:
        for cat in categories:
            for region in regions:
                m = date.month - 1
                trend = 1 + m * 0.015
                base = base_sales[cat] * region_weights[region] * seasonal[cat][m] * trend
                sales = int(base * np.random.uniform(0.80, 1.20))
                orders = max(1, int(sales / np.random.randint(30000, 80000)))
                visitors = int(orders * np.random.uniform(8, 15))
                satisfaction = round(np.random.uniform(3.5, 5.0), 1)
                records.append({
                    "날짜": date, "카테고리": cat, "지역": region,
                    "매출액": sales, "주문수": orders,
                    "방문자수": visitors, "고객만족도": satisfaction,
                })
    return pd.DataFrame(records)


@st.cache_data
def generate_customer_data():
    """고객 세그먼트 분석용 가상 데이터를 생성합니다."""
    np.random.seed(123)
    n = 2000
    age_groups = np.random.choice(
        ["10대", "20대", "30대", "40대", "50대", "60대+"],
        size=n, p=[0.05, 0.25, 0.30, 0.22, 0.13, 0.05])
    genders = np.random.choice(["남성", "여성"], size=n, p=[0.45, 0.55])
    channels = np.random.choice(
        ["검색엔진", "SNS", "직접방문", "이메일", "제휴사"],
        size=n, p=[0.30, 0.28, 0.20, 0.12, 0.10])
    age_purchase = {"10대": 35000, "20대": 55000, "30대": 85000,
                    "40대": 95000, "50대": 75000, "60대+": 60000}
    purchase_amounts = [int(age_purchase[a] * np.random.uniform(0.5, 2.0)) for a in age_groups]
    is_repeat = np.random.choice([True, False], size=n, p=[0.35, 0.65])
    months = np.random.choice(range(1, 13), size=n)
    return pd.DataFrame({
        "고객ID": [f"C{str(i).zfill(5)}" for i in range(1, n + 1)],
        "연령대": age_groups, "성별": genders, "유입채널": channels,
        "구매금액": purchase_amounts, "재구매여부": is_repeat, "구매월": months,
    })


@st.cache_data
def generate_funnel_data():
    """전환 펀넬 데이터를 생성합니다."""
    return pd.DataFrame({
        "단계": ["사이트 방문", "상품 조회", "장바구니 추가", "결제 시작", "결제 완료"],
        "사용자수": [50000, 32000, 18000, 12000, 8500],
    })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 헬퍼 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def kpi_card(icon, label, value, delta="", positive=True):
    """HTML 기반 프리미엄 KPI 카드를 렌더링합니다."""
    d_cls = "positive" if positive else "negative"
    d_arrow = "▲" if positive else "▼"
    d_html = f'<div class="kpi-delta {d_cls}">{d_arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {d_html}
    </div>""", unsafe_allow_html=True)


def section_header(text):
    """좌측 액센트 보더가 있는 섹션 헤더를 렌더링합니다."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def sparkline(values, color="#6C63FF", height=60):
    """미니 스파크라인 차트를 생성합니다."""
    fig = go.Figure(go.Scatter(
        y=values, mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy",
        fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=height,
        xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False,
    )
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 데이터 로딩
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
df_all = generate_sales_data()
cust_df_all = generate_customer_data()
funnel_df = generate_funnel_data()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. 사이드바 (글로벌 필터)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 1.5rem 0;">
        <div style="font-size:2.5rem; margin-bottom:4px;">📊</div>
        <div style="font-size:1.1rem; font-weight:700; color:#C8C8FF; letter-spacing:1px;">
            BIZ ANALYTICS</div>
        <div style="font-size:0.75rem; color:#8B8FA3; margin-top:2px;">
            Business Intelligence Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.header("🎛️ 필터 설정")

    # 기간 프리셋
    period = st.radio("📅 분석 기간", ["전체", "최근 30일", "최근 90일", "상반기", "하반기", "커스텀"], horizontal=False)
    if period == "커스텀":
        date_range = st.date_input("날짜 범위", value=[df_all["날짜"].min(), df_all["날짜"].max()],
                                   min_value=df_all["날짜"].min(), max_value=df_all["날짜"].max())
        if len(date_range) == 2:
            df_all = df_all[(df_all["날짜"] >= pd.to_datetime(date_range[0])) &
                            (df_all["날짜"] <= pd.to_datetime(date_range[1]))]
    elif period == "최근 30일":
        df_all = df_all[df_all["날짜"] >= df_all["날짜"].max() - pd.Timedelta(days=30)]
    elif period == "최근 90일":
        df_all = df_all[df_all["날짜"] >= df_all["날짜"].max() - pd.Timedelta(days=90)]
    elif period == "상반기":
        df_all = df_all[df_all["날짜"].dt.month <= 6]
    elif period == "하반기":
        df_all = df_all[df_all["날짜"].dt.month > 6]

    st.divider()

    # 카테고리 필터
    selected_cats = st.multiselect("🏷️ 카테고리", df_all["카테고리"].unique().tolist(),
                                   default=df_all["카테고리"].unique().tolist())
    # 지역 필터
    selected_regions = st.multiselect("📍 지역", df_all["지역"].unique().tolist(),
                                      default=df_all["지역"].unique().tolist())

    st.divider()
    st.markdown('<div style="text-align:center; color:#8B8FA3; font-size:0.75rem;">'
                '© 2025 BIZ Analytics<br>Powered by Streamlit</div>', unsafe_allow_html=True)

# 필터 적용
filtered = df_all[df_all["카테고리"].isin(selected_cats) & df_all["지역"].isin(selected_regions)]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. KPI 계산
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
total_sales = filtered["매출액"].sum()
total_orders = filtered["주문수"].sum()
avg_satisfaction = filtered["고객만족도"].mean()
avg_unit_price = int(total_sales / max(total_orders, 1))

# 전반/후반 비교
mid = filtered["날짜"].min() + (filtered["날짜"].max() - filtered["날짜"].min()) / 2
first_h = filtered[filtered["날짜"] <= mid]["매출액"].sum()
second_h = filtered[filtered["날짜"] > mid]["매출액"].sum()
sales_delta = round((second_h - first_h) / max(first_h, 1) * 100, 1)

first_o = filtered[filtered["날짜"] <= mid]["주문수"].sum()
second_o = filtered[filtered["날짜"] > mid]["주문수"].sum()
orders_delta = round((second_o - first_o) / max(first_o, 1) * 100, 1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. 메인 헤더 + KPI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="gradient-title">📊 BIZ Analytics Dashboard</div>'
            '<div class="page-subtitle">비즈니스 핵심 성과를 한눈에 파악하세요</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("💰", "총 매출액", f"{total_sales:,.0f}원",
             f"{abs(sales_delta)}% (후반기)", sales_delta >= 0)
with c2:
    kpi_card("📦", "총 주문 수", f"{total_orders:,}건",
             f"{abs(orders_delta)}% (후반기)", orders_delta >= 0)
with c3:
    kpi_card("💳", "평균 객단가", f"{avg_unit_price:,}원")
with c4:
    kpi_card("⭐", "고객 만족도", f"{avg_satisfaction:.2f}점",
             "목표 4.5점 이상", avg_satisfaction >= 4.5)

st.markdown("")
st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. 메인 탭 (4개 영역)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_sales, tab_customer, tab_data = st.tabs(
    ["🏠 종합 개요", "📊 매출 분석", "👥 고객 분석", "📋 데이터 관리"]
)

# ──────────────────────────────────────────────
# 탭 1: 종합 개요
# ──────────────────────────────────────────────
with tab_overview:
    section_header("📈 월별 추이 요약")
    monthly = filtered.groupby(filtered["날짜"].dt.to_period("M")).agg(
        매출액=("매출액", "sum"), 주문수=("주문수", "sum"),
        방문자수=("방문자수", "sum"), 고객만족도=("고객만족도", "mean"),
    ).reset_index()

    sp1, sp2, sp3, sp4 = st.columns(4)
    with sp1:
        st.caption("월별 매출 추이")
        st.plotly_chart(sparkline(monthly["매출액"].tolist(), "#6C63FF"), use_container_width=True)
    with sp2:
        st.caption("월별 주문 추이")
        st.plotly_chart(sparkline(monthly["주문수"].tolist(), "#00D2FF"), use_container_width=True)
    with sp3:
        st.caption("월별 방문자 추이")
        st.plotly_chart(sparkline(monthly["방문자수"].tolist(), "#FFD93D"), use_container_width=True)
    with sp4:
        st.caption("월별 만족도 추이")
        st.plotly_chart(sparkline(monthly["고객만족도"].tolist(), "#6BCB77"), use_container_width=True)

    st.markdown("")
    section_header("🗂️ 카테고리 · 지역 한눈에 보기")

    ov1, ov2 = st.columns(2)
    with ov1:
        cat_s = filtered.groupby("카테고리").agg(매출액=("매출액", "sum")).reset_index()
        fig_pie = px.pie(cat_s, names="카테고리", values="매출액", hole=0.55,
                         color_discrete_sequence=COLORS)
        fig_pie.update_traces(textposition="inside", textinfo="percent+label",
                              marker=dict(line=dict(color="#0E1117", width=2)))
        st.plotly_chart(apply_dark(fig_pie, "카테고리별 매출 비율"), use_container_width=True)

    with ov2:
        reg_s = filtered.groupby("지역").agg(매출액=("매출액", "sum")).reset_index().sort_values("매출액", ascending=True)
        fig_bar = px.bar(reg_s, x="매출액", y="지역", orientation="h", color_discrete_sequence=COLORS)
        fig_bar.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(apply_dark(fig_bar, "지역별 총 매출 비교"), use_container_width=True)

# ──────────────────────────────────────────────
# 탭 2: 매출 분석
# ──────────────────────────────────────────────
with tab_sales:
    stab1, stab2, stab3 = st.tabs(["📈 매출 추이", "🗺️ 히트맵 · 트리맵", "📦 분포 분석"])

    with stab1:
        section_header("일별 매출 추이 (이동평균 포함)")
        daily = filtered.groupby("날짜").agg(매출액=("매출액", "sum")).reset_index()
        fig_area = px.area(daily, x="날짜", y="매출액", color_discrete_sequence=COLORS)
        fig_area.update_traces(line=dict(width=1.5), opacity=0.7)
        if len(daily) > 7:
            ma = daily["매출액"].rolling(window=7, min_periods=1).mean()
            fig_area.add_trace(go.Scatter(
                x=daily["날짜"], y=ma, mode="lines", name="7일 이동평균",
                line=dict(color="#FFD93D", width=2.5, dash="dot"),
            ))
        st.plotly_chart(apply_dark(fig_area, "일별 총 매출 + 7일 이동평균"), use_container_width=True)

        st.markdown("")
        section_header("카테고리별 매출 추이")
        daily_cat = filtered.groupby(["날짜", "카테고리"]).agg(매출액=("매출액", "sum")).reset_index()
        fig_cat = px.area(daily_cat, x="날짜", y="매출액", color="카테고리", color_discrete_sequence=COLORS)
        fig_cat.update_traces(line=dict(width=1.5), opacity=0.7)
        st.plotly_chart(apply_dark(fig_cat, "카테고리별 일별 매출"), use_container_width=True)

    with stab2:
        section_header("지역 × 카테고리 히트맵")
        pivot_heat = filtered.pivot_table(values="매출액", index="지역", columns="카테고리", aggfunc="sum")
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot_heat.values, x=pivot_heat.columns.tolist(), y=pivot_heat.index.tolist(),
            colorscale=[[0, "#1A1F2E"], [0.5, "#6C63FF"], [1, "#00D2FF"]],
            hoverongaps=False,
        ))
        st.plotly_chart(apply_dark(fig_heat, "지역 × 카테고리 매출 분포"), use_container_width=True)

        st.markdown("")
        section_header("매출 구성 트리맵")
        tree_data = filtered.groupby(["카테고리", "지역"]).agg(매출액=("매출액", "sum")).reset_index()
        fig_tree = px.treemap(tree_data, path=["카테고리", "지역"], values="매출액",
                              color="매출액", color_continuous_scale=["#1A1F2E", "#6C63FF", "#00D2FF"])
        fig_tree.update_traces(marker=dict(line=dict(width=1, color="#0E1117")), textfont=dict(size=13))
        fig_tree.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E0E0E0"),
                               margin=dict(l=10, r=10, t=40, b=10), coloraxis_colorbar=dict(title=""))
        if True:
            fig_tree.update_layout(title=dict(text="카테고리 > 지역 매출 구성", font=dict(size=16, color="#C8C8FF")))
        st.plotly_chart(fig_tree, use_container_width=True)

    with stab3:
        section_header("요일별 매출 분포 (Box Plot)")
        box_df = filtered.copy()
        day_map = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
        box_df["요일"] = box_df["날짜"].dt.dayofweek.map(day_map)
        box_df["요일"] = pd.Categorical(box_df["요일"], categories=["월", "화", "수", "목", "금", "토", "일"], ordered=True)
        box_df = box_df.sort_values("요일")
        fig_box = px.box(box_df, x="요일", y="매출액", color="카테고리", color_discrete_sequence=COLORS)
        fig_box.update_traces(marker=dict(opacity=0.6))
        st.plotly_chart(apply_dark(fig_box, "요일별 카테고리 매출 분포"), use_container_width=True)

        st.markdown("")
        section_header("월별 카테고리 매출 막대 차트")
        m_df = filtered.copy()
        m_df["월"] = m_df["날짜"].dt.month.astype(str) + "월"
        m_agg = m_df.groupby(["월", "카테고리"]).agg(매출액=("매출액", "sum")).reset_index()
        fig_mbar = px.bar(m_agg, x="월", y="매출액", color="카테고리", barmode="group",
                          color_discrete_sequence=COLORS)
        fig_mbar.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(apply_dark(fig_mbar, "월별 카테고리 매출"), use_container_width=True)

# ──────────────────────────────────────────────
# 탭 3: 고객 분석
# ──────────────────────────────────────────────
with tab_customer:
    ctab1, ctab2, ctab3 = st.tabs(["🔍 유입 분석", "👤 세그먼트", "⭐ 만족도 · 재구매"])

    with ctab1:
        section_header("고객 전환 펀넬")
        fig_fun = go.Figure(go.Funnel(
            y=funnel_df["단계"], x=funnel_df["사용자수"],
            textinfo="value+percent initial",
            marker=dict(color=COLORS[:5], line=dict(width=1, color="#0E1117")),
            connector=dict(line=dict(color="rgba(108,99,255,0.3)", width=1)),
        ))
        fig_fun.update_layout(height=400)
        st.plotly_chart(apply_dark(fig_fun, "전환 펀넬 분석"), use_container_width=True)

        st.markdown("")
        fc1, fc2 = st.columns(2)
        with fc1:
            section_header("유입 채널별 고객 분포")
            ch_data = cust_df_all.groupby("유입채널").size().reset_index(name="고객수")
            fig_ch = px.pie(ch_data, names="유입채널", values="고객수", hole=0.55,
                            color_discrete_sequence=COLORS)
            fig_ch.update_traces(textposition="inside", textinfo="percent+label",
                                 marker=dict(line=dict(color="#0E1117", width=2)))
            st.plotly_chart(apply_dark(fig_ch, "채널별 고객 비율"), use_container_width=True)

        with fc2:
            section_header("채널별 평균 구매금액")
            ch_pur = cust_df_all.groupby("유입채널").agg(평균구매금액=("구매금액", "mean")).reset_index()
            ch_pur = ch_pur.sort_values("평균구매금액", ascending=True)
            fig_chb = px.bar(ch_pur, x="평균구매금액", y="유입채널", orientation="h",
                             color_discrete_sequence=COLORS)
            fig_chb.update_traces(marker_line_width=0, opacity=0.9)
            st.plotly_chart(apply_dark(fig_chb, "채널별 평균 구매금액"), use_container_width=True)

    with ctab2:
        sg1, sg2 = st.columns(2)
        with sg1:
            section_header("연령대별 고객 분포")
            age_d = cust_df_all.groupby("연령대").size().reset_index(name="고객수")
            age_order = ["10대", "20대", "30대", "40대", "50대", "60대+"]
            age_d["연령대"] = pd.Categorical(age_d["연령대"], categories=age_order, ordered=True)
            age_d = age_d.sort_values("연령대")
            fig_age = px.bar(age_d, x="연령대", y="고객수", color_discrete_sequence=COLORS)
            fig_age.update_traces(marker_line_width=0, opacity=0.9)
            st.plotly_chart(apply_dark(fig_age, "연령대별 고객 수"), use_container_width=True)

        with sg2:
            section_header("성별 매출 기여도")
            gen_d = cust_df_all.groupby("성별").agg(총구매금액=("구매금액", "sum")).reset_index()
            fig_gen = px.pie(gen_d, names="성별", values="총구매금액", hole=0.55,
                             color_discrete_sequence=COLORS)
            fig_gen.update_traces(textposition="inside", textinfo="percent+label",
                                  marker=dict(line=dict(color="#0E1117", width=2)))
            st.plotly_chart(apply_dark(fig_gen, "성별 구매금액 비율"), use_container_width=True)

        st.markdown("")
        section_header("연령대별 월간 구매 추이")
        mag = cust_df_all.groupby(["구매월", "연령대"]).agg(구매금액=("구매금액", "sum")).reset_index()
        mag["구매월"] = mag["구매월"].astype(str) + "월"
        fig_mag = px.area(mag, x="구매월", y="구매금액", color="연령대", color_discrete_sequence=COLORS)
        fig_mag.update_traces(line=dict(width=1.5), opacity=0.7)
        st.plotly_chart(apply_dark(fig_mag, "연령대별 월간 구매금액"), use_container_width=True)

    with ctab3:
        repeat_rate = cust_df_all["재구매여부"].mean() * 100
        avg_pur = cust_df_all["구매금액"].mean()

        g1, g2 = st.columns(2)
        with g1:
            section_header("재구매율 게이지")
            fig_g1 = go.Figure(go.Indicator(
                mode="gauge+number", value=repeat_rate,
                number=dict(suffix="%", font=dict(size=36, color="#FFFFFF")),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor="#8B8FA3"),
                    bar=dict(color="#6C63FF"), bgcolor="rgba(26,31,46,0.8)", borderwidth=0,
                    steps=[dict(range=[0, 40], color="rgba(255,82,82,0.2)"),
                           dict(range=[40, 70], color="rgba(255,217,61,0.2)"),
                           dict(range=[70, 100], color="rgba(0,230,118,0.15)")],
                    threshold=dict(line=dict(color="#00E676", width=3), thickness=0.8, value=repeat_rate),
                ),
            ))
            fig_g1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E0E0E0"),
                                 height=280, margin=dict(l=30, r=30, t=50, b=20),
                                 title=dict(text="전체 재구매율", font=dict(size=14, color="#C8C8FF")))
            st.plotly_chart(fig_g1, use_container_width=True)

        with g2:
            section_header("평균 구매금액 게이지")
            fig_g2 = go.Figure(go.Indicator(
                mode="gauge+number", value=avg_pur / 1000,
                number=dict(suffix="K", font=dict(size=36, color="#FFFFFF")),
                gauge=dict(
                    axis=dict(range=[0, 200], tickcolor="#8B8FA3"),
                    bar=dict(color="#00D2FF"), bgcolor="rgba(26,31,46,0.8)", borderwidth=0,
                    steps=[dict(range=[0, 80], color="rgba(255,82,82,0.2)"),
                           dict(range=[80, 140], color="rgba(255,217,61,0.2)"),
                           dict(range=[140, 200], color="rgba(0,230,118,0.15)")],
                    threshold=dict(line=dict(color="#00E676", width=3), thickness=0.8, value=avg_pur / 1000),
                ),
            ))
            fig_g2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E0E0E0"),
                                 height=280, margin=dict(l=30, r=30, t=50, b=20),
                                 title=dict(text="평균 구매금액 (천원)", font=dict(size=14, color="#C8C8FF")))
            st.plotly_chart(fig_g2, use_container_width=True)

        st.markdown("")
        section_header("채널별 재구매율")
        ch_rep = cust_df_all.groupby("유입채널").agg(재구매율=("재구매여부", "mean"), 고객수=("고객ID", "count")).reset_index()
        ch_rep["재구매율"] = (ch_rep["재구매율"] * 100).round(1)
        ch_rep = ch_rep.sort_values("재구매율", ascending=True)
        fig_rep = px.bar(ch_rep, x="재구매율", y="유입채널", orientation="h", color_discrete_sequence=COLORS)
        fig_rep.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(apply_dark(fig_rep, "채널별 재구매율 (%)"), use_container_width=True)

        st.markdown("")
        section_header("연령대별 재구매 상세")
        age_rep = cust_df_all.groupby("연령대").agg(
            재구매율=("재구매여부", "mean"), 평균구매금액=("구매금액", "mean"), 고객수=("고객ID", "count")).reset_index()
        age_rep["재구매율"] = (age_rep["재구매율"] * 100).round(1)
        age_rep["평균구매금액"] = age_rep["평균구매금액"].astype(int)
        st.dataframe(
            age_rep.style.background_gradient(subset=["재구매율"], cmap="RdYlGn")
                .background_gradient(subset=["평균구매금액"], cmap="Blues")
                .format({"재구매율": "{:.1f}%", "평균구매금액": "{:,}원"}),
            use_container_width=True, hide_index=True,
        )

# ──────────────────────────────────────────────
# 탭 4: 데이터 관리
# ──────────────────────────────────────────────
with tab_data:
    dtab1, dtab2, dtab3 = st.tabs(["🔍 데이터 탐색", "📐 피벗 분석", "📥 다운로드"])

    with dtab1:
        section_header("인터랙티브 데이터 편집기")
        max_rows = st.slider("표시 행 수", 10, 500, 100)
        explore_df = filtered.head(max_rows)
        st.caption(f"📌 총 {len(filtered):,}건 중 상위 {max_rows}건 표시")

        st.data_editor(
            explore_df, use_container_width=True, hide_index=True,
            num_rows="dynamic", height=450,
            column_config={
                "날짜": st.column_config.DateColumn("날짜", format="YYYY-MM-DD"),
                "매출액": st.column_config.NumberColumn("매출액", format="%d원"),
                "주문수": st.column_config.NumberColumn("주문수", format="%d건"),
                "방문자수": st.column_config.NumberColumn("방문자수", format="%d명"),
                "고객만족도": st.column_config.NumberColumn("고객만족도", format="%.1f"),
            },
        )

        st.markdown("")
        section_header("요약 통계")
        desc = explore_df.select_dtypes(include="number").describe().T
        desc.columns = ["건수", "평균", "표준편차", "최소", "25%", "50%", "75%", "최대"]
        st.dataframe(desc.style.format("{:,.1f}").background_gradient(cmap="Blues", subset=["평균"]),
                     use_container_width=True)

    with dtab2:
        section_header("동적 피벗 테이블")
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            pv_row = st.selectbox("행 (Index)", ["카테고리", "지역", "요일"])
        with pc2:
            pv_col = st.selectbox("열 (Columns)", ["지역", "카테고리"])
        with pc3:
            pv_val = st.selectbox("값 (Values)", ["매출액", "주문수", "방문자수", "고객만족도"])
        pv_agg = st.radio("집계 함수", ["합계", "평균", "최대", "최소"], horizontal=True)
        agg_map = {"합계": "sum", "평균": "mean", "최대": "max", "최소": "min"}

        pv_df = filtered.copy()
        pv_df["요일"] = pv_df["날짜"].dt.dayofweek.map({0:"월",1:"화",2:"수",3:"목",4:"금",5:"토",6:"일"})

        if pv_row != pv_col:
            pv_result = pd.pivot_table(pv_df, values=pv_val, index=pv_row, columns=pv_col,
                                       aggfunc=agg_map[pv_agg], fill_value=0)
            st.dataframe(pv_result.style.format("{:,.0f}").background_gradient(cmap="YlOrRd"),
                         use_container_width=True)

            st.markdown("")
            section_header("피벗 결과 시각화")
            pv_m = pv_result.reset_index().melt(id_vars=pv_row, var_name=pv_col, value_name=pv_val)
            fig_pv = px.bar(pv_m, x=pv_row, y=pv_val, color=pv_col, barmode="group",
                            color_discrete_sequence=COLORS)
            fig_pv.update_traces(marker_line_width=0, opacity=0.9)
            st.plotly_chart(apply_dark(fig_pv, f"{pv_row}별 {pv_val} ({pv_agg})"), use_container_width=True)
        else:
            st.warning("행과 열에 서로 다른 필드를 선택해주세요.")

    with dtab3:
        section_header("데이터 다운로드 센터")
        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown("""<div class="kpi-card">
                <div class="kpi-icon">📄</div>
                <div class="kpi-value" style="font-size:1.1rem;">CSV 다운로드</div>
                <div class="kpi-label" style="margin-top:8px;">필터 적용된 매출 데이터</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("")
            csv = filtered.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 CSV 다운로드", csv, "biz_analytics_data.csv", "text/csv",
                               use_container_width=True)
        with dl2:
            st.markdown("""<div class="kpi-card">
                <div class="kpi-icon">📊</div>
                <div class="kpi-value" style="font-size:1.1rem;">Excel 다운로드</div>
                <div class="kpi-label" style="margin-top:8px;">필터 적용된 매출 데이터</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("")
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                filtered.to_excel(writer, index=False, sheet_name="매출데이터")
            buf.seek(0)
            st.download_button("📥 Excel 다운로드", buf, "biz_analytics_data.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)

        st.markdown("")
        st.caption(f"📌 현재 필터 적용 데이터: {len(filtered):,}건")
