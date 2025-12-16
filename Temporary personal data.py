import pandas as pd
import random
import re
from faker import Faker
from datetime import datetime

# Faker 한국어 설정 초기화
fake = Faker('ko_KR')

# --- 주요 함수 및 데이터 리스트 준비 ---

# 주민등록번호 생성 함수 (생년월일 + 성별 반영)
def generate_korean_jumin_no(birth_date: datetime, gender: str) -> str:
    year_str = str(birth_date.year)[2:]
    month_str = birth_date.month
    day_str = birth_date.day
    front_part = f"{year_str}{month_str:02d}{day_str:02d}"

    # 성별 코드 로직
    if gender == 'M':
        gender_code = '1' if birth_date.year < 2000 else '3'
    else: # gender == 'F'
        gender_code = '2' if birth_date.year < 2000 else '4'

    back_part_tail = fake.numerify('######') # 뒷자리 랜덤 6자리
    return f"{front_part}-{gender_code}{back_part_tail}"

# 이름 리스트 (20~30대 남녀 14개씩)
male_names = ['도윤', '서준', '하준', '은우', '시우', '지호', '예준', '유준', '준우', '민준', '건우', '정우', '주원', '승우']
female_names = ['지아', '서아', '하윤', '서윤', '하은', '지유', '윤슬', '아윤', '수아', '시아', '예원', '아린', '나율', '채원']

# 은행명 및 계좌번호 패턴
banks = ["농협", "국민", "신한", "우리", "하나", "SC제일", "카카오"]
bank_account_formats = {
    "농협": '###-####-####-###',
    "국민": '######-##-######',
    "신한": '###-###-######',
    "우리": '###-###-######',
    "하나": '###-######-#####',
    "SC제일": '###-##-######',
    "카카오": '####-##-#######'
}

# 전화번호 생성 (010-####-####)
def generate_phone_number():
    return f"010-{random.randint(0,9999):04d}-{random.randint(0,9999):04d}"

# 은행계좌 번호 생성
def generate_bank_account():
    bank = random.choice(banks)
    pattern = bank_account_formats[bank]
    num = fake.numerify(pattern)
    return f"{bank} {num}"

# --- 남성/여성 데이터 생성 ---
customers = []

# 남성 50명 생성
for _ in range(50):
    age = random.randint(20, 30)
    birth_year = datetime.now().year - age
    birth_date = datetime(birth_year, random.randint(1,12), random.randint(1,28))
    name = fake.last_name() + random.choice(male_names) # 성 + 이름
    jumin_no = generate_korean_jumin_no(birth_date, 'M')
    phone = generate_phone_number()
    email = f"{fake.user_name()}@{random.choice(['gmail.com', 'naver.com', 'daum.net'])}"
    bank_account = generate_bank_account()
    address_raw = fake.address()
    # 주소 정규화 (예: '서울특별시 중구' 또는 '부산광역시 부산진구')
    addr_parts = address_raw.split()
    address = ' '.join(addr_parts[:3]) if re.search(r'[시군구]$', ' '.join(addr_parts[:3])) else ' '.join(addr_parts[:2])

    customers.append({
        "이름": name,
        "주소": address,
        "전화번호": phone,
        "이메일": email,
        "나이": age,
        "성별": '남',
        "주민등록번호": jumin_no,
        "은행계좌": bank_account
    })

# 여성 50명 생성
for _ in range(50):
    age = random.randint(20, 30)
    birth_year = datetime.now().year - age
    birth_date = datetime(birth_year, random.randint(1,12), random.randint(1,28))
    name = fake.last_name() + random.choice(female_names) # 성 + 이름
    jumin_no = generate_korean_jumin_no(birth_date, 'F')
    phone = generate_phone_number()
    email = f"{fake.user_name()}@{random.choice(['gmail.com', 'naver.com', 'daum.net'])}"
    bank_account = generate_bank_account()
    address_raw = fake.address()
    # 주소 정규화 (예: '서울특별시 중구' 또는 '부산광역시 부산진구')
    addr_parts = address_raw.split()
    address = ' '.join(addr_parts[:3]) if re.search(r'[시군구]$', ' '.join(addr_parts[:3])) else ' '.join(addr_parts[:2])

    customers.append({
        "이름": name,
        "주소": address,
        "전화번호": phone,
        "이메일": email,
        "나이": age,
        "성별": '여',
        "주민등록번호": jumin_no,
        "은행계좌": bank_account
    })

# --- DataFrame 변환 및 CSV 저장 ---
df_customers = pd.DataFrame(customers)
df_customers.to_csv('Temporary personal data.csv', index=False, encoding='utf-8-sig')

# --- 생성 완료 메시지 + 샘플 출력 ---
print("총 100명의 초강력 가짜 고객 데이터가 'Temporary personal data.csv' 파일로 생성됐어요!")
print(df_customers.head())