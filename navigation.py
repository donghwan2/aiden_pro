import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 배너 이름/아이콘(맨 윗줄에 위치)
st.set_page_config(
    layout = 'wide',
    page_title = 'Aiden Pro - Auto Report Agent',
    page_icon=":computer:"
)

# 주기적으로 자동 새로고침 (1000ms=1초, 60000=1분, 3600000=1시간)
st_autorefresh(interval=3600000, key="refresh")

# 스트림릿 상단 메뉴 바/하단 Made with Streamlit 숨김
st.markdown(
    """
    <style>
        footer {display: none}     /* Streamlit의 기본 푸터(하단 Made with Streamlit 문구)를 숨김 */
        [data-testid="stHeader"] {display: none}     /* Streamlit의 기본 헤더(상단 메뉴 바)를 숨김 */
    </style>
    """, unsafe_allow_html = True
)

####################### 세션 스테이트 초기화 #######################

if "two_num_relation" not in st.session_state:
    st.session_state["two_num_relation"] = None
if "two_cat_relation" not in st.session_state:
    st.session_state["two_cat_relation"] = None
if "regression" not in st.session_state:
    st.session_state["regression"] = None

# 임시 데이터 세션 스테이트에 넣기
df_ins = pd.read_csv("data/insurance.csv")
df_titanic = pd.read_csv("data/titanic.csv")
df_ohlcv = pd.read_csv("data/crypto_ohlcv.csv")
st.session_state['df_ins'] = df_ins
st.session_state['df_titanic'] = df_titanic
st.session_state['df_ohlcv'] = df_ohlcv


# 대시보드
dashboard = st.Page("dashboard/dashboard.py", title="대시보드", icon=":material/house:", 
                    default=True)
# 통계 분석
relation_analysis = st.Page("stat/relation_analysis.py", title="변수 관계 분석", icon=":material/house:")

# 회귀분석
regression = st.Page("stat/regression.py", title="선형회귀 분석", icon=":material/house:")

# 머신러닝
ml_classification = st.Page("ml/ml_classification.py", title="머신러닝 분류", icon=":material/house:")
ml_regression = st.Page("ml/ml_regression.py", title="머신러닝 회귀", icon=":material/house:")

# AI report
ai_analysis = st.Page("ai_report/ai_analysis.py", title="보고서로 정리", icon=":material/house:")

# 여러 개의 st.Page 객체를 묶어서 내비게이션 메뉴 생성
pages_navi = st.navigation(
    {
        "데이터 파악" : [dashboard],
        "통계 분석" : [relation_analysis, regression],
        "머신러닝" : [ml_classification, ml_regression],
        "AI Report" : [ai_analysis]
    }
)

pages_navi.run()




