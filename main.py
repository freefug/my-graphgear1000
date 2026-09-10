import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 진짜 datetime 타입으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 변환
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 및 관련 지표 변화를 탐색합니다.")
st.divider()

# ==========================================
# 구역 1: 특정 영화의 날짜별 일관객 변화
# ==========================================
st.header("📌 구역 1. 영화별 날짜별 일관객 변화")

# 영화 목록 추출 (관객 수 많은 순 정렬)
movie_list = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()

selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    options=movie_list,
    index=0
)

# 선택한 영화 데이터 필터링
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

    # 마우스 오버(호버) 스타일 설정
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

    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 아래 문구 자리 (설명 지움)
    st.info("💡 **이 그래프로 알 수 있는 것:** ")
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

st.divider()

# ==========================================
# 구역 2: 추가 그래프 영역
# ==========================================
st.header("📌 구역 2. 추가 그래프 영역 (추후 확장용)")
st.caption("앞으로 시간 흐름 관련 추가 그래프가 이곳에 추가될 예정입니다.")
