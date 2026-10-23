"""Ridgeline petty cash counts (TechHub challenge 411, solution).

Level 3, Storage: store managers record each surprise count of a store's petty cash fund, and the counts live in a
Supabase database (hosted PostgreSQL), so they survive when Streamlit Community Cloud restarts the app.

Secrets (.streamlit/secrets.toml in your codespace; Settings > Secrets on Streamlit Community Cloud):
    [connections.supabase]
    url = "postgresql://postgres.<project-ref>:<database-password>@<pooler-host>:5432/postgres"
"""
import datetime as dt

import pandas as pd
import streamlit as st
from sqlalchemy import text

STORES = ["Ridgeline Orem", "Ridgeline Lehi", "Ridgeline Ogden", "Ridgeline Logan", "Ridgeline St. George",
          "Ridgeline Park City", "Ridgeline Idaho Falls", "Ridgeline Pocatello", "Ridgeline Twin Falls",
          "Ridgeline Boise", "Ridgeline Cedar City", "Ridgeline Distribution Center"]

st.set_page_config(page_title="Ridgeline petty cash counts", layout="wide")
st.title("Ridgeline petty cash counts")


def connect():
    """Supabase: the connection string comes from the app's secrets, never from the code."""
    if "supabase" not in st.secrets.get("connections", {}):
        st.error("Add a [connections.supabase] url to the app's secrets (see README.md).")
        st.stop()
    return st.connection("supabase", type="sql")


def run(sql, **params):
    """Change the data: one statement, with the values passed as parameters (never pasted into the SQL)."""
    with conn.session as s:
        s.execute(text(sql), params)
        s.commit()


conn = connect()

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
            run("""INSERT INTO cash_counts (count_date, store, counted_by, expected, counted)
                   VALUES (:count_date, :store, :counted_by, :expected, :counted)""",
                count_date=count_date, store=store, counted_by=counted_by.strip(),
                expected=round(expected, 2), counted=round(counted, 2))
            st.success("Saved.")

table = conn.query("""SELECT id AS "ID", count_date AS "Date", store AS "Store", counted_by AS "CountedBy",
                             expected AS "Expected", counted AS "Counted", counted - expected AS "Variance"
                      FROM cash_counts ORDER BY count_date, store""", ttl=0)
for col in ("Expected", "Counted", "Variance"):
    table[col] = table[col].astype(float).round(2)

st.subheader(f"Counts on file ({len(table)})")
st.dataframe(table, hide_index=True)
st.download_button("Download counts (CSV)", table.drop(columns="ID").to_csv(index=False), "cash_counts.csv", "text/csv")

with st.expander("Delete a count entered by mistake"):
    if len(table):
        gone = st.selectbox("Count", table["ID"], format_func=lambda i: " | ".join(
            str(x) for x in table.loc[table["ID"] == i, ["Date", "Store", "CountedBy", "Counted"]].iloc[0]))
        if st.button("Delete"):
            run("DELETE FROM cash_counts WHERE id = :id", id=int(gone))
            st.rerun()
