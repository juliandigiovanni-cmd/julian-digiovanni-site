# Deploy runbook

> **Bluehost era, kept as a record.** This is how the site was first deployed, on
> 2026-09-20. It now deploys to GitHub Pages: every push to `main` runs
> `.github/workflows/deploy.yml`, which builds and publishes `dist/`. There is no zip and
> no cPanel. Pages ignores `.htaccess`, so its two redirects are repeated in
> `src/pages/404.astro`. The steps here still apply to the Bluehost copy for as long as
> DNS points at it.
>
> **One thing this runbook relied on does not carry over.** It left `/Papers/` on the
> server because the server held more than the repo: the ten replication archives are not
> in `public/Papers/`, so on Pages the `dataCode` links to them 404. They need a new home,
> and the links need to follow, before DNS moves. A copy was downloaded on 2026-09-29 to
> `Julian/bluehost-backup-2026-09/Papers/`, outside the repo.

Replacing the WordPress site at `julian.digiovanni.ca` with this Astro build, on Bluehost
shared hosting, through the cPanel File Manager.

This follows the process used for George's site on 2026-09-11, which was the same
WordPress-to-static cutover on the same hosting account. Where a step here carries a warning,
it is because that deploy hit the problem. It assumes no context from the session that produced
it.

**Why File Manager and not FTP.** George's `docs/after-launch.md` measured it: FileZilla
connects and then hangs on every directory listing from the work network, which runs an FTP
gateway that reads the plaintext control channel to find the passive data port. Plain FTP
succeeded 3/3, FTP over TLS timed out 3/3 at 20s with zero bytes. Active versus passive makes
no difference. SFTP on port 22 also works if SSH is enabled on the account.

---

## What is being uploaded, and what is not

> **`/Papers/` holds more than the repo does. Never rebuild it from `public/Papers/`.**
> Alongside the PDFs it carries **ten replication archives, about 247 MB**, the largest
> `diGiovanni_Hale_StockGlobalNetwork_ReplicationFiles.zip` at 195 MB. None of them are in
> this repo, and journals' replication policies point at those URLs. The server directory is
> the only copy. A wipe-and-re-upload of `/Papers/` destroys them.

The build is 65 MB, but **64 MB of that is `/Papers/`, which is already on the server and
byte-identical to the repo**. It was verified before this deploy: all 73 PDFs then on the
server matched `public/Papers/` on `Content-Length`, with none differing and none missing.
That check looked only at PDFs, which is how the replication archives above went unnoticed
until the backup was opened — a reminder to compare the whole directory, not one file type.

So `/Papers/` is left in place and the upload is **11 files, 476 KB**. Nothing about a paper
URL changes at any point during the cutover, which matters because `data/cv-source.json` shows
about 28 `/Papers/` links baked into the published CV and the RePEc listings. Some of those are
`http://`, which is why the `.htaccess` forces HTTPS rather than leaving it to the host.

Seven superseded drafts were deleted from `public/Papers/` in the same change that added this
file, taking it from 73 to 66. They are deleted from the server by hand in step 6. They were
unlinked from the new site, unlinked from the old one, and absent from the CV source.

## URL continuity

| Live before | After | How |
|---|---|---|
| `/` | `/` | new `index.html` |
| `/research` | `/research/` | `build: { format: 'directory' }`; Apache `DirectoryIndex` serves it |
| `/policy-blogs` | `/policy-writing/` | 301 in `.htaccess` — the only path not reproduced |
| `/cv_diGiovanni.pdf` | unchanged | from `public/` |
| `/Papers/*.pdf` | unchanged | left on the server |
| `/feed`, `/wp-json/`, `/xmlrpc.php`, `/wp-login.php` | 404 | WordPress cruft, dropped on purpose |

There are no dated WordPress permalinks to preserve: `/2023/`, `/2023/12/` and `/2022/` all
returned 404 on the live site before the cutover. The old site was three pages.

---

## Part 1 — On the Mac

```bash
cd Julian/site
npm run clean && npm run build      # never rm -rf dist; this repo is in Dropbox
npm run links
chmod -R u=rwX,go=rX dist
rm -f site.zip
(cd dist && zip -rq ../site.zip . -x 'Papers/*' -x 'assets/*' -x 'chunks/*' -x 'pages/*')
unzip -l site.zip
```

