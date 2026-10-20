# Ridgeline petty cash counts

TechHub challenge 411: **Save Cash Counts in a Turso Database**. Full instructions, data dictionary and hints: https://techhub.byuaccounting.net/t/411-streamlit-save-cash-counts-in-a-turso-database/9411/

*Ridgeline series:* you work in accounting at Ridgeline Home & Tool, a home-improvement retailer with eleven stores
in Utah and Idaho and a distribution center.

Each store counts its petty cash fund every few days, and the counts live in a spreadsheet someone emails around. This app records a count (date, store, who counted, expected and counted amounts), shows every count with its variance, and downloads them. It works on your computer, but it saves to a local file, which Streamlit Community Cloud throws away.

## Get your own copy

Click **Use this template › Create a new repository**. Keep the name `ridgeline-cash-count-app` and make it **Public**.
(Or open it straight in a codespace: https://codespaces.new/techhub-training/ridgeline-cash-count-app?quickstart=1.) Work in your copy, not this one.

## Open it

**In your browser (nothing to install):** on your copy of this repository, click **Code › Codespaces › Create codespace on main**.
The app installs and starts by itself, and a preview opens in a few minutes. Stop the codespace when you're done
(github.com/codespaces › ••• › Stop) so it doesn't use your free hours.

**On your computer:** you need Python 3.10 or newer and Git.

```
git clone https://github.com/<you>/ridgeline-cash-count-app.git
cd ridgeline-cash-count-app
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
## Why a database, and why Turso

Streamlit Community Cloud runs your app on a machine it can restart at any time, and when it does, any file the app
wrote is gone. A petty-cash count that vanishes on Tuesday is worse than no app at all. So the counts go in a database
that lives somewhere else: [Turso](https://turso.tech), a hosted SQLite database with a free tier.

1. Sign up at turso.tech (GitHub sign-in works) and create a database, for example `ridgeline-cash`.
2. On the database's page, copy its **URL** (`libsql://ridgeline-cash-<you>.turso.io`) and create a **token**.
3. Put both in `.streamlit/secrets.toml` (never in the code; `.gitignore` already keeps this file out of Git):

   ```toml
   TURSO_DATABASE_URL = "libsql://ridgeline-cash-<you>.turso.io"
   TURSO_AUTH_TOKEN = "eyJ..."
   ```


## Your task

1. Create your Turso database and put its URL and token in secrets (above).
2. In `app.py`, change `connect()` so it opens your Turso database. With the `libsql` package this is an
   *embedded replica*: a local copy that syncs with Turso.

   ```python
   conn = libsql.connect("cash_counts.db", sync_url=st.secrets["TURSO_DATABASE_URL"],
                         auth_token=st.secrets["TURSO_AUTH_TOKEN"])
   conn.sync()
   ```

   Then call `conn.sync()` again after every write (the insert and the delete) so Turso gets the change.
3. Publish the app on Streamlit Community Cloud with the two secrets. Enter these six counts on your **published** app:

   | Date | Store | Counted by | Expected | Counted |
   |---|---|---|---|---|
   | 2026-10-01 | Ridgeline Orem | Dana Whitaker | 500.00 | 500.00 |
   | 2026-10-01 | Ridgeline Ogden | Theo Barnes | 500.00 | 487.50 |
   | 2026-10-02 | Ridgeline St. George | Mei Chen | 300.00 | 300.00 |
   | 2026-10-02 | Ridgeline Idaho Falls | Luis Ortega | 300.00 | 312.25 |
   | 2026-10-03 | Ridgeline Twin Falls | Dana Whitaker | 250.00 | 250.00 |
   | 2026-10-03 | Ridgeline Orem | Priya Raman | 500.00 | 498.00 |

4. Prove the counts survive: on share.streamlit.io, open your app's menu and choose **Reboot app**. The six counts should still be there.
   (Typo? Delete the count and enter it again.)

## Publish it on Streamlit Community Cloud

1. Commit and push your work to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. **Create app › Deploy a public app from GitHub**: pick this repository, branch `main`, main file `app.py`.
4. Open **Advanced settings › Secrets** and paste the two Turso lines. Click **Deploy**. The app gets a public address like `https://<name>.streamlit.app`.

Every push to `main` redeploys the app. An app nobody visits for a while goes to sleep; the first visitor wakes it up.


## Check your answer

After the reboot, click **Download counts (CSV)** on your published app and upload `cash_counts.csv` to the TechHub checker. Checker: https://techhub.byuaccounting.net/check/?c=411

The worked solution is on the [`solution` branch](https://github.com/techhub-training/ridgeline-cash-count-app/tree/solution). Try it yourself first.
