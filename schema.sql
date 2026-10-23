-- Ridgeline petty cash counts: the table the app saves to (TechHub challenge 411).
-- Paste this into Supabase › SQL Editor › New query, and click Run. Run it once.

create table cash_counts (
  id          bigint generated always as identity primary key,
  count_date  date          not null,
  store       text          not null,
  counted_by  text          not null,
  expected    numeric(10,2) not null check (expected >= 0),
  counted     numeric(10,2) not null check (counted >= 0)
);

-- Supabase also offers every table through a public web API. This app doesn't use that API, so lock it:
-- with row-level security on and no policies, the public key can't read or change a single row.
-- The app still can: it connects as the database owner, through the connection string in its secrets.
alter table cash_counts enable row level security;
