import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 여덟 자리 문자열에서 datetime 타입으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    return df

df = load_data()

# 제목
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("시간 흐름에 따른 박스오피스 데이터를 분석하는 대시보드입니다.")
st.divider()

# ==========================================
# 구역 1: 영화별 날짜별 일관객 변화
# ==========================================
st.header("📌 구역 1: 영화별 일일 관객수 변화")

# 영화 목록 추출 (총 관객수 기준 내림차순 정렬)
movie_list = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()

selected_movie = st.selectbox(
    "데이터를 확인할 영화를 고르세요:",
    options=movie_list,
    index=0
)

# 선택한 영화로 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # 플롯리 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"[{selected_movie}] 날짜별 일관객 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True
    )

    # 마우스 오버(호버) 시 날짜와 관객수 표시
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>",
        line=dict(width=2.5)
    )
    
    fig1.update_layout(hovermode="x unified")

    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 아래 설명 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** ")
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

st.divider()

# ==========================================
# 구역 2: 상위 5개 영화 비교
# ==========================================
st.header("📌 구역 2: 누적 관객수 상위 5개 영화 일관객 비교")

# 일관객 합계가 가장 큰 상위 5개 영화 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# 상위 5개 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

if not top5_df.empty:
    # 플롯리 선 그래프 생성 (color 파라미터로 영화 구분)
    fig2 = px.line(
        top5_df,
        x='날짜',
        y='일관객',
        color='영화명',
        title="총 관객수 상위 5개 영화의 날짜별 일관객 추이",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)', '영화명': '영화명'},
        markers=True
    )

    # 마우스 오버(호버) 시 날짜와 관객수 표시
    fig2.update_traces(
        line=dict(width=2.5)
    )
    
    # hovertemplate을 각 영화명과 함께 나오도록 설정
    fig2.update_layout(
        hovermode="x unified",
        legend_title_text='영화명 (클릭하여 켜기/끄기)'
    )

    # 그래프 출력
    st.plotly_chart(fig2, use_container_width=True)

    # 그래프 아래 설명 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** ")
else:
    st.warning("데이터가 없습니다.")

st.divider()

# ==========================================
# 구역 3: 날짜별 10위권 일관객 합계 (영역 그래프)
# ==========================================
st.header("📌 구역 3: 날짜별 10위권 일관객 합계")

# 날짜별로 일관객 합계 계산
daily_total = df.groupby('날짜', as_index=False)['일관객'].sum()

if not daily_total.empty:
    # 플롯리 영역 그래프 생성
    fig3 = px.area(
        daily_total,
        x='날짜',
        y='일관객',
        title="날짜별 10위권 일관객 총합 추이",
        labels={'날짜': '날짜', '일관객': '총 일관객 수(명)'}
    )
    
    # 합계가 가장 컸던 날 3일 추출
    top3_days = daily_total.nlargest(3, '일관객')
    
    # 상위 3일에 어노테이션(텍스트와 화살표) 추가
    for _, row in top3_days.iterrows():
        fig3.add_annotation(
            x=row['날짜'],
            y=row['일관객'],
            text=row['날짜'].strftime('%Y-%m-%d'),  # 날짜를 문자열로 표시
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            ax=0,
            ay=-40  # 텍스트를 위로 조금 띄워서 표시
        )

    # 마우스 오버(호버) 시 날짜와 총 관객수 표시
    fig3.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>총 일관객:</b> %{y:,}명<extra></extra>"
    )
    
    fig3.update_layout(hovermode="x unified")

    # 그래프 출력
    st.plotly_chart(fig3, use_container_width=True)

    # 그래프 아래 설명 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** ")
else:
    st.warning("데이터가 없습니다.")

st.divider()

# ==========================================
# 구역 4: 총 관객수 TOP 10 영화 (가로 막대그래프)
# ==========================================
st.header("📌 구역 4: 총 관객수 TOP 10 영화")

# 영화별 총 관객수와 10위권 진입 일수(데이터에 등장한 횟수) 계산
movie_stats = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    진입일수=('날짜', 'count')
).reset_index()

# 총 관객수 기준 상위 10개 추출 
# (플롯리 가로 막대그래프에서 값이 큰 항목이 위로 가도록 하려면 오름차순으로 정렬해야 함)
top10_movies = movie_stats.nlargest(10, '총관객수').sort_values('총관객수', ascending=True)

if not top10_movies.empty:
    # 플롯리 가로 막대그래프 생성
    fig4 = px.bar(
        top10_movies,
        x='총관객수',
        y='영화명',
        orientation='h',
        title="기간 내 총 관객수 TOP 10 영화",
        labels={'총관객수': '총 관객 수(명)', '영화명': '영화명'},
        custom_data=['진입일수'] # 호버에 표시할 추가 데이터
    )
    
    # 마우스 오버(호버) 시 총 관객수와 10위권 진입 일수 표시
    fig4.update_traces(
        hovertemplate="<b>%{y}</b><br>총 관객수: %{x:,}명<br>10위권 진입 일수: %{customdata[0]}일<extra></extra>"
    )

    # 그래프 출력
    st.plotly_chart(fig4, use_container_width=True)

    # 그래프 아래 설명 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** ")
else:
    st.warning("데이터가 없습니다.")

st.divider()

# ==========================================
# 구역 5: 추가 그래프 영역
# ==========================================
st.header("📌 구역 5: (새로운 그래프가 추가될 자리)")
st.caption("앞으로 추가될 그래프들은 이 아래로 구역을 나누어 배치됩니다.")
