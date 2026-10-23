# Ridgeline petty cash counts

TechHub challenge 411: **Save Cash Counts in a Supabase Database**. Full instructions, data dictionary and hints: https://techhub.byuaccounting.net/t/411-streamlit-save-cash-counts-in-a-supabase-database/9411/

*Ridgeline series:* you work in accounting at Ridgeline Home & Tool, a home-improvement retailer with eleven stores
in Utah and Idaho and a distribution center.

Each store counts its petty cash fund every few days, and the counts live in a spreadsheet someone emails around. This app records a count (date, store, who counted, expected and counted amounts), shows every count with its variance, and downloads them. It works in your codespace, but it saves to a file next to the app, which Streamlit Community Cloud throws away.

## Get your own copy

Click **Use this template › Create a new repository**. Keep the name `ridgeline-cash-count-app` and make it **Public**.
(Or open it straight in a codespace: https://codespaces.new/techhub-training/ridgeline-cash-count-app?quickstart=1.) Work in your copy, not this one.

## Open it

On your copy of this repository, click **Code › Codespaces › Create codespace on main**. Everything runs in the
codespace, in your browser: Python, the packages and Claude Code are already installed, the app starts by itself,
and a preview opens in a few minutes. Type `claude` in the terminal to work with Claude Code (sign in the first time).
Stop the codespace when you're done (github.com/codespaces › ••• › Stop) so it doesn't use your free hours.

## Why a database, and why Supabase

Streamlit Community Cloud runs your app on a machine it can restart at any time, and when it does, any file the app
wrote is gone. A petty-cash count that vanishes on Tuesday is worse than no app at all. So the counts move up to
**Level 3, Storage**: a database that lives somewhere else. [Supabase](https://supabase.com) runs a PostgreSQL
database for you, with a free tier, and the SQL is the SQL you already know.

1. **Create a project.** Sign up at supabase.com (GitHub sign-in works) and click **New project**. Name it
   `ridgeline-cash` and pick a region near you. Set a **database password** using only letters and numbers (it goes
   inside a web address, where symbols cause trouble) and save it somewhere safe. The project takes a minute or two.
2. **Create the table.** Open **SQL Editor › New query**, paste all of `schema.sql`, and click **Run**. Then open
   **Table Editor**: `cash_counts` is there, empty. Designing the table is the first step of any Storage, and
   `schema.sql` is that design: column types, rules (no negative amounts), and row-level security.
3. **Copy the connection string.** Click **Connect** at the top of the project page and choose the **Session pooler**
   connection string (the direct connection doesn't work from Streamlit Community Cloud). It looks like
   `postgresql://postgres.<project-ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres`.
   Replace `[YOUR-PASSWORD]` (brackets too) with your database password.
4. **Keep it in secrets.** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste the string in.
   This file is a key to your database: `.gitignore` keeps it out of Git, and it never goes in the code.

   ```toml
   [connections.supabase]
   url = "postgresql://postgres.abcdefghijklmnop:YourPassword123@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
   ```

Free Supabase projects pause after a stretch without use. If the app can't connect, open the project on
supabase.com and restore it.

## Where your data goes (Level 3, Storage)

| Question | Answer |
|---|---|
| Who runs the code? | Streamlit Community Cloud runs `app.py` (Level 2, Processing). |
| Where does the data go? | Every count goes into the `cash_counts` table in your Supabase project and stays there until someone deletes it (Level 3, Storage). Nothing is kept on Streamlit's machine. |
| Who can reach it? | Anyone with the app's link can add and delete counts, so use made-up data. The connection string (with the database password) is only in secrets. Supabase also offers every table through a public web API; row-level security, turned on in `schema.sql` with no policies, keeps that door shut. |

## Your task

1. Create your Supabase project and the `cash_counts` table, and put the connection string in secrets (above).
2. In `app.py`, replace the body of `connect()` with one line that opens your Supabase database:

   ```python
   return st.connection("supabase", type="sql")
   ```

   Delete the local `CREATE TABLE` too: in Supabase the table was created once, in the SQL Editor. Nothing else
   changes. The app's `INSERT`, `SELECT` and `DELETE` work the same on PostgreSQL.
3. Run the app in your codespace, save one test count, and find it in Supabase's **Table Editor**. That row is your
   Storage. Delete the test count in the app.
4. Publish the app on Streamlit Community Cloud with the secret, then enter these six counts on your **published** app:

   | Date | Store | Counted by | Expected | Counted |
   |---|---|---|---|---|
   | 2026-10-01 | Ridgeline Orem | Dana Whitaker | 500.00 | 500.00 |
   | 2026-10-01 | Ridgeline Ogden | Theo Barnes | 500.00 | 487.50 |
   | 2026-10-02 | Ridgeline St. George | Mei Chen | 300.00 | 300.00 |
   | 2026-10-02 | Ridgeline Idaho Falls | Luis Ortega | 300.00 | 312.25 |
   | 2026-10-03 | Ridgeline Twin Falls | Dana Whitaker | 250.00 | 250.00 |
   | 2026-10-03 | Ridgeline Orem | Priya Raman | 500.00 | 498.00 |

5. Prove the counts survive: on share.streamlit.io, open your app's menu and choose **Reboot app**. The six counts should still be there.
   (Typo? Delete the count and enter it again.)
6. Fill in the **Where your data goes** table above for your own app, in your own words, and commit it.

## Publish it on Streamlit Community Cloud

1. Commit and push your work to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. **Create app › Deploy a public app from GitHub**: pick this repository, branch `main`, main file `app.py`.
4. Open **Advanced settings › Secrets** and paste the two lines from your `secrets.toml` (the `[connections.supabase]` line and the `url` line). Click **Deploy**. The app gets a public address like `https://<name>.streamlit.app`.

Every push to `main` redeploys the app. An app nobody visits for a while goes to sleep; the first visitor wakes it up.


## Check your answer

After the reboot, click **Download counts (CSV)** on your published app and upload `cash_counts.csv` to the TechHub checker. Checker: https://techhub.byuaccounting.net/check/?c=411

The worked solution is on the [`solution` branch](https://github.com/techhub-training/ridgeline-cash-count-app/tree/solution). Try it yourself first.
