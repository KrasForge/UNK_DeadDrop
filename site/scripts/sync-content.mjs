import { cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const workspaceRoot = resolve(siteRoot, '..');
const seriesRoot = resolve(workspaceRoot, 'deliverables/blog-series');
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
for (const page of ['index.md', 'research-materials.md']) {
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
  .replaceAll('](assets/', '](../assets/')
  .replaceAll('](../preprint/evidence/', '](../../evidence/')
  .replaceAll('](../preprint/UNK_DeadDrop-Preprint.pdf)', '](../../downloads/UNK_DeadDrop-Preprint.pdf)')
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
await cp(resolve(seriesRoot, 'assets'), resolve(docsRoot, 'assets'), { recursive: true });
await cp(resolve(workspaceRoot, 'deliverables/preprint/evidence'), resolve(publicRoot, 'evidence'), {
  recursive: true,
  filter: (source) => !source.endsWith('build.py')
});
await copyFile(
  resolve(workspaceRoot, 'deliverables/preprint/UNK_DeadDrop-Preprint.pdf'),
  resolve(publicRoot, 'downloads/UNK_DeadDrop-Preprint.pdf')
);
await copyFile(
  resolve(seriesRoot, 'UNK_DeadDrop-Blog-Series.zip'),
  resolve(publicRoot, 'downloads/UNK_DeadDrop-Blog-Series.zip')
);

const companionFiles = [
  'LICENSE',
  'requirements-dev.txt',
  'tests/test_detections.py',
  'tests/test_blog_boundaries.py',
  'rules/yara/deaddrop_wallet_agent.yar',
  'rules/sigma/linux_google_agent_persistence.yml',
  'rules/sigma/windows_capture_task.yml'
];

for (const relativePath of companionFiles) {
  await copyFile(
    resolve(workspaceRoot, 'deliverables/public-repository', relativePath),
    resolve(publicRoot, 'companion', relativePath)
  );
}

console.log(`Synced ${sourceFiles.length} articles and their public evidence.`);
