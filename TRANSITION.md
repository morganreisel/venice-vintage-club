# Venice Vintage Club — Transition Guide

Everything you need to run venicevintageclub.com without Freddie.

---

## Quick Reference

| What | Where |
|------|-------|
| **Live site** | [venicevintageclub.com](https://venicevintageclub.com) |
| **GitHub repo** | [github.com/morganreisel/venice-vintage-club](https://github.com/morganreisel/venice-vintage-club) |
| **Google Drive (photos)** | Shared folder: `VVC Media` (ID: `1RQYXWqeBc-NXHm_OqCLkf6MBkUJVUGAu`) |
| **Domain** | `venicevintageclub.com` — registered on Freddie's Cloudflare (pending transfer to Morgan after ~June 2026) |
| **Hosting** | GitHub Pages (free, auto-deploys) + Cloudflare Pages backup at `venice-vintage-club.pages.dev` |
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
│   ├── lookbook-*.jpg      ← Lookbook magazine spreads (synced from Drive)
│   ├── morgan-*.jpg        ← Morgan's film scans
│   ├── globe-logo*.png     ← Spinning globe brand asset
│   ├── vvc-logo*.png       ← VVC text logos (clean, purple, neon variants)
│   └── hero.jpg            ← Hero background
├── .github/workflows/
│   ├── deploy.yml          ← Auto-deploy to GitHub Pages on push
│   └── sync-drive.yml      ← Google Drive photo sync (daily 9am PT + manual trigger)
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

**Workflow:** `.github/workflows/sync-drive.yml` (runs daily + manual trigger)
**Script:** `sync-drive.py`

### How it works

1. Morgan (or anyone) drops photos into the **VVC Media** shared Google Drive folder
2. Every day at **9am PT**, `sync-drive.yml` runs automatically via GitHub Actions cron
3. The script downloads all photos, converts them to optimized JPGs, deduplicates identical files, and updates `index.html`
4. Changes get committed and pushed — the site auto-deploys with the new photos

**Note:** If a Drive folder is emptied, the corresponding images are removed from the site. Duplicate files (same content, different names) are automatically skipped so photos don't appear twice.

### Drive Folder Structure

The Drive folder must have these subfolders. Drop photos into the right one:

| Drive Folder | What it controls | How many |
|---|---|---|
| `HERO/` | Hero section background image | 1 photo |
| `MOOD/` | Mood slideshow (auto-advances) | As many as you want |
| `COMMUNITY/` | Community filmstrip carousel | As many as you want |
| `SPACE/` | "The Space" photo grid | As many as you want |
| `LOOKBOOK/` | Lookbook magazine spreads (two photos side by side per page) | Even number works best |
| `EVENT/` | Event section background | 1 photo |
| `MORGAN/` | About section background (Morgan portrait) | 1 photo |

### Photo orientation — important!

The site layout is **landscape/horizontal** — slideshows, backgrounds, and grids are all wider than they are tall. If you upload **portrait/vertical photos** (like most phone photos), the site will crop the sides to make them fit. This means parts of the photo will be cut off.

**For best results:**
- **HERO, MOOD, EVENT** — Use **landscape (horizontal)** photos. These sections are full-width and will crop portrait photos heavily.
- **COMMUNITY** — Landscape works best, but portrait photos will still look OK (the site shows the top of the image so faces stay visible).
- **LOOKBOOK** — **Portrait (vertical) photos work great here.** Photos display two side by side in a magazine spread layout, so portrait shots naturally fill the space. Upload an even number so they pair up evenly.
- **SPACE** — A mix of landscape and portrait is fine here since it's a grid, but landscape photos fill the grid cells more naturally.
- **MORGAN** — Portrait is fine here since it's a person photo. The site is set up to show the face/upper body.

If a photo looks cut off on the site, it's almost always because a vertical photo is being displayed in a horizontal space. The easiest fix is to swap it for a landscape version of the same shot.

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
**Registrar:** Cloudflare (registered on Freddie's account: fredpmannion@gmail.com)
**Hosting:** GitHub Pages (via the `CNAME` file in the repo)
**DNS:** Cloudflare (Freddie's account, DNS-only mode pointing to GitHub Pages)

### Current Setup (as of April 6, 2026)

The domain is registered on Freddie's Cloudflare account but the site is hosted on Morgan's GitHub Pages. DNS records on Freddie's Cloudflare:

- 4 **A records** → GitHub Pages IPs (`185.199.108-111.153`) — DNS only (grey cloud)
- **CNAME** `www` → `morganreisel.github.io` — DNS only (grey cloud)

Morgan also has:
- A **Cloudflare account** (morgyreisel@gmail.com, Account ID: `6b8936b45b933868bbf8a4e03d486ab4`)
- A **Cloudflare Pages project** at `venice-vintage-club.pages.dev` (working backup, not currently used for the live domain)
- The domain `venicevintageclub.com` added as a site on her Cloudflare (pending nameserver verification)

### Pending: Domain Transfer to Morgan (after ~June 2026)

The domain was registered within the last 60 days, so ICANN rules prevent transferring it to another Cloudflare account until that window passes. The domain expires **March 27, 2027**.

**When the 60-day lock expires, do this:**

1. **Freddie** logs into Cloudflare → Domains → Registrations → `venicevintageclub.com` → Configuration
2. Click **"Move to another Cloudflare account"**
3. Enter Morgan's Account ID: `6b8936b45b933868bbf8a4e03d486ab4`
4. **Morgan** accepts the transfer on her Cloudflare dashboard
5. **Morgan** updates DNS on her account to point to GitHub Pages (same A records and CNAME as above)
6. **Freddie** deletes the `venicevintageclub.com` zone from his Cloudflare — done

After the transfer, Morgan can optionally switch from GitHub Pages to Cloudflare Pages by adding `venicevintageclub.com` as a custom domain on her Pages project.

### DNS basics (in case you ever need them)

The DNS must point to GitHub Pages:

- If using an apex domain (`venicevintageclub.com`): A records to GitHub's IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`)
- If using `www`: CNAME record pointing to `morganreisel.github.io`
- Records must be **DNS only (grey cloud)** so GitHub can handle SSL

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
- [x] Drop a real Morgan portrait into Drive `MORGAN/` folder
- [x] Swap hero placeholder for final garage photo (Drive `HERO/` folder)
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

*Last updated: April 9, 2026*
