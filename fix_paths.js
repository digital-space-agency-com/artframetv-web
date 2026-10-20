const fs = require('fs');
const path = require('path');

// Array of files to update
const filesToFix = [
  'index.html',
  'privacy.html',
  'main.js',
  'styles.css'
];

filesToFix.forEach((filename) => {
  const filePath = path.join(__dirname, filename);

  if (!fs.existsSync(filePath)) {
    console.log(`Skipping ${filename} (file not found)`);
    return;
  }

  let content = fs.readFileSync(filePath, 'utf8');

  if (filename.endsWith('.html')) {
    // 1. Remove leading slashes from src, href, content (e.g. /styles.css -> styles.css)
    content = content.replace(/(src|href|content)="\/(?!\/)([^"]*)"/g, '$1="$2"');

    // 2. Fix empty brand href links (href="" -> href="./")
    content = content.replace(/href=""/g, 'href="./"');

    // 3. Ensure page links have .html extension if missing (href="privacy" -> href="privacy.html")
    content = content.replace(/href="(privacy|articles)"/g, 'href="$1.html"');
  }

  if (filename.endsWith('.js')) {
    // Remove leading slashes from image path strings in JS (e.g. '/images/' -> 'images/')
    content = content.replace(/(['"])\/images\//g, '$1images/');
  }

  if (filename.endsWith('.css')) {
    // Remove leading slashes from CSS url() references (e.g. url('/images/...') -> url('images/...'))
    content = content.replace(/url\((['"]?)\/([^'")]*)\)/g, 'url($1$2)');
  }

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Updated paths in ${filename}`);
});

console.log('\nAll paths have been updated to relative paths!');