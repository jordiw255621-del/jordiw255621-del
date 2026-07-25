# 🎧 Spotify "Now Playing" — one-time setup

The widget in the README goes live once you connect your Spotify account. It
needs a tiny serverless deploy because Spotify's API requires a private secret
that can't live in a public README.

## Steps (~10 min)

1. **Create a Spotify app**
   - Go to https://developer.spotify.com/dashboard → *Create app*
   - Add redirect URI: `https://spotify-github-profile.kittinanx.com/api/callback`
   - Copy the **Client ID** and **Client Secret**

2. **Deploy the widget backend (free)**
   - Fork https://github.com/kittinan/spotify-github-profile
   - Deploy it to **Vercel** (free tier) and set the env vars it asks for
     (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `FIREBASE_*` — the repo's
     README walks through it), **or** use the hosted instance below.

3. **Authorize your account**
   - Visit `https://spotify-github-profile.kittinanx.com/api/login`
   - Log in with Spotify → it gives you a `uid`

4. **Drop your `uid` into the README**
   - In `README.md`, find `uid=CHANGE_ME` in the "Now Playing" section
   - Replace `CHANGE_ME` with your `uid`

That's it — the card will show your last / currently-playing track.

> ⚠️ This step needs **your** Spotify login and a Vercel account, so it can't be
> automated for you — but the widget markup is already wired up and waiting.
