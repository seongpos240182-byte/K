import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("❤️ 국가별 장르 취향 및 변화 분석")

@st.cache_data
def load_data():
    df = pd.read_csv('k_contents_trend_data.csv')
    year_cols = [col for col in df.columns if col.startswith('year_')]
    df_melted = df.melt(id_vars=['country', 'genre'], value_vars=year_cols, 
                        var_name='year', value_name='popularity')
    df_melted['year'] = df_melted['year'].str.replace('year_', '').astype(int)
    return df_melted

df = load_data()

# 1. 국가 선택 사이드바
countries = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox("국가를 선택하세요", countries)

country_df = df[df['country'] == selected_country]

if not country_df.empty:
    # 2. 가장 인기 있는 장르 추출 (전체 연도 평균 기준)
    favorite_genre = country_df.groupby('genre')['popularity'].mean().idxmax()
    max_val = country_df.groupby('genre')['popularity'].mean().max()
    
    st.success(f"👑 {selected_country}에서 가장 인기 있는 장르는 **[{favorite_genre}]** 입니다! (평균 인기도: {max_val:.2f})")
    st.markdown("---")
    
    # 3. 가장 인기 있는 장르의 연도별 변화 그래프
    st.subheader(f"📈 {selected_country} 내 [{favorite_genre}] 장르의 연도별 인기도 변화")
    
    fav_genre_df = country_df[country_df['genre'] == favorite_genre].sort_values(by='year')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='year', y='popularity', data=fav_genre_df, marker='s', color='darkorange', linewidth=2, ax=ax)
    ax.set_title(f"{selected_country} - {favorite_genre} 장르 트렌드")
    ax.set_xlabel("연도")
    ax.set_ylabel("인기도")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xticks(fav_genre_df['year'].unique())
    
    st.pyplot(fig)
else:
    st.warning("선택한 국가의 데이터가 없습니다.")
