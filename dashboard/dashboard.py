import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly
import plotly.express as px
import altair as alt
# from lightweight_charts.widgets import StreamlitChart

####################### style.css 적용 #######################

# # streamlit 우상단 메뉴 표시
# st.markdown(
#     """
#     <style>
#         footer {display: none}
#         [data-testid="stHeader"] {display: none}
#     </style>
#     """, unsafe_allow_html = True
# )

# with open('style.css', encoding="utf-8-sig") as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

####################### /style.css 적용 #######################

# 업로드된 CSV 파일 세션 스테이트 초기화 
if "df" not in st.session_state:
    st.session_state["df"] = "test"

# 임시 데이터 세션 스테이트 초기화
if "df_ins" not in st.session_state:
    st.session_state["df_ins"] = None
if "df_titanic" not in st.session_state:
    st.session_state["df_titanic"] = None
if "df_ohlcv" not in st.session_state:
    st.session_state["df_ohlcv"] = None



################################ 기능함수 구현 ################################

# 도넛 차트 생성기
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text


################################ /기능함수 구현 ################################


################################ 사이드바 ################################
with st.sidebar:
    # clr_btn = st.button("대화 초기화")  # 대화 내용을 초기화하는 버튼

    # CSV 파일 업로드
    uploaded_file = st.file_uploader(
        "csv 파일을 업로드 해주세요.", type=['csv'], accept_multiple_files=False)
    print("/n", "업로드된 파일:", uploaded_file, "/n")

    # 대시보드 생성 버튼
    apply_btn = st.button("대시보드 생성")  


################################ /사이드바 ################################

################################ 데이터 전처리 ################################

# 임시 데이터 불러오기
df_ins = st.session_state['df_ins']
df_titanic = st.session_state['df_titanic']
df_ohlcv = st.session_state['df_ohlcv']

df_titanic["Last_Name"] = df_titanic["Name"].map(lambda x: x.split('.')[-1])
df_titanic['Fare_int'] = df_titanic['Fare'].map(lambda x: int(x))
fare_sorted = df_titanic.sort_values(by='Fare_int', ascending=False)[["Last_Name", "Fare_int"]].set_index("Last_Name")


################################ /데이터 전처리 ################################


########################### 1번째 컨테이너 ###########################

st.markdown('#### Basic statistics')
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(label = "Avg age",
        value = df_ins['age'].mean().round(1),
        delta = 1.4)

c2.metric(label = "avg bmi",
            value = df_ins['bmi'].mean().round(1),
            delta = -5)

c3.metric(label = "avg charges",
            value = df_ins['charges'].mean().round(1),
            delta = 15)

with c5.expander('About', expanded=False):
    st.write('''
        - Data: [Insurance Charges](<https://www.kaggle.com/datasets/awaiskaggler/insurance-csv>).
        - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
        - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
        ''')

st.markdown("<br>", unsafe_allow_html=True)

########################### 2번째 컨테이너 ###########################

c6, c7, c8, c9, c10 = st.columns([0.8, 2, 0.2, 1, 0.01])

# Donut chart 생성
c6.markdown('#### States Migration')
donut_chart_greater = make_donut(55, 'Inbound Migration', 'green')
c6.write('Man charged')
c6.altair_chart(donut_chart_greater)

c6.write('Woman charged')
donut_chart_less = make_donut(80, 'Outbound Migration', 'red')
c6.altair_chart(donut_chart_less)

# Scatter chart 생성
c7.markdown('#### Bmi & Charges')
fig_scatter = px.scatter(df_ins, x='bmi', y='charges', 
                color='smoker', 
            #  labels={'sepal_width':'Sepal width', 
            #        'sepal_length':'Sepal length'}, 
            #  title='Correlation between BMI and charges of smokers' 
    )
fig_scatter.update_layout(width=500, height=500)  # 그래프 사이즈 조절
c7.plotly_chart(fig_scatter, use_container_width=True)

# DataFrame 생성
c9.markdown('#### Top Fares')
# st.markdown("<br><br>", unsafe_allow_html=True)
c9.dataframe(fare_sorted, 
             column_config={
                    "Name": st.column_config.TextColumn(
                        "Name",
                    ),
                    "Fare_int": st.column_config.ProgressColumn(
                        "Fare",
                        format="%f",
                        min_value=0,
                        max_value=max(fare_sorted["Fare_int"]),
                     )}
                 )

st.markdown("<br>", unsafe_allow_html=True)

########################### 3번째 컨테이너 ###########################

c11, c12, c13, c14, c15 = st.columns([0.3, 3, 1, 3, 0.7])

# Pie chart 생성
c12.markdown('#### Region Ratio')
region_count = df_ins['region'].value_counts()
fig_pie = px.pie(df_ins, values=region_count.values, names=region_count.index,
            #  title='count by region'
            )
# fig_pie.update_layout(width=800, height=800)  # 그래프 사이즈 조절
# 텍스트 크기 조정 (update_traces 및 update_layout 사용)
fig_pie.update_traces(
    textfont_size=18,  # Pie 차트 내부 텍스트 크기
    hoverinfo="label+percent+value",  # 툴팁 형식
    textinfo="percent+label"  # 라벨에 표시할 정보
)
c12.plotly_chart(fig_pie)

# 상관관계 Heatmap 생성
c14.markdown('#### Correlations')
df_corr_titanic = df_titanic.select_dtypes(include=["number"]).corr().round(2)
fig_heatmap = px.imshow(df_corr_titanic, 
                        text_auto=True)      # 값(annotation) 표시)
c14.plotly_chart(fig_heatmap)

st.markdown("<br>", unsafe_allow_html=True)

########################### 4번째 컨테이너 ###########################

c16, c17, c18, c19, c20 = st.columns([0.3, 3, 1, 3, 0.7])

# Bar chart
with c17:
    st.markdown('#### Pclass Count')
    pclass_count = df_titanic["Pclass"].value_counts()

    fig_bar = px.bar(df_titanic, x=pclass_count.index, y=pclass_count.values)

    # x축, y축 label 지정
    fig_bar.update_layout(
        xaxis_title = 'Pclass',   # x축 레이블
        yaxis_title = 'Count',     # y축 레이블
        xaxis=dict(
                tickvals=[1, 2, 3],  # 표시할 눈금 값
                ticktext=["1", "2", "3"]  # 눈금에 표시할 텍스트
            )
        )
    st.plotly_chart(fig_bar)

# candle chart
# with c17:
    # st.markdown('#### OHLCV Candle chart')
    # chart = StreamlitChart(height = 450, width = 450)   # height = 450, width = 650
    # chart.grid(vert_enabled = True, horz_enabled = True)

    # chart.layout(background_color='#131722', font_family='Trebuchet MS', font_size = 16)

    # chart.candle_style(up_color='#2962ff', down_color='#e91e63',
    #                 border_up_color='#2962ffcb', border_down_color='#e91e63cb',
    #                 wick_up_color='#2962ffcb', wick_down_color='#e91e63cb')

    # chart.volume_config(up_color='#2962ffcb', down_color='#e91e63cb')
    # chart.legend(visible = True, font_family = 'Trebuchet MS', ohlc = True, percent = True)

    # chart.set(df_ohlcv)
    # chart.load()




