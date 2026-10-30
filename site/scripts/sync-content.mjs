import { cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const workspaceRoot = resolve(siteRoot, '..');
const seriesRoot = resolve(workspaceRoot, 'deliverables/blog-series');
const companionRoot = resolve(workspaceRoot, 'deliverables/unk-deaddrop-companion');
const docsRoot = resolve(siteRoot, 'src/content/docs');
const contentRoot = resolve(siteRoot, 'content');
const generatedRoot = resolve(docsRoot, 'articles');
const publicRoot = resolve(siteRoot, 'public');
const repository = process.env.GITHUB_REPOSITORY ?? '';
const [repositoryOwnerPart, repositoryNamePart] = repository.split('/');
const repositoryOwner = repositoryOwnerPart || 'example';
const repositoryName = repositoryNamePart || 'UNK_DeadDrop';
const isRootPagesRepository = repositoryName.toLowerCase() === `${repositoryOwner}.github.io`.toLowerCase();
const configuredBase = process.env.BASE_PATH ?? (isRootPagesRepository ? '/' : `/${repositoryName}`);
const basePrefix = configuredBase === '/' ? '' : configuredBase;

const sourceFiles = (await readdir(seriesRoot))
  .filter((name) => /^\d{2}-.*\.md$/.test(name))
  .sort();

await mkdir(docsRoot, { recursive: true });
for (const page of ['index.md', 'research-materials.md', 'about.md']) {
  const template = await readFile(resolve(contentRoot, page), 'utf8');
  await writeFile(resolve(docsRoot, page), template.replaceAll('__BASE_PATH__', basePrefix));
}

await rm(generatedRoot, { recursive: true, force: true });
await mkdir(generatedRoot, { recursive: true });

const yamlValue = (frontmatter, key) => {
  const match = frontmatter.match(new RegExp(`^${key}:\\s*["']?(.*?)["']?\\s*$`, 'm'));
  return match?.[1] ?? '';
};

const rewriteLinks = (body) => body
  .replace(/\]\(assets\/([^\s)]+\.svg)\)/g, `](${basePrefix}/diagrams/$1)`)
  .replaceAll('](assets/', '](../assets/')
  .replaceAll('](../preprint/evidence/', '](../../evidence/')
  .replaceAll('](../preprint/UNK_DeadDrop-Preprint.pdf)', '](../../downloads/UNK_DeadDrop-Preprint.pdf)')
  .replaceAll('](../scanner-paper/UNK-Scanner-Paper.pdf)', '](../../downloads/UNK-Scanner-Paper.pdf)')
  .replaceAll('](historical-indicators.md)', '](../../indicators/)')
  .replaceAll('](artifact-reference.md)', '](../../artifacts/)')
  .replaceAll('](../public-repository/', '](../../companion/')
  .replaceAll('```yara', '```text')
  .replace(/\]\((\d{2}-[a-z0-9-]+)\.md\)/g, '](../$1/)')
  .replaceAll('](README.md)', '](/)');

for (const [index, fileName] of sourceFiles.entries()) {
  const source = await readFile(resolve(seriesRoot, fileName), 'utf8');
  const match = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) throw new Error(`Missing frontmatter in ${fileName}`);

  const [, frontmatter, body] = match;
  const title = yamlValue(frontmatter, 'title');
  const description = yamlValue(frontmatter, 'description');
  const date = yamlValue(frontmatter, 'date');
  const slug = fileName.replace(/\.md$/, '');
  const output = `---\ntitle: ${JSON.stringify(title)}\ndescription: ${JSON.stringify(description)}\nlastUpdated: ${date}\nsidebar:\n  order: ${index + 1}\n---\n\n${rewriteLinks(body)}`;
  await writeFile(resolve(generatedRoot, `${slug}.md`), output);
}

const copyFile = async (source, destination) => {
  await mkdir(dirname(destination), { recursive: true });
  await cp(source, destination);
};

await rm(resolve(publicRoot, 'assets'), { recursive: true, force: true });
await rm(resolve(publicRoot, 'evidence'), { recursive: true, force: true });
await rm(resolve(publicRoot, 'companion'), { recursive: true, force: true });
await rm(resolve(publicRoot, 'downloads'), { recursive: true, force: true });

await rm(resolve(docsRoot, 'assets'), { recursive: true, force: true });
await cp(resolve(seriesRoot, 'assets'), resolve(docsRoot, 'assets'), {
  recursive: true,
  filter: (source) => !source.endsWith('.md') && !source.endsWith('.json')
});
await mkdir(resolve(publicRoot, 'diagrams'), { recursive: true });
for (const name of await readdir(resolve(seriesRoot, 'assets'))) {
  if (name.endsWith('.svg')) await cp(resolve(seriesRoot, 'assets', name), resolve(publicRoot, 'diagrams', name));
}
await cp(resolve(workspaceRoot, 'deliverables/preprint/evidence'), resolve(publicRoot, 'evidence'), {
  recursive: true,
  filter: (source) => !source.endsWith('build.py')
});
await copyFile(
  resolve(workspaceRoot, 'deliverables/preprint/UNK_DeadDrop-Preprint.pdf'),
  resolve(publicRoot, 'downloads/UNK_DeadDrop-Preprint.pdf')
);
await copyFile(
  resolve(workspaceRoot, 'deliverables/scanner-paper/UNK-Scanner-Paper.pdf'),
  resolve(publicRoot, 'downloads/UNK-Scanner-Paper.pdf')
);
await copyFile(
  resolve(seriesRoot, 'UNK_DeadDrop-Blog-Series.zip'),
  resolve(publicRoot, 'downloads/UNK_DeadDrop-Blog-Series.zip')
);

const copyCompanionTree = async (source, destination) => {
  await mkdir(destination, { recursive: true });
  for (const entry of await readdir(source, { withFileTypes: true })) {
    if (['.git', '.venv', 'node_modules', '__pycache__'].includes(entry.name)) continue;
    const from = resolve(source, entry.name);
    const to = resolve(destination, entry.name);
    if (entry.isDirectory()) await copyCompanionTree(from, to);
    else if (entry.isFile()) await copyFile(from, to);
  }
};

await copyCompanionTree(companionRoot, resolve(publicRoot, 'companion'));

console.log(`Synced ${sourceFiles.length} articles and their public evidence.`);
