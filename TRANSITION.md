# Venice Vintage Club — Transition Guide

Everything you need to run venicevintageclub.com without Freddie.

---

## Quick Reference

| What | Where |
|------|-------|
| **Live site** | [venicevintageclub.com](https://venicevintageclub.com) |
| **GitHub repo** | [github.com/morganreisel/venice-vintage-club](https://github.com/morganreisel/venice-vintage-club) |
| **Google Drive (photos)** | Shared folder: `VVC Media` (ID: `1RQYXWqeBc-NXHm_OqCLkf6MBkUJVUGAu`) |
| **Domain** | `venicevintageclub.com` — managed by client (separate from GitHub) |
| **Hosting** | GitHub Pages (free, auto-deploys) |
| **Email** | `hello@venicevintageclub.com` — needs Google Workspace setup ($7/mo) |
| **Instagram** | [@venicevintageclub](https://instagram.com/venicevintageclub) |

---

## How the Site Works

The entire site is a **single HTML file** (`index.html`) with all CSS and JavaScript inline. No build step, no framework, no server. Push to `main` and it's live.

### File Structure (what matters)

```
venice-vintage-club/
├── index.html              ← The entire website (HTML + CSS + JS, all inline)
├── CNAME                   ← Custom domain config (venicevintageclub.com)
├── favicon.svg             ← Browser tab icon
├── sync-drive.py           ← Auto-syncs photos from Google Drive
├── launch.md               ← Pre-launch checklist & TODOs
├── scope-of-work.md        ← Retainer agreement & what's in/out of scope
├── images/                 ← All site images (optimized JPGs + brand PNGs)
│   ├── community-*.jpg     ← Community carousel (synced from Drive)
│   ├── mood-*.jpg          ← Mood slideshow (synced from Drive)
│   ├── space-*.jpg         ← The Space grid (synced from Drive)
│   ├── lookbook-*.jpg      ← Lookbook filmstrip (synced from Drive)
│   ├── morgan-*.jpg        ← Morgan's film scans
│   ├── globe-logo*.png     ← Spinning globe brand asset
│   ├── vvc-logo*.png       ← VVC text logos (clean, purple, neon variants)
│   └── hero.jpg            ← Hero background
├── .github/workflows/
│   ├── deploy.yml          ← Auto-deploy to GitHub Pages on push
│   ├── sync-drive.yml      ← Google Drive photo sync (triggered by scheduler)
│   └── scheduler.yml       ← Daily 9am PT trigger for the photo sync
└── .drive-manifest.json    ← Tracks which Drive photos have been synced
```

---

## Deployment (Auto — Nothing to Do)

Every push to the `main` branch automatically deploys to GitHub Pages. There is no build step.

**Workflow:** `.github/workflows/deploy.yml`

1. You push code to `main`
2. GitHub Actions picks it up
3. Site is live at venicevintageclub.com within ~60 seconds

**No secrets or API keys needed.** It just works.

### How to check if a deploy succeeded
1. Go to [github.com/morganreisel/venice-vintage-club/actions](https://github.com/morganreisel/venice-vintage-club/actions)
2. Look for the most recent "Deploy" workflow run
3. Green checkmark = live. Red X = something broke.

---

## Google Drive Photo Sync (Auto — Daily)

Photos upload to Google Drive, and the site pulls them in automatically every day.

**Workflows:** `.github/workflows/scheduler.yml` (triggers the sync daily) + `.github/workflows/sync-drive.yml` (does the actual work)
**Script:** `sync-drive.py`

### How it works

1. Morgan (or anyone) drops photos into the **VVC Media** shared Google Drive folder
2. Every day at **9am PT**, a scheduler workflow triggers `sync-drive.py` via GitHub Actions
3. The script downloads all photos, converts them to optimized JPGs, and updates `index.html`
4. Changes get committed and pushed — the site auto-deploys with the new photos

### Drive Folder Structure

The Drive folder must have these subfolders. Drop photos into the right one:

| Drive Folder | What it controls | How many |
|---|---|---|
| `HERO/` | Hero section background image | 1 photo |
| `MOOD/` | Mood slideshow (auto-advances) | As many as you want |
| `COMMUNITY/` | Community filmstrip carousel | As many as you want |
| `SPACE/` | "The Space" photo grid | As many as you want |
| `LOOKBOOK/` | Lookbook filmstrip gallery | As many as you want |
| `EVENT/` | Event section background | 1 photo |
| `MORGAN/` | About section background (Morgan portrait) | 1 photo |

### Supported photo formats
`.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.heic`, `.webp` — all get converted to optimized JPG automatically.

### Image naming
Photos are auto-named `{section}-01.jpg`, `{section}-02.jpg`, etc. You don't need to name them anything specific in Drive.

### Running a sync manually
1. Go to the repo's **Actions** tab on GitHub
2. Click **"Sync Google Drive Photos"** in the left sidebar
3. Click **"Run workflow"**
4. Choose `replace` (swap all photos) or `add` (append new ones)
5. Click the green **"Run workflow"** button

### If the sync breaks
- Check the Actions log for errors
- Most common issue: Drive folder permissions changed (must be publicly viewable, or shared with anyone who has the link)
- The Drive folder ID is hardcoded in `sync-drive.py` line 36: `1RQYXWqeBc-NXHm_OqCLkf6MBkUJVUGAu`

---

## Domain & DNS

**Domain:** `venicevintageclub.com`
**Hosting:** GitHub Pages (via the `CNAME` file in the repo)
**DNS:** Cloudflare (proxies traffic to GitHub Pages)

### Moving the domain to your own Cloudflare account

The VVC domain needs to move from Freddie's Cloudflare account to yours. This is a one-time setup that takes about 10 minutes. The site may be briefly unreachable while the nameservers update (usually under an hour, sometimes up to 24 hours).

**Step 1 — Create your own Cloudflare account**
1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) and sign up with your email (morgyreisel@gmail.com or the VVC email)
2. It's free — no payment needed

**Step 2 — Add the VVC domain to your new account**
1. Once logged in, click **"Add a site"**
2. Enter `venicevintageclub.com`
3. Choose the **Free** plan
4. Cloudflare will scan your existing DNS records — let it finish
5. You should see your existing records listed. If not, add these manually:
   - **Type:** CNAME | **Name:** `@` | **Target:** `morganreisel.github.io` | **Proxy:** ON (orange cloud)
   - **Type:** CNAME | **Name:** `www` | **Target:** `morganreisel.github.io` | **Proxy:** ON (orange cloud)
6. Cloudflare will give you **two new nameservers** — write these down (they look like `anna.ns.cloudflare.com` and `bob.ns.cloudflare.com`)

**Step 3 — Update nameservers at the domain registrar**
1. Log in to wherever the domain was purchased (check the VVC PRD doc — this is the domain registrar, separate from Cloudflare)
2. Find the **Nameservers** or **DNS** settings for `venicevintageclub.com`
3. Replace the old nameservers with the two new ones Cloudflare gave you
4. Save

**Step 4 — Wait and verify**
1. Cloudflare will show the domain as "Pending" until the nameservers update — this can take 10 minutes to 24 hours
2. Once it switches to "Active", your Cloudflare account is in control
3. Check that [venicevintageclub.com](https://venicevintageclub.com) loads correctly

**Step 5 — Tell Freddie to remove the domain from his account**
Once everything is working on your end, let Freddie know so he can delete `venicevintageclub.com` from his Cloudflare account.

### After the GitHub repo transfer

The GitHub repo moved from `fmannion10/venice-vintage-club` to `morganreisel/venice-vintage-club`. Make sure the Cloudflare DNS points to the right place:

- The CNAME record should point to `morganreisel.github.io` (NOT `fmannion10.github.io`)
- If you set up the DNS records in Step 2 above, this is already correct

### DNS basics (in case you ever need them)

The DNS must point to GitHub Pages:

- If using an apex domain (`venicevintageclub.com`): Set a CNAME to `morganreisel.github.io`, or A records to GitHub's IPs (found in [GitHub Pages docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-github-pages))
- If using `www`: Set a CNAME record pointing to `morganreisel.github.io`

**Do not delete the `CNAME` file** in the repo — it tells GitHub Pages which domain to serve.

---

## Mailchimp (Email Signup)

The "Join the Club" email capture form is built but has **placeholder values that must be replaced** before it will actually capture emails.

### What to do

1. Log into Mailchimp and create an audience/list
2. Go to **Signup forms → Embedded forms**
3. Copy the form action URL — it looks like:
   ```
   https://venicevintageclub.usXX.list-manage.com/subscribe/post?u=XXXXX&id=XXXXX
   ```
4. In `index.html`, find and replace:
   - `MAILCHIMP_ACTION_URL_PLACEHOLDER` → your actual form action URL
   - `b_PLACEHOLDER` → the honeypot field name from Mailchimp's embed code (looks like `b_abc123def456`)

### Where in the code
Search `index.html` for `MAILCHIMP_ACTION_URL_PLACEHOLDER` — it's in the email capture form near the bottom of the file (around line 2900).

---

## Google Workspace Email

`hello@venicevintageclub.com` is referenced in the site footer but **has not been set up yet**.

To set it up:
1. Go to [workspace.google.com](https://workspace.google.com)
2. Sign up for a Business Starter plan ($7/mo)
3. Verify domain ownership (follow Google's DNS instructions)
4. Create the `hello@` address

---

## How to Make Common Changes

### Update text/copy
1. Open `index.html` in any text editor
2. Search for the text you want to change
3. Edit it
4. Commit and push to `main` — the site auto-deploys

### Update event date or details
Search `index.html` for the current event info (e.g., "May 2") and update. The countdown timer auto-calculates from the date in the JavaScript near the bottom of the file.

### Add/change photos
Drop them in the right folder in Google Drive. Wait for the next daily sync (9am PT), or trigger a manual sync from the Actions tab.

### Change brand colors
Search `index.html` for `:root` at the top of the `<style>` block. The CSS variables are:
- `--cream` — main text/background color
- `--orange` — accent color
- `--purple` — brand purple

---

## Branding Assets

All in the `images/` folder:

| File | What |
|---|---|
| `globe-logo.png` | Spinning globe (original) |
| `globe-logo-clean.png` | Spinning globe (clean, no background) |
| `vvc-logo.png` | VVC text logo |
| `vvc-logo-clean.png` | VVC text logo (clean) |
| `vvc-logo-purple.png` | VVC text logo (purple) |
| `vvc-logo-neon.png` | VVC neon sign graphic |
| `favicon.svg` | Browser tab icon |

These should also be backed up to Google Drive (in a `BRANDING/` folder).

---

## What's Still TODO Before May 2nd

- [ ] Replace Mailchimp placeholders (see Mailchimp section above)
- [ ] Set up `hello@venicevintageclub.com` via Google Workspace
- [ ] Drop a real Morgan portrait into Drive `MORGAN/` folder
- [ ] Swap hero placeholder for final garage photo (Drive `HERO/` folder)
- [ ] Create Stripe payment links for products (or keep DM-to-purchase)
- [ ] Upload branding assets to Drive `BRANDING/` folder

---

## Costs

| Service | Cost | What it does |
|---|---|---|
| GitHub Pages | Free | Hosts the site |
| Google Drive | Free | Photo storage + auto-sync |
| Domain renewal | Varies | `venicevintageclub.com` (client manages) |
| Google Workspace | $7/mo | `hello@venicevintageclub.com` email |
| Mailchimp | Free (up to 500 contacts) | Email list |
| Stripe | 2.9% + $0.30 per transaction | Payment links (if used) |

---

## GitHub Repo Access

The repo is at [github.com/morganreisel/venice-vintage-club](https://github.com/morganreisel/venice-vintage-club).

To give someone else access:
1. Go to **Settings → Collaborators** in the repo
2. Click **Add people**
3. Enter their GitHub username or email

They'll need push access to `main` to make changes that auto-deploy.

**No secrets or environment variables are configured** — the repo uses only public/free services (GitHub Pages, public Google Drive folder).

---

*Last updated: April 6, 2026*
