import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 날짜 데이터에서 월과 요일 추출
df['날짜'] = pd.to_datetime(df['날짜'])
df['월'] = df['날짜'].dt.month

# 한국어 요일 추출 ('월요일', '화요일' 등)
df['요일'] = df['날짜'].dt.day_name(locale='ko_KR.utf8') 
# 운영체제 환경에 따라 locale='ko_KR' 이나 일반 dt.day_name() 후 영문 요일을 사용해야 할 수 있습니다.

# 2. 월 × 요일별 일관객 합계 피벗 데이터 생성
pivot_df = df.pivot_table(index='월', columns='요일', values='일관객', aggfunc='sum')

# 3. 요일 순서를 월요일~일요일로 강제 정렬
day_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
# 영문일 경우: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_df = pivot_df.reindex(columns=day_order)

# 4. 히트맵 시각화
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_df, 
            cmap='Blues',       # 관객이 많을수록 진한 파란색으로 표시 (Reds, YlGnBu 등 사용 가능)
            annot=True,         # 셀에 실제 값 표시 여부
            fmt='.0f',          # 값을 소수점 없는 정수로 표시
            linewidths=0.5)     # 셀 사이 경계선

plt.title('월 및 요일별 일관객 합계 히트맵')
plt.xlabel('요일')
plt.ylabel('월')
plt.show()
