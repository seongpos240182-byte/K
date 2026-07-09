import streamlit as st
import pandas as pd

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
    
    # 시각화용 데이터 인덱스 세팅
    fav_genre_df = country_df[country_df['genre'] == favorite_genre].set_index('year')['popularity']
    
    # Streamlit 내장 선그래프로 교체하여 한글 깨짐 원천 방지
    st.line_chart(fav_genre_df)
else:
    st.warning("선택한 국가의 데이터가 없습니다.")
