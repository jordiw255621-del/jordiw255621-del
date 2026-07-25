# 📅 Calendar Activity setup

The **What I'm Up To** section is refreshed every 30 min by the
`Update Calendar Activity` workflow, which reads your Google Calendar's
private iCal feed and rewrites the block between the
`<!--START_SECTION:calendar-->` markers in `README.md`.

Only **event titles and times** are shown — locations, descriptions, notes and
attendees are never read, so nothing private leaks onto your public profile.

## One-time setup

1. **Get your secret iCal URL** (per calendar you want to show):
   Google Calendar → hover the calendar in the left sidebar → **⋮ → Settings
   and sharing** → scroll to **"Secret address in iCal format"** → copy the
   `https://calendar.google.com/.../basic.ics` link.
   > Treat this like a password — anyone with it can read that calendar.

2. **Add it as a repo secret:**
   Repo **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `CAL_ICS_URL`
   - Value: the `.ics` URL (paste **multiple**, comma-separated, to merge
     several calendars, e.g. work + uni)

3. **Run it once:** Actions tab → *Update Calendar Activity* → **Run workflow**.

## Customising

- **Emoji per activity:** edit the `EMOJI` list in
  `scripts/calendar_activity.py`.
- **Refresh rate:** change the `cron` in
  `.github/workflows/update-calendar.yml`.
- **Timezone:** `TZ = ZoneInfo("Australia/Sydney")` in the script.
