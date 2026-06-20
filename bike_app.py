# bike_app.py
"""자전거 취미 웹 앱 (Streamlit)
이 파일을 실행하면 자전거 타기의 장점, 칼로리 소모량, 경사·바람 시뮬레이션, 사진·영상 갤러리 등을 확인할 수 있습니다.
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
# Define assets directory early for later use
PHOTO_DIR = Path(__file__).parent / "자전거 풍경 사진"
VIDEO_PATH = Path(__file__).parent / "intro_video.mp4"
LOG_PATH = Path(__file__).parent / "goal_log.csv"

# ---- 기본 설정 --------------------------------------------------------------
st.set_page_config(page_title="내 자전거 취미", layout="wide")



# ---- 스타일 ---------------------------------------------------------------
st.markdown(
    """
    <style>
    body {background-color: #2E3A59; color: #FFFFFF; font-family: 'Inter', sans-serif;}
    .stButton>button {background-color:#FFB400; color:#2E3A59; border-radius:8px;}
    .stSidebar {background-color:#1F2A3C;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- 이미지/동영상 폴더 -----------------------------------------------------


# ---- 1️⃣ 소개 및 영상 --------------------------------------------------------
st.title("🚴‍♂️ 나의 자전거 취미")
st.subheader("자전거는 몸과 마음을 동시에 힐링시키는 최고의 유산소 운동입니다.")
st.markdown('<div style="text-align: right; font-weight: bold;">c431317 이민석</div>', unsafe_allow_html=True)
if VIDEO_PATH.exists():
    st.video(str(VIDEO_PATH))

# ---- 2️⃣ 자전거와 다른 운동 비교 -------------------------------------------
st.header("📊 자전거 vs. 다른 유산소 운동")
compare_df = pd.DataFrame(
    {
        "운동": ["걷기", "조깅", "수영", "실내 자전거", "자전거 타기"],
        "30분당 칼로리(kcal)": [120, 250, 210, 300, 340],
        "근육 사용 부위": ["하체(대퇴사두·종아리)", "하체+코어", "전신(어깨·등·다리)", "하체", "하체+코어"],
        "부상 위험 (설명)": [
            "효율 낮음, 큰 효과 적음",
            "무릎·골반 통증 가능",
            "수영장 이용 필요",
            "낮음",
            "낮음, 장시간 지속 가능"
        ]
    }
)
st.dataframe(compare_df)
# 바 차트
chart = alt.Chart(compare_df).mark_bar().encode(
    x=alt.X("운동", sort="-y"),
    y="30분당 칼로리(kcal)",
    color="운동",
)
st.altair_chart(chart, use_container_width=True)

# ---- 3️⃣ 칼로리 시뮬레이터 (경사·바람) -------------------------------
st.header("🧮 칼로리 계산기 – 경사·바람 고려")
weight = st.slider("몸무게 (kg)", 40, 120, 70)
# 평균 속도 (km/h)
speed = st.slider("평균 속도 (km/h)", 5, 35, 20)
# 경사도 %
gradient = st.slider("경사도 (%)", 0, 15, 0)
# 바람 속도 (km/h, 머리 방향 양수, 뒷쪽 음수)
wind = st.slider("바람 속도 (km/h)", -20, 20, 0)
time_min = st.slider("운동 시간 (분)", 10, 120, 30)

# MET 값 보정: 기본 7.5, 경사·바람에 따라 가중치 조정
base_met = 7.5
met = base_met * (1 + gradient / 100) * (1 - wind / 30)
calories = met * weight * (time_min / 60)
st.metric(label="예상 칼로리 소모량 (kcal)", value=f"{calories:.0f}")

# ---- 4️⃣ 자전거 타기의 추가 장점 ------------------------------------------
st.header("🌟 자전거만의 장점")
st.markdown(
    """
    - **풍경 감상**: 자연을 보며 장시간 탈 수 있어 정신적 힐링 효과가 큽니다.
    - **진입 장벽 낮음**: 별도의 장비·복장이 거의 필요 없으며, 언제 어디서든 탈 수 있습니다.
    - **전신 운동**: 하체·코어·상체를 고루 쓰면서도 관절에 무리 없이 지속 가능.
    - **환경·경제 효율**: 자동차 대비 탄소 배출량 90% 감소, 연간 교통비 절감.
    - **장시간 지속**: 힘들지 않게 오래 탈 수 있습니다.
    """
)

# ---- 5️⃣ 사진 갤러리 -------------------------------------------------------
st.header("📸 내 라이딩 사진 갤러리")
if PHOTO_DIR.exists():
    img_files = [f for f in PHOTO_DIR.iterdir() if f.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    if img_files:
        # 파일명 → 캡션 매핑 (사용자가 정의한 설명)
        captions = {
            "풍경2.jpg": "한강에서 라이딩 후 찍은 사진",
            "풍경3.jpg": "섬바위 마을까지 라이딩 후 찍은 사진",
            "풍경4.jpg": "양재천 라이딩 중 찍은 사진",
            "풍경5.jpg": "양재천 라이딩 중 찍은 사진",
            "풍경10.jpg": "양재천 라이딩 중 찍은 사진",
            "풍경11.jpg": "야간 라이딩 중 찍은 사진",
            "풍경12.jpg": "야간 라이딩 중 찍은 사진",
            "풍경6.jpg": "과천까지 라이딩 중 찍은 사진",
            "풍경7.jpg": "과천까지 라이딩 중 찍은 사진",
            "풍경8.jpg": "과천까지 라이딩 중 찍은 사진",
        }
        cols = st.columns(3)
        for idx, img_path in enumerate(img_files):
            with cols[idx % 3]:
                img = Image.open(img_path)
                # EXIF 메타데이터에 따라 자동 회전
                img = ImageOps.exif_transpose(img)
                caption = captions.get(img_path.name, img_path.stem)
                st.image(img, caption=caption, width=250)
    else:
        st.info("자전거 풍경 사진 폴더에 사진이 없습니다. 사진을 추가해 주세요.")
else:
    st.info("‘자전거 풍경 사진’ 폴더가 존재하지 않습니다. 폴더를 만들고 사진을 넣어 주세요.")

# ---- 6️⃣ 목표 트래커 ------------------------------------------------------
st.header("🎯 오늘의 라이딩 목표")
st.caption("목표 달성 시 아래 버튼을 누르세요.")
today_str = datetime.now().date().isoformat()
# 30분 완료 버튼
if st.button("30분 타기 완료!", key="minute_button"):
    st.success("멋집니다! 지속적인 라이딩을 응원합니다.")
    df = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame(columns=["date","status"])
    df = df[df["date"] != today_str]
    df = pd.concat([df, pd.DataFrame([{"date": today_str, "status": "Success"}])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)

# 1시간 완료 버튼
if st.button("1시간 타기 완료!", key="hour_button"):
    st.success("대단해요! 1시간 목표 달성!")
    df = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame(columns=["date","status"])
    df = df[df["date"] != today_str]
    df = pd.concat([df, pd.DataFrame([{"date": today_str, "status": "Success"}])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)

# 2시간 완료 버튼
if st.button("2시간 타기 완료!", key="twohour_button"):
    st.success("멋져요! 2시간 목표 달성!")
    df = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame(columns=["date", "status"])
    df = df[df["date"] != today_str]
    df = pd.concat([df, pd.DataFrame([{"date": today_str, "status": "Success"}])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)

# 그 이상 완료 버튼
if st.button("그 이상 타기 완료!", key="beyond_button"):
    st.success("대단합니다! 목표 초과 달성!")
    df = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame(columns=["date", "status"])
    df = df[df["date"] != today_str]
    df = pd.concat([df, pd.DataFrame([{"date": today_str, "status": "Success"}])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)


# ---- 7️⃣ 마무리 ------------------------------------------------------------
st.caption("이 웹 앱은 Streamlit 로 제작되었으며, 바이브 코딩 과제 제출용으로 설계되었습니다.")
