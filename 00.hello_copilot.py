# 1부터 100사이의 임의의 숫자를 정하고 최단 횟수로 이를 맞추는 게임
# 코드는 웹에서 실행 가능하다. 
# streamlit 라이브러리를 사용하여 웹 인터페이스로 구현한다.

import random
import streamlit as st

# 처음 실행될 때만 초기화
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 100)
    st.session_state.count = 0
    st.session_state.finished = False

st.write("1부터 100사이의 숫자를 맞춰보세요!")

guess = st.number_input("숫자를 입력하세요:", min_value=1, max_value=100, step=1, key="guess")

if st.button("확인"):
    st.session_state.count += 1
    if guess < st.session_state.answer:
        st.write("더 큰 숫자입니다.")
    elif guess > st.session_state.answer:
        st.write("더 작은 숫자입니다.")
    else:
        st.write(f"축하합니다! {st.session_state.count}번 만에 맞추셨습니다.")
        st.session_state.finished = True