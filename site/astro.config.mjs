import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const repository = process.env.GITHUB_REPOSITORY ?? '';
const [repositoryOwner, repositoryNamePart] = repository.split('/');
const owner = repositoryOwner || 'example';
const repositoryName = repositoryNamePart || 'UNK_DeadDrop';
const isRootPagesRepository = repositoryName.toLowerCase() === `${owner}.github.io`.toLowerCase();
const site = process.env.SITE_URL ?? `https://${owner}.github.io`;
const base = process.env.BASE_PATH ?? (isRootPagesRepository ? '/' : `/${repositoryName}`);

export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: 'UNK_DeadDrop',
      description: 'A technical investigation of developer-targeted phishing, collection tooling, infrastructure, and detection engineering.',
      favicon: 'favicon.svg',
      customCss: ['./src/styles/custom.css'],
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 2 },
      lastUpdated: true,
      credits: true,
      sidebar: [
        { label: 'Series overview', link: '/' },
        {
          label: 'Delivery and collection',
          items: [
            { label: '1. Clipboard substitution', link: '/articles/01-clickfix-clipboard-manipulation/' },
            { label: '2. VS Code task', link: '/articles/02-vsix-editor-execution/' },
            { label: '3. AES key recovery', link: '/articles/03-acorn-deobfuscation/' },
            { label: '4. Browser and wallet files', link: '/articles/04-credential-wallet-collection/' },
            { label: '5. Screen capture', link: '/articles/05-screen-capture-analysis/' }
          ]
        },
        {
          label: 'Infrastructure and operations',
          items: [
            { label: '6. GitLab resolver', link: '/articles/06-gitlab-dead-drop-infrastructure/' },
            { label: '7. Target pools', link: '/articles/07-developer-target-harvesting/' },
            { label: '8. rms-platform', link: '/articles/08-administration-platform/' },
            { label: '9. ECHOES archives', link: '/articles/09-echoes-lineage-image-provenance/' },
            { label: 'Historical indicators', link: '/indicators/' },
            { label: 'Sample and repository artifacts', link: '/artifacts/' }
          ]
        },
        {
          label: 'Synthesis and defense',
          items: [
            { label: '10. Three lure paths', link: '/articles/10-investigation-connections/' },
            { label: '11. YARA replay', link: '/articles/11-detection-engineering/' },
            { label: '12. Overlord markers', link: '/articles/12-framework-and-collection-boundary/' },
            { label: '13. Scanner benchmark', link: '/articles/13-scanner-registry-benchmark/' },
            { label: '14. Recovery variants', link: '/articles/14-scanner-recovery-and-bypasses/' }
          ]
        },
        { label: 'Research materials', link: '/research-materials/' }
      ]
    })
  ]
});
