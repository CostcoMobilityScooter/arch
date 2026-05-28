# How to Publish ARCH on GitHub

## Step 1 — Create the Repository

1. Go to https://github.com/new
2. Name it `arch`
3. Set it to **Public**
4. Check **Add a README file**
5. Click **Create repository**

---

## Step 2 — Upload Your Files

Upload these files to the repo root:

```
arch.py
arch_config.json
arch.ico
requirements.txt
BUILD_EXE.bat
patch_model.py
README.md          ← rename your existing README
```

To upload: click **Add file → Upload files** on GitHub,
or use Git if you're comfortable with it.

---

## Step 3 — Create a Release (for the .exe download)

1. Build `ARCH.exe` on your PC using `BUILD_EXE.bat`
2. On GitHub, click **Releases** (right sidebar) → **Create a new release**
3. Click **Choose a tag** → type `v4.52` → click **Create new tag**
4. Title: `ARCH v4.52`
5. Description:
   ```
   ## ARCH v4.52

   Terminal-style app launcher for Windows.

   ### What's new
   - Gemini AI integration (free API key)
   - Persistent config saving fixed
   - Two-column help display

   ### Install
   1. Download `ARCH_build_package.zip` below
   2. Extract and run `BUILD_EXE.bat`
   3. Launch `dist\ARCH.exe`
   ```
6. Drag and drop these files into the assets section:
   - `ARCH.exe` (your built exe)
   - `ARCH_build_package.zip` (the source zip)
7. Click **Publish release**

---

## Step 4 — Enable GitHub Pages (the website)

1. In your repo, click **Settings** → **Pages** (left sidebar)
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main`, Folder: `/ (root)`
4. Click **Save**
5. Create a folder called `docs/` in your repo
6. Upload `index.html` (the website file) into `docs/`
7. Go back to Settings → Pages and change folder to `/docs`
8. Wait ~2 minutes, then visit:
   `https://YOUR_USERNAME.github.io/arch`

---

## Step 5 — Update the Links

In `index.html`, replace every instance of:
```
YOUR_USERNAME
```
with your actual GitHub username.

---

## Step 6 — Get a Custom Domain (Optional, Free)

If you want `arch.yourdomain.com` instead of `github.io`:

1. Buy a domain (Namecheap, Porkbun, Cloudflare — ~$10/yr)
2. Add a CNAME record pointing to `YOUR_USERNAME.github.io`
3. In GitHub Pages settings, enter your custom domain
4. Check **Enforce HTTPS**

---

## Your Links After Setup

| What | URL |
|------|-----|
| Website | `https://YOUR_USERNAME.github.io/arch` |
| Source code | `https://github.com/YOUR_USERNAME/arch` |
| Latest release | `https://github.com/YOUR_USERNAME/arch/releases/latest` |
| Direct .exe download | `https://github.com/YOUR_USERNAME/arch/releases/latest/download/ARCH.exe` |
| Direct zip download | `https://github.com/YOUR_USERNAME/arch/releases/latest/download/ARCH_build_package.zip` |

---

## Keeping It Updated

When you release a new version:
1. Update the version number in `arch.py` and `index.html`
2. Build a new `ARCH.exe`
3. Create a new GitHub Release with the new tag (e.g. `v4.53`)
4. Upload the new exe and zip as assets
5. The download links above always point to the **latest** release automatically
