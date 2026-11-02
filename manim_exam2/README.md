# CMSC335 Exam 2 study videos (Manim)

Exam 2: Thu Nov 5, 2026, 75 minutes, closed book, handwritten code, 200 pts.
Videos are in `videos/`, ordered by exam weight (watch 01 first). Every video ends with
1-2 exam-style practice questions: pause on the question, then check the answer.
Every JS output shown on screen was checked with Node (`verify/`); browser `this`
behavior was checked in a `vm` context where the global object acts as `window`.

| # | Video | Length | Exam weight |
|---|-------|--------|-------------|
| 01 | [Form + JS validation](videos/01_form_validation.mp4) | 3:52 | 46-78 pts, the biggest problem |
| 02 | [Default Pattern custom types + inheritance](videos/02_default_pattern.mp4) | 3:31 | 40-48 pts |
| 03 | [Prototype diagram](videos/03_prototype_diagram.mp4) | 2:53 | 10-14 pts |
| 04 | [class syntax + custom errors](videos/04_class_syntax.mp4) | 3:32 | 34-40 pts |
| 05 | [Promises + fetch without await](videos/05_promises_fetch.mp4) | 4:07 | ~30 pts (last exam) |
| 06 | [Event loop](videos/06_event_loop.mp4) | 3:09 | Problem 1 puzzles |
| 07 | [this / context object](videos/07_this_context.mp4) | 3:06 | Problem 1 puzzle |
| 08 | [Currying, closures, IIFE](videos/08_currying_closures_iife.mp4) | 2:49 | Problem 1, every exam |
| 09 | [Short-circuit, typeof, instanceof](videos/09_short_circuit.mp4) | 3:26 | Problem 1 |
| 10 | [Argument validation](videos/10_argument_validation.mp4) | 3:07 | Problem 1 |
| 11 | [Array methods, destructuring, spread, JSON](videos/11_array_methods.mp4) | 3:34 | ~38 pts on 2022-23 exams |
| 12 | [freeze / seal / preventExtensions](videos/12_freeze_seal.mp4) | 2:43 | Problem 1 |

## Summaries

**01 Form validation.** The HTML form (action, method="post", name vs id, a bare `<button>` submits, `type="reset"`) and `window.onsubmit = validateRequest;`.
A full worked problem: `trim() === ""`, `split("-")` with destructuring, `toLowerCase()`, `Number()` + `isNaN()` range checks, and building an `"|No name|Invalid state"` error string.
One `alert()` then `return false`, or `return window.confirm(msg)`, so the form is sent only on OK.

**02 Default Pattern.** A constructor function with default params for data, and methods on the prototype (one shared copy, not one per object).
Replacing `Type.prototype = {...}` drops `constructor` unless you put it back.
Child type: `Parent.call(this, ...)`, `Object.create(Parent.prototype)`, restore `.constructor`, override with `Parent.prototype.m.call(this)`.

**03 Prototype diagram.** Builds the exam diagram for `Boat`: the function, `Boat.prototype`, the instances, and Object.prototype, with every arrow up to null.
Animates property lookup walking the `__proto__` chain (own, prototype, Object.prototype, then undefined at null).
Shows shadowing (`a.capacity = 10`) and changing a shared prototype value.

**04 class syntax.** `static #total`, `#private` fields, a constructor that bumps `ClassName.#total++`, getters and setters with validation, static methods, `return this` chaining.
`[Symbol.toPrimitive]()` as the course's toString, so that `${obj}` works. Covers the setter-only and getter-only traps.
`extends` / `super(...)` / `super.method()`, plus `class DataRangeError extends Error` with throw/try/catch/finally.

**05 Promises + fetch.** Promise states, settling only once, and "pending forever" when resolve is never called.
The exam's `getImageURL(index, jsonFile)` built with `new Promise` + `fetch().then(r => r.json())`, used with `.then().catch()`.
`.then` returns a promise, async functions always return a promise, the async/await equivalent, `Promise.all`, and wrapping setTimeout in a promise.

**06 Event loop.** Animated call stack, microtask queue and macrotask queue.
`Dog Lion Cat`, then a mixed promise + setTimeout ordering puzzle (`1 4 3 2`).
The trap where a value assigned inside setInterval comes back as `undefined`, and setInterval + clearInterval.

**07 this.** A strict-mode plain call gives `this === undefined`; a method call gives the object before the dot; a detached method loses its `this`.
Arrow functions take `this` lexically (window at the top level), and `.call` can't change it. Also call vs apply vs bind.
Ends with the exam puzzle printing `undefined UMD UMD`.

**08 Currying, closures, IIFE.** `getValue(a,b,c)` turned into `(a,b)(c)` and `(a)(b,c)`.
Closures with a counter factory (each call to the outer function gets its own variables).
Named function rewritten as an arrow IIFE `(num => {...})(3)`, plus the async IIFE with await fetch.

**09 Short-circuit.** Truthy and falsy; `&&` / `||` / `??` return values (`"0" || "Kate"` gives `"0"`, `0 ?? "John"` gives `0`).
Optional chaining `?.`.
typeof quick hits (`null` is "object", `NaN` is "number") and instanceof.

**10 Argument validation.** `fn.length` vs `arguments.length` (defaults and rest params are not counted).
Worked `print_squares(text, limit)`: check the count, then the types with typeof, and return "Invalid Arguments" (or throw).
Traps: NaN passes `typeof === "number"`, and null does not trigger a default param.

**11 Array methods.** forEach / find / findIndex / every / some / map / join / reduce (max value, max object, sum) on an array of objects.
Sorting with numeric and `localeCompare` comparators toggled by a boolean; sort mutates the array and its default is string order.
Array and object destructuring, spread vs rest, and JSON.stringify / JSON.parse.

**12 freeze / seal / preventExtensions.** A table of add/delete/modify/read for each one.
The exam's `Object.seal(game)` example: changes are silently ignored in sloppy mode and throw a TypeError in strict mode.
freeze is shallow.

## Re-rendering

```
pip install manim          # v0.22 used here; no LaTeX needed
python render.py           # all scenes, or: python render.py 01 05
node verify/05_06.js       # re-check the outputs shown on screen
```
`render.py` renders at `-qm` (720p30) into `media/` (gitignored) and copies the mp4s into `videos/`.
