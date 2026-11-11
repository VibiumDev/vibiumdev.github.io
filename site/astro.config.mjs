import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightSidebarTopics from 'starlight-sidebar-topics';
import remarkSurfaceGroups from './src/plugins/remark-surface-groups.mjs';

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
    redirects: {
        '/docs/client-libraries': withBase('/docs/libraries/'),
        '/docs/mcp-integration': withBase('/docs/mcp/'),
        '/docs/getting-started': withBase('/docs/cli/'),
    },
    markdown: { remarkPlugins: [remarkSurfaceGroups] },
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
                LanguageSelect: './src/components/starlight/SurfaceSelect.astro',
                Footer: './src/components/starlight/Footer.astro',
            },
            plugins: [
                starlightSidebarTopics([
                    {
                        label: 'Start',
                        link: '/docs/introduction/',
                        items: [
                            { label: 'Introduction', slug: 'docs/introduction' },
                            { label: 'Installation', slug: 'docs/installation' },
                            { label: 'Quickstart', slug: 'docs/quickstart' },
                            { label: 'Glossary', slug: 'docs/concepts' },
                            { label: 'Troubleshooting', slug: 'docs/troubleshooting' },
                            { label: 'FAQ', slug: 'docs/faq' },
                            { label: "What's in Nightly", slug: 'docs/nightly' },
                            { label: 'Contributing', slug: 'docs/contributing' },
                        ],
                    },
                    {
                        label: 'Guides',
                        link: '/docs/tutorial/',
                        items: [
                            { label: 'Tutorial', slug: 'docs/tutorial' },
                            { label: 'Run and Check', slug: 'docs/run-and-check' },
                            { label: 'Model Providers', slug: 'docs/ai-providers' },
                            { label: 'Using Firefox', slug: 'docs/using-firefox' },
                            { label: 'Concurrent Sessions', slug: 'docs/sessions' },
                            { label: 'Recording', slug: 'docs/recording' },
                            { label: 'Scripting and Agents', slug: 'docs/scripting' },
                        ],
                    },
                    {
                        label: 'CLI',
                        link: '/docs/cli/',
                        items: [
                            { label: 'Getting Started', slug: 'docs/cli' },
                            { label: 'Command Reference', autogenerate: { directory: 'docs/commands' } },
                        ],
                    },
                    {
                        label: 'MCP',
                        link: '/docs/mcp/',
                        items: [
                            { label: 'Overview', slug: 'docs/mcp' },
                            { label: 'Client Setup', slug: 'docs/mcp/setup' },
                        ],
                    },
                    {
                        label: 'Libraries',
                        link: '/docs/libraries/',
                        items: [
                            { label: 'Overview', slug: 'docs/libraries' },
                            { label: 'JavaScript', slug: 'docs/libraries/javascript' },
                            { label: 'Python', slug: 'docs/libraries/python' },
                            { label: 'Java', slug: 'docs/libraries/java' },
                        ],
                    },
                ]),
            ],
        }),
    ],
    vite: {
        server: { allowedHosts: ["oberon.orca-arctic.ts.net", "localhost", "0.0.0.1", "127.0.0.1"] },
    }
});
