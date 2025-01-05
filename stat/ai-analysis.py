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

st.markdown("# ai 분석")

# if st.session_state["two_num_relation"]:
st.write(st.session_state["two_num_relation"])
st.write(st.session_state["two_cat_relation"])
st.write(st.session_state["regression"])

