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
