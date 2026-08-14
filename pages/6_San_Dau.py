"""Sàn đấu toán học: trả lời 5 câu hỏi trong 30 giây để tích điểm rank."""

import time

import streamlit as st
import streamlit.components.v1 as components

from src.api_client import post_action
from src.auth import get_username, require_login

st.set_page_config(page_title="Sàn Đấu Toán Học", page_icon="⚔️")

require_login()

st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
st.markdown("---")

#: Giới hạn thời gian làm bài (giây).
QUIZ_TIME_SECONDS = 30
#: Số câu hỏi mỗi trận.
QUESTIONS_PER_MATCH = 5
#: Điểm thưởng cho mỗi câu trả lời đúng.
POINTS_PER_CORRECT = 10

player_name = get_username() or "Cao thủ ẩn danh"

st.title("⚔️ Sàn Đấu Toán Học")
st.markdown(f"Chào mừng **{player_name}** đến với đấu trường trí tuệ!")

# --- Khởi tạo bộ nhớ phiên (session state) cho trận đấu ---
match_defaults: dict = {
    "questions": [],
    "current_q": 0,
    "score": 0,
    "is_playing": False,
    "start_time": None,
    "match_ended": False,
    "total_score": 0,
}
for key, value in match_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def get_rank_name(score: int) -> str:
    """Quy đổi tổng điểm tích lũy thành danh hiệu rank."""
    if score <= 100:
        return "🥉 Tân binh (Rank Đồng)"
    if score <= 300:
        return "🥈 Học giả (Rank Bạc)"
    if score <= 600:
        return "🥇 Tinh anh (Rank Vàng)"
    return "💎 Thách đấu (Rank Kim Cương)"


def fetch_questions() -> None:
    """Lấy bộ câu hỏi mới từ backend và bắt đầu trận đấu."""
    with st.spinner("Đang xáo trộn đề..."):
        res = post_action("get_match_questions", limit=QUESTIONS_PER_MATCH)

    if res and res.get("status") == "success":
        st.session_state.questions = res.get("data", [])
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.is_playing = True
        st.session_state.match_ended = False
        st.rerun()
    elif res:
        st.error(f"Lỗi từ máy chủ: {res.get('message')}")


def update_score_to_server() -> None:
    """Đồng bộ điểm trận vừa chơi lên hệ thống để tích lũy rank."""
    with st.spinner("Đang đồng bộ điểm số lên hệ thống..."):
        res = post_action(
            "update_score", username=player_name, points=st.session_state.score
        )
    if res and res.get("status") == "success":
        st.session_state.total_score = res.get("new_total", st.session_state.score)
        st.toast("Đã lưu điểm thành công! ☁️", icon="✅")
    elif res:
        st.error(f"Lỗi lưu điểm: {res.get('message')}")
    else:
        st.error("Không thể lưu điểm lúc này, vui lòng kiểm tra kết nối mạng.")


def check_answer(selected_option: str, correct_answer: str) -> None:
    """Chấm điểm câu trả lời và chuyển sang câu tiếp theo."""
    elapsed = time.time() - (st.session_state.start_time or time.time())
    if elapsed > QUIZ_TIME_SECONDS:
        st.warning("⏰ Ối! Bạn đã trả lời sau khi hết thời gian!")
    elif selected_option == correct_answer:
        st.session_state.score += POINTS_PER_CORRECT
        st.toast(f"Chính xác! +{POINTS_PER_CORRECT} điểm 🎉", icon="✅")
    else:
        st.toast(f"Sai rồi! Đáp án đúng là {correct_answer} ❌", icon="🚨")
    st.session_state.current_q += 1


# === GIAO DIỆN THI ĐẤU ===
if not st.session_state.is_playing and not st.session_state.match_ended:
    st.info(f"Bạn có {QUIZ_TIME_SECONDS} giây để hoàn thành {QUESTIONS_PER_MATCH} câu hỏi.")
    if st.button("🚀 BẮT ĐẦU CÀY RANK", use_container_width=True, type="primary"):
        fetch_questions()

elif st.session_state.match_ended:
    st.success("🏁 Trận đấu kết thúc!")
    st.balloons()

    rank_name = get_rank_name(st.session_state.total_score)
    st.markdown(
        f"""
        <div style='text-align: center; padding: 20px; background-color: #1E1E1E;
                    border-radius: 10px; margin-bottom: 20px;'>
            <h3>Điểm trận này</h3>
            <h1 style='color: #FFD700; font-size: 40px;'>+{st.session_state.score} 🏆</h1>
            <hr>
            <h4>Tổng điểm tích lũy của bạn</h4>
            <h2 style='color: #4CAF50;'>{st.session_state.total_score}</h2>
            <h3 style='color: #00BCD4;'>Danh hiệu: {rank_name}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 Tiếp tục cày Rank", use_container_width=True):
        fetch_questions()

else:
    elapsed = time.time() - (st.session_state.start_time or time.time())
    time_left = max(0, QUIZ_TIME_SECONDS - int(elapsed))

    # Hết giờ hoặc hết câu hỏi -> tổng kết trận đấu
    if time_left == 0 or st.session_state.current_q >= len(st.session_state.questions):
        st.session_state.is_playing = False
        st.session_state.match_ended = True
        update_score_to_server()
        st.rerun()
    else:
        question = st.session_state.questions[st.session_state.current_q]

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Tiến độ",
            f"Câu {st.session_state.current_q + 1} / {len(st.session_state.questions)}",
        )
        col2.metric("Điểm hiện tại", f"{st.session_state.score} 🏆")

        # Đồng hồ đếm ngược JS: tự động bấm nút "HẾT GIỜ" khi về 0
        with col3:
            clock_html = f"""
            <div style="font-family: sans-serif; font-size: 1.5rem; text-align: center;
                        margin-top: 10px;">
                ⏳ Thời gian còn<br>
                <strong style="color: #FF4B4B; font-size: 2rem;">
                    <span id="clock">{time_left}</span> s
                </strong>
            </div>
            <script>
                var timeLeft = {time_left};
                var elem = document.getElementById('clock');
                var timerId = setInterval(function() {{
                    if (timeLeft <= 0) {{
                        clearTimeout(timerId);
                        var buttons = window.parent.document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {{
                            if (buttons[i].innerText.includes('HẾT GIỜ')) {{
                                buttons[i].click();
                                break;
                            }}
                        }}
                    }} else {{
                        timeLeft--;
                        elem.innerHTML = timeLeft;
                    }}
                }}, 1000);
            </script>
            """
            components.html(clock_html, height=100)

        st.progress(time_left / QUIZ_TIME_SECONDS)

        st.subheader(f"❓ {question['question']}")
        st.caption(f"Độ khó: {question['level']}")
        st.write("")

        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            if st.button(f"A. {question['opt_a']}", use_container_width=True):
                check_answer("A", question["answer"])
                st.rerun()
            if st.button(f"C. {question['opt_c']}", use_container_width=True):
                check_answer("C", question["answer"])
                st.rerun()
        with opt_col2:
            if st.button(f"B. {question['opt_b']}", use_container_width=True):
                check_answer("B", question["answer"])
                st.rerun()
            if st.button(f"D. {question['opt_d']}", use_container_width=True):
                check_answer("D", question["answer"])
                st.rerun()

        st.write("---")
        if st.button("⏳ HẾT GIỜ - TỔNG KẾT ĐIỂM", use_container_width=True):
            st.rerun()
