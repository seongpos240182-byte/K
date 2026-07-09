import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="K-콘텐츠 트렌드 대시보드",
    page_icon="🎬",
    layout="wide"
)

# 공통 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv('k_contents_trend_data.csv')
    year_cols = [col for col in df.columns if col.startswith('year_')]
    
    df_melted = df.melt(
        id_vars=['country', 'genre'], 
        value_vars=year_cols, 
        var_name='year', 
        value_name='popularity'
    )
    
    df_melted['year'] = df_melted['year'].str.replace('year_', '').astype(int)
    return df_melted

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 읽어오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바 메뉴
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
    본 대시보드는 `k_contents_trend_data.csv` 파일을 기반으로 **전 세계 국가의 K-콘텐츠 인기도 트렌드**를 다각도로 분석합니다.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 1️⃣ 인기인기\n**장르별 인기도 분석**\n- 선택 장르 평균 인기도 확인\n- 전체 장르 인기도 비교 순위")
    with col2:
        st.success("### 2️⃣ 발전발전\n**국가별 성장 트렌드**\n- 국가별 연도별 인기도 선그래프 시각화")
    with col3:
        st.warning("### 3️⃣ 취향취향\n**국가별 장르 취향**\n- 국가별 최애 장르 자동 선정 및 추이 분석")

# ----------------------------------------------------
# 1. 인기인기 페이지 (st.bar_chart 활용)
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
    
    # 데이터 그룹화 및 정렬
    total_genre_popularity = df.groupby('genre')['popularity'].mean().sort_values(ascending=False)
    
    # Streamlit 내장 가로 바 차트 (한글 깨짐 없음)
    st.bar_chart(total_genre_popularity, horizontal=True)

# ----------------------------------------------------
# 2. 발전발전 페이지 (st.line_chart 활용)
# ----------------------------------------------------
elif menu == "2. 발전발전 (국가별 트렌드)":
    st.title("📈 국가별 K-콘텐츠 발전 트렌드")

    countries = sorted(df['country'].unique())
    selected_country = st.sidebar.selectbox("국가를 선택하세요", countries, key="country_box_1")

    country_df = df[df['country'] == selected_country]
    
    # 차트에 넣기 좋게 인덱스를 year로 설정
    yearly_popularity = country_df.groupby('year')['popularity'].mean()

    st.subheader(f"🌍 {selected_country}의 연도별 K-콘텐츠 인기도 변화")
    if not yearly_popularity.empty:
        # Streamlit 내장 선 그래프 (한글 깨짐 없음, x축 연도 지정)
        st.line_chart(yearly_popularity)
    else:
        st.warning("데이터가 부족합니다.")

# ----------------------------------------------------
# 3. 취향취향 페이지 (st.line_chart 활용)
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
        
        # 선호 장르 데이터 추출 및 차트 포맷팅
        fav_genre_df = country_df[country_df['genre'] == favorite_genre].set_index('year')['popularity']
        
        # Streamlit 내장 선 그래프
        st.line_chart(fav_genre_df)
    else:
        st.warning("데이터가 없습니다.")
