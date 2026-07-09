import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 기본 설정
st.set_page_config(
    page_title="K-콘텐츠 트렌드 대시보드",
    page_icon="🎬",
    layout="wide"
)

# 한글 폰트 설정 (깨짐 방지)
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

# 공통 데이터 로드 함수 (구조를 한눈에 볼 수 있게 정돈)
@st.cache_data
def load_data():
    df = pd.read_csv('k_contents_trend_data.csv')
    year_cols = [col for col in df.columns if col.startswith('year_')]
    
    # 괄호 처리를 명확하게 작성
    df_melted = df.melt(
        id_vars=['country', 'genre'], 
        value_vars=year_cols, 
        var_name='year', 
        value_name='popularity'
    )
    
    df_melted['year'] = df_melted['year'].str.replace('year_', '').astype(int)
    return df_melted

# 데이터 미리 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 읽어오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바에서 분석 페이지 선택
st.sidebar.title("📌 메뉴 선택")
menu = st.sidebar.radio(
    "원하는 분석을 선택하세요:",
    ["홈 (표지)", "1. 인기인기 (장르별 분석)", "2. 발전발전 (국가별 트렌드)", "3. 취향취향 (국가별 선호도)"]
)

# ----------------------------------------------------
# 홈 (표지) 화면
# ----------------------------------------------------
if menu == "홈 (표지)":
    st.title("🎬 K-콘텐츠 글로벌 트렌드 데이터 대시보드")
    st.markdown("---")
    
    st.markdown("""
    ### 📊 대시보드 개요
    본 대시보드는 `k_contents_trend_data.csv` 파일을 기반으로 **전 세계 국가의 K-콘텐츠(드라마, 음악, 뷰티, 게임 등) 인기도 트렌드**를 다각도로 분석하기 위해 제작되었습니다.
    
    왼쪽 사이드바의 메뉴를 이용해 원하는 분석 페이지로 이동할 수 있습니다.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 1️⃣ 인기인기\n**장르별 인기도 분석**\n- 선택한 장르의 평균 인기도 확인\n- 전체 장르 간 인기도 비교 순위 제공")
        
    with col2:
        st.success("### 2️⃣ 발전발전\n**국가별 성장 트렌드**\n- 특정 국가 선택 가능\n- 2020년~2025년 K-콘텐츠 인기도 연도별 선그래프")
        
    with col3:
        st.warning("### 3️⃣ 취향취향\n**국가별 장르 취향**\n- 국가별 가장 인기 있는 최애 장르 자동 탑재\n- 해당 장르의 연도별 트렌드 변화 추적")

# ----------------------------------------------------
# 1. 인기인기 페이지
# ----------------------------------------------------
elif menu == "1. 인기인기 (장르별 분석)":
    st.title("🎬 K-콘텐츠 장르별 인기도 분석")

    genres = sorted(df['genre'].unique())
    selected_genre = st.sidebar.selectbox("원하는 장르를 선택하세요", genres, key="genre_box")

    genre_df = df[df['genre'] == selected_genre]
    avg_popularity = genre_df['popularity'].mean()
    
    st.metric(label=f"✨ 선택한 [{selected_genre}] 장르의 평균 인기도 (2020-2025)", value=f"{avg_popularity:.2f}")
    st.markdown("---")

    st.subheader("📊 전체 장르별 평균 인기도 비교")
    total_genre_popularity = df.groupby('genre')['popularity'].mean().reset_index().sort_values(by='popularity', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='popularity', y='genre', data=total_genre_popularity, palette='viridis', ax=ax)
    st.pyplot(fig)

# ----------------------------------------------------
# 2. 발전발전 페이지
# ----------------------------------------------------
elif menu == "2. 발전발전 (국가별 트렌드)":
    st.title("📈 국가별 K-콘텐츠 발전 트렌드")

    countries = sorted(df['country'].unique())
    selected_country = st.sidebar.selectbox("국가를 선택하세요", countries, key="country_box_1")

    country_df = df[df['country'] == selected_country]
    yearly_popularity = country_df.groupby('year')['popularity'].mean().reset_index()

    st.subheader(f"🌍 {selected_country}의 연도별 K-콘텐츠 인기도 변화")
    if not yearly_popularity.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='year', y='popularity', data=yearly_popularity, marker='o', color='b', linewidth=2, ax=ax)
        ax.set_xticks(yearly_popularity['year'].unique())
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    else:
        st.warning("데이터가 부족합니다.")

# ----------------------------------------------------
# 3. 취향취향 페이지
# ----------------------------------------------------
elif menu == "3. 취향취향 (국가별 선호도)":
    st.title("❤️ 국가별 장르 취향 및 변화 분석")

    countries = sorted(df['country'].unique())
    selected_country = st.sidebar.selectbox("국가를 선택하세요", countries, key="country_box_2")

    country_df = df[df['country'] == selected_country]

    if not country_df.empty:
        favorite_genre = country_df.groupby('genre')['popularity'].mean().idxmax()
        max_val = country_df.groupby('genre')['popularity'].mean().max()
        
        st.success(f"👑 {selected_country}에서 가장 인기 있는 장르는 **[{favorite_genre}]** 입니다! (평균 인기도: {max_val:.2f})")
        st.markdown("---")
        
        st.subheader(f"📈 {selected_country} 내 [{favorite_genre}] 장르의 연도별 인기도 변화")
        fav_genre_df = country_df[country_df['genre'] == favorite_genre].sort_values(by='year')
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='year', y='popularity', data=fav_genre_df, marker='s', color='darkorange', linewidth=2, ax=ax)
        ax.set_xticks(fav_genre_df['year'].unique())
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    else:
        st.warning("데이터가 없습니다.")
