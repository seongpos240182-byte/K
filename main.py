import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (깨짐 방지)
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

st.title("🎬 K-콘텐츠 장르별 인기도 분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    # 실제 파일 경로에 맞게 수정하세요
    df = pd.read_csv('k_contents_trend_data.csv')
    return df

df = load_data()

# 1. 장르 선택 사이드바
genres = df['Genre'].unique()
selected_genre = st.sidebar.selectbox("원하는 장르를 선택하세요", genres)

# 2. 선택한 장르의 평균 인기도 출력
genre_df = df[df['Genre'] == selected_genre]
avg_popularity = genre_df['Popularity'].mean()

st.metric(label=Lines := f"✨ 선택한 [{selected_genre}] 장르의 평균 인기도", value=f"{avg_popularity:.2f}")

st.markdown("---")

# 3. 전체 장르별 인기도 시각화
st.subheader("📊 전체 장르별 평균 인기도 비교")

# 장르별 평균 계산 및 정렬
total_genre_popularity = df.groupby('Genre')['Popularity'].mean().reset_index().sort_values(by='Popularity', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='Popularity', y='Genre', data=total_genre_popularity, palette='viridis', ax=ax)
ax.set_title("전체 장르별 평균 인기도 트렌드")
ax.set_xlabel("평균 인기도")
ax.set_ylabel("장르")

st.pyplot(fig)
