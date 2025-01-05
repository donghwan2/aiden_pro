import streamlit as st
import pandas as pd; import numpy as np

# 회귀 라이브러리
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.metrics import r2_score

# 워닝 무시
import warnings; warnings.filterwarnings('ignore')

st.markdown("# 회귀분석")

df_ins = st.session_state['df_ins']
df_titanic = st.session_state['df_titanic']
df_ohlcv = st.session_state['df_ohlcv']

total_list = df_ins.columns.tolist()
numeric_list = df_ins.select_dtypes(include=['number']).columns.tolist()
category_list = df_ins.select_dtypes(include=['object', 'category']).columns.tolist()

########################## 기능함수 구현 ##########################

def regression(df, y):
    # X : 설명변수/독립변수 ,   y: 관심변수/종속변수
    
    df_dummies = pd.get_dummies(data=df, dtype='int', drop_first=True)
    X = df_dummies.drop(columns=[y])
    y = df_dummies[y]
    X_sm = sm.add_constant(X)   # 상수항 추가(모델을 유연하게 만들어줌)

    # 선형회귀 모델 적합(fit)
    ls = sm.OLS(y, X_sm).fit()
    st.write(ls.summary())

    return ls.summary()
    



########################## /기능함수 구현 ##########################


################## 사이드바 ##################
with st.sidebar:
    # # 초기화 버튼
    # clr_btn = st.button("대화 초기화")

    target = st.selectbox(
        "타겟 변수", numeric_list, index=0 
        )

    analysis_btn = st.button("회귀분석 시작") 

################## /사이드바 ##################

if analysis_btn:
    ls_summary = regression(df_ins, target)
    st.session_state["regression"] = ls_summary




