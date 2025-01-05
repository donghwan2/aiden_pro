import os; import pandas as pd; import numpy as np; import streamlit as st    
import matplotlib as plt; import seaborn as sns; import plotly   
import warnings; warnings.filterwarnings('ignore')
from dotenv import load_dotenv; load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages.chat import ChatMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from dashboard.dashboard import df_ins

# agent
from file_llm import pdf_chain, process_imagefile, multimodal_answer
from langchain_experimental.tools import PythonREPLTool, PythonAstREPLTool  # PythonREPL
from typing import List, Dict, Union, Annotated              # 데이터 타입
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent # Pandas
# from langchain_teddynote.messages import AgentCallbacks      # Agent callback 함수
# from langchain_teddynote.messages import AgentStreamParser   # Agent 중간단계 스트리밍

import plotly
import plotly.express as px
from scipy import stats

st.markdown("# 변수 관계 분석")

df_ins = st.session_state['df_ins']
df_titanic = st.session_state['df_titanic']
df_ohlcv = st.session_state['df_ohlcv']

numeric_list = df_ins.select_dtypes(include=['number']).columns.tolist()
category_list = df_ins.select_dtypes(include=['object', 'category']).columns.tolist()

########################## 기능함수 구현 ##########################

# 수치형 변수 간 상관관계 분석
def num_correlation(df, var1, var2):
    corr_df = df.select_dtypes(include=['number']).corr().round(3)
    tow_num_corr = df[[var1, var2]].corr()

    # 전체 변수 상관계수 히트맵
    fig_heatmap = px.imshow(corr_df, 
                            text_auto=True)  # 값(annotation) 표시)
    st.plotly_chart(fig_heatmap)
    return tow_num_corr


# 범주형 변수 간 독립성 검정
def chi2_test(df, var1, var2):
    agg = pd.crosstab(df[var1], df[var2])
    df_chi2 = stats.chi2_contingency(agg)
    st.dataframe(df_chi2)
    return df_chi2

########################## /기능함수 구현 ##########################

################## 사이드바 ##################
with st.sidebar:
    # # 초기화 버튼
    # clr_btn = st.button("대화 초기화")

    analysis_type = st.selectbox(
        "분석 종류", ["두 개의 수치형 변수", 
                  "두 개의 범주형 변수", 
                  "한 개의 수치형 & 한 개의 범주형 변수"], index=0 
        )
    
    if analysis_type == "두 개의 수치형 변수":
        variables = st.multiselect(
        "변수명", numeric_list,
        default = [f'{numeric_list[0]}', f'{numeric_list[1]}']
        )

    elif analysis_type == "두 개의 범주형 변수":
        variables = st.multiselect(
        "변수명", category_list,
        default = [f'{category_list[0]}', f'{category_list[1]}']
        )
        
    analysis_btn = st.button("관계 분석 시작") 
    

################## /사이드바 ##################

if analysis_type == "두 개의 수치형 변수" and analysis_btn:   
    tow_num_corr = num_correlation(df_ins, variables[0], variables[1])
    st.session_state["two_num_relation"] = tow_num_corr

elif analysis_type == "두 개의 범주형 변수" and analysis_btn:
    df_chi2 = chi2_test(df_ins, variables[0], variables[1])
    st.session_state["two_cat_relation"] = df_chi2

