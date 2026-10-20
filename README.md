# Ridgeline petty cash counts: solution

The worked solution to TechHub challenge 411, **Save Cash Counts in a Turso Database** (https://techhub.byuaccounting.net/t/411-streamlit-save-cash-counts-in-a-turso-database/9411/).
The starter that students copy is on the `main` branch of https://github.com/techhub-training/ridgeline-cash-count-app.

`connect()` opens an embedded replica of the Turso database and syncs it; `add_count()` and `delete_count()`
call `conn.sync()` after they commit, so every change reaches Turso before the app moves on.

To run it, create a Turso database and put `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` in `.streamlit/secrets.toml`
(see the README on `main`). With no secrets the app stops with a message saying what to add.

The six counts in the challenge give these variances (counted minus expected): Ogden −12.50, Idaho Falls +12.25,
Orem on October 3 −2.00, and zero for the other three.

Other ways to keep data outside the app: Supabase or Neon (PostgreSQL), Google Sheets through an API, or a
TechHub-style API of your own. Turso is the shortest step from SQLite.
