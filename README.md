# Static Site Generator

A custom-built Python static site generator that transforms Markdown content into a fully functional HTML website. This project parses Markdown text, builds an intermediate structured data tree, and renders standard HTML.

## Acknowledgements

This project was inspired by and built as part of the [Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python) course on [Boot.dev](https://www.boot.dev).

## Architecture

For a deep dive into how the Markdown parsing pipeline and site orchestration work, please see the [Architecture Documentation](architecture.md).

## Usage

You can build and preview the site in two different ways depending on your target environment.

### Local Development

To build the site for a local environment and immediately preview it using Python's built-in HTTP server:

```bash
./local.sh
```
This will serve the site at `http://localhost:8888/` with the root path `/`.

### GitHub Pages Deployment

To build the site for production hosting on GitHub Pages (or any subdirectory), run the build script:

```bash
./build.sh
```
This script passes the `/static-site-gen/` basepath argument to the generator. The site files will be built into the `docs/` directory, which is the default folder GitHub Pages uses to serve static assets.
