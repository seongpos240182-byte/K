import streamlit as st
import pandas as pd

st.title("🎬 K-콘텐츠 장르별 인기도 분석")

@st.cache_data
def load_data():
    df = pd.read_csv('k_contents_trend_data.csv')
    year_cols = [col for col in df.columns if col.startswith('year_')]
    df_melted = df.melt(id_vars=['country', 'genre'], value_vars=year_cols, 
                        var_name='year', value_name='popularity')
    df_melted['year'] = df_melted['year'].str.replace('year_', '').astype(int)
    return df_melted

df = load_data()

# 1. 장르 선택 사이드바
genres = sorted(df['genre'].unique())
selected_genre = st.sidebar.selectbox("원하는 장르를 선택하세요", genres)

# 2. 선택한 장르의 평균 인기도 출력
genre_df = df[df['genre'] == selected_genre]
avg_popularity = genre_df['popularity'].mean()

st.metric(label=f"✨ 선택한 [{selected_genre}] 장르의 평균 인기도 (2020-2025)", value=f"{avg_popularity:.2f}")

st.markdown("---")

# 3. 전체 장르별 인기도 시각화
st.subheader("📊 전체 장르별 평균 인기도 비교")

total_genre_popularity = df.groupby('genre')['popularity'].mean().sort_values(ascending=False)

# Streamlit 내장 가로 바 차트로 교체하여 한글 깨짐 원천 방지
st.bar_chart(total_genre_popularity, horizontal=True)
