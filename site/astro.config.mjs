import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const site = process.env.SITE_URL ?? 'https://vibium.com';
const base = normalizeBase(process.env.BASE_PATH ?? '/');

function normalizeBase(value) {
    const trimmed = value.trim();

    if (!trimmed || trimmed === '/') {
        return '/';
    }

    return `/${trimmed.replace(/^\/+|\/+$/g, '')}`;
}

function withBase(path) {
    const prefix = base === '/' ? '' : base;
    return `${prefix}/${path.replace(/^\/+/, '')}`;
}

export default defineConfig({
    site,
    base,
    integrations: [
        starlight({
            title: 'Vibium',
            logo: {
                light: './src/assets/brand/logo-light.png',
                dark: './src/assets/brand/logo-dark.webp',
                replacesTitle: true,
                alt: 'Vibium',
            },
            // Points Starlight's default <link rel="shortcut icon"> at a real file
            // so it doesn't 404 to the built-in /favicon.svg default. The full
            // multi-size set is wired explicitly in `head` below.
            favicon: withBase('/favicon.png'),
            social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/VibiumDev/vibium' }],
            customCss: [
                './src/styles/colors-and-type.css',
                './src/styles/starlight-vibium.css',
            ],
            components: {
                Head: './src/components/starlight/Head.astro',
                ThemeProvider: './src/components/starlight/ThemeProvider.astro',
                ThemeSelect: './src/components/starlight/ThemeSelect.astro',
            },
            sidebar: [
                { label: 'Introduction', slug: 'docs/introduction' },
                { label: 'Installation', slug: 'docs/installation' },
                { label: 'Quickstart', slug: 'docs/quickstart' },
                { label: 'Getting Started', slug: 'docs/getting-started' },
                { label: 'Tutorial', slug: 'docs/tutorial' },
                { label: 'Glossary', slug: 'docs/concepts' },
                { label: 'MCP Integration', slug: 'docs/mcp-integration' },
                { label: 'Client Libraries', slug: 'docs/client-libraries' },
                { label: 'Troubleshooting', slug: 'docs/troubleshooting' },
                { label: 'FAQ', slug: 'docs/faq' },
                { label: 'Contributing', slug: 'docs/contributing' },
                { label: 'Command Reference', autogenerate: { directory: 'docs/commands', collapsed: true } },
            ],
        }),
    ],
    vite: {
        server: { allowedHosts: ["oberon.orca-arctic.ts.net", "localhost", "0.0.0.1", "127.0.0.1"] },
    }
});
