# Venice Vintage Club — Site Guide

This is everything you need to know to manage the VVC website. No coding required.

---

## How the Site Gets Its Photos

The site pulls photos directly from a **shared Google Drive folder** called **VVC Media**. Whatever photos are in that Drive folder **are** the photos on the site.

**This is the most important thing to understand:**

> The Drive folders REPLACE the site photos — they don't add to them.
> If you want a photo on the site, it must be in the Drive folder.
> If you remove a photo from Drive, it disappears from the site.
> Don't just add new photos and delete old ones unless you want the old ones gone.

### The Drive Folders

Each folder in Google Drive maps to a section of the website:

| Drive Folder | What It Controls | How Many Photos |
|---|---|---|
| `HERO/` | The big background image at the very top | 1 photo |
| `MOOD/` | The full-screen slideshow below the hero (click arrows to browse) | As many as you want |
| `COMMUNITY/` | The slideshow in "The Club" section with "Vintage With a Pulse" text over it | As many as you want |
| `SPACE/` | The venue photos in "The Space" section (2-column grid) | 2+ photos |
| `LOOKBOOK/` | The slideshow in the Lookbook section (click arrows to browse) | As many as you want |
| `EVENT/` | The background image behind the event/RSVP section | 1 photo |
| `MORGAN/` | The background image in the "About VVC" section | 1 photo |

### Photo Tips

- Photos are automatically resized and optimized for web — upload full-quality originals
- Supported formats: JPG, PNG, HEIC (iPhone photos), TIFF, WebP
- Name your files in the order you want them to appear (e.g., `01.jpg`, `02.jpg`, `03.jpg`)
- For slideshows (MOOD, COMMUNITY, LOOKBOOK), landscape/wide photos work best
- For HERO and EVENT, use wide landscape photos (they fill the full screen width)
- For MORGAN, a vertical or square photo works well

---

## When Photos Update

Photos sync from Google Drive to the site automatically **every day at 9am Pacific Time**.

### If You Need Photos Updated Right Now