`unzip -l` must show `index.html` at the top level — **not** `dist/`, and **not** `Papers/`.
Expect 11 files, about 476 KB.

**The `chmod` is load-bearing.** George's launch returned 403 on eleven PDFs because files
copied out of Dropbox carried owner-only permissions (`-rw-------`); the zip preserved them and
cPanel's extract kept them, so Apache refused to serve them. That was commit `fb931f2` there.

`Papers/` is excluded because it is already on the server. `assets/`, `chunks/` and `pages/`
are empty directories Astro leaves behind, sometimes mode `0700`; excluding them keeps
unreadable directories off the server.

Two files go up, both from this repo:

| File | Where it goes |
|---|---|
| `site.zip` | `<docroot>`, then Extract |
| `deploy/htaccess` | `<docroot>`, **renamed to `.htaccess`** |

## Part 2 — In cPanel

Do this from home or a phone hotspot, **not the work network**. Signing in via `bluehost.com`
routes through `my.bluehost.com` behind Cloudflare, which answers `cf-mitigated: challenge`,
and from a corporate egress IP the challenge can loop forever. Port 2083 is blocked there too.

**1. Log in.** Go directly to `https://digiovanni.ca/cpanel`.

**2. The document root is `public_html/julian`** — confirmed in File Manager on 2026-09-20;
the account home is `/home2/digiovan`, so the full path is
`/home2/digiovan/public_html/julian`. It is **not** the account's main `public_html`, which
belongs to a different site. Everything below calls it `<docroot>`. Getting this wrong is the
likeliest way to damage the wrong site.

**3. File Manager settings.** Open File Manager, then Settings:
- **Show Hidden Files (dotfiles)** — on, or `.htaccess` is invisible and step 7 misses it.
- Tick **Skip the trash** when deleting. A trashed PDF is still on the account.

**4. Back up. Nothing after this is reversible without it.**
- Files: open `<docroot>` → Select All → **Compress** → Zip Archive → **Download** it.
  **Expect about 1.5 GB, not the 65 MB the live site suggests** — the docroot carries a
  gallery, two large personal archives and the replication data. On 2026-09-20 it came to
  1.5 GB compressed, 1.83 GB and 39,587 files uncompressed. cPanel names the archive after the first selected item, so it
  may come out called `.well-known.zip` — the name means nothing, but it also means the name
  cannot confirm the archive is complete. **Check the size is ~65 MB.** A few KB means only one
  item was selected and there is no safety net.
- Database: cPanel → **phpMyAdmin** → select the WordPress database → **Export** → Go.
- Save both to a dated folder **outside** the Dropbox site directory.
- Check both are non-zero bytes before going on.

**5. Note the database name.** Open `<docroot>/wp-config.php` in the File Manager editor and
write down `DB_NAME` before anything deletes it. Needed in step 7.

**6. Delete the seven superseded drafts** from `<docroot>/Papers/`, with *Skip the trash*:

```
DNdiGDo_climate_inflation v1.pdf
DNdiGDo_climate_inflation v2.pdf
diGiovanniRogers_Revision1_ARC22.pdf
diGiovanniRogers_FinalDraft_ARC22.pdf
TwoRicardo_SPresubmit3.pdf
multi_revised3.pdf
errmonetary_sept07.pdf
```

**Leave the other 66 alone.** They are the live papers and are not in `site.zip`. Note that
`WebAppendix_errmonetary_sept07.pdf` stays, so its parent paper goes while the appendix
remains — deliberate, but worth a glance.

> **Update, 2026-09-20:** Julian also removed fourteen working-paper versions of published
> papers from the server, beyond the seven above. The repo was brought back in step, so
> `public/Papers/` and the server both hold 52 PDFs plus the ten archives. One of the fourteen,
> `DGKOS_InflationSupplyChainTrade.pdf`, was linked from both sites; the ECB Sintra entry now
> points at `_SintraFinal.pdf`, which survives, and `.htaccess` redirects the old URL to it.
> The published CV references 31 `/Papers/` files and none were affected — checked.

