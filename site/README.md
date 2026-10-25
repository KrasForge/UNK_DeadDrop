# UNK_DeadDrop website

Astro + Starlight site for the twelve-part technical series. The editable article sources remain in `deliverables/blog-series/`; the site generates its article collection from them before every local or CI build.

## Local preview

```sh
cd site
npm install
npm run dev
```

## Production build

```sh
cd site
npm ci
npm run build
```

The build is written to `site/dist/`. Set `SITE_URL` and `BASE_PATH` to preview a specific deployment URL. In GitHub Actions, the Astro configuration derives both from `GITHUB_REPOSITORY`.

## GitHub Pages

The repository workflow builds from `site/` and deploys through GitHub Pages. In the repository settings, choose **GitHub Actions** as the Pages source. The workflow responds to pushes on `master` and `main`, and can also be started manually.

For a custom domain, set `SITE_URL` and `BASE_PATH` in the workflow environment and add the domain through the repository's Pages settings.
