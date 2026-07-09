import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("❤️ 국가별 장르 취향 및 변화 분석")

@st.cache_data
def load_data():
    return pd.read_csv('k_contents_trend_data.csv')

df = load_data()

# 1. 국가 선택 사이드바
countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("국가를 선택하세요", countries)

# 2. 해당 국가에서 가장 인기 있는 장르 찾기
country_df = df[df['Country'] == selected_country]

if not country_df.empty:
    # 장르별 총 인기도(또는 평균)를 구해서 가장 높은 장르 추출
    favorite_genre = country_df.groupby('Genre')['Popularity'].mean().idxmax()
    max_val = country_df.groupby('Genre')['Popularity'].mean().max()
    
    st.success(f"👑 {selected_country}에서 가장 인기 있는 장르는 **[{favorite_genre}]** 입니다! (평균 인기도: {max_val:.2f})")
    
    st.markdown("---")
    
    # 3. 가장 인기 있는 장르의 연도별 변화 그래프
    st.subheader(f"📈 {selected_country} 내 [{favorite_genre}] 장르의 연도별 인기도 변화")
    
    fav_genre_df = country_df[country_df['Genre'] == favorite_genre].groupby('Year')['Popularity'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Year', y='Popularity', data=fav_genre_df, marker='s', color='darkorange', linewidth=2, ax=ax)
    ax.set_title(f"{selected_country} - {favorite_genre} 장르 트렌드")
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 인기도")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xticks(fav_genre_df['Year'].unique())
    
    st.pyplot(fig)
else:
    st.warning("선택한 국가의 데이터가 없습니다.")
