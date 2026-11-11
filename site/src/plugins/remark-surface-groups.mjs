// Wraps runs of adjacent code fences that target different surfaces (CLI, MCP,
// JavaScript, Python, Java) so the header picker can filter them. Sources stay
// plain Markdown: a fence's surface comes from title="<Surface>" or its language.
// A shell fence is CLI only when every command in it is a vibium command, so an
// install step next to library code is never hidden.

export const SURFACES = {
	cli: 'CLI',
	mcp: 'MCP',
	javascript: 'JavaScript',
	python: 'Python',
	java: 'Java',
};

const SHELL = new Set(['sh', 'bash', 'shell']);
const VIBIUM_COMMAND = /^(npx (-y )?)?vibium(\s|$)/;

const BY_LANG = {
	js: 'javascript',
	javascript: 'javascript',
	mjs: 'javascript',
	ts: 'javascript',
	typescript: 'javascript',
	py: 'python',
	python: 'python',
	java: 'java',
};

const BY_TITLE = Object.fromEntries(
	Object.entries(SURFACES).map(([key, label]) => [label.toLowerCase(), key])
);

const TITLE_RE = /\btitle="([^"]*)"/;

function isVibiumShell(node) {
	const commands = (node.value ?? '')
		.split('\n')
		.map((line) => line.trim())
		.filter((line, i, lines) => line && !line.startsWith('#') && !lines[i - 1]?.endsWith('\\'));
	return commands.length > 0 && commands.every((line) => VIBIUM_COMMAND.test(line));
}

export function surfaceOf(node) {
	if (node.type !== 'code') return undefined;
	const title = TITLE_RE.exec(node.meta ?? '')?.[1];
	const named = BY_TITLE[title?.trim().toLowerCase()];
	if (named) return named;
	const lang = (node.lang ?? '').toLowerCase();
	if (SHELL.has(lang)) return isVibiumShell(node) ? 'cli' : undefined;
	return BY_LANG[lang];
}

function wrap(run) {
	return {
		type: 'surfaceGroup',
		data: { hName: 'div', hProperties: { className: ['surface-group'] } },
		children: run.map(({ node, surface }) => {
			if (!TITLE_RE.test(node.meta ?? '')) {
				node.meta = `${node.meta ?? ''} title="${SURFACES[surface]}"`.trim();
			}
			return {
				type: 'surfaceBlock',
				data: {
					hName: 'div',
					hProperties: { className: ['surface-block'], dataSurface: surface },
				},
				children: [node],
			};
		}),
	};
}

function groupChildren(parent) {
	const out = [];
	let run = [];
	const flush = () => {
		if (run.length >= 2) out.push(wrap(run));
		else out.push(...run.map((entry) => entry.node));
		run = [];
	};
	for (const child of parent.children) {
		const surface = surfaceOf(child);
		if (surface && !run.some((entry) => entry.surface === surface)) {
			run.push({ node: child, surface });
			continue;
		}
		flush();
		if (surface) run.push({ node: child, surface });
		else out.push(child);
	}
	flush();
	parent.children = out;
}

function walk(node) {
	if (!Array.isArray(node.children)) return;
	for (const child of node.children) walk(child);
	groupChildren(node);
}

export default function remarkSurfaceGroups() {
	return (tree) => walk(tree);
}
