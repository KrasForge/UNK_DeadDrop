# Rotation example

The input program imports `child_process` and prints a URL alongside the type of `spawn`:

```javascript
const cp = require("child_process");
const url = "https://example.invalid/setup";
console.log(url, typeof cp.spawn);
```

The program never calls `spawn`. Its URL uses the reserved `.invalid` domain.

With rotation enabled, javascript-obfuscator 5.9.0 (seed 19, plain strings) replaces the four application strings with decoder calls. The output contains thirteen array entries. Nine are numeric-prefix strings used by the startup checksum.

The generated program is shown in two blocks below, with declarations placed before their callers. It is separate from the input program above.

```javascript
function W() {
    const a = [
        "416VKoFbO", "68MVpWjx", "spawn",
        "3664340cHkggg", "272844EERGGb",
        "2935488qIidkn", "28811hhXjYz", "2767497Wyegbc",
        "https://example.invalid/setup",
        "3715170urlFCz", "5448065HFAxTT", "log", "child_process"
    ];
    W = function () {
        return a;
    };
    return W();
}

function f(G, d) {
    G = G - 0x107;
    const t = W();
    let E = t[G];
    return E;
}
```

`W()` allocates the array on its first call, then replaces itself with a closure that returns the same object. Subsequent calls share that array. The startup loop therefore mutates the array that `f()` reads.

The decoder subtracts `0x107` (263) from its first argument and returns the entry at that index. Its second parameter is unused. Plain-string decoding needs only the offset and the correct array order.

```javascript
(function (G, d) {
    const t = G();
    while (!![]) {
        try {
            const E =
                -parseInt(f(0x110)) / 0x1
                    * (-parseInt(f(0x10b)) / 0x2)
                + parseInt(f(0x111)) / 0x3
                + parseInt(f(0x10d)) / 0x4
                + parseInt(f(0x113)) / 0x5
                + -parseInt(f(0x10f)) / 0x6
                + -parseInt(f(0x107)) / 0x7
                + parseInt(f(0x10a)) / 0x8
                    * (-parseInt(f(0x10e)) / 0x9);
            if (E === d) {
                break;
            } else {
                t["push"](t["shift"]());
            }
        } catch (L) {
            t["push"](t["shift"]());
        }
    }
}(W, 0xaf1a1));

const cp = require(f(0x109));
const url = f(0x112);
console[f(0x108)](url, typeof cp[f(0x10c)]);
```

The startup loop computes `E` and compares it with `0xaf1a1` (717,217). A mismatch moves the first entry to the end. The exception handler performs the same rotation. Once the checksum matches, the loop stops and the application calls use the resulting order.

Static recovery reproduces that search over candidate rotations. For a left rotation of `r` positions:

```text
f(i) = stored_array[(i - 263 + r) mod 13]
```

The evaluator substitutes these values into the checksum expression. It never calls the submitted `W()` or `f()`.

Rotations 0 through 9 produce NaN: at least one `parseInt` operand resolves to an application string with no numeric prefix. Rotation 10 produces 717,217. No other rotation matches. A separate Python implementation of the checksum returns the same solution.

| Decoder call | Value at rotation 10 |
| --- | --- |
| `f(0x109)` | `child_process` |
| `f(0x112)` | `https://example.invalid/setup` |
| `f(0x108)` | `log` |
| `f(0x10c)` | `spawn` |

All four values are printable even under the wrong rotation because every array entry is a plain string. Printability cannot select the order here. The checksum supplies the deciding constraint.

