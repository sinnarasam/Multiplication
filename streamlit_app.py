import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="곱셈 학습 앱", layout="wide")

st.title("🧮 초등학교 곱셈 학습 앱")
st.write("두 개의 숫자를 입력하고 시각화를 통해 곱셈을 학습해보세요!")

# 세션 상태 초기화
if 'result_checked' not in st.session_state:
    st.session_state.result_checked = False
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = False

# 사이드바에서 입력받기
st.sidebar.header("📝 입력")

num1 = st.sidebar.number_input("첫 번째 숫자를 입력하세요", min_value=1, max_value=12, value=3, step=1)
num2 = st.sidebar.number_input("두 번째 숫자를 입력하세요", min_value=1, max_value=12, value=4, step=1)

visualization_type = st.sidebar.selectbox(
    "시각화 방법을 선택하세요",
    ["⭕ 동그라미", "⬜ 사각형", "🟩 색칠된 칸", "🎨 무지개 칸", "🍪 이미지(캐릭터/음식)"]
)

# 이미지 카테고리 선택 (이미지 옵션 선택 시)
image_category = None
if visualization_type == "🍪 이미지(캐릭터/음식)":
    image_category = st.sidebar.selectbox("이미지 종류를 선택하세요", ["음식", "캐릭터"]) 
    # 내부 키값
    image_category = "food" if image_category == "음식" else "character"

# 시각화 함수들
def visualize_circles(num1, num2):
    """동그라미로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))
    circle_size = 300
    
    for i in range(num1):
        for j in range(num2):
            circle = plt.Circle((j + 1, num1 - i), 0.4, color='skyblue', ec='navy', linewidth=2)
            ax.add_patch(circle)
    
    ax.set_xlim(0, num2 + 1)
    ax.set_ylim(0, num1 + 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig

def visualize_squares(num1, num2):
    """사각형으로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for i in range(num1):
        for j in range(num2):
            rect = patches.Rectangle((j, num1 - i - 1), 0.8, 0.8, 
                                     linewidth=2, edgecolor='darkblue', 
                                     facecolor='lightblue', alpha=0.7)
            ax.add_patch(rect)
    
    ax.set_xlim(-0.5, num2 + 0.5)
    ax.set_ylim(-0.5, num1 + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig

def visualize_colored_grid(num1, num2):
    """색칠된 칸으로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    for i in range(num1):
        for j in range(num2):
            color = colors[(i + j) % len(colors)]
            rect = patches.Rectangle((j, num1 - i - 1), 0.9, 0.9, 
                                     linewidth=2, edgecolor='black', 
                                     facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            # 숫자 표시
            ax.text(j + 0.45, num1 - i - 0.55, str(i*num2 + j + 1), 
                   ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-0.5, num2 + 0.5)
    ax.set_ylim(-0.5, num1 + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig

def visualize_rainbow_grid(num1, num2):
    """무지개 칸으로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 무지개 색상
    colors_rainbow = plt.cm.rainbow(np.linspace(0, 1, max(num1, num2)))
    
    for i in range(num1):
        for j in range(num2):
            hue = (i / num1 + j / num2) / 2
            color = plt.cm.hsv(hue)
            rect = patches.Rectangle((j, num1 - i - 1), 0.9, 0.9, 
                                     linewidth=2, edgecolor='white', 
                                     facecolor=color, alpha=0.9)
            ax.add_patch(rect)
    
    ax.set_xlim(-0.5, num2 + 0.5)
    ax.set_ylim(-0.5, num1 + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig


# 이미지 로드 캐시
@st.cache_data
def load_image_from_url(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGBA")


def visualize_images(num1, num2, category="food"):
    """이미지(캐릭터/음식)로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # 트위모지 CDN에서 간단한 이모지 이미지를 사용
    emoji_sets = {
        "food": [
            "https://twemoji.maxcdn.com/v/latest/72x72/1f355.png",  # pizza
            "https://twemoji.maxcdn.com/v/latest/72x72/1f354.png",  # burger
            "https://twemoji.maxcdn.com/v/latest/72x72/1f35f.png",  # fries
            "https://twemoji.maxcdn.com/v/latest/72x72/1f34e.png",  # apple
        ],
        "character": [
            "https://twemoji.maxcdn.com/v/latest/72x72/1f431.png",  # cat
            "https://twemoji.maxcdn.com/v/latest/72x72/1f436.png",  # dog
            "https://twemoji.maxcdn.com/v/latest/72x72/1f60a.png",  # smiling face
            "https://twemoji.maxcdn.com/v/latest/72x72/1f47b.png",  # ghost (cute)
        ]
    }

    urls = emoji_sets.get(category, emoji_sets["food"])

    # 미리 로드
    images = [load_image_from_url(u) for u in urls]

    for i in range(num1):
        for j in range(num2):
            img = images[(i * num2 + j) % len(images)]
            # 이미지 크기와 위치를 맞춰 그리기
            extent = (j, j + 0.9, num1 - i - 1, num1 - i - 1 + 0.9)
            ax.imshow(img, extent=extent, aspect='auto')

    ax.set_xlim(-0.5, num2 + 0.5)
    ax.set_ylim(-0.5, num1 + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig

# 메인 콘텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 시각화")
    
    if visualization_type == "⭕ 동그라미":
        fig = visualize_circles(int(num1), int(num2))
    elif visualization_type == "⬜ 사각형":
        fig = visualize_squares(int(num1), int(num2))
    elif visualization_type == "🟩 색칠된 칸":
        fig = visualize_colored_grid(int(num1), int(num2))
    elif visualization_type == "🎨 무지개 칸":
        fig = visualize_rainbow_grid(int(num1), int(num2))
    else:  # 🍪 이미지(캐릭터/음식)
        fig = visualize_images(int(num1), int(num2), category=image_category or "food")
    
    st.pyplot(fig)

with col2:
    st.header("🧠 문제 풀기")
    
    correct_answer = int(num1) * int(num2)
    
    st.info(f"**문제:** {num1} × {num2} = ?")
    st.write(f"위의 그림을 세어보고 답을 입력해보세요!")
    
    user_answer = st.number_input(
        "답을 입력하세요",
        min_value=0,
        max_value=144,
        value=0,
        step=1,
        key="user_answer_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ 정답 확인", use_container_width=True):
            st.session_state.result_checked = True
            st.session_state.is_correct = (user_answer == correct_answer)
    
    with col_btn2:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.result_checked = False
            st.session_state.is_correct = False
            st.rerun()
    
    # 결과 표시
    if st.session_state.result_checked:
        if st.session_state.is_correct:
            st.success(f"🎉 정답입니다! {num1} × {num2} = {correct_answer}")
            st.balloons()
        else:
            st.error(f"❌ 틀렸습니다. 정답은 {correct_answer}입니다. (입력값: {user_answer})")
            st.write(f"다시 한 번 세어보고 도전해보세요! 💪")

# 하단 팁
st.divider()
st.write("**💡 팁:** 시각화를 보면서 각 줄의 개수와 줄의 수를 세어보세요!")
st.write("곱셈은 같은 크기의 그룹이 몇 개인지 세는 것과 같습니다.")
