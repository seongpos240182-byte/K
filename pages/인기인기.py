import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Windows: Malgun Gothic, Mac: AppleGothic)
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

st.title("🎬 K-콘텐츠 장르별 인기도 분석")

@st.cache_data
def load_data():
    df = pd.read_csv('k_contents_trend_data.csv')
    # 연도별 컬럼들을 하나의 'year'와 'popularity' 컬럼으로 변환
    year_cols = [col for col in df.columns if col.startswith('year_')]
    df_melted = df.melt(id_vars=['country', 'genre'], value_vars=year_cols, 
                        var_name='year', value_name='popularity')
    # 'year_2020' -> 2020 (숫자형) 변환
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

total_genre_popularity = df.groupby('genre')['popularity'].mean().reset_index().sort_values(by='popularity', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='popularity', y='genre', data=total_genre_popularity, palette='viridis', ax=ax)
ax.set_title("전체 장르별 평균 인기도 트렌드")
ax.set_xlabel("평균 인기도")
ax.set_ylabel("장르")

st.pyplot(fig)
