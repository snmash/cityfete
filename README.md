# City Fête Events

Static rebuild of cityfete.com (previously on Wix), served with GitHub Pages.

- `build.py` holds all page content and generates the five HTML pages. Edit it, run `python3 build.py`, commit.
- `assets/site.css` and `assets/site.js` hold styling and the homepage gallery behaviour.
- `assets/img/` holds the site's photos resized for the web (2000 px on the long edge, JPEG), the gallery thumbnails, the City Fête logo, and the press logos in `press/`. `city-fete-logo-original.png` is the full-size logo and is not referenced by any page. The full-resolution originals are kept outside the site folder.
- The contact page links to Calendly and to `mailto:paruul@cityfete.com`. Change `CONTACT_EMAIL` in `build.py` to update the address.

## Publishing

1. Create a public repository and upload everything in this folder (keep the `assets/` folder structure and the `.nojekyll` file).
2. In the repository: Settings → Pages → Deploy from a branch → `main`, folder `/ (root)`.
