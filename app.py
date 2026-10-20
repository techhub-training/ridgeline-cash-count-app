"""Ridgeline petty cash counts (TechHub challenge 411).

Store managers record each surprise count of a store's petty cash fund. The app works, but it saves the counts in a
file next to the app (cash_counts.db). Streamlit Community Cloud throws that file away whenever it restarts the app.
README.md says how to move the data to Turso so it survives."""
import datetime as dt
import libsql
import pandas as pd
import streamlit as st

STORES = ["Ridgeline Orem", "Ridgeline Lehi", "Ridgeline Ogden", "Ridgeline Logan", "Ridgeline St. George",
          "Ridgeline Park City", "Ridgeline Idaho Falls", "Ridgeline Pocatello", "Ridgeline Twin Falls",
          "Ridgeline Boise", "Ridgeline Cedar City", "Ridgeline Distribution Center"]

st.set_page_config(page_title="Ridgeline petty cash counts", layout="wide")
st.title("Ridgeline petty cash counts")


def connect():
    """TODO: this file disappears when Streamlit restarts the app. Connect to your Turso database instead."""
    return libsql.connect("cash_counts.db")


conn = connect()
conn.execute("""CREATE TABLE IF NOT EXISTS cash_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, count_date TEXT NOT NULL, store TEXT NOT NULL, counted_by TEXT NOT NULL,
    expected REAL NOT NULL, counted REAL NOT NULL)""")
conn.commit()

with st.form("count", clear_on_submit=True):
    st.subheader("Record a count")
    a, b, c = st.columns(3)
    count_date = a.date_input("Date", dt.date(2026, 10, 1))
    store = b.selectbox("Store", STORES)
    counted_by = c.text_input("Counted by")
    d, e = st.columns(2)
    expected = d.number_input("Fund balance (expected)", min_value=0.0, step=0.01, format="%.2f")
    counted = e.number_input("Cash counted", min_value=0.0, step=0.01, format="%.2f")
    if st.form_submit_button("Save count"):
        if not counted_by.strip():
            st.warning("Enter who counted the cash.")
        else:
            conn.execute("INSERT INTO cash_counts (count_date, store, counted_by, expected, counted) VALUES (?, ?, ?, ?, ?)",
                         (count_date.isoformat(), store, counted_by.strip(), round(expected, 2), round(counted, 2)))
            conn.commit()
            st.success("Saved.")

rows = conn.execute("""SELECT id, count_date, store, counted_by, expected, counted, ROUND(counted - expected, 2)
                       FROM cash_counts ORDER BY count_date, store""").fetchall()
table = pd.DataFrame(rows, columns=["ID", "Date", "Store", "CountedBy", "Expected", "Counted", "Variance"])

st.subheader(f"Counts on file ({len(table)})")
st.dataframe(table, hide_index=True)
st.download_button("Download counts (CSV)", table.drop(columns="ID").to_csv(index=False), "cash_counts.csv", "text/csv")

with st.expander("Delete a count entered by mistake"):
    if len(table):
        gone = st.selectbox("Count", table["ID"], format_func=lambda i: " | ".join(
            str(x) for x in table.loc[table["ID"] == i, ["Date", "Store", "CountedBy", "Counted"]].iloc[0]))
        if st.button("Delete"):
            conn.execute("DELETE FROM cash_counts WHERE id = ?", (int(gone),))
            conn.commit()
            st.rerun()
