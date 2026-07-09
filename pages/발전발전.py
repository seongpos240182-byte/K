import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("📈 국가별 K-콘텐츠 발전 트렌드")

@st.cache_data
def load_data():
    return pd.read_csv('k_contents_trend_data.csv')

df = load_data()

# 1. 국가 선택 사이드바
countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("국가를 선택하세요", countries)

# 2. 선택한 국가의 데이터 필터링
country_df = df[df['Country'] == selected_country]

# 연도별 평균 인기도 계산
yearly_popularity = country_df.groupby('Year')['Popularity'].mean().reset_index()

st.subheader(f"🌍 {selected_country}의 연도별 K-콘텐츠 인기도 변화")

# 3. 선그래프 시각화
if not yearly_popularity.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Year', y='Popularity', data=yearly_popularity, marker='o', color='b', linewidth=2, ax=ax)
    ax.set_title(f"{selected_country}의 연도별 인기도 성장 추이")
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 인기도")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # x축 연도가 소수점으로 나오는 것 방지
    ax.set_xticks(yearly_popularity['Year'].unique())
    
    st.pyplot(fig)
else:
    st.warning("선택한 국가의 데이터가 부족합니다.")
