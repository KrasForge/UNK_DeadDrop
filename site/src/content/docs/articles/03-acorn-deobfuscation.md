---
title: "Parsing Without Executing: JavaScript Deobfuscation with Acorn"
description: "Rebuilding an AES key from sixteen obfuscated fragments with Acorn, and proving it with authenticated decryption without ever running the malicious extension."
lastUpdated: 2026-10-25
sidebar:
  order: 3
---


The VSIX loader did not contain a readily searchable AES key. It assembled one from sixteen fragments: nine returned by obfuscated decoder calls and seven written as literals. Resolving those calls required mapping wrapper functions and a rotated string table. My first shortcut failed because one wrapper declared an intermediate value before returning. A later attempt produced five plausible but incorrect array rotations. Then the correct encrypted-blob layout appeared to fail because `openssl enc` was the wrong tool for the authentication step.

The final result was three authenticated plaintext files, recovered without executing the extension. This post follows the checks that distinguished a valid decode from a plausible-looking result. [Proofpoint's report](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) already describes the key and Windows architecture; the focus here is the static analysis method.

> **Key Takeaways**
>
> - The loader assembled its AES key from nine decoder calls and seven literals, hidden behind wrapper functions and a rotated string table.
> - Acorn parses the wrappers into a syntax tree without executing them, which avoids the regex failure that missed a declaration before a return statement.
> - The correct rotation, with rotation offsets of 391 and 261, decoded fifteen of fifteen tested call sites, against three for the runner-up.
> - The decisive check was authentication: all three payloads passed once Node's crypto library replaced `openssl enc` for the GCM workflow.

## Start with the calls around the key expression

The key assignment combines literals with calls to several wrapper functions, and reading any one of those calls in isolation is not enough, because a wrapper may change the index, reorder its arguments or add an offset before it ever invokes the underlying decoder. The July analysis identified seven wrappers in the bootstrap and five in `extension.js`, and for each of them I needed to map out three things:

```text
Which argument supplies the string-table index?
Which argument supplies the decoder key?
What offset is applied before the underlying call?
```

A regex that expects every wrapper to return a decoder call immediately will miss any function that first declares an intermediate value, and that is precisely where the original pass failed. [Acorn](https://github.com/acornjs/acorn) fixes this structural problem by representing both statements in the syntax tree, and although it does not solve the decoder automatically, it gives the analysis something far more reliable to work with than text patterns.

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

![The static recovery workflow](../assets/03-deobfuscation.png)

*Figure 1. Static reconstruction followed by authenticated decryption. Parsing and decoding the retained bytes did not invoke the extension's activation code.*

### One readable string was not enough

The string array had been rotated, so a valid-looking index could point to the wrong encoded element until the array order was resolved. An early search used one expected `crypt` anchor and produced five misleading candidates. The stronger approach compared each rotation against all resolved call sites.

The recorded offsets were 391 for the extension and 261 for the bootstrap. The selected candidate produced printable decodes at 15 of 15 tested sites; the runner-up produced 3 of 15. That gap was useful, but printability remained a heuristic. The next checks were whether each string fit its call context and whether the key fragments could be reconstructed in source order. The encrypted payloads would provide a stronger validation.

### Rebuilding the sixteen fragments

The key expression combined nine decoder results with seven literal fragments. Recovering their values was only half the work; the fragments also had to be concatenated in the original order, including values nested inside parenthesized additions.

A small bounded evaluator handled only string literals and already-decoded values. It never ran the sample code, activated the extension or contacted a server. I have omitted the key itself. Its expected length would be weak evidence; the stronger result is that the recovered key authenticated the retained encrypted payloads.

## From authenticated payloads to triage

The loader specified the encrypted blob layout directly:

```text
bytes  0–11    initialization vector
bytes 12–27    authentication tag
bytes 28–end   ciphertext
```

The first attempt with this layout appeared to fail. The historical analysis attributes that result to using `openssl enc` for a GCM authentication workflow. Switching to [Node's cryptographic library](https://nodejs.org/api/crypto.html) allowed the stored tag to be checked correctly. This tooling error could have sent the analysis back into the decoder: a failed command did not show that the key, rotation or field boundaries were wrong.

With the corrected operation, all three payloads passed authentication: `detect_malware.py` (60,054 bytes), the browser-related decryption component; `windows-agent-node.js` (56,093 bytes), the Windows collection agent; and `windows-js-pipeline.js` (32,324 bytes), the collection and elevation coordinator.

The plaintext was readable, commented source, which made the next analysis easier. The comments did not establish successful decryption; authentication tied the plaintext to its encrypted input under the recovered parameters. Nor did authentication establish that the payloads ran or collected data. Those are runtime questions. This recovery was completed in July and was not repeated while drafting this series.

### The smaller scanner built afterward

The companion scanner uses Acorn as well, but it solves a rather different problem, finding selected clipboard-write calls and campaign markers, returning their source locations along with an input hash, and folding a limited set of literal string expressions. A literal addition, for example, can be resolved without evaluating arbitrary JavaScript, whereas a variable reference or function call remains unresolved, and the scanner makes no attempt to reproduce the wrapper mapping or rotated-array recovery described above. Its implementation limits input to 8 MiB and bounds nested literal folding, and the October validation record reports eight AST tests passing, while static spot checks found two clipboard-write sites in the lure bundle and five campaign-marker findings in the larger JavaScript collector. Those results make it useful for triage rather than a universal deobfuscator, and because parsing remains an in-process operation, a byte limit alone is no guarantee against expensive adversarial syntax.

In this case, the complete recovery depended on several checks working together:

1. structural parsing of the wrappers;
2. mapping each wrapper's index, key and offset;
3. agreement across call sites for the chosen rotation;
4. exact fragment ordering in the key expression;
5. authenticated decryption of the payloads.

It was that last step that proved most valuable, because instead of stopping at source that looked reasonable, the analysis had a cryptographic test of the recovered bytes.

### Recovered-file hashes

```text
detect_malware.py
4c3fdd86a59d52a0e29f472666cbf9472b6fd83c38ef2a4b547f31c72b8ee87e

windows-agent-node.js
e5b7d6411d0c95da047185d94fca98d454b73df2e7f46f2753e212af2ca45da5

windows-js-pipeline.js
bf820623e8deaa37092650c7fae594e56b8d81c27b541419006cca2d0536353b
```
