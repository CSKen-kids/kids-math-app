import streamlit as st
from utils import *
import sqlite3
import pandas as pd

DB_PATH = "kids_math_app.db"

st.set_page_config(page_title="小学生のための算数アプリ", page_icon="🧶")

# テーマ選択と画像表示
theme = st.sidebar.selectbox("テーマをえらんでね", ["かわいい", "かっこいい", "シンプル"])
theme_images = {
    "かわいい": "https://img.icons8.com/clouds/100/owl.png",
    "かっこいい": "https://img.icons8.com/dusk/100/robot-3.png",
    "シンプル": "https://img.icons8.com/ios/100/book.png"
}
st.sidebar.image(theme_images[theme], caption=f"{theme}テーマ")

# メニュー選択
menu = st.sidebar.radio("メニュー", [
    "📚 勉強する", "📊 きろくを見る", "❓ 質問する", "🔁 間違えた問題の復習", "👪 保護者メニュー"
])

# 📚 勉強する
if menu == "📚 勉強する":
    st.header("📚 勉強しよう！")
    category = st.selectbox("カテゴリを選んでね", ["たし算・ひき算", "かけ算・わり算", "分数"])

    if "quiz" not in st.session_state:
        st.session_state.quiz = []
        st.session_state.current = 0
        st.session_state.correct = 0

    if st.button("問題をスタート！", disabled=bool(st.session_state.quiz)):
        st.session_state.quiz = [generate_question(category) for _ in range(5)]
        st.session_state.current = 0
        st.session_state.correct = 0

    if st.session_state.quiz:
        q, ans = st.session_state.quiz[st.session_state.current]
        st.markdown(f"**Q{st.session_state.current+1}: {q} は？**")
        user_ans = st.number_input("こたえを入れてね", step=1, key=f"answer_{st.session_state.current}")

        if st.button("こたえを送る"):
            correct_flag = int(user_ans == ans)
            save_result(q, user_ans, ans, correct_flag)
            if correct_flag:
                st.success("🌟 せいかい！")
                st.session_state.correct += 1
            else:
                st.error(f"ちがうよ。せいかいは {ans} だよ。")

            st.session_state.current += 1

            if st.session_state.current >= len(st.session_state.quiz):
                st.balloons()
                st.success(f"ぜんぶおわったよ！ {st.session_state.correct}問せいかいだったね！")
                st.session_state.quiz = []

# 📊 きろくを見る
elif menu == "📊 きろくを見る":
    st.header("📊 今までのきろく")
    df = get_results()
    if df.empty:
        st.write("まだきろくがないよ。")
    else:
        st.dataframe(df)

# ❓ 質問する
elif menu == "❓ 質問する":
    st.header("❓ 先生にしつもんしよう！")
    content = st.text_area("わからないところを書いてね")
    if st.button("おくる"):
        save_question(content)
        st.success("おくったよ！せんせいがよんでくれるよ。")

# 🔁 間違えた問題の復習
elif menu == "🔁 間違えた問題の復習":
    st.header("🔁 まちがえた問題をやりなおそう！")
    if "review" not in st.session_state:
        df = get_wrong_questions(limit=5)
        st.session_state.review = df.to_dict(orient="records")
        st.session_state.r_current = 0
        st.session_state.r_correct = 0

    if st.session_state.review:
        r = st.session_state.review[st.session_state.r_current]
        q = r["question"]
        ans = r["correct_answer"]
        st.markdown(f"**Q{st.session_state.r_current+1}: {q} は？**")
        user_ans = st.number_input("こたえを入れてね", step=1, key=f"r_answer_{st.session_state.r_current}")

        if st.button("こたえを送る（復習）"):
            correct_flag = int(user_ans == ans)
            save_result(q, user_ans, ans, correct_flag)
            if correct_flag:
                st.success("🌟 せいかい！")
                st.session_state.r_correct += 1
            else:
                st.error(f"ちがうよ。せいかいは {ans} だよ。")

            st.session_state.r_current += 1

            if st.session_state.r_current >= len(st.session_state.review):
                st.balloons()
                st.success(f"復習おわり！ {st.session_state.r_correct}問せいかいだったね！")
                st.session_state.review = []

# 👪 保護者メニュー
elif menu == "👪 保護者メニュー":
    st.header("👪 保護者・先生用 管理メニュー")
    password = st.text_input("パスコードを入力してください", type="password")
    if password == "1234":
        st.subheader("📊 勉強の記録（全件）")
        df_all = get_all_study_results(limit=100)
        st.dataframe(df_all)
        csv = df_all.to_csv(index=False).encode("utf-8")
        st.download_button("📅 CSVダウンロード", data=csv, file_name="study_results.csv", mime="text/csv")

        st.subheader("❓ 質問の一覧")
        qdf = get_all_questions(limit=100)
        if qdf.empty:
            st.info("質問はまだありません。")
        else:
            st.dataframe(qdf)
    else:
        st.warning("正しいパスコードを入力してください（例: 1234）")


