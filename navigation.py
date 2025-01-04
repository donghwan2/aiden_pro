import streamlit as st

# st.set_page_config(page_title="Aiden Pro(AI&Data Enhancer)", page_icon="")

st.set_page_config(
    layout = 'wide',
    page_title = 'Aiden Pro',
    page_icon=":computer:"
)


# 대시보드
dashboard = st.Page("dashboard/dashboard.py", title="대시보드", icon=":material/house:", 
                    default=True)
# 통계 분석
relation_analysis = st.Page("stat/relation_analysis.py", title="변수 관계 분석", icon=":material/house:")
regression = st.Page("stat/regression.py", title="선형회귀 분석", icon=":material/house:")

# 머신러닝
ml_classification = st.Page("ml/ml_classification.py", title="머신러닝 분류", icon=":material/house:")
ml_regression = st.Page("ml/ml_regression.py", title="머신러닝 회귀", icon=":material/house:")

# 여러 개의 st.Page 객체를 묶어서 내비게이션 메뉴 생성
pages_navi = st.navigation(
    {
        "데이터 파악" : [dashboard],
        "통계 분석" : [relation_analysis, regression],
        "머신러닝" : [ml_classification, ml_regression]
    }
)

pages_navi.run()




