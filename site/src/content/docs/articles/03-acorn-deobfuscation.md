---
title: "Parsing Without Executing: JavaScript Deobfuscation with Acorn"
description: "Rebuilding an AES key from sixteen obfuscated fragments with Acorn, and proving it with authenticated decryption without ever running the malicious extension."
lastUpdated: 2026-10-25
sidebar:
  order: 3
---


The VSIX loader assembled one AES key from sixteen fragments: nine decoder calls and seven literals. Recovering it required mapping wrapper functions and a rotated string table. A simple regex missed a wrapper that declared an intermediate value before returning, and five plausible rotations failed checks across the call sites.

The final result was three authenticated plaintext files, recovered without executing the extension. This post follows the checks that distinguished a valid decode from a plausible-looking result. [Proofpoint's report](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) already describes the key and Windows architecture; the focus here is the static analysis method.

> **Key Takeaways**
>
> - The loader assembled its AES key from nine decoder calls and seven literals, hidden behind wrapper functions and a rotated string table.
> - Acorn parses the wrappers into a syntax tree without executing them, which avoids the regex failure that missed a declaration before a return statement.
> - The correct rotation, with rotation offsets of 391 and 261, decoded fifteen of fifteen tested call sites, against three for the runner-up.
> - The decisive check was authentication: all three payloads passed once Node's crypto library replaced `openssl enc` for the GCM workflow.

## Start with the calls around the key expression

The key assignment combines literals with calls to several wrapper functions. A wrapper may change the index, reorder its arguments or add an offset before invoking the underlying decoder, so each call must be traced through its wrapper. The July analysis identified seven wrappers in the bootstrap and five in `extension.js`. Each needed three fields mapped:

```text
Which argument supplies the string-table index?
Which argument supplies the decoder key?
What offset is applied before the underlying call?
```

A regex that expects every wrapper to return a decoder call immediately can miss a function that first declares an intermediate value. [Acorn](https://github.com/acornjs/acorn) represents both statements in the syntax tree. It does not solve the decoder automatically, but it provides a more reliable structure to inspect than text patterns.

### Parsing an obfuscated wrapper

The small example below is invented to illustrate the relevant shape, and it parses source containing a wrapper without ever calling that wrapper:

```javascript
import { parse } from 'acorn';

const source = `
function wrapper(index, key) {
  const adjusted = index - 17;
  return decode(adjusted, key);
}
`;

const ast = parse(source, {
  ecmaVersion: 2022,
  sourceType: 'script',
  locations: true
});

const fn = ast.body[0];
const returned = fn.body.body.find(
  node => node.type === 'ReturnStatement'
);

console.log(fn.type, returned.argument.type);
// FunctionDeclaration CallExpression
```

`decode` is undefined, but parsing does not require it to exist. Acorn reads the program as a string and returns the structure of declarations and expressions; it does not resolve or run them.

The workflow never imported or evaluated the target, or ran the extension in a VM. It recovered selected transformations from the syntax tree and implemented those separately. This remains sample-specific analysis: an AST can describe arbitrary behavior, and parsing does not prove what a program will do. The narrower goal was to recover the index and key transformations used by these wrappers.

![From obfuscated syntax to authenticated files](../assets/03-deobfuscation.png)

*Figure 1. From obfuscated syntax to authenticated files. Parsing is not execution; the companion scanner does not implement full recovery.*


The string array had been rotated, so a valid-looking index could point to the wrong encoded element until the array order was resolved. Searching from one expected `crypt` anchor yielded five plausible rotations. Comparing each rotation against all resolved call sites narrowed the candidates.

The recorded offsets were 391 for the extension and 261 for the bootstrap. The selected candidate produced printable decodes at 15 of 15 tested sites; the runner-up produced 3 of 15. That gap was useful, but printability remained a heuristic. The next checks were whether each string fit its call context and whether the key fragments could be reconstructed in source order. The encrypted payloads would provide a stronger validation.

### Rebuilding the sixteen fragments

The key expression combined nine decoder results with seven literal fragments. Recovering their values was only half the work; the fragments also had to be concatenated in the original order, including values nested inside parenthesized additions.

A small bounded evaluator handled only string literals and already-decoded values. It never ran the sample code, activated the extension or contacted a server. The key's expected length would be weak evidence; successful authentication of the retained encrypted payloads provides a stronger check.

## From authenticated payloads to triage

The loader specified the encrypted blob layout directly:

```text
bytes  0–11    initialization vector
bytes 12–27    authentication tag
bytes 28–end   ciphertext
```

The initial `openssl enc` attempt failed because that command did not provide the required GCM authentication check. Switching to [Node's cryptographic library](https://nodejs.org/api/crypto.html) allowed the stored tag to be verified. The failed command did not show that the key, rotation or field boundaries were wrong.

With the corrected operation, all three payloads passed authentication: `detect_malware.py` (60,054 bytes), the browser-related decryption component; `windows-agent-node.js` (56,093 bytes), the Windows collection agent; and `windows-js-pipeline.js` (32,324 bytes), the collection and elevation coordinator.

All three payloads decrypted to readable, commented source. Authentication tied each plaintext to its encrypted input under the recovered parameters, but did not establish that a payload ran or collected data. Those remain runtime questions.

### The smaller scanner built afterward

The companion scanner also uses Acorn, but for a narrower task: it locates selected clipboard-write calls and campaign markers, reports source locations with an input hash, and folds a limited set of literal strings. It can resolve literal additions but leaves variable references and function calls unresolved. It does not reproduce the wrapper mapping or rotated-array recovery described above.

The scanner limits input to 8 MiB and bounds nested literal folding. Eight AST tests cover its parser behavior. Static spot checks found two clipboard-write sites in the lure and five campaign markers in the larger collector. These results support triage use, not general deobfuscation. Because parsing runs in process, the byte limit alone cannot prevent expensive adversarial syntax.

Confidence in the recovery came from several checks working together:

1. structural parsing of the wrappers;
2. mapping each wrapper's index, key and offset;
3. agreement across call sites for the chosen rotation;
4. exact fragment ordering in the key expression;
5. authenticated decryption of the payloads.

Authenticated decryption was decisive: it tested the recovered bytes rather than whether the source merely looked plausible.

```text
detect_malware.py
4c3fdd86a59d52a0e29f472666cbf9472b6fd83c38ef2a4b547f31c72b8ee87e

windows-agent-node.js
e5b7d6411d0c95da047185d94fca98d454b73df2e7f46f2753e212af2ca45da5

windows-js-pipeline.js
bf820623e8deaa37092650c7fae594e56b8d81c27b541419006cca2d0536353b
```