1. Go to the GitHub repository (github.com — ask Freddie for the link if you don't have it)
2. Click the **"Actions"** tab at the top
3. Click **"Sync Google Drive Photos"** in the left sidebar
4. Click the **"Run workflow"** button on the right
5. Click the green **"Run workflow"** button in the dropdown
6. Wait a few minutes — the site will update automatically

---

## The Website Sections (Top to Bottom)

1. **Ticker Banner** — The scrolling orange text at the very top (event info)
2. **Navigation** — Logo + links (Events, The Space, The Club, Lookbook)
3. **Hero** — Big background photo with the neon VVC sign
4. **Mood Slideshow** — Full-screen photo slideshow (click arrows to change photos)
5. **Globe + Event Countdown** — The spinning globe with countdown timer
6. **The Club (Community)** — Photo slideshow with "Vintage With a Pulse" overlay text
7. **The Space** — Venue description + photo grid
8. **Lookbook** — Photo slideshow with arrows
9. **The Event** — RSVP section with background photo
10. **About VVC** — Morgan's bio with background photo
11. **Email Signup** — Mailing list capture
12. **Footer** — Links + social

---

## Event Countdown

The globe section has a countdown timer to the May 2nd pop-up. Here's what happens automatically:

- **Before the event:** Countdown shows days, hours, minutes, seconds until May 2nd at 11am PT
- **During the event (May 2-3):** Countdown reaches zero and the timer disappears
- **After the event (May 4 onward):** The countdown hides completely and the section changes to say "Thanks for Coming — Stay tuned for the next one."

**No action needed** — this all happens on its own. If you want to set up a countdown for a future event, ask a developer to update the date in the code.

---

## Setting Up Mailchimp (Email Signups)

The site has two email signup forms — one in the RSVP/event section and one at the bottom of the page. Right now they're **not connected** to Mailchimp yet. Here's how to set them up:

1. **Create a Mailchimp account** at [mailchimp.com](https://mailchimp.com) (free plan works fine)
2. **Create an Audience** (Mailchimp's term for a mailing list) — call it something like "VVC Mailing List"
3. **Get your form action URL:**
   - In Mailchimp, go to **Audience** > **Signup forms** > **Embedded forms**
   - Look for the `<form action="..."` line in the code Mailchimp gives you
   - Copy the URL inside the `action=""` — it looks something like: `https://venicevintageclub.us21.list-manage.com/subscribe/post?u=XXXXX&id=XXXXX`
4. **Give that URL to a developer** (or Freddie) — they need to paste it into two places in `index.html` where it currently says `MAILCHIMP_ACTION_URL_PLACEHOLDER`

That's it. Once the URL is in, both signup forms will send emails straight to your Mailchimp audience.

---

## Common Tasks

### "I want to change the photos on the site"
1. Open the Google Drive folder (VVC Media)
2. Go to the subfolder for the section you want to change (e.g., MOOD/)
3. Add, remove, or replace photos as needed
4. **Remember: keep ALL the photos you want on the site in the folder — whatever's in the folder is what shows up**
5. Wait for the next auto-sync (daily at 9am PT) or trigger a manual sync (see above)

### "I want to change text on the site"
Text changes require editing the code (index.html). Ask Freddie or a developer to help.

### "I want to add a Shop/Products section back"
This was removed intentionally. If you want it back, ask a developer — it's straightforward to re-add.

### "The photos aren't updating"
- Make sure the photos are in the correct Drive folder
- Check that the files are actual image files (JPG, PNG, HEIC, etc.)
- Try running a manual sync from GitHub Actions
- If it still doesn't work, check the Actions tab for error messages

---

## Accounts & Credentials

All login info for VVC accounts can be found in the Google Doc called **"VVC PRD"**. Below is every account involved in running the site, what it's for, and when you'd need to log in.

### 1. Google Workspace (Gmail, Drive, Calendar)

| | |
|---|---|
| **What it is** | The VVC email (hello@venicevintageclub.com) and Google Drive where photos live |
| **Login** | Go to [gmail.com](https://gmail.com) or [drive.google.com](https://drive.google.com) and sign in with the VVC email + password from the "VVC PRD" doc |
| **Admin panel** | [admin.google.com](https://admin.google.com) — use this to add/remove users, reset passwords, or manage billing |
| **When you need it** | To upload/change photos in Drive, check VVC email, or manage the account |

### 2. GitHub (Where the website code lives)

| | |
|---|---|
| **What it is** | The code repository and the system that automatically deploys the site |
| **Login** | Go to [github.com](https://github.com) and sign in — credentials are in "VVC PRD" |
| **Repository** | github.com/fmannion10/venice-vintage-club |
| **When you need it** | Only to trigger a manual photo sync (Actions tab) or if a developer needs access to the code |

**How to trigger a manual photo sync:**
1. Log in to GitHub
2. Go to the repository (link above)
3. Click **"Actions"** tab
4. Click **"Sync Google Drive Photos"** on the left
5. Click **"Run workflow"** > green **"Run workflow"** button
6. Wait 2-3 minutes — site updates automatically

### 3. Cloudflare (Domain & DNS)

| | |
|---|---|
| **What it is** | Controls the domain name (venicevintageclub.com) and where it points |
| **Login** | Go to [dash.cloudflare.com](https://dash.cloudflare.com) — credentials are in "VVC PRD" |
| **When you need it** | Almost never. Only if the domain expires, you need to change DNS settings, or you're moving the site to a new host. **Do not change anything here unless you know what you're doing or a developer is helping.** |

**Important:** The domain has an annual renewal. Make sure the payment method on Cloudflare stays current or the domain will expire and the site will go down.

### 4. Mailchimp (Email Marketing)

| | |
|---|---|
| **What it is** | Manages the mailing list — collects emails from the signup forms on the site |
| **Login** | Go to [mailchimp.com](https://mailchimp.com) — credentials are in "VVC PRD" (or create a new account if one hasn't been set up yet) |
| **When you need it** | To view your subscriber list, send email campaigns/newsletters, or manage signup form settings |

**Note:** Mailchimp is **not connected yet**. See the "Setting Up Mailchimp" section above for step-by-step instructions.

---

## Taking Over the Site — Step by Step

If you're the new person managing VVC's website, here's exactly what to do:

### First Day
1. **Get the "VVC PRD" Google Doc** from Freddie or whoever is handing this off to you — it has all the login credentials
2. **Log in to Google Workspace** ([gmail.com](https://gmail.com)) with the VVC email to make sure you have access
3. **Log in to GitHub** ([github.com](https://github.com)) and find the repository — bookmark it
4. **Read this entire document** so you know what's what

### Ongoing (What You'll Actually Do)
- **Swap photos:** Drag files in/out of Google Drive folders → site updates daily at 9am PT automatically
- **Check email:** Log in to Gmail with the VVC account for any site-related inquiries
- **Send newsletters:** Log in to Mailchimp (once set up) to email your subscriber list

### Things You Should NOT Touch
- **Don't edit any code files** unless you know what you're doing
- **Don't change anything in Cloudflare** unless a developer is helping
- **Don't delete the GitHub repository** — that's the entire website
- **Don't remove the `.drive-manifest.json` file** from the repository — the photo sync needs it

### If Something Breaks
1. Don't panic — the site is static HTML, so it's very hard to break permanently
2. Check if the problem is just photos not updating (try a manual sync from GitHub Actions)
3. If the site is completely down, check Cloudflare to make sure the domain hasn't expired
4. Contact Freddie or a developer for anything else

---

## Who to Contact

- **Freddie** — Built the site, can help with any technical changes
- **GitHub Actions** — Automated photo syncing (runs on its own, no action needed)
