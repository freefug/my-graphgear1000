import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리 (st.cache_data 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 여덟 자리 숫자로 된 날짜 열을 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 보정
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

df = load_data()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 및 관련 지표 변화를 탐색합니다.")
st.divider()

# ==========================================
# 구역 1: 특정 영화의 날짜별 일관객 변화
# ==========================================
st.header("📌 구역 1. 영화별 날짜별 일관객 변화")

# 드롭다운 선택 메뉴 (관객 수 많은 순으로 정렬)
movie_list = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("조회할 영화를 선택하세요:", options=movie_list, index=0)

# 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객 수 추이",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True
    )

    # 마우스 오버 시 날짜 및 관객 수 표시 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>",
        line=dict(width=2.5)
    )

    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # '이 그래프로 알 수 있는 것' 안내 문구
    st.info(f"💡 **이 그래프로 알 수 있는 것:** '{selected_movie}'인기가 많다.")

st.divider()

# ==========================================
# 구역 2: 추후 그래프 추가 구역
# ==========================================
st.header("📌 구역 2. 추가 그래프 영역 (추후 확장용)")
st.caption("앞으로 시간 흐름 관련 추가 그래프가 이곳에 시각화될 예정입니다.")