**6b. Delete the pre-WordPress leftovers.** The docroot holds a layer of files older than the
WordPress install, none of them referenced by the new site and none visible from outside except
by guessing the URL. Because extracting over the docroot never deletes, they survive the
cutover unless removed by hand. All of these were returning 200 before the cutover:

| Delete | Why |
|---|---|
| `Teaching/` | Course directories from 2011–2014 (`BMSS`, `BRIXEN14`, `ECO365_F11`, `ECO2507_W12`), browsable, not linked from the new site |
| `cv_diGiovanni.tex` | The LaTeX **source** of the CV, publicly downloadable |
| `cv_jdg.pdf`, `cv_jdg.tex` | A superseded CV and its source |
| `email.jpg`, `email_black.jpg`, `email_blue1.jpg`, `email_blue2.jpg` | Old address-obfuscation images |
| `gift_surprise.jpg` | Stray image |
| `error_log` | Apache already returns 403, but it does not belong in a web root |
| `404.shtml`, `500.shtml` | Broken SSI stubs — both render "[an error occurred while processing this directive]". The new site ships its own `404.html`. |
| `.htaccess.phpupgrader.be5c52b0`, `.htaccess.phpupgrader.initial` | Backups left by a PHP upgrade tool |
| `gallery/` | 560 MB, 26,583 files — a dead Gallery 2 PHP install, already 403 throughout |
| `Rome 2010.zip` (509 MB), `Surprise.zip` (148 MB) | Personal archives that were **publicly downloadable** |
| `Julian_temple.jpg`, `JulianSpain.jpg`, `Julian_Mysore.jpg`, `Lucha_GeikieGlacier.jpg`, `Julian_BW1.jpg`, `Julian_BW1c.jpg` | Personal photos in the web root |

Everything in the last three rows, plus `Teaching/` and the old CV files, was copied out of the
backup into `Websites/Julian/server-archive-2026-09-20/` before deletion, verified byte for
byte, so the 1.5 GB backup can be discarded afterwards without losing any of it.

**Keep `favicon.ico`.** The new site ships no favicon, so the server's one fills a real gap.
`cv_diGiovanni.pdf` is overwritten by the upload, correctly: the server's copy is from January
2026 and the repo's was regenerated on 2026-09-18.

**7. Remove WordPress.**
- Preferred: cPanel → **WordPress Tools** / *My Sites* / Installatron → remove the
  installation. It drops files and database together and de-registers the install. If it offers
  to wipe the whole directory, make sure `site.zip` is not in there yet.
- Manual fallback: delete `wp-admin/`, `wp-includes/`, `wp-content/`, every `wp-*.php`,
  `xmlrpc.php`, `index.php`, `readme.html`, `license.txt`, and `.htaccess`. Then drop the
  database in phpMyAdmin using the name from step 5.
- **`index.php` and the old `.htaccess` are the two that must go.** Leaving either beside the
  new `index.html` gives a half-broken state where Apache may keep serving the old WordPress
  homepage, and WordPress's `RewriteRule . /index.php` will swallow `/research/`.

**8. Check what is left.** `<docroot>` should hold `Papers/` (about 310 MB — 66 PDFs plus the
ten replication archives), `favicon.ico`, and nothing else of substance.
**Do not delete `cgi-bin/` or `.well-known/`** — `.well-known` is how AutoSSL proves domain
control, and removing it can break certificate renewal.

**9. Upload and extract.** Upload `site.zip` into `<docroot>`, then right-click → **Extract**.
Confirm `index.html`, `_astro/`, `coffee/`, `cv/`, `fonts/`, `policy-writing/`, `research/` and
`cv_diGiovanni.pdf` are now at the top level of `<docroot>`, beside `Papers/`. A site that
loads unstyled means the zip went in one level too deep.

**10. Upload `.htaccess`.** Upload `deploy/htaccess` into `<docroot>` and **rename it to
`.htaccess`**. Upload and rename rather than pasting into the cPanel editor: the editor can
silently turn a straight quote into a curly one and break a rule with no error.

**11. Clean up the server.** Delete `site.zip` and the step-4 backup zip from `<docroot>`. The
backup sits in the web root and would otherwise be publicly downloadable.

