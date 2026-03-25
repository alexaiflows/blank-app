import streamlit as st
import datetime
import hashlib
import random
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="🃏 데스티니 타로카드", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# ─── 세션 상태 초기화 ───
if "history" not in st.session_state: st.session_state["history"] = []

# ─── CSS 스타일 ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Gowun+Dodum&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

.stApp { background: radial-gradient(circle at center, #1a0b2e 0%, #11071f 50%, #05020a 100%); color: #e2d9f3; font-family: 'Gowun Dodum', 'Noto Sans KR', sans-serif; }
.stars-bg { position: fixed; top:0; left:0; right:0; bottom:0; z-index:-1;
    background-image: radial-gradient(1px 1px at 20px 30px, #fff, transparent), radial-gradient(1px 1px at 40px 70px, #fff, transparent), radial-gradient(1.5px 1.5px at 50px 160px, #fff, transparent);
    background-size: 200px 200px; animation: twinkle 5s infinite; opacity: 0.3; }
@keyframes twinkle { 0%, 100% { opacity: 0.2; } 50% { opacity: 0.6; } }

.glass-box { background: rgba(26, 11, 46, 0.45); backdrop-filter: blur(12px); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin: 1rem 0; }
.gold-text { background: linear-gradient(135deg, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-family: 'Cinzel', serif; }
.main-title { text-align: center; font-size: 3.5rem; margin-bottom: 0.5rem; }
.sub-title { text-align: center; color: #bfa1df; font-size: 1.2rem; margin-bottom: 2rem; }

/* CSS 카드 플립 & Glow 효과 */
.card-container { perspective: 1000px; width: 220px; height: 350px; margin: 0 auto 20px auto; }
.tarot-card { width: 100%; height: 100%; position: relative; transition: transform 0.8s, box-shadow 0.3s; transform-style: preserve-3d; cursor: pointer; border-radius: 12px; }
.tarot-card:hover { transform: translateY(-10px) scale(1.05); }

.tarot-card.flipped { transform: rotateY(180deg); box-shadow: 0 0 25px rgba(255, 215, 0, 0.5); }
.tarot-card.flipped.reversed { transform: rotateY(180deg) rotateZ(180deg); box-shadow: 0 0 25px rgba(138, 43, 226, 0.6); }

.card-face { position: absolute; width:100%; height:100%; backface-visibility: hidden; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: center; align-items: center; }
.card-back { background: linear-gradient(135deg, #11071f, #2b1055); border: 3px solid #bf953f; background-image: repeating-linear-gradient(45deg, rgba(212,175,55,0.1) 25%, transparent 25%, transparent 75%, rgba(212,175,55,0.1) 75%, rgba(212,175,55,0.1)); background-size: 20px 20px; }
.card-back::after { content: '✵'; font-size: 4rem; color: rgba(212,175,55,0.5); }
.card-front { background: linear-gradient(135deg, #fcf6ba, #bf953f); border: 2px solid #5a3a1f; transform: rotateY(180deg); padding: 10px; }
.tarot-card.flipped.reversed .card-front::after { content: ''; position: absolute; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.25); border-radius: 10px; pointer-events:none; }
.tarot-card.flipped.reversed .card-front .card-content { transform: rotateZ(180deg); }

.card-content { width: 100%; height: 100%; border: 1px solid rgba(26,11,46,0.2); border-radius: 8px; background: rgba(255,255,255,0.9); display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 10px; box-sizing: border-box; color: #1a0b2e; }
.c-num { font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: bold; }
.c-emoji { font-size: 4rem; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2)); margin: 10px 0; }
.c-name { font-family: 'Cinzel', serif; font-size: 1rem; font-weight: bold; text-align: center; }
.c-kor { font-size: 0.9rem; font-weight: bold; color: #5a3a1f; text-align: center; margin-top: 5px; }
.reversed-label { background: #8a2be2; color: #fff; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px; font-weight: bold; margin-top:5px; box-shadow: 0 0 10px #8a2be2; }

/* 십자가 형태 레이아웃 래퍼 */
.grid-5card { display: grid; grid-template-columns: 1fr 1fr 1fr; grid-gap: 20px; justify-items: center; align-items: center; margin-top: 2rem; }
.pos-1 { grid-column: 2; grid-row: 2; z-index: 2; }
.pos-2 { grid-column: 2; grid-row: 2; transform: rotate(90deg); z-index: 3; opacity: 0.95; }
.pos-3 { grid-column: 2; grid-row: 3; }
.pos-4 { grid-column: 1; grid-row: 2; }
.pos-5 { grid-column: 3; grid-row: 2; }

.stButton>button { background: linear-gradient(135deg, #bf953f, #aa771c); color: #1a0b2e; border: none; border-radius: 8px; font-weight: bold; transition: all 0.3s; }
.stButton>button:hover { box-shadow: 0 0 15px rgba(212,175,55,0.8); }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #ffd700 !important; border-bottom: 2px solid #ffd700 !important; }
</style>
<div class="stars-bg"></div>
""", unsafe_allow_html=True)

# ─── 22장 메이저 아르카나 + 확장 필드 (요소, 3가지 카테고리 해석) ───
TAROT_DECK = [
    {
        "id": 0, "num": "0", "name": "The Fool", "kor": "바보", "emoji": "🎒", "el": "공기",
        "kw": "시작, 모험, 가능성, 순수", "tr": {"행동력": 90, "감성": 80, "지성": 40, "직관": 95, "의지": 60, "소통": 50},
        "m_up": {"종합": "새로운 여정의 시작입니다. 직관을 믿고 도약하세요.", "연애": "설레는 새 인연이나 가벼운 썸이 생깁니다.", "직장": "새로운 직업이나 프로젝트에 도전하기 좋은 시기.", "재물": "투자에 대한 긍정적 신호. 모험이 성과를 냅니다."},
        "m_rev": {"종합": "준비 부족이나 무모함을 경계하세요.", "연애": "무책임하거나 진지하지 못한 관계에 빠질 수 있습니다.", "직장": "계획 없는 행동으로 인한 구설이나 실패 위험.", "재물": "충동적인 과소비나 묻지마 투자를 조심하세요."}
    },
    {
        "id": 1, "num": "I", "name": "The Magician", "kor": "마법사", "emoji": "✨", "el": "공기",
        "kw": "창조력, 잠재력, 능력, 집중", "tr": {"행동력": 85, "감성": 50, "지성": 95, "직관": 70, "의지": 90, "소통": 85},
        "m_up": {"종합": "모든 도구와 능력을 갖추었습니다. 행동으로 옮길 때입니다.", "연애": "매력이 넘치는 시점! 적극적으로 어필하면 사랑을 얻습니다.", "직장": "아이디어가 채택되고 실력을 발휘해 돋보입니다.", "재물": "새로운 수입원을 만들 수 있는 창의적인 시도 성공."},
        "m_rev": {"종합": "능력을 과대평가하거나 속임수 우려.", "연애": "상대방의 진정성을 의심해봐야 합니다. 겉치레 주의.", "직장": "실력 발휘를 못하거나 말뿐인 사람과 얽힐 수 있음.", "재물": "가짜 정보에 속거나 불필요한 곳에 돈을 쓸 위험."}
    },
    {
        "id": 2, "num": "II", "name": "The High Priestess", "kor": "여사제", "emoji": "🌙", "el": "물",
        "kw": "직관, 무의식, 통찰", "tr": {"행동력": 20, "감성": 85, "지성": 90, "직관": 100, "의지": 60, "소통": 30},
        "m_up": {"종합": "상황을 관망하고 직관을 믿으세요. 내면에 답이 있습니다.", "연애": "속마음을 쉽게 드러내지 않는 관계. 정신적인 교감이 중요.", "직장": "표면에 드러나지 않은 문제를 통찰하게 됩니다.", "재물": "현금 흐름을 조용히 지키고 비밀스런 이익을 모으는 시기."},
        "m_rev": {"종합": "내면의 목소리를 외면하여 혼란이 옵니다.", "연애": "오해가 생기거나 숨겨진 비밀이 드러납니다.", "직장": "부정확한 정보에 휘둘려 답답한 상황 발생.", "재물": "판단력이 흐려져 잘못된 금전 계약을 맺을 수 있음."}
    },
    {
        "id": 3, "num": "III", "name": "The Empress", "kor": "여황제", "emoji": "🌾", "el": "흙",
        "kw": "풍요, 아름다움, 창조", "tr": {"행동력": 50, "감성": 100, "지성": 60, "직관": 80, "의지": 70, "소통": 90},
        "m_up": {"종합": "물질적, 감정적 풍요. 보살핌이 결실을 맺습니다.", "연애": "헌신적이고 깊은 사랑. 결혼이나 임신, 안정적 관계.", "직장": "포용력 있는 리더십으로 인정을 받고 편안한 업무 분위기.", "재물": "수입이 늘어나고 여유가 생기며 물질적 만족감이 큼."},
        "m_rev": {"종합": "과도한 의존심, 허영이 우려됩니다.", "연애": "과한 집착과 소유욕 혹은 권태.", "직장": "게을러지거나 감정적 판단으로 업무를 르침.", "재물": "사치와 허영으로 인한 지출 증가."}
    },
    {
        "id": 4, "num": "IV", "name": "The Emperor", "kor": "황제", "emoji": "👑", "el": "불",
        "kw": "권위, 체계, 규칙", "tr": {"행동력": 80, "감성": 30, "지성": 85, "직관": 40, "의지": 100, "소통": 60},
        "m_up": {"종합": "확고한 계획과 규율로 안정과 주도권을 쥡니다.", "연애": "책임감 있는 만남. 주도권을 쥔 든든한 연애.", "직장": "체계 구축. 승진이나 권위를 가지고 프로젝트 리드.", "재물": "보수적인 자산 관리로 탄탄하게 재산을 불림."},
        "m_rev": {"종합": "권력 남용이나 억압적인 태도.", "연애": "통제하려는 태도로 인해 상대방이 숨막혀 합니다.", "직장": "고집불통 리더와의 마찰, 권위주의로 무너짐.", "재물": "유연성 부족으로 재테크 기회를 상실함."}
    },
    {
        "id": 5, "num": "V", "name": "The Hierophant", "kor": "교황", "emoji": "📜", "el": "흙",
        "kw": "전통, 교육, 신념, 멘토", "tr": {"행동력": 40, "감성": 60, "지성": 80, "직관": 70, "의지": 80, "소통": 95},
        "m_up": {"종합": "기존 규칙을 수용하고 훌륭한 멘토를 만나세요.", "연애": "소개팅, 선 등 정통적인 만남. 보수적이나 안정적.", "직장": "협회/조직의 도움이나 멘토링이 효과적.", "재물": "전통적인 재테크(예적금, 부동산)가 길함."},
        "m_rev": {"종합": "구속하는 틀에서 벗어나고 싶어합니다.", "연애": "주변 시선이나 조건에서 자유로워지는 만남 추구.", "직장": "조직의 낡은 관행과 마찰, 잘못된 조언자.", "재물": "권유받은 투자에 속거나 비공식적 지출 발생."}
    },
    {
        "id": 6, "num": "VI", "name": "The Lovers", "kor": "연인", "emoji": "💞", "el": "공기",
        "kw": "조화, 사랑, 올바른 선택", "tr": {"행동력": 60, "감성": 100, "지성": 40, "직관": 80, "의지": 50, "소통": 90},
        "m_up": {"종합": "가슴이 이끄는 올바른 선택. 운명적 만남.", "연애": "최고의 궁합. 강한 끌림과 조화로운 관계 발전.", "직장": "시너지가 좋은 파트너십 구축, 즐거운 협업.", "재물": "동업 제안, 서로 윈윈하는 투자 기회 발생."},
        "m_rev": {"종합": "관계 불균형, 무책임한 선택.", "연애": "삼각관계, 갈등, 혹은 순간적 쾌락에 취함.", "직장": "파트너와의 불화, 어리석은 제휴, 유혹에 빠짐.", "재물": "관계로 인한 금전 손실, 잘못된 계약 우려."}
    },
    {
        "id": 7, "num": "VII", "name": "The Chariot", "kor": "전차", "emoji": "🏇", "el": "물",
        "kw": "전진, 통제, 승리", "tr": {"행동력": 100, "감성": 40, "지성": 60, "직관": 50, "의지": 95, "소통": 40},
        "m_up": {"종합": "강한 의지로 장애물을 돌파하고 승리합니다.", "연애": "직진하는 사랑. 추진력을 발휘해 관계 성취.", "직장": "목표 달성, 경쟁에서의 승리, 빠른 승진.", "재물": "적극적인 자산 증식 모드. 단기 차익 실현."},
        "m_rev": {"종합": "방향감 상실, 통제력 잃음.", "연애": "과도한 들이댐이나 급발진으로 관계 그르침.", "직장": "무리수로 인한 좌절, 외부 변수에 밀려남.", "재물": "속도 조절 실패. 성급한 투자로 인한 손해."}
    },
    {
        "id": 8, "num": "VIII", "name": "Strength", "kor": "힘", "emoji": "🦁", "el": "불",
        "kw": "포용, 용기, 외유내강", "tr": {"행동력": 70, "감성": 90, "지성": 60, "직관": 70, "의지": 95, "소통": 80},
        "m_up": {"종합": "따뜻함과 인내로 두려움을 길들입니다.", "연애": "어려움을 극복하는 단단한 사랑. 상대방을 포용함.", "직장": "부드러운 카리스마로 문제를 은근히 통제함.", "재물": "인내심이 보상을 가져다줌. 안정적인 장기적 불림."},
        "m_rev": {"종합": "자신감 부족, 두려움에 압도됨.", "연애": "감정 소모가 커 포기하고 싶음. 열등감 폭발.", "직장": "체력 고갈, 본능을 누르지 못해 터지는 불화.", "재물": "유혹을 이기지 못한 지출, 인내심 끊어짐."}
    },
    {
        "id": 9, "num": "IX", "name": "The Hermit", "kor": "은둔자", "emoji": "🕯️", "el": "흙",
        "kw": "은둔, 성찰, 지혜", "tr": {"행동력": 20, "감성": 50, "지성": 95, "직관": 90, "의지": 70, "소통": 20},
        "m_up": {"종합": "성찰의 시간입니다. 내면에서 지혜를 구하세요.", "연애": "혼자만의 시간이 필요한 때. 짝사랑, 정신적 교감.", "직장": "심도 있는 연구나 조용한 뒷바라지에 적합.", "재물": "돈보다 지식과 명예에 집중해야 이로운 시기."},
        "m_rev": {"종합": "과도한 소외감. 현실 도피.", "연애": "과도한 철벽, 마음을 닫고 고립됨.", "직장": "정보 교류 단절, 조직에서의 고립.", "재물": "재물 정보를 알지 못해 기회를 눈앞에서 놓침."}
    },
    {
        "id": 10, "num": "X", "name": "Wheel of Fortune", "kor": "운수", "emoji": "🎡", "el": "불",
        "kw": "전환, 기회, 필연", "tr": {"행동력": 80, "감성": 70, "지성": 50, "직관": 80, "의지": 40, "소통": 60},
        "m_up": {"종합": "상황이 유리하게 전환되는 좋은 운의 시기.", "연애": "운명 같은 타이밍. 뜻밖의 재회나 진전.", "직장": "행운이 따르고 좋은 부서 이동/승진 기회.", "재물": "예상치 못한 재물. 횡재수나 상황 반전."},
        "m_rev": {"종합": "원치 않는 변화, 운의 정체.", "연애": "엇갈리는 타이밍. 인연이 아니라고 느낌.", "직장": "통제 불가한 부정적 외부 요인 들이닥침.", "재물": "갑작스런 지출이나 투자 타이밍 오판."}
    },
    {
        "id": 11, "num": "XI", "name": "Justice", "kor": "정의", "emoji": "⚖️", "el": "공기",
        "kw": "공정함, 인과응보, 결정", "tr": {"행동력": 50, "감성": 30, "지성": 100, "직관": 50, "의지": 80, "소통": 70},
        "m_up": {"종합": "뿌린 대로 거두는 공정한 결과가 주어집니다.", "연애": "감정보다 이성이 앞서는 합리적 만남.", "직장": "정당한 보상, 정확한 룰에 따른 평가, 소송 승리.", "재물": "계약, 서류 작업이 명확해지고 이익 분배 공정."},
        "m_rev": {"종합": "불공평한 대우. 부도덕의 대가.", "연애": "이해타산적인 관계, 차가운 단절.", "직장": "편파적 평가, 법적/비율적 문제 얽힘.", "재물": "사기꾼을 만나거나 부당한 손해 감수."}
    },
    {
        "id": 12, "num": "XII", "name": "The Hanged Man", "kor": "매달린사람", "emoji": "🙃", "el": "물",
        "kw": "희생, 보류, 관점 전환", "tr": {"행동력": 10, "감성": 70, "지성": 80, "직관": 90, "의지": 60, "소통": 30},
        "m_up": {"종합": "잠시 멈춰서 새로운 관점을 깨닫는 보류의 시기.", "연애": "발전 없이 정체됨. 한 사람의 헌신/희생.", "직장": "프로젝트 지연. 인내심과 관점의 전환 필요.", "재물": "자금이 묶임. 장기 투자는 유지하되 단기는 불리."},
        "m_rev": {"종합": "무의미한 희생, 이기심.", "연애": "헛된 희생에 대한 보상심리, 이제는 벗어나야 할 때.", "직장": "아집을 버리지 못해 시간을 낭비함.", "재물": "손절해야 하는데 미련으로 버티다가 손해 확대."}
    },
    {
        "id": 13, "num": "XIII", "name": "Death", "kor": "죽음", "emoji": "💀", "el": "물",
        "kw": "종결, 대변화, 새 시작", "tr": {"행동력": 80, "감성": 30, "지성": 60, "직관": 70, "의지": 85, "소통": 20},
        "m_up": {"종합": "낡은 것을 완전히 쓸어버리고 새로운 막이 오릅니다.", "연애": "관계의 종료 후 재탄생, 완전히 다른 챕터 시작.", "직장": "이직, 퇴사, 개편. 끝냄으로써 숨통 트임.", "재물": "금융 포트폴리오의 극적 리셋. 새로운 파이프라인."},
        "m_rev": {"종합": "미련, 변화에 대한 저항.", "연애": "끝난 인연을 버리지 못해 괴로움.", "직장": "마무리되지 않은 옛날 업무로 고통 지속.", "재물": "망가진 것에 집착하여 손해만 가중됨."}
    },
    {
        "id": 14, "num": "XIV", "name": "Temperance", "kor": "절제", "emoji": "🫗", "el": "불",
        "kw": "균형, 중용, 순환", "tr": {"행동력": 40, "감성": 80, "지성": 70, "직관": 60, "의지": 70, "소통": 90},
        "m_up": {"종합": "상반된 것들의 조화로운 융합, 절제 필요.", "연애": "배려와 타협이 잘 되는 잔잔하고 평온한 관계.", "직장": "원활한 소통, 여러 부서가 매끄럽게 협업함.", "재물": "현금 흐름 원활. 수익/지출의 완벽한 밸런스."},
        "m_rev": {"종합": "균형 상실, 과욕이나 충돌.", "연애": "감정이 극단으로 치닫고 다툼이 잦음.", "직장": "소통 단절, 타협 불능으로 업무 마비.", "재물": "과소비로 인한 잔고 급감. 낭비벽 조심."}
    },
    {
        "id": 15, "num": "XV", "name": "The Devil", "kor": "악마", "emoji": "👿", "el": "흙",
        "kw": "유혹, 집착, 물질주의", "tr": {"행동력": 90, "감성": 80, "지성": 30, "직관": 40, "의지": 85, "소통": 50},
        "m_up": {"종합": "헤어나기 힘든 나쁜 인연이나 치명적 매력.", "연애": "육체적, 치명적, 혹은 독이 되는 집착적 관계.", "직장": "스트레스 받으나 대우(돈) 때문에 못 벗어남.", "재물": "큰 이익에 눈멀어 불법/편법의 유혹에 빠짐."},
        "m_rev": {"종합": "속박에서 벗어나 자유를 찾음.", "연애": "가스라이팅이나 불행한 관계로의 미련 털어냄.", "직장": "악순환의 고리를 자르고 벗어남(퇴사 등).", "재물": "나쁜 투자/빚을 청산하고 재정 자립."}
    },
    {
        "id": 16, "num": "XVI", "name": "The Tower", "kor": "탑", "emoji": "⚡", "el": "불",
        "kw": "붕괴, 재난, 해방", "tr": {"행동력": 100, "감성": 20, "지성": 40, "직관": 60, "의지": 50, "소통": 10},
        "m_up": {"종합": "기피하던 진실 폭로. 붕괴 속에서 오는 해방감.", "연애": "갑작스런 충돌, 번개 같은 충격적 이별 통보.", "직장": "직장 붕괴, 계획 무산, 예기치 않은 재난.", "재물": "순식간에 들이닥친 큰 재정적 손실. 위장 파산."},
        "m_rev": {"종합": "터질 게 터짐. 재난의 여파 지속.", "연애": "불안감이 결국 현실화, 상처 회복 기미 없음.", "직장": "꾸역꾸역 버티지만 붕괴를 막을 수 없음.", "재물": "피할 수 없는 파산/소송의 데미지 안고 감."}
    },
    {
        "id": 17, "num": "XVII", "name": "The Star", "kor": "별", "emoji": "🌟", "el": "공기",
        "kw": "희망, 치유, 이상", "tr": {"행동력": 50, "감성": 90, "지성": 50, "직관": 95, "의지": 60, "소통": 70},
        "m_up": {"종합": "폭풍이 지난 후 찾아로는 빛. 상처 치유.", "연애": "이상적인 관계 연모, 영혼을 울리는 맑은 사랑.", "직장": "밝은 전망, 창의적 영감이 샘솟음.", "재물": "재정 회복 조짐, 장기적으로 크게 길한 씨앗."},
        "m_rev": {"종합": "희망 상실, 이상과 현실의 괴리.", "연애": "기대가 컸던 만큼의 실망감, 환상이 깨짐.", "직장": "방향성 상실. 의기소침하여 슬럼프.", "재물": "돈 쓸어 모을 줄 알았던 낙관론의 패배."}
    },
    {
        "id": 18, "num": "XVIII", "name": "The Moon", "kor": "달", "emoji": "🌕", "el": "물",
        "kw": "불안, 환상, 숨겨진 진실", "tr": {"행동력": 20, "감성": 95, "지성": 40, "직관": 100, "의지": 30, "소통": 40},
        "m_up": {"종합": "혼란과 불안감. 내면과 무의식을 살펴야 할 때.", "연애": "마음을 알 수 없는 애매모호한 인연. 삼각관계 위험.", "직장": "불확실한 상황, 소문과 사기가 난무함.", "재물": "투명하지 않은 돈거래 주의, 사기 위험."},
        "m_rev": {"종합": "안개가 걷히고 거짓과 진실이 분명해짐.", "연애": "오해가 풀리거나, 불편한 진실을 직면함.", "직장": "사건의 실체를 파악하고 불안감에서 해방됨.", "재물": "어두웠던 재정 상황에 해결책이 보임."}
    },
    {
        "id": 19, "num": "XIX", "name": "The Sun", "kor": "태양", "emoji": "☀️", "el": "불",
        "kw": "성공, 성취, 명확함", "tr": {"행동력": 90, "감성": 90, "지성": 70, "직관": 60, "의지": 95, "소통": 90},
        "m_up": {"종합": "모든 의문 해소! 밝은 기운, 생명력 만개.", "연애": "최고의 궁합과 즐거운 연애, 관계의 축복.", "직장": "눈부신 성과 보장, 스포트라이트를 한 몸에 받음.", "재물": "재물이 확실하게 들어오며 풍족함을 누림."},
        "m_rev": {"종합": "성공이 조금 지연되거나 열정이 살짝 식음.", "연애": "열정이 시들거나 불필요한 번아웃.", "직장": "자신감 부족으로 스포트라이트를 놓침.", "재물": "기대치보다 수익이 저조하나 그래도 손해는 아님."}
    },
    {
        "id": 20, "num": "XX", "name": "Judgement", "kor": "심판", "emoji": "📯", "el": "불",
        "kw": "부활, 결과, 결단", "tr": {"행동력": 60, "감성": 60, "지성": 85, "직관": 80, "의지": 75, "소통": 60},
        "m_up": {"종합": "노력에 대한 최종 보상과 환생(부활)의 계기.", "연애": "헤어진 인연과의 재회 혹은 명확한 결론 도출.", "직장": "면접 합격통지, 밀려있던 일의 시원한 결실.", "재물": "투자 원금 회수 재기회, 판결/소송으로 인한 이득."},
        "m_rev": {"종합": "과거 후회에 얽매임. 책임을 회피.", "연애": "잘못된 만남의 미련에서 벗어나지 못해 괴로움.", "직장": "과오에 발목 잡혀 평가 하락, 시기를 놓침.", "재물": "재평가로 가치 하락, 벌금이나 위약금 발생."}
    },
    {
        "id": 21, "num": "XXI", "name": "The World", "kor": "세계", "emoji": "🌍", "el": "흙",
        "kw": "완성, 해피엔딩, 통합", "tr": {"행동력": 85, "감성": 85, "지성": 85, "직관": 85, "의지": 85, "소통": 85},
        "m_up": {"종합": "하나의 챕터 완벽 종료. 완벽한 도약과 성취.", "연애": "결혼까지 골인하는 완벽하고 둥근 결말.", "직장": "최고 수위의 프로젝트 성공, 목표 달성 졸업.", "재물": "결과물 손에 쥐게 됨. 최고의 금전적 피우스."},
        "m_rev": {"종합": "마지막 1%가 부족함. 미완성 상태의 정체.", "연애": "확실한 결착이나 선을 넘지 못한 답답함.", "직장": "매듭이 지어지지 않은 상태의 프로젝트.", "재물": "거의 손에 들어왔던 돈을 놓치거나 지연됨."}
    }
]

# ─── 유틸리티 함수 ───
def get_seed(date_str, user_name, category, spread_mode):
    raw = f"{date_str}_{user_name}_{category}_{spread_mode}"
    return int(hashlib.sha256(raw.encode()).hexdigest(), 16)

def pick_cards(seed, num_cards):
    random.seed(seed)
    chosen_ids = random.sample(range(22), num_cards)
    cards = []
    for cid in chosen_ids:
        c = TAROT_DECK[cid].copy()
        c["is_reversed"] = random.choice([True, False])
        cards.append(c)
    return cards

def render_tarot_card(card, key_suffix, pos_class=""):
    rev_class = "reversed" if card["is_reversed"] else ""
    rev_label = "<div class='reversed-label'>▼ 역방향 (Reversed)</div>" if card["is_reversed"] else ""
    return f"""
    <div class="card-container {pos_class}" id="card_{key_suffix}">
        <div class="tarot-card flipped {rev_class}">
            <div class="card-face card-back"></div>
            <div class="card-face card-front">
                <div class="card-content">
                    <div class="c-num">{card['num']}</div>
                    <div class="c-emoji">{card['emoji']}</div>
                    <div><div class="c-name">{card['name']}</div><div class="c-kor">{card['kor']}</div></div>
                </div>
            </div>
        </div>
        <div style="text-align:center; height: 30px;">{rev_label}</div>
    </div>
    """

def get_message(card, category):
    base_cat = category.split()[1]
    if base_cat == "종합":
        base = card["m_up"]["종합"] if not card["is_reversed"] else card["m_rev"]["종합"]
        love = card["m_up"]["연애"] if not card["is_reversed"] else card["m_rev"]["연애"]
        work = card["m_up"]["직장"] if not card["is_reversed"] else card["m_rev"]["직장"]
        return f"{base}<br><span style='color:rgba(255,255,255,0.7); font-size:0.95em;'>(연애: {love} / 직장: {work})</span>"
    else:
        q_map = {"연애": "연애", "직장": "직장", "재물운": "재물"}
        key = q_map.get(base_cat, "종합")
        return card["m_up"][key] if not card["is_reversed"] else card["m_rev"][key]

def calculate_radar(cards):
    s = {"행동력": 0, "감성": 0, "지성": 0, "직관": 0, "의지": 0, "소통": 0}
    for c in cards:
        f = 0.85 if c["is_reversed"] else 1.0
        for k in s: s[k] += c["tr"][k] * f
    return {k: v/len(cards) for k, v in s.items()}

def calc_synergy(cards):
    elements = {"불": 0, "물": 0, "공기": 0, "흙": 0}
    for c in cards: elements[c["el"]] += 1
    dom = max(elements, key=elements.get)
    if dom == "불": return "열정과 강한 에너지가 돋보이는 카드 조합입니다. 빠른 실행력이 관건입니다."
    if dom == "물": return "감성과 관계성이 지배하는 흐름입니다. 이성보다 직관과 공감이 해답입니다."
    if dom == "공기": return "지성과 소통, 객관적 사고를 요하는 콤비네이션입니다. 이성적으로 판단하세요."
    return "현실성과 안정감이 느껴지는 카드 조합입니다. 무리수보다 기존의 방식을 고수하세요."

# ─── 레이아웃 구성 ───
tab_main, tab_daily, tab_ency = st.tabs(["🔮 나의 리딩 방", "🎯 오늘의 조언 (1카드)", "📖 마스터 도감"])

with tab_ency:
    st.markdown('<div class="main-title gold-text">MAGICAL CARDS</div>', unsafe_allow_html=True)
    sel_el = st.selectbox("원소 필터", ["전체보기", "🔥 불 (행동/열정)", "💧 물 (감성/무의식)", "💨 공기 (지성/소통)", "🌱 흙 (물질/안정)"])
    cols = st.columns(4)
    idx = 0
    for card in TAROT_DECK:
        el_key = sel_el.split()[1] if sel_el != "전체보기" else ""
        if el_key and el_key != card["el"]: continue
        
        with cols[idx % 4]:
            c_mock = card.copy(); c_mock["is_reversed"] = False
            st.markdown(render_tarot_card(c_mock, f"doc_{card['id']}"), unsafe_allow_html=True)
            with st.expander(f"{card['num']}. {card['kor']} 상세"):
                st.markdown(f"**원소:** {card['el']} / **키워드:** {card['kw']}")
                st.markdown(f"✅ **정방향:** {card['m_up']['종합']}")
                st.markdown(f"🚫 **역방향:** {card['m_rev']['종합']}")
        idx += 1

with tab_daily:
    st.markdown('<div class="main-title gold-text">🎯 DAILY INSPIRATION</div>', unsafe_allow_html=True)
    cName = st.text_input("당신의 이름을 입력하면 오늘의 운세 카드가 열립니다", key="dName")
    if st.button("🌟 오늘의 1카드 뽑기", use_container_width=True) or cName:
        dSeed = get_seed(datetime.date.today().strftime("%Y%m%d"), cName, "daily", "daily")
        dCard = pick_cards(dSeed, 1)[0]
        st.markdown('<div class="glass-box" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(render_tarot_card(dCard, "daily"), unsafe_allow_html=True)
        msg = get_message(dCard, "🌟 종합")
        st.markdown(f"<h3>{dCard['kor']} ({dCard['name']})</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.1rem; color:#ffd700;'>{msg}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab_main:
    # ─── 사이드바: 입력 ───
    with st.sidebar:
        st.markdown('<div class="main-title gold-text" style="font-size: 2rem;">DESTINY TAROT</div>', unsafe_allow_html=True)
        st.markdown("---")
        user_name = st.text_input("당신의 이름", value="여행자")
        q_category = st.radio("어떤 고민이 있으신가요?", ["🌟 종합 / 오늘 하루", "💕 연애 / 인간관계", "💼 직장 / 학업", "💰 재물운 / 사업"])
        s_mode = st.radio("스프레드 방식", ["🃏 원오라클 (1카드)", "🃏🃏🃏 과거/현재/미래 (3카드)", "✝️ 셀틱 축소판 (5카드)"])
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        st.markdown("<br>", unsafe_allow_html=True)
        draw_btn = st.button("🔮 진심을 다해 뽑기", use_container_width=True)
        
        # ─── 히스토리 표시 ───
        if st.session_state["history"]:
            with st.expander("📜 지난 리딩 기록 (최근 10건)"):
                for h in reversed(st.session_state["history"][-10:]):
                    st.markdown(f"<div style='font-size:0.85rem; border-bottom:1px solid rgba(255,255,255,0.1); padding:5px 0;'><b>{h['cat']}</b> | {h['mode']}<br><span style='color:#bfa1df;'>{h['cards']}</span></div>", unsafe_allow_html=True)

    if not draw_btn and 'drawn' not in st.session_state:
        st.markdown('<div class="main-title gold-text" style="font-size:3.5rem; margin-top:5vh;">SEEK THE TRUTH</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">22장의 메이저 아르카나가 당신의 의문을 해소해 줍니다.</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding: 20px;">
            <div class="tarot-card" style="display:inline-block; width:120px; height:180px; margin:-10px; transform:rotate(-15deg); box-shadow:0 0 15px rgba(255,215,0,0.5);"><div class="card-face card-back" style="font-size:0.4rem;"></div></div>
            <div class="tarot-card" style="display:inline-block; width:120px; height:180px; margin:-10px; position:relative; z-index:2; box-shadow:0 0 15px rgba(255,215,0,0.5);"><div class="card-face card-back" style="font-size:0.4rem;"></div></div>
            <div class="tarot-card" style="display:inline-block; width:120px; height:180px; margin:-10px; transform:rotate(15deg); box-shadow:0 0 15px rgba(255,215,0,0.5);"><div class="card-face card-back" style="font-size:0.4rem;"></div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state['drawn'] = True
        num_cards = 1
        if "3카드" in s_mode: num_cards = 3
        elif "5카드" in s_mode: num_cards = 5
            
        seed = get_seed(date_str, user_name, q_category, s_mode)
        drawn_cards = pick_cards(seed, num_cards)
        
        # 히스토리 추가
        if draw_btn:
            c_str = ", ".join([c["kor"] + ("(역)" if c["is_reversed"] else "") for c in drawn_cards])
            st.session_state["history"].append({"cat": q_category.split()[1], "mode": s_mode.split()[1], "cards": c_str})
        
        st.markdown('<div class="main-title gold-text" style="font-size:2.5rem; text-align:left;">🔮 THE REVELATION</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-box" style="text-align:center;">', unsafe_allow_html=True)
        spread_labels = {
            1: ["핵심 조언"],
            3: ["과거의 토대", "현재 상황", "미래 발전"],
            5: ["현재의 나", "방해/도움(크로스)", "내면/과거", "가까운 미래", "최종 결과"]
        }
        labels = spread_labels[num_cards]
        
        if num_cards == 5:
            # 셀틱 크로스 형 CSS 레이아웃
            st.markdown('<div class="grid-5card">', unsafe_allow_html=True)
            for i in range(5):
                st.markdown(f"<div class='pos-{i+1}'>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:#ffd700; font-weight:bold; margin-bottom:5px;'>✦ {labels[i]} ✦</div>", unsafe_allow_html=True)
                st.markdown(render_tarot_card(drawn_cards[i], i), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            cols = st.columns(num_cards)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"<div style='color:#ffd700; font-weight:bold; font-size:1.1rem; margin-bottom:15px; letter-spacing:1px;'>✦ {labels[i]} ✦</div>", unsafe_allow_html=True)
                    st.markdown(render_tarot_card(drawn_cards[i], i), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 조합 에너지 (2카드 이상)
        if num_cards > 1:
            st.markdown('<div class="glass-box" style="background: rgba(212,175,55,0.1); border-color:#ffd700; text-align:center;">', unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#ffd700; margin:0;'>✨ 융합 에너지: {calc_synergy(drawn_cards)}</h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-title gold-text" style="font-size:2rem; text-align:left; margin-top:2rem;">📜 DETAILS</div>', unsafe_allow_html=True)
        
        for i, c in enumerate(drawn_cards):
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            cA, cB = st.columns([1, 4])
            s_color = "#8a2be2" if c["is_reversed"] else "#ffd700"
            s_txt = "역방향" if c["is_reversed"] else "정방향"
            meaning = get_message(c, q_category)
            
            with cA:
                st.markdown(f"<div style='font-size:4rem; text-align:center;'>{c['emoji']}</div><div style='text-align:center; font-family:Cinzel; font-weight:bold;'>{labels[i]}</div>", unsafe_allow_html=True)
            with cB:
                st.markdown(f"<h3 style='margin:0 0 5px 0;'>{c['kor']} <span style='color:#a1c4fd; font-size:1rem'>[{c['el']}]</span></h3>", unsafe_allow_html=True)
                st.markdown(f"<span style='background:{s_color}; padding:2px 8px; border-radius:10px; color:#fff; font-size:0.8rem;'>{s_txt}</span> <span style='color:#bfa1df; font-size:0.9rem;'>{c['kw']}</span>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:1.1rem; line-height:1.7; padding:15px; margin-top:10px; background:rgba(0,0,0,0.3); border-left: 4px solid {s_color}; border-radius:0 8px 8px 0;'>{meaning}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="main-title gold-text" style="font-size:2rem; text-align:left; margin-top:2rem;">📊 ENERGY CHART</div>', unsafe_allow_html=True)
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            rd = calculate_radar(drawn_cards)
            fig = go.Figure(go.Scatterpolar(r=list(rd.values())+[list(rd.values())[0]], theta=list(rd.keys())+[list(rd.keys())[0]], fill='toself', fillcolor='rgba(212,175,55,0.2)', line=dict(color='#ffd700')))
            fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#e2d9f3'))), showlegend=False, margin=dict(l=30, r=30, t=30, b=30), height=300, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with stat_col2:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            pos = int((sum(1 for c in drawn_cards if not c["is_reversed"]) / num_cards) * 100)
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=pos, number={'font': {'size': 50, 'color': '#ffd700'}, 'suffix': "%"}, gauge={'axis': {'range': [None, 100], 'visible': False}, 'bar': {'color': "#ffd700"}, 'bgcolor': "rgba(255,255,255,0.05)", 'borderwidth': 0}))
            fig_g.update_layout(height=220, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar': False})
            msg = "정방향 주도: 원활한 상황 전개가 기대됩니다!" if pos >= 50 else "역방향 주도: 신중한 접근과 내면 성찰이 필요합니다."
            st.markdown(f"<div style='text-align:center; color:#bfa1df;'>{msg}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
