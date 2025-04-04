# ReCHor Documentation Generator

This project generates static HTML documentation for the ReCHor project.

## Structure

```
unofficialDoc/
├── docs/              # Generated documentation (GitHub Pages root)
│   ├── index.html    # Main landing page
│   ├── parts/        # Individual part pages
│   ├── concepts/     # Individual concept pages
│   └── classes/      # Individual class pages
├── python/           # Python source code
│   └── generate_static_docs.py
└── summaries/        # Source JSON files
    └── extracted/    # Extracted handout data
```

## Local Development

1. Make sure you have Python 3.6+ installed
2. Run the documentation generator:
   ```bash
   cd python
   python generate_static_docs.py
   ```
3. The generated documentation will be in the `docs/` directory
4. Open `docs/index.html` in your browser to preview

## Deploying to GitHub Pages

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Update documentation"
   git push
   ```

2. Configure GitHub Pages:
   - Go to your repository's Settings
   - Navigate to "Pages" in the sidebar
   - Under "Source", select "Deploy from a branch"
   - Select the branch you want to deploy from (e.g., `main`)
   - Set the folder to `/docs`
   - Click "Save"

3. Your documentation will be available at `https://<username>.github.io/<repository>/`

## Customizing

- Edit the CSS styles in `generate_static_docs.py` to customize the appearance
- Modify the HTML templates in the Python code to change the structure
- Update the JSON files in `summaries/extracted/` to change the content

## License

This project is licensed under the MIT License - see the LICENSE file for details.
