import assert from 'node:assert/strict';
import { readdir, readFile, stat } from 'node:fs/promises';
import test from 'node:test';

import { surfaceOf } from '../src/plugins/remark-surface-groups.mjs';

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

const SURFACES = ['cli', 'mcp', 'javascript', 'python', 'java'];
const MOVED = {
  'docs/client-libraries': '/docs/libraries/',
  'docs/mcp-integration': '/docs/mcp/',
  'docs/getting-started': '/docs/cli/',
};

// Every Starlight page as a dist-relative directory, e.g. "docs/libraries/python".
async function docsPages() {
  const entries = await readdir(new URL('docs/', dist), { recursive: true });
  return entries
    .filter((entry) => entry.endsWith('index.html'))
    .map((entry) => `docs/${entry}`.replace(/\/?index\.html$/, ''))
    .filter((page) => page !== 'docs' && !(page in MOVED));
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

test('AGENTS.md is published with the required sections', async () => {
  const md = await readBuilt('AGENTS.md');

  assert.match(md, /^## Installation$/m);
  assert.match(md, /^## Configuration$/m);
  assert.match(md, /^## Usage$/m);
});

test('llms.txt list links all point to markdown files', async () => {
  const txt = await readBuilt('llms.txt');
  const links = [...txt.matchAll(/^- \[[^\]]+\]\(([^)]+)\)/gm)].map((m) => m[1]);

  assert.ok(links.length > 0);
  for (const link of links) {
    assert.match(link, /\.(md|mdx)$/, `non-markdown link in llms.txt: ${link}`);
  }
});

test('well-known agent discovery files are published', async () => {
  const index = JSON.parse(await readBuilt('.well-known/agent-skills/index.json'));
  assert.ok(Array.isArray(index.skills) && index.skills.length >= 2);
  for (const skill of index.skills) {
    assert.match(skill.sha256, /^[0-9a-f]{64}$/);
    assert.equal(await exists(skill.url.replace(/^\//, '')), true);
  }

  const catalog = JSON.parse(await readBuilt('.well-known/api-catalog'));
  assert.ok(Array.isArray(catalog.linkset) && catalog.linkset.length > 0);

  const robots = await readBuilt('robots.txt');
  assert.match(robots, /^Content-Signal: search=yes, ai-input=yes, ai-train=yes$/m);
});

test('markdown mirrors carry the documented vibium version', async () => {
  const md = await readBuilt('docs/introduction.md');

  assert.match(md, /^doc_version: "vibium \d+\.\d+\.\d+"$/m);
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
  const pages = await docsPages();
  assert.ok(pages.length > 90);
  for (const page of pages) {
    assert.equal(await exists(`${page}.md`), true, `no Markdown mirror for /${page}/`);
  }
});

test('every docs page links to a Markdown alternate that exists', async () => {
  for (const page of await docsPages()) {
    const html = await readBuilt(`${page}/index.html`);
    const href = html.match(/<link rel="alternate" type="text\/markdown" href="\/([^"]+)">/)?.[1];
    assert.ok(href, `no Markdown alternate on /${page}/`);
    assert.equal(await exists(href), true, `dead Markdown alternate on /${page}/: /${href}`);
  }
});

test('every docs page links to the glossary', async () => {
  for (const page of await docsPages()) {
    const html = await readBuilt(`${page}/index.html`);
    assert.match(html, /<a href="\/docs\/concepts\/">Glossary<\/a>/, `no glossary link on /${page}/`);
  }
});

test('llms.txt lists every docs page and every link resolves', async () => {
  const text = await readBuilt('llms.txt');
  const links = [...text.matchAll(/\]\(https:\/\/vibium\.com\/([^)]+)\)/g)].map((match) => match[1]);
  for (const link of links) {
    assert.equal(await exists(link), true, `llms.txt link does not resolve: /${link}`);
  }
  for (const page of await docsPages()) {
    assert.ok(
      links.includes(`llms/${page}.md`) || links.includes(`llms/${page}/index.md`),
      `/${page}/ is missing from llms.txt`
    );
  }
  for (const section of ['CLI', 'MCP', 'JavaScript', 'Python', 'Java']) {
    assert.match(text, new RegExp(`^## ${section}$`, 'm'));
  }
});

test('moved pages redirect and keep a Markdown pointer', async () => {
  for (const [page, target] of Object.entries(MOVED)) {
    const html = await readBuilt(`${page}/index.html`);
    assert.ok(html.includes(`url=${target}`), `/${page}/ does not redirect to ${target}`);
    for (const stub of [`${page}.md`, `llms/${page}.md`]) {
      assert.match(await readBuilt(stub), /This page moved to \[/, `no pointer at /${stub}`);
    }
  }
});

test('surface sections are published', async () => {
  for (const page of [
    'docs/cli',
    'docs/mcp',
    'docs/mcp/setup',
    'docs/mcp/tools',
    'docs/libraries',
    'docs/libraries/javascript',
    'docs/libraries/javascript/api',
    'docs/libraries/python',
    'docs/libraries/python/api',
    'docs/libraries/java',
    'docs/libraries/java/api',
    'docs/reference/api-matrix',
  ]) {
    assert.equal(await exists(`${page}/index.html`), true, `missing /${page}/`);
  }
});

test('api.json maps each operation across the five surfaces', async () => {
  const api = JSON.parse(await readBuilt('api.json'));
  assert.match(api.stableVersion, /^\d+\.\d+\.\d+$/);
  assert.deepEqual(api.surfaces, SURFACES);
  assert.ok(api.operations.length > 150);
  for (const op of api.operations) {
    for (const surface of SURFACES) {
      assert.ok(surface in op, `operation ${op.id} has no ${surface} field`);
    }
  }
  const go = api.operations.find((op) => op.cli === 'vibium go <url>');
  assert.equal(go.mcp, 'browser_navigate');
  assert.equal(go.python, 'page.go(url)');
});

test('mcp-tools.json carries the server tool schemas', async () => {
  const { tools } = JSON.parse(await readBuilt('mcp-tools.json'));
  assert.ok(tools.length > 50);
  const navigate = tools.find((tool) => tool.name === 'browser_navigate');
  assert.deepEqual(navigate.inputSchema.required, ['url']);
  const page = await readBuilt('docs/mcp/tools.md');
  for (const tool of tools) {
    assert.ok(page.includes(`### \`${tool.name}\``), `tools.md has no section for ${tool.name}`);
  }
});

test('sitemap announces the JSON endpoints for agents', async () => {
  const sitemap = await readBuilt('sitemap-0.xml');
  for (const name of ['commands.json', 'api.json', 'mcp-tools.json']) {
    assert.ok(sitemap.includes(`<loc>https://vibium.com/${name}</loc>`), `${name} is not in the sitemap`);
  }
});

test('api-catalog entries point at published files', async () => {
  const catalog = JSON.parse(await readBuilt('.well-known/api-catalog'));
  for (const entry of catalog.linkset) {
    const path = new URL(entry.anchor).pathname.slice(1);
    assert.equal(await exists(path), true, `api-catalog anchor is not published: /${path}`);
  }
});

test('surface picker ships on docs pages and hides nothing by default', async () => {
  const html = await readBuilt('docs/installation/index.html');
  assert.match(html, /<vibium-surface-select/);
  assert.match(html, /<script src="\/surface\.js"><\/script>/);
  assert.equal(await exists('surface.js'), true);
  for (const surface of ['all', ...SURFACES]) {
    assert.match(html, new RegExp(`<option value="${surface}"`));
  }
  assert.doesNotMatch(html, /<html[^>]*data-surface=/);
});

test('surface groups keep every surface in the HTML and in the mirror', async () => {
  for (const page of ['docs/installation', 'docs/quickstart']) {
    const html = await readBuilt(`${page}/index.html`);
    const blocks = [...html.matchAll(/class="surface-block" data-surface="([a-z]+)"/g)];
    assert.deepEqual(blocks.map((match) => match[1]), SURFACES, `surface group on /${page}/`);

    const mirror = await readBuilt(`${page}.md`);
    const fences = [...mirror.matchAll(/^```(\w+)(.*)$/gm)].map(([, lang, meta]) =>
      surfaceOf({ type: 'code', lang, meta })
    );
    for (const surface of SURFACES) {
      assert.ok(fences.includes(surface), `${page}.md has no ${surface} example`);
    }
  }
});

test('a shell fence is CLI only when it runs vibium commands', () => {
  const shell = (value, meta) => surfaceOf({ type: 'code', lang: 'sh', meta, value });
  assert.equal(shell('vibium go https://example.com\nvibium text'), 'cli');
  assert.equal(shell('# open a page\nnpx -y vibium go https://example.com'), 'cli');
  assert.equal(shell('pip install vibium'), undefined);
  assert.equal(shell('npm install vibium\nvibium go https://example.com'), undefined);
  assert.equal(shell('pip install vibium', 'title="Python"'), 'python');
});

test('per-surface llms bundles carry shared docs plus their surface', async () => {
  const marker = {
    cli: '--- file: docs/commands/go.md ---',
    mcp: '--- file: docs/mcp/setup.md ---',
    javascript: '--- file: docs/libraries/javascript/index.md ---',
    python: '--- file: docs/libraries/python/index.md ---',
    java: '--- file: docs/libraries/java/index.md ---',
  };
  for (const surface of SURFACES) {
    const bundle = await readBuilt(`llms-${surface}.txt`);
    assert.ok(bundle.includes('--- file: docs/quickstart.md ---'), `llms-${surface}.txt lacks shared docs`);
    for (const other of SURFACES) {
      assert.equal(
        bundle.includes(marker[other]),
        other === surface,
        `llms-${surface}.txt and ${other} pages`
      );
    }
  }
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
