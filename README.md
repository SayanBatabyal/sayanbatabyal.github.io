# Sayan Batabyal's Website

A personal static website for Sayan Batabyal, ready for GitHub Pages.

## Structure

- `index.html`: home page (bio and career timeline)
- `publications.html`: renders `data/publications.json`
- `teaching.html`: course list
- `blog.html`: renders `data/blog.json`
- `css/style.css`, `js/*.js`: styling and rendering
- `images/`: profile photo and book cover images
- `pubs/`: optional, for hosting PDFs locally (publication links currently point to the original site)
- `404.html`: not-found page
- `.nojekyll`: tells GitHub Pages to serve files as-is

## Deploy to GitHub Pages

1. Create a GitHub Pages repository and push these files to the root of the publishing branch.
2. Repo Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site goes live at `https://<user>.github.io/` (or `/<repo>/` for project repos).

For a custom domain, add a `CNAME` file containing the domain and configure DNS.

## Adding content

- New publication: add an object to `data/publications.json`.
- New blog post: write `blog/<slug>.html` (copy the layout of an existing page), then add an entry to `data/blog.json`.
- New course: add an `<li>` to `teaching.html`.

## Notes

- Some blog and publication links point to their original source pages. To self-host them, copy the content locally and update the corresponding URLs.
