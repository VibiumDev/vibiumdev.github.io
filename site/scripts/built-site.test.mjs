import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import test from 'node:test';

const dist = new URL('../dist/', import.meta.url);

async function exists(path) {
  try {
    await stat(new URL(path, dist));
    return true;
  } catch (error) {
    if (error && error.code === 'ENOENT') return false;
    throw error;
  }
}

async function readBuilt(path) {
  return readFile(new URL(path, dist), 'utf8');
}

test('homepage is the Vibium landing page and links to docs', async () => {
  const html = await readBuilt('index.html');

  assert.match(html, /The verification layer for coding agents/);
  assert.match(html, /app\.loops\.so\/api\/newsletter-form/);
  assert.match(html, /cmj0qy2u60s8s0y0icsxtqeqq/);
  assert.match(html, /href="\/docs\/"/);
  assert.match(html, /Subscribe for Vibium updates/);
  assert.match(html, /Vibium links/);
});

test('homepage publishes agent-readable metadata', async () => {
  const html = await readBuilt('index.html');

  assert.match(html, /<link rel="canonical" href="https:\/\/vibium\.com\/">/);
  assert.match(
    html,
    /<link rel="alternate" type="text\/markdown" href="\/llms\/README\.md">/
  );
  assert.match(html, /<script type="application\/ld\+json">/);
  assert.match(html, /"@type":"WebSite"/);
  assert.match(html, /"@type":"BreadcrumbList"/);
  assert.match(html, /"dateModified":"\d{4}-\d{2}-\d{2}"/);
  assert.match(html, /<a href="\/docs\/concepts\/">Glossary<\/a>/);
});

test('Starlight docs are mounted under /docs only', async () => {
  assert.equal(await exists('docs/index.html'), true);
  assert.equal(await exists('docs/quickstart/index.html'), true);
  assert.equal(await exists('quickstart/index.html'), false);
});

test('Starlight docs publish agent-readable metadata', async () => {
  const html = await readBuilt('docs/introduction/index.html');

  assert.match(
    html,
    /<meta name="description" content="Browser automation for AI agents and humans, built on WebDriver BiDi\.">/
  );
  assert.match(
    html,
    /<meta property="og:description" content="Browser automation for AI agents and humans, built on WebDriver BiDi\.">/
  );
  assert.match(
    html,
    /<link rel="alternate" type="text\/markdown" href="\/llms\/docs\/introduction\.md">/
  );
});

test('agent-readable Markdown stays rooted at /llms', async () => {
  assert.equal(await exists('llms.txt'), true);
  assert.equal(await exists('llms-full.txt'), true);
  assert.equal(await exists('llms/docs/quickstart.md'), true);
});

test('HTML pages have same-path Markdown mirrors', async () => {
  assert.equal(await exists('index.md'), true);
  assert.equal(await exists('docs.md'), true);
  assert.equal(await exists('docs/introduction.md'), true);
  assert.equal(await exists('docs/commands.md'), true);
  assert.equal(await exists('docs/commands/go.md'), true);
});

test('docs links use indexed command overview route', async () => {
  const html = await readBuilt('docs/introduction/index.html');

  assert.match(html, /href="\/docs\/commands\/"/);
  assert.doesNotMatch(html, /href="\/docs\/commands\/index\/"/);
});

test('robots.txt points agents at the generated sitemap', async () => {
  const text = await readBuilt('robots.txt');

  assert.match(text, /User-agent: \*/);
  assert.match(text, /Allow: \//);
  assert.match(text, /Sitemap: https:\/\/vibium\.com\/sitemap-index\.xml/);
});

test('generated code blocks expose language classes', async () => {
  const html = await readBuilt('docs/commands/go/index.html');
  const preCodeBlocks = html.match(/<pre\b[^>]*><code\b[^>]*>/g) ?? [];

  assert.ok(preCodeBlocks.length > 0);
  for (const block of preCodeBlocks) {
    assert.match(block, /\b(?:language|lang)-[a-z0-9-]+/i);
  }
});

test('sitemap entries include lastmod values', async () => {
  const sitemap = await readBuilt('sitemap-0.xml');
  const entries = sitemap.match(/<url>.*?<\/url>/g) ?? [];

  assert.ok(entries.length > 0);
  for (const entry of entries) {
    assert.match(entry, /<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/);
  }
});

test('markdown sitemap is published', async () => {
  const sitemap = await readBuilt('sitemap.md');

  assert.match(sitemap, /^# Sitemap/m);
  assert.match(sitemap, /\/docs\/commands\/go\//);
});

test('Google Analytics is present on homepage and docs pages', async () => {
  const homepage = await readBuilt('index.html');
  const docs = await readBuilt('docs/index.html');

  assert.match(homepage, /G-EKPFFWY13G/);
  assert.match(docs, /G-EKPFFWY13G/);
});