---

## Verify

```bash
D=julian.digiovanni.ca
for p in / /research/ /policy-writing/ /coffee/ /cv/ /cv_diGiovanni.pdf; do
  echo "$p -> $(curl -s -o /dev/null -w '%{http_code}' https://$D$p)"; done
curl -s -o /dev/null -w 'policy-blogs -> %{http_code} %{redirect_url}\n' https://$D/policy-blogs
curl -s -o /dev/null -w 'Papers index -> %{http_code} (want 403)\n' https://$D/Papers/
curl -s -o /dev/null -w 'http -> %{http_code} %{redirect_url}\n' http://$D/
curl -s -o /dev/null -w 'wp-login -> %{http_code} (want 404)\n' https://$D/wp-login.php
for p in /Teaching/ /cv_diGiovanni.tex /cv_jdg.pdf /error_log /404.shtml; do
  echo "$p -> $(curl -s -o /dev/null -w '%{http_code}' https://$D$p) (want 404)"; done
curl -s https://$D/no-such-page | grep -c 'Page not found'   # want 1: the new 404 page
```

Expected: the six paths 200; `/policy-blogs` 301 to `/policy-writing/`; `/Papers/` **403**,
which is `Options -Indexes` working; `http://` 301 to `https://`; `wp-login.php` 404, meaning
WordPress is gone rather than hidden.

Then check by hand:
- Five `/Papers/` PDFs still 200, including both of the awkward names,
  `Bems_diGiovanni_AEAP&P18.pdf` and `diGiovanni_Levchenko_Mejean_AERP&P17.pdf` — the `&` has
  to survive URL-encoding. No surviving filename contains a space; the only ones that did were
  among the seven deleted in step 6.
- The seven deleted drafts now 404.
- The coffee page on a phone, scrolling the cappuccino figure sideways.

**Rollback:** re-upload the step-4 zip and re-import the database.

## Every future update

`/Papers/` and `.htaccess` stay on the server. Extracting over the docroot overwrites files but
never deletes the ones already there, so a redeploy is just:

```bash
npm run clean && npm run build
chmod -R u=rwX,go=rX dist
rm -f site.zip
(cd dist && zip -rq ../site.zip . -x 'Papers/*' -x 'assets/*' -x 'chunks/*' -x 'pages/*')
```

then upload, Extract, delete the zip. **Leave `.htaccess` alone** — it is not produced by the
build, and an extract that overwrites it undoes the redirect and the `-Indexes` with nothing
visibly broken.

If a paper is added to `public/Papers/`, it will not reach the server this way, because the zip
excludes that directory. Upload new PDFs individually, or drop the `-x 'Papers/*'` for that one
deploy and accept the 64 MB.

## Known gaps

The site has no favicon of its own and relies on the one already on the server, which is why
`favicon.ico` is the one file in the docroot that is deliberately not deleted.

`public/googleb8fc2c9df817cee0.html` is the Google Search Console verification file. It is in
the build rather than only on the server, so a rebuild cannot silently un-verify the site. The
token is per Google account, not per property, so it is the same file George's site carries.

`robots.txt` and the sitemap were added after the cutover: `public/robots.txt` points at
`/sitemap-index.xml`, which `@astrojs/sitemap` generates from the five pages at build time.
The 404 page is excluded automatically.

## What actually happened on 2026-09-20

Recorded because the next cutover should expect it.

- The backup came to **1.5 GB, not the ~65 MB the live site implied** — a Gallery 2 install,
  two large personal archives and the replication data, none of it visible from outside.
- **The backup zip was left in the docroot and served publicly.** With `.htaccess` and
  `index.php` already deleted and no `index.html` yet, Apache fell back to a directory index
  and the 1.65 GB archive — including `wp-config.php` with the database credentials in plain
  text — was downloadable over HTTPS. Delete the backup from the server as soon as it has been
  downloaded, and prefer the order below.
- **Extract the new site before deleting WordPress.** The old `.htaccess` keeps routing to
  `index.php`, so the new files sit inert beside it and the cutover happens the moment those
  two are removed. That is a few seconds of downtime instead of several minutes, and it never
  leaves the docroot without an `index.html`.
