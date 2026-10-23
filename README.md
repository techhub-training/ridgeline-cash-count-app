# Ridgeline petty cash counts: solution

The worked solution to TechHub challenge 411, **Save Cash Counts in a Supabase Database** (https://techhub.byuaccounting.net/t/411-streamlit-save-cash-counts-in-a-supabase-database/9411/).
The starter that students copy is on the `main` branch of https://github.com/techhub-training/ridgeline-cash-count-app.

`connect()` is one line, `st.connection("supabase", type="sql")`, which reads the connection string from
`[connections.supabase]` in the app's secrets. Reads use `conn.query(..., ttl=0)` so the table is always current;
writes go through `run()`, which passes every value as a parameter (`:store`, `:counted`...) rather than pasting it
into the SQL, so a name like `O'Brien` or `'; DROP TABLE` is stored as text and never run.

The table is created once, in the Supabase SQL Editor, from `schema.sql`: `numeric(10,2)` columns for money, `check`
rules that refuse negative amounts, and row-level security turned on with no policies. The app connects as the
database owner, so it isn't affected; the public web API Supabase puts in front of every table can't read a row.

With no secrets the app stops with a message saying what to add.

The six counts in the challenge give these variances (counted minus expected): Ogden −12.50, Idaho Falls +12.25,
Orem on October 3 −2.00, and zero for the other three.

## Where your data goes (Level 3, Storage)

| Question | Answer |
|---|---|
| Who runs the code? | Streamlit Community Cloud runs `app.py` (Level 2, Processing). |
| Where does the data go? | Every count goes into the `cash_counts` table in your Supabase project and stays there until someone deletes it (Level 3, Storage). Nothing is kept on Streamlit's machine. |
| Who can reach it? | Anyone with the app's link can add and delete counts, so use made-up data. The connection string (with the database password) is only in secrets. Supabase also offers every table through a public web API; row-level security, turned on in `schema.sql` with no policies, keeps that door shut. |



