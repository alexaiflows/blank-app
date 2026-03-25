import streamlit as st
import datetime
import hashlib
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─── 페이지 기본 설정 ───
st.set_page_config(
    page_title="🔮 우주 대운세",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS 스타일 ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Gowun+Dodum&display=swap');

/* 전체 앱 테마 - 우주 애니메이션 배경 */
.stApp {
    background: radial-gradient(circle at center, #2b1055 0%, #170d36 60%, #0d061e 100%);
    color: #e2d9f3;
    font-family: 'Gowun Dodum', 'Noto Sans KR', sans-serif;
    animation: stars 120s linear infinite;
}

@keyframes stars {
    0% { background-position: 0 0; }
    100% { background-position: 1000px 1000px; }
}

/* 글래스모피즘 카드 */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeIn 0.8s ease-out forwards;
}
.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 타이틀 텍스트 그라데이션 */
.gradient-text {
    background: linear-gradient(135deg, #ffd194 0%, #70e1f5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}

.main-title {
    text-align: center;
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    font-family: 'Noto Sans KR', sans-serif;
    letter-spacing: -1px;
}
.sub-title {
    text-align: center;
    color: #bfa1df;
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
}

/* 점수별 컬러 매핑 */
.score-high { color: #ffd194; text-shadow: 0 0 15px rgba(255,209,148,0.6); }
.score-mid { color: #a1c4fd; text-shadow: 0 0 15px rgba(161,196,253,0.6); }
.score-low { color: #ff9a9e; text-shadow: 0 0 15px rgba(255,154,158,0.6); }

/* 별점 표시 */
.stars {
    letter-spacing: 3px;
    font-size: 1.3rem;
}
.star-filled { color: #ffd194; text-shadow: 0 0 8px rgba(255,209,148,0.5); }
.star-empty { color: rgba(255,255,255,0.15); }

/* 카테고리 기호 뱃지 */
.cat-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 55px;
    height: 55px;
    border-radius: 20px;
    font-size: 1.8rem;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.badge-love { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }
.badge-money { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
.badge-health { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); }
.badge-work { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); }
.badge-luck { background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); }

/* 럭키 아이템 태그 */
.lucky-tag {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    border-radius: 50px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    margin: 6px;
    font-size: 0.95rem;
    color: #e2d9f3;
    transition: all 0.2s;
}
.lucky-tag:hover {
    background: rgba(255,209,148,0.15);
    border-color: #ffd194;
    color: #ffd194;
}

/* 진행바 (게이지) */
.gauge-bg {
    height: 10px;
    background: rgba(0,0,0,0.3);
    border-radius: 5px;
    overflow: hidden;
    margin-top: 12px;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);
}
.gauge-fill {
    height: 100%;
    border-radius: 5px;
    transition: width 1.5s ease-out;
}

/* 차트 배경 투명화 */
.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* 탭 스타일링 커스텀 */
div[data-testid="stTabs"] button {
    font-size: 1.1rem;
    padding-bottom: 1rem;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 1.1rem;
    font-weight: 500;
}

/* 사이드바 스타일링 */
[data-testid="stSidebar"] {
    background: rgba(13, 6, 30, 0.8) !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* 메인 분석 버튼 */
.stButton>button {
    background: linear-gradient(135deg, #8a2be2 0%, #4a00e0 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.6rem 2rem;
    font-weight: 700;
    box-shadow: 0 4px 20px rgba(138,43,226,0.3);
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03) translateY(-2px);
    box-shadow: 0 8px 25px rgba(138,43,226,0.5);
}

/* Expander 타겟 스타일 */
.streamlit-expanderHeader {
    font-size: 1.1rem !important;
    color: #ffd194 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── 데이터 딕셔너리 ───

ZODIAC_DATA = [
    {"name": "물병자리", "start": (1, 20), "end": (2, 18), "symbol": "♒", "element": "공기", "trait": "독창성, 진보적"},
    {"name": "물고기자리", "start": (2, 19), "end": (3, 20), "symbol": "♓", "element": "물", "trait": "상상력, 공감능력"},
    {"name": "양자리", "start": (3, 21), "end": (4, 19), "symbol": "♈", "element": "불", "trait": "열정, 리더십"},
    {"name": "황소자리", "start": (4, 20), "end": (5, 20), "symbol": "♉", "element": "흙", "trait": "인내심, 안정성"},
    {"name": "쌍둥이자리", "start": (5, 21), "end": (6, 21), "symbol": "♊", "element": "공기", "trait": "호기심, 소통능력"},
    {"name": "게자리", "start": (6, 22), "end": (7, 22), "symbol": "♋", "element": "물", "trait": "감수성, 보호본능"},
    {"name": "사자자리", "start": (7, 23), "end": (8, 22), "symbol": "♌", "element": "불", "trait": "자신감, 위풍당당"},
    {"name": "처녀자리", "start": (8, 23), "end": (9, 22), "symbol": "♍", "element": "흙", "trait": "분석력, 완벽주의"},
    {"name": "천칭자리", "start": (9, 23), "end": (10, 22), "symbol": "♎", "element": "공기", "trait": "조화, 외교력"},
    {"name": "전갈자리", "start": (10, 23), "end": (11, 21), "symbol": "♏", "element": "물", "trait": "통찰력, 결단력"},
    {"name": "사수자리", "start": (11, 22), "end": (12, 21), "symbol": "♐", "element": "불", "trait": "낙천성, 자유로움"},
    {"name": "염소자리", "start": (12, 22), "end": (1, 19), "symbol": "♑", "element": "흙", "trait": "책임감, 야망"},
]

BLOOD_TYPE_TRAITS = {
    "A형": "세심하고 신중하며 책임감이 강한 완벽주의자 🌿",
    "B형": "창의적이고 자유분방하며 호기심이 많은 모험가 🔥",
    "O형": "적극적이고 사교적이며 리더십이 뛰어난 평화주의자 ☀️",
    "AB형": "합리적이고 분석적이며 독창적인 매력의 소유자 ✨"
}

# 5단계 세분화 메시지 (0~20, 21~40, 41~60, 61~80, 81~100)
# 각 구간마다 2~3개의 풀에서 랜덤하게 선택되도록 2D 리스트 구조 사용 (가상의 랜덤 인덱스는 해시로 결정)
FORTUNE_MESSAGES = {
    "love": [
        ["관계 향방을 알 수 없는 짙은 안개 속입니다.", "오해가 생기기 쉬우니 언행에 주의하세요."],
        ["당신의 감정을 솔직하게 표현하기 어려운 날입니다.", "사소한 갈등이 있을 수 있으니 한발 양보하세요."],
        ["평이한 하루입니다. 잔잔한 마음을 유지하는 것이 좋습니다.", "특별한 이슈 없이 평화로운 애정운입니다."],
        ["호감을 얻기 좋은 날입니다. 미소가 큰 무기가 됩니다.", "기다리던 연락이 오거나 관계가 한층 발전합니다."],
        ["모든 이목이 집중되는 날입니다! 매력이 100% 발산됩니다.", "영화 같은 운명적 만남이나 로맨틱한 순간이 옵니다."]
    ],
    "money": [
        ["지출 계획을 전면 수정해야 합니다. 지갑을 꼭 닫아두세요.", "금전적 손실이 우려됩니다. 보수적으로 행동하세요."],
        ["예상치 못한 가벼운 지출이 발생할 수 있습니다.", "무리한 투자는 삼가고 가진 것을 지키세요."],
        ["수입과 지출의 균형이 잘 맞는 무난한 하루입니다.", "작은 절약이 모여 큰 기쁨이 되는 평범한 날입니다."],
        ["막혔던 돈줄이 서서히 풀리는 기분 좋은 날입니다.", "소소한 이익을 기대해볼 만한 상승장입니다."],
        ["재복이 깃드는 날! 기다렸던 반가운 소식이 들려옵니다.", "투자의 결실을 보거나 예상 밖의 큰 수입이 생깁니다."]
    ],
    "health": [
        ["컨디션이 바닥입니다. 무조건 휴식을 최우선으로 하세요.", "몸이 보내는 작은 신호도 무시하지 말고 건강을 챙기세요."],
        ["스트레스 지수가 높습니다. 심호흡과 명상이 필요합니다.", "체력이 금방 고갈되니 무리한 활동은 피하세요."],
        ["어제와 비슷한 무난한 컨디션입니다. 가벼운 운동을 곁들이세요.", "평소 하던 대로 규칙적인 생활을 유지하면 좋습니다."],
        ["몸이 한결 가볍고 머리도 맑아지는 하루입니다.", "새로운 운동이나 식단 관리를 시작하기 딱 좋은 타이밍입니다."],
        ["에너지 200% 충전 완료! 뭐든 거뜬히 해낼 수 있는 최상의 컨디션입니다.", "신체 활력이 극에 달해 피로를 전혀 느끼지 못할 것입니다."]
    ],
    "work": [
        ["업무 집중도가 크게 떨어집니다. 중요도 순으로 차분히 처리하세요.", "주변 사람과 마찰이 생길 수 있으니 감정 조절이 필수입니다."],
        ["평소보다 처리해야 할 일이 많아 벅차게 느껴집니다.", "생각대로 일이 풀리지 않으니 플랜B를 준비하세요."],
        ["원만하게 흘러가는 하루입니다. 협업의 효과가 좋습니다.", "루틴한 업무를 조용히 마무리하기에 좋은 날입니다."],
        ["직관력과 집중력이 높아집니다. 어려운 문제도 척척 해결합니다.", "당신의 아이디어가 주목받고 긍정적인 평가를 받습니다."],
        ["거침없이 질주하는 날! 기획, 발표, 승진 등 모든 면에서 완벽합니다.", "오랜 노력의 결실을 맺으며 조직 내 에이스로 인정받습니다."]
    ],
    "luck": [
        ["오늘은 철저한 자기방어가 필요한 날입니다. 돌다리도 두드려보세요.", "매사에 신중을 기하세요. 요행을 바라면 역효과가 납니다."],
        ["결과가 다소 아쉬울 수 있으니 미련을 버리는 것이 현명합니다.", "작은 실수가 겹칠 수 있으니 꼼꼼한 확인이 필요합니다."],
        ["세상의 시계와 내 시계가 딱 맞물려 돌아가는 잔잔한 하루입니다.", "소소한 우연이 미소를 짓게 만드는 평범한 날입니다."],
        ["생각지도 못했던 도움이 찾아오거나 타이밍이 기가 막힌 날입니다.", "당신이 선택하는 것마다 정답이 되는 기분 좋은 흐름입니다."],
        ["기적처럼 우주가 당신을 돕습니다. 로또를 사도 될 만큼 최고의 행운!", "모든 문이 활짝 열려있습니다. 간절히 원하던 것이 이루어집니다."]
    ]
}

ADVICE = {
    "love": ["따뜻한 커피 한 잔과 함께 진심어린 칭찬을 건네보세요 ☕", "의견 차이가 생기면 잠시 심호흡을 하고 '그럴 수 있지'라고 생각하세요 🌿", "화사한 색상의 옷을 입어 매력을 더 높여보세요 🌸"],
    "money": ["오늘은 온라인 쇼핑몰 장바구니를 비우는 대신 저축 계좌 잔액을 확인하세요 💳", "할인율에 속지 말고 '정말 필요한가?' 세 번 질문하세요 🛑", "동전 하나라도 소중히 다루면 금전운이 살아납니다 🪙"],
    "health": ["물을 하루 2리터 마시는 미션에 도전해 보세요 💧", "점심 식사 후 10분 산책이 오후의 활력을 책임집니다 🚶‍♀️", "잠들기 전 5분 스트레칭으로 긴장을 풀어주세요 🧘‍♂️"],
    "work": ["중요한 문서는 두 번, 세 번 크로스체크 하세요 📝", "동료의 부탁을 들어주면 나중에 큰 보답으로 돌아옵니다 🤝", "어려운 과제일수록 가장 먼저 시작해서 매를 먼저 맞으세요 ⏰"],
    "luck": ["현관 신발을 가지런히 정리하면 집안으로 행운이 들어옵니다 👞", "오랜만에 연락처 목록을 보고 반가운 인사를 건네보세요 📱", "오늘 처음 본 사람에게 가벼운 목례를 건네면 기분 좋은 일이 생깁니다 👋"]
}

COLORS_DATA = {"빨강 🔴": "#ff4d4d", "주황 🟠": "#ffa64d", "노랑 🟡": "#ffdb4d", "초록 🟢": "#4dff4d", "파랑 🔵": "#4d4dff", "보라 🟣": "#cc33ff", "핑크 🌸": "#ff66b3", "흰색 ⚪": "#ffffff", "검정 ⚫": "#262626"}
DIRECTIONS = ["동쪽 (새로운 시작)", "서쪽 (재물운)", "남쪽 (명예운)", "북쪽 (안정감)"]
FOODS = ["따뜻한 국물 요리 🍲", "신선한 샐러드 🥗", "달콤한 케이크 🍰", "매콤한 면 요리 🍜", "담백한 초밥 🍣", "에너지 뿜뿜 고기 🥩", "향긋한 아메리카노 ☕"]
GENRES = ["재즈 🎷", "클래식 🎻", "신나는 팝 🎧", "어쿠스틱 🎸", "뉴에이지 🎹", "힙합 🎤", "시티팝 🌃"]

# ─── 유틸리티 함수 ───

def get_zodiac(month, day):
    for z in ZODIAC_DATA:
        if (month == z["start"][0] and day >= z["start"][1]) or \
           (month == z["end"][0] and day <= z["end"][1]):
            return z
    return ZODIAC_DATA[11]

def get_birth_number(bdate_str):
    num_str = bdate_str.replace("-", "")
    while len(num_str) > 1:
        num_str = str(sum(int(d) for d in num_str))
    return int(num_str)

def generate_fortune_seed(bdate_str, blood_type, target_date_str):
    raw = f"{bdate_str}_{blood_type}_{target_date_str}"
    return int(hashlib.sha256(raw.encode()).hexdigest(), 16)

def get_score(seed, offset):
    random_val1 = (seed + offset) % 34 + 1
    random_val2 = (seed + offset * 2) % 34 + 1
    random_val3 = (seed + offset * 3) % 34
    score = random_val1 + random_val2 + random_val3
    if score > 100: score = 100
    if score < 10: score = 10 + (score % 10)
    return score

def get_stars_and_idx(score):
    if score >= 81: return 5, 4
    elif score >= 61: return 4, 3
    elif score >= 41: return 3, 2
    elif score >= 21: return 2, 1
    else: return 1, 0

def get_msg_and_advice(category, score, seed):
    _, idx = get_stars_and_idx(score)
    msg_list = FORTUNE_MESSAGES[category][idx]
    msg = msg_list[(seed + len(msg_list)) % len(msg_list)]
    
    advice_list = ADVICE[category]
    adv = advice_list[seed % len(advice_list)]
    return msg, adv

def render_gauge(score, gradient_type):
    gradients = {
        "love": ("#ff9a9e", "#fecfef"),
        "money": ("#f6d365", "#fda085"),
        "health": ("#84fab0", "#8fd3f4"),
        "work": ("#a1c4fd", "#c2e9fb"),
        "luck": ("#d4fc79", "#96e6a1"),
    }
    g_start, g_end = gradients[gradient_type]
    return f"""
    <div class="gauge-bg">
        <div class="gauge-fill" style="width: {score}%; background: linear-gradient(90deg, {g_start}, {g_end}); box-shadow: 0 0 10px {g_start};"></div>
    </div>
    """

def calc_zodiac_ranking(target_date_str, bdate_str, blood_type):
    ranking = []
    # 내 점수 시드 기준점 역할을 하기 위해 내 속성도 섞어서 각 별자리의 오늘 운세를 뽑습니다 (재미 요소)
    base_seed_str = f"{target_date_str}_{bdate_str}_{blood_type}"
    for z in ZODIAC_DATA:
        z_seed = int(hashlib.sha256(f"{z['name']}_{base_seed_str}".encode()).hexdigest(), 16)
        z_score = int(sum(get_score(z_seed, i) for i in range(1, 6)) / 5)
        ranking.append({"별자리": f"{z['symbol']} {z['name']}", "점수": z_score, "raw_name": z['name']})
    
    df = pd.DataFrame(ranking).sort_values(by="점수", ascending=True) # Plotly bar chart y-axis 역순을 위해
    return df

def get_weekly_trend(bdate_str, blood_type, center_date):
    days = []
    for delta in range(-3, 4):
        d = center_date + datetime.timedelta(days=delta)
        seed = generate_fortune_seed(bdate_str, blood_type, str(d))
        avg = int(sum(get_score(seed, i+1) for i in range(5)) / 5)
        days.append({"날짜": d.strftime("%m/%d"), "총점": avg, "상태": "오늘" if delta == 0 else ""})
    return pd.DataFrame(days)

def calc_compatibility(seed1, seed2):
    # 두 시드를 활용한 간단한 궁합 로직
    comp_score = (seed1 ^ seed2) % 61 + 40 # 40~100점 사이
    if comp_score >= 90: return comp_score, "천생연분! 영혼의 단짝입니다. 💏", "#ff9a9e"
    elif comp_score >= 75: return comp_score, "호흡이 척척 맞는 아주 좋은 인연입니다. 🥰", "#fecfef"
    elif comp_score >= 60: return comp_score, "서로를 위해 조금씩 맞춰가면 좋은 관계입니다. 🤝", "#a1c4fd"
    else: return comp_score, "성향 차이가 큽니다. 서로의 다름을 존중하는 노력이 필요해요. ⚖️", "#bfa1df"


# ─── 사이드바: 입력 ───

with st.sidebar:
    st.markdown('<div class="main-title gradient-text" style="font-size: 2.2rem; margin-top:20px;">우주 대운세</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#bfa1df;'>마스터 데이터 입력</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    name = st.text_input("당신의 이름 (선택사항)", placeholder="우주여행자")
    bdate = st.date_input("생년월일", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), value=datetime.date(1995, 1, 1))
    blood = st.selectbox("혈액형", ["A형", "B형", "O형", "AB형"])
    
    target_date = datetime.date.today()
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("운세 동기화 🔮", use_container_width=True)
    
    st.markdown("---")
    with st.expander("💘 소셜 듀오 궁합 체커"):
        st.markdown("<p style='font-size:0.9rem; color:#bfa1df;'>상대방의 정보를 입력하세요.</p>", unsafe_allow_html=True)
        p2_name = st.text_input("상대방 이름", placeholder="파트너")
        p2_bdate = st.date_input("상대방 생년월일", value=datetime.date(1996, 5, 5), key="p2_bdate")
        p2_blood = st.selectbox("상대방 혈액형", ["A형", "B형", "O형", "AB형"], key="p2_blood")
        check_comp = st.button("궁합 확인하기 💞", use_container_width=True)


# ─── 메인 대시보드 ───
if name == "": name = "별빛 탐험가"

if check_comp:
    st.session_state['mode'] = 'compatibility'
elif analyze_btn or 'mode' not in st.session_state:
    st.session_state['mode'] = 'daily'

if st.session_state['mode'] == 'compatibility':
    # ─── 궁합 모드 ───
    st.markdown(f'<div class="main-title gradient-text">우주 듀오 궁합 리포트</div>', unsafe_allow_html=True)
    if p2_name == "": p2_name = "파트너"
    
    z1 = get_zodiac(bdate.month, bdate.day)
    z2 = get_zodiac(p2_bdate.month, p2_bdate.day)
    
    s1 = generate_fortune_seed(str(bdate), blood, "COMPAT")
    s2 = generate_fortune_seed(str(p2_bdate), p2_blood, "COMPAT")
    c_score, c_msg, c_color = calc_compatibility(s1, s2)
    
    st.markdown('<div class="glass-card" style="text-align:center; padding: 3rem;">', unsafe_allow_html=True)
    colA, colB, colC = st.columns([2, 1, 2])
    with colA:
        st.markdown(f"<h2>🧑 {name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<span class='lucky-tag'>{z1['symbol']} {z1['name']} ({z1['element']})</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='lucky-tag'>🩸 {blood}</span>", unsafe_allow_html=True)
    with colB:
        st.markdown("<h1 style='font-size:4rem; color:#ff9a9e; animation: pulse 2s infinite;'>❤</h1>", unsafe_allow_html=True)
    with colC:
        st.markdown(f"<h2>👱 {p2_name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<span class='lucky-tag'>{z2['symbol']} {z2['name']} ({z2['element']})</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='lucky-tag'>🩸 {p2_blood}</span>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1); margin: 3rem 0;'>", unsafe_allow_html=True)
    
    # 도넛 게이지 - 궁합 점수
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = c_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'font': {'size': 60, 'color': c_color}, 'suffix': "점"},
        gauge = {
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': c_color},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 0,
        }
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"<h3 style='text-align:center; color:{c_color};'>{c_msg}</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("⬅ 오늘의 개인 운세로 돌아가기", use_container_width=True):
        st.session_state['mode'] = 'daily'
        st.rerun()

elif st.session_state['mode'] == 'daily' and 'analyzed' in st.session_state or analyze_btn:
    st.session_state['analyzed'] = True
    
    seed = generate_fortune_seed(str(bdate), blood, str(target_date))
    
    scores = {
        "love": get_score(seed, 1),
        "money": get_score(seed, 2),
        "health": get_score(seed, 3),
        "work": get_score(seed, 4),
        "luck": get_score(seed, 5)
    }
    avg_score = int(sum(scores.values()) / 5)
    stars_total, _ = get_stars_and_idx(avg_score)
    zodiac = get_zodiac(bdate.month, bdate.day)
    birth_num = get_birth_number(str(bdate))
    
    # ─── 상단 종합 운세 카드 (도넛 게이지 추가) ───
    st.markdown(f'<div class="main-title gradient-text">{target_date.strftime("%Y년 %m월 %d일")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">우주가 <b>{name}</b>님에게 보내는 오늘의 메시지</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    
    if avg_score >= 81: 
        status = "대길 (大吉) 🌟"
        main_msg = "우주의 긍정적 에너지가 당신을 완벽히 감싸는 하루입니다!"
        d_color = "#ffd194"
    elif avg_score >= 61: 
        status = "길 (吉) ✨"
        main_msg = "진행하는 일들이 순조롭게 풀리는 기분 좋은 흐름입니다."
        d_color = "#96e6a1"
    elif avg_score >= 41: 
        status = "보통 (平) 🍃"
        main_msg = "큰 흔들림 없이 잔잔한 바다와 같은 무난한 하루입니다."
        d_color = "#a1c4fd"
    elif avg_score >= 21: 
        status = "소흉 (小凶) 🌧️"
        main_msg = "변수가 생길 수 있으니 한 템포 쉬어가는 지혜가 필요합니다."
        d_color = "#ff9a9e"
    else: 
        status = "흉 (凶) ☔"
        main_msg = "매사에 신중함을 유지하고 긍정적인 방어 태세를 갖추세요."
        d_color = "#ff66b3"

    with c1:
        # 도넛 게이지
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_score,
            title = {'text': "종합 운세 지수", 'font': {'color': '#bfa1df', 'size': 18}},
            number = {'font': {'size': 50, 'color': d_color}},
            gauge = {
                'axis': {'range': [None, 100], 'visible': False},
                'bar': {'color': d_color},
                'bgcolor': "rgba(255,255,255,0.05)",
                'borderwidth': 0,
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with c2:
        st.markdown(f"""
        <div style="padding-top: 1.5rem;">
            <div style="font-size:2rem; font-weight:800; color:{d_color}; margin-bottom:10px;">{status}</div>
            <div class='stars' style="margin-bottom:15px;">
                <span class='star-filled'>{'★'*stars_total}</span><span class='star-empty'>{'★'*(5-stars_total)}</span>
            </div>
            <div style="font-size:1.2rem; line-height:1.6;">{main_msg}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ─── 탭 기반 상세 콘텐츠 분리 ───
    tab1, tab2, tab3 = st.tabs(["📑 부문별 상세 운세", "📈 우주 트렌드 & 랭킹", "🎁 럭키 아이템 & 내 정보"])
    
    with tab1:
        colA, colB = st.columns([3, 2])
        with colA:
            cats = [
                ("💕 애정운", "love", scores["love"]),
                ("💰 금전운", "money", scores["money"]),
                ("💪 바이오", "health", scores["health"]),
                ("💼 커리어", "work", scores["work"]),
                ("🍀 럭키픽", "luck", scores["luck"])
            ]
            for title, key, act_score in cats:
                msg, adv = get_msg_and_advice(key, act_score, seed)
                s_count, _ = get_stars_and_idx(act_score)
                st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)
                c_icon, c_content = st.columns([1, 4])
                with c_icon:
                    st.markdown(f"<div class='cat-badge badge-{key}'>{title.split()[0]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-weight:900; font-size:1.1rem; text-align:center;'>{act_score}점</div>", unsafe_allow_html=True)
                with c_content:
                    st.markdown(f"<div style='font-weight:700; font-size:1.2rem; color:#e2d9f3;'>{title.split()[1]}</div>", unsafe_allow_html=True)
                    s_str = f"<span class='star-filled'>{'★'*s_count}</span><span class='star-empty'>{'★'*(5-s_count)}</span>"
                    st.markdown(f"<div class='stars' style='font-size:0.9rem; margin-top:2px;'>{s_str}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:1rem; margin-top:8px;'>{msg}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:0.9rem; color:#ffd194; margin-top:5px;'><b>💡 Tip:</b> {adv}</div>", unsafe_allow_html=True)
                    st.markdown(render_gauge(act_score, key), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="glass-card" style="position: sticky; top: 2rem;">', unsafe_allow_html=True)
            st.markdown("<h4 style='text-align:center; color:#bfa1df; margin-bottom:1rem;'>🎯 오늘의 5각 밸런스</h4>", unsafe_allow_html=True)
            categories = ['애정', '금전', '바이오', '커리어', '럭키픽']
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[scores["love"], scores["money"], scores["health"], scores["work"], scores["luck"], scores["love"]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(112, 225, 245, 0.25)',
                line=dict(color='#70e1f5', width=3),
                marker=dict(color='#ffd194', size=10, symbol='star')
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.2)'), showline=False),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#e2d9f3', size=14, weight='bold'))
                ),
                showlegend=False,
                margin=dict(l=30, r=30, t=30, b=30),
                height=350,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        colX, colY = st.columns(2)
        with colX:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 이번 주 종합 운세 흐름")
            st.markdown("<p style='font-size:0.85rem; color:#bfa1df;'>오늘을 기준으로 전후 7일간의 운세 변화입니다.</p>", unsafe_allow_html=True)
            trend_df = get_weekly_trend(str(bdate), blood, target_date)
            fig_line = px.line(trend_df, x='날짜', y='총점', markers=True, text='상태')
            fig_line.update_traces(
                line_color='#ffd194', line_width=4, 
                marker=dict(size=12, color='#ff9a9e', line=dict(width=2, color='white')),
                textposition="top center",
                textfont=dict(color='#70e1f5', size=13, weight='bold')
            )
            fig_line.update_layout(
                yaxis=dict(range=[10, 105], gridcolor='rgba(255,255,255,0.1)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=20, b=10),
                height=320
            )
            st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with colY:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"#### 🏆 오늘의 별자리 12궁 랭킹")
            st.markdown("<p style='font-size:0.85rem; color:#bfa1df;'>전체 별자리 중 오늘의 우주 기운 집중도입니다.</p>", unsafe_allow_html=True)
            rank_df = calc_zodiac_ranking(str(target_date), str(bdate), blood)
            colors = ['#70e1f5' if row['raw_name'] == zodiac['name'] else 'rgba(255,255,255,0.15)' for _, row in rank_df.iterrows()]
            
            fig_bar = go.Figure(go.Bar(
                x=rank_df['점수'],
                y=rank_df['별자리'],
                orientation='h',
                marker_color=colors,
                text=rank_df['점수'],
                textposition='outside',
                textfont=dict(color='#e2d9f3')
            ))
            fig_bar.update_layout(
                xaxis=dict(range=[0, 110], visible=False),
                yaxis=dict(tickfont=dict(color='#e2d9f3', size=12, weight='bold')),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        lucky_color_name = list(COLORS_DATA.keys())[seed % len(COLORS_DATA)]
        lucky_color_hex = COLORS_DATA[lucky_color_name]
        lucky_num = (seed % 99) + 1
        lucky_dir = DIRECTIONS[(seed * 2) % len(DIRECTIONS)]
        lucky_food = FOODS[(seed * 3) % len(FOODS)]
        lucky_genre = GENRES[(seed * 4) % len(GENRES)]

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎁 오늘 하루를 채워줄 럭키 아이템")
        
        l_col1, l_col2 = st.columns([1, 4])
        with l_col1:
            st.markdown(f"""
            <div style="text-align:center; padding-top:10px;">
                <div style="width:70px; height:70px; border-radius:50%; background-color:{lucky_color_hex}; box-shadow:0 0 15px {lucky_color_hex}; margin: 0 auto 10px auto; border: 3px solid rgba(255,255,255,0.8);"></div>
                <div style="font-weight:bold;">{lucky_color_name}</div>
                <div style="font-size:0.8rem; color:#bfa1df;">행운의 색상</div>
            </div>
            """, unsafe_allow_html=True)
        with l_col2:
            st.markdown(f"""
            <div style="line-height:2.8; margin-top: 15px;">
                <span class="lucky-tag" style="border-color:#ff9a9e;">🔢 행운의 수: <b>{lucky_num}</b></span>
                <span class="lucky-tag" style="border-color:#a1c4fd;">🧭 향할 곳: <b>{lucky_dir}</b></span>
                <span class="lucky-tag" style="border-color:#f6d365;">🍽️ 추천 메뉴: <b>{lucky_food}</b></span>
                <span class="lucky-tag" style="border-color:#84fab0;">🎵 BGM: <b>{lucky_genre}</b></span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        c_info1, c_info2 = st.columns(2)
        with c_info1:
            st.markdown('<div class="glass-card" style="height:100%;">', unsafe_allow_html=True)
            st.markdown(f"#### 별자리: {zodiac['symbol']} {zodiac['name']}")
            st.markdown(f"<p style='color:#ffd194; font-size:1rem; font-weight:bold;'>우주 원소: {zodiac['element']} &nbsp;|&nbsp; 고유 특성: {zodiac['trait']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.95rem; color:#e2d9f3;'>당신이 태어난 날인 {zodiac['start'][0]}월 {zodiac['start'][1]}일 ~ {zodiac['end'][0]}월 {zodiac['end'][1]}일 사이에는 태양이 이 별자리에 머물렀습니다. 이는 당신의 기본 성향에 지대한 영향을 미칩니다.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c_info2:
            st.markdown('<div class="glass-card" style="height:100%;">', unsafe_allow_html=True)
            st.markdown(f"#### 🧬 {blood} 혈액 & 🔢 탄생수 {birth_num}")
            st.markdown(f"<p style='color:#70e1f5; font-size:1rem; font-weight:bold;'>{BLOOD_TYPE_TRAITS[blood]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.95rem; color:#e2d9f3;'>당신의 생년월일을 모두 더해 나온 탄생수 <b>{birth_num}</b>은 수비학(Numerology)에서 영혼의 목적과 내재된 재능을 암시하는 중요한 숫자입니다.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
