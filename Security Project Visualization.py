import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 1. 시뮬레이션 결과 데이터 (가정치이며, 실제 시뮬레이션 결과에 맞춰 수정해야 합니다!)
# 이 데이터는 복호화 시나리오 세 가지를 나타냅니다: 1. 정상 복호화, 2. 랜덤 데이터 손상, 3. 인증키 제거.
total_records = 100
scenarios_data = {
    "Scenario": ["1. Normal Decryption", "2. Random Corruption", "3. Key Removal"],
    "Attempted Records": [total_records, total_records, total_records],
    "Successfully Decrypted": [total_records, total_records - 50, 0], # 시나리오 2에서는 50개 실패로 가정
    "Decryption Failure": [0, 50, total_records] # 시나리오 2에서는 50개 실패로 가정
}
df_scenarios = pd.DataFrame(scenarios_data)

# --- 폰트 설정 (영어 전용) ---
# 한글 폰트를 강제하지 않고, Matplotlib의 기본 영문 폰트 (예: sans-serif)를 사용하도록 설정합니다.
plt.rcParams['font.family'] = 'sans-serif'  # 일반적인 영문 폰트 계열 사용
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호가 깨지는 것을 방지하는 설정입니다.

# 두 개의 서브플롯을 위한 Figure를 생성합니다.
fig, axes = plt.subplots(1, 2, figsize=(30, 15)) # 포트폴리오 프레젠테이션에 적합하게 크기 조정

# --- 서브플롯 1: 시나리오별 복호화 결과 누적 막대 그래프 ---
# 각 시나리오별 성공적으로 복호화된 레코드 수와 복호화 실패 레코드 수를 표시합니다.
sns.barplot(x="Scenario", y="Successfully Decrypted", data=df_scenarios, color='skyblue', label='Successfully Decrypted', ax=axes[0])
sns.barplot(x="Scenario", y="Decryption Failure", data=df_scenarios, color='salmon', bottom=df_scenarios["Successfully Decrypted"], label='Decryption Failure', ax=axes[0])

# 첫 번째 서브플롯의 제목 및 라벨을 설정합니다.
axes[0].set_title("Decryption Results per Scenario (Stacked Bar)", fontsize=35, fontweight='bold') # 제목 폰트 크기 및 두께 조정
axes[0].set_ylabel("Number\nof\nRecords", fontsize=30, rotation=0, ha='center', va='center', labelpad=45) # Y축 라벨 '두 줄' + 패딩 추가
axes[0].set_xlabel("", fontsize=0) # X축 라벨 텍스트를 삭제합니다. (이미지에 라벨이 필요 없으므로)
axes[0].set_ylim(0, total_records * 1.1) # Y축의 상한선을 설정하여 그래프 상단에 여백을 둡니다.
axes[0].tick_params(axis='x', rotation=15, labelsize=25) # X축 틱 라벨을 15도 회전하고 폰트 크기를 조정합니다.
axes[0].tick_params(axis='y', labelsize=25) # Y축 틱 라벨의 폰트 크기를 조정합니다.
axes[0].legend(loc='upper right', fontsize=20) # 범례 크기 줄임!

# 각 막대 세그먼트 위에 값을 표시하여 세부적인 인사이트를 제공합니다.
for idx, row in df_scenarios.iterrows():
    if row["Successfully Decrypted"] > 0:
        axes[0].text(idx, row["Successfully Decrypted"] / 2, str(row["Successfully Decrypted"]),
                     fontsize=22, fontweight='bold', color='black', ha='center', va='center') # 성공 수치 텍스트 표시
    if row["Decryption Failure"] > 0:
        axes[0].text(idx, row["Successfully Decrypted"] + row["Decryption Failure"] / 2, str(row["Decryption Failure"]),
                     fontsize=22, fontweight='bold', color='white', ha='center', va='center') # 실패 수치 텍스트 표시


# --- 서브플롯 2: 복호화 성공률 추이 선 그래프 ---
# 시도된 총 레코드 대비 성공적으로 복호화된 레코드 비율로 성공률을 계산합니다.
df_scenarios['Success_Rate'] = df_scenarios['Successfully Decrypted'] / df_scenarios['Attempted Records'] * 100

sns.lineplot(
    x="Scenario", y="Success_Rate", data=df_scenarios,
    marker='o', color='purple', linewidth=3, ax=axes[1],
    label='Success Rate Trend'
)

# 두 번째 서브플롯의 제목 및 라벨을 설정합니다.
axes[1].set_title("Decryption Success Rate Trend per Scenario", fontsize=35, fontweight='bold') # 제목 폰트 크기 및 두께 조정
axes[1].set_ylabel("Success\nRate\n(%)", fontsize=30, rotation=0, ha='center', va='center', labelpad=45) # Y축 라벨 '두 줄' + 패딩 추가
axes[1].set_xlabel("", fontsize=0) # X축 라벨 텍스트 삭제 (너의 지시대로!)
axes[1].set_ylim(-5, 105) # Y축 범위를 0-100%와 약간의 여백을 포함하여 설정합니다.
axes[1].grid(True, linestyle='--', alpha=0.6) # 가독성을 높이기 위해 격자를 추가합니다.
axes[1].tick_params(axis='x', rotation=15, labelsize=25) # X축 틱 라벨을 15도 회전하고 폰트 크기를 조정합니다.
axes[1].tick_params(axis='y', labelsize=25) # Y축 틱 라벨의 폰트 크기를 조정합니다.
axes[1].legend(loc='upper right', fontsize=20) # 범례 크기 줄임!

# 선 그래프의 각 지점 위에 성공률 퍼센티지를 표시합니다.
for idx, row in df_scenarios.iterrows():
    axes[1].text(idx + 0.08, row["Success_Rate"], f"{row['Success_Rate']:.0f}%", # X 위치 살짝 더 밀어내기
                 fontsize=22, color='purple', ha='left', va='center') # 폰트 살짝 줄임

# 모든 서브플롯과 요소들이 겹치지 않도록 레이아웃을 자동으로 조정합니다.
plt.tight_layout()
plt.show() # 포트폴리오용 그래프를 화면에 표시합니다!