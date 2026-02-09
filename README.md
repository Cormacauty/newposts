# Custom Atom Feed for Blog Releases

This repository automatically generates a custom Atom feed from GitHub releases.

## Setup Instructions

1. **Add the workflow file**
   - Create `.github/workflows/generate-feed.yml` in your `newposts` repository
   - Copy the contents from the workflow file provided

2. **Add the Python script**
   - Create `generate_feed.py` in the root of your `newposts` repository
   - Copy the contents from the Python script provided

3. **Enable GitHub Pages**
   - Go to your repository Settings → Pages
   - Under "Source", select "Deploy from a branch"
   - Select the `main` branch (or whichever branch you use)
   - Select `/root` as the folder
   - Click Save

4. **Run the workflow manually (first time)**
   - Go to the Actions tab in your repository
   - Click "Generate Atom Feed" workflow
   - Click "Run workflow"
   - This will create the initial `feed.xml` file

5. **Your feed URL will be:**
   ```
   https://[your-github-username].github.io/newposts/feed.xml
   ```

## How It Works

- Every time you create a new release, the GitHub Action automatically runs
- It fetches all your releases via the GitHub API
- Generates a custom Atom feed with your branding
- Commits the updated `feed.xml` to your repository
- GitHub Pages serves it publicly

## Customization

Edit the configuration variables at the top of `generate_feed.py`:
- `FEED_TITLE` - The title of your feed
- `FEED_DESCRIPTION` - Description that appears in feed readers
- `FEED_AUTHOR` - Your name
- `FEED_ICON` - URL to your icon/logo
- `BLOG_URL` - Your blog's main URL

## Your Private Blog Repo

Your main blog repository remains completely private. This setup only uses public data (releases) from this public `newposts` repository.
