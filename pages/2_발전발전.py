import streamlit as st
import pandas as pd

st.title("📈 국가별 K-콘텐츠 발전 트렌드")

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

# 2. 선택한 국가의 데이터 필터링 및 연도별 평균 계산
country_df = df[df['country'] == selected_country]
yearly_popularity = country_df.groupby('year')['popularity'].mean()

st.subheader(f"🌍 {selected_country}의 연도별 K-콘텐츠 인기도 변화")

# 3. 선그래프 시각화
if not yearly_popularity.empty:
    # Streamlit 내장 선그래프로 교체하여 한글 깨짐 원천 방지
    st.line_chart(yearly_popularity)
else:
    st.warning("선택한 국가의 데이터가 부족합니다.")
