import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import koreanize_matplotlib

st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
) # 웹페이지 탭 디자인 설정


st.markdown("# 자동차 연비 🚗")
st.sidebar.markdown("# 자동차 연비 🚗")

# github에서 csv 불러오기
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"

# 캐시 생성
@st.cache
def load_data(nrows):
    data = pd.read_csv(url, nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# data = sns.load_dataset("mpg")

st.sidebar.header('피처를 선택해주세요') # 사이드바 헤더 생성

# Sidebar - year
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(data.model_year.min(),data.model_year.max())))
   ) # 연도 리스트 selectbox 생성(내림차순)

if selected_year > 0 :
   data = data[data.model_year == selected_year] # 선택된 year만 보여주기

# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin) # origin 고유값 multiselect 생성

if len(selected_origin) > 0: # origin에 값이 들어있다면
   data = data[data.origin.isin(selected_origin)] # origin에 해당되는 값들을 return

st.dataframe(data) # 데이터프레임 띄우기

st.line_chart(data["mpg"]) # 선그래프 띄우기

st.bar_chart(data["mpg"]) # 막대그래프 띄우기

fig, ax = plt.subplots(figsize=(10,3))
sns.countplot(data=data, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)

pxh = px.histogram(data, x="origin", title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

fig, ax = plt.subplots(figsize=(10,3))
sns.barplot(data=data, x="model_year", y="mpg", hue="origin", ci=None).set_title("연도별 지역별 연비")
st.pyplot(fig)