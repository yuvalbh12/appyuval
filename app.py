import streamlit as st
import pandas as pd
import os
from datetime import datetime

DB_FILE = "attendance_log.csv"

def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["תאריך", "כניסה", "יציאה", "סה שעות"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

st.set_page_config(page_title="שעון נוכחות יובל", layout="centered")
st.title("⏰ שעון נוכחות - יובל")

# --- דיווח מהיר ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔔 כניסה", use_container_width=True):
        st.session_state.start_time = datetime.now()
        st.success(f"כניסה ב-{st.session_state.start_time.strftime('%H:%M')}")
with col2:
    if st.button("🛑 יציאה", use_container_width=True):
        if 'start_time' in st.session_state:
            end = datetime.now()
            start = st.session_state.start_time
            dur = round((end - start).total_seconds() / 3600, 2)
            df = load_data()
            new_row = {"תאריך": start.strftime("%d/%m/%Y"), "כניסה": start.strftime("%H:%M"), "יציאה": end.strftime("%H:%M"), "סה שעות": dur}
            save_data(pd.concat([df, pd.DataFrame([new_row])], ignore_index=True))
            st.balloons()
            del st.session_state.start_time
            st.rerun()

st.divider()

# --- עריכה ומחיקה ---
data = load_data()
if not data.empty:
    st.subheader("📝 עריכה וניהול")
    selected_index = st.selectbox("בחר שורה:", data.index, format_func=lambda x: f"שורה {x}: {data.iloc[x]['תאריך']}")
    
    # שדות עריכה לשורה הנבחרת
    c1, c2, c3 = st.columns(3)
    new_date = c1.text_input("תאריך", data.iloc[selected_index]['תאריך'])
    new_start = c2.text_input("כניסה", data.iloc[selected_index]['כניסה'])
    new_end = c3.text_input("יציאה", data.iloc[selected_index]['יציאה'])
    
    col_save, col_del = st.columns(2)
    if col_save.button("✅ שמור שינויים", use_container_width=True):
        data.at[selected_index, 'תאריך'] = new_date
        data.at[selected_index, 'כניסה'] = new_start
        data.at[selected_index, 'יציאה'] = new_end
        # חישוב שעות מחדש פשוט (אופציונלי)
        save_data(data)
        st.success("עודכן!")
        st.rerun()
        
    if col_del.button("🗑️ מחק שורה", type="primary", use_container_width=True):
        save_data(data.drop(selected_index).reset_index(drop=True))
        st.rerun()

    st.dataframe(data, use_container_width=True)
