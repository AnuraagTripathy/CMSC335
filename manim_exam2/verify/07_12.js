const vm = require("vm");
// Browser-like classic script: global object === window, top-level this === window
function browser(src) {
  const out = [];
  const ctx = { console: { log: (...a) => out.push(a.map(x => typeof x === "string" ? x : String(x)).join(" ")) } };
  ctx.window = ctx;
  vm.createContext(ctx);
  ctx.window = vm.runInContext("this", ctx);
  try { vm.runInContext(src, ctx); } catch (e) { out.push("THROWS " + e.name + ": " + e.message); }
  return out.join(" | ");
}
console.log("== 07");
console.log(browser(`"use strict";
window.gameLocation = "UMD";
const loc = { gameLocation: "VA" };
function f() { console.log(this?.gameLocation); }
const g = () => console.log(this?.gameLocation);
f(); g(); g.call(loc); f.call(loc); f.bind(loc)();`));
console.log(browser(`"use strict"; function f(){ console.log(this); } f();`));
console.log(browser(`function f(){ console.log(this === window); } f();`));
console.log(browser(`"use strict";
window.carColor = "red";
const show = () => console.log(this.carColor);
show(); show.call({ carColor: "blue" });`));
console.log(browser(`"use strict";
const p = { name: "Kim" };
function intro(greet, punct) { return greet + ", " + this.name + punct; }
console.log(intro.call(p, "Hi", "!"));
console.log(intro.apply(p, ["Hello", "?"]));
const bound = intro.bind(p, "Hey");
console.log(bound("."));`));
console.log(browser(`"use strict";
window.carColor = "red";
const car = { carColor: "blue",
  show() { return this?.carColor; },
  arrow: () => this?.carColor };
const s = car.show;
console.log(car.show(), car.arrow(), s(), s.call(car));`));
console.log(browser(`"use strict";
const team = { name: "Terps",
  later() { setTimeout(() => console.log("arrow:", this.name), 0); } };
team.later();`));
console.log(browser(`"use strict"; const obj = { x: 1, f() { function inner() { return this; } return inner(); } }; console.log(obj.f());`));
// practice 2 for 07
console.log(browser(`"use strict";
window.score = 10;
const game = { score: 99 };
function a() { return this?.score; }
const b = () => this?.score;
const c = a.bind(game);
console.log(a(), b(), c(), b.apply(game), a.call(game));`));

console.log("== 08");
function getValue(a, b, c) { return a * b - c; }
function getValueCurried(a, b) { return function (c) { return a * b - c; }; }
const getValueCurried2 = a => (b, c) => a * b - c;
console.log(getValue(2, 5, 3), getValueCurried(2, 5)(3), getValueCurried2(2)(5, 3));
const tenMinus = getValueCurried(2, 5);
console.log(tenMinus(1), tenMinus(4));
function makeCounter() { let count = 0; return () => ++count; }
const c1 = makeCounter(), c2 = makeCounter();
console.log(c1(), c1(), c2(), c1());
(num => { for (let i = 1; i <= num; i++) console.log(i * 2); })(3);
try { new Function("num => { console.log(num) }(3)"); console.log("no syntax error"); } catch (e) { console.log(e.name, e.message); }
const area = l => w => h => l * w * h;
const area2 = (l, w) => h => l * w * h;
console.log(area(2)(3)(4), area2(2, 3)(4));
function makeAdder(x) { return y => x + y; }
const add5 = makeAdder(5);
let x = 100;
console.log(add5(1), makeAdder(x)(1));
(function (msg, times) { console.log(msg.repeat(times)); })("ab", 3);
((msg, times) => console.log(msg.repeat(times)))("ab", 3);
// practice2 closure
function makeBank(start) {
  let balance = start;
  return { deposit: amt => balance += amt, get: () => balance };
}
const acct = makeBank(10);
acct.deposit(5);
const acct2 = makeBank(0);
console.log(acct.get(), acct2.get(), acct.balance);

console.log("== 09");
const show = v => typeof v === "string" ? JSON.stringify(v) : String(v);
const cases = {
  '"Mike" && 14.5': "Mike" && 14.5, '"0" || "Kate"': "0" || "Kate", "false && 100": false && 100,
  '0 || "John"': 0 || "John", '0 ?? "John"': 0 ?? "John", 'null ?? "x"': null ?? "x",
  '"" || "default"': "" || "default", '"" ?? "default"': "" ?? "default", 'null && "x"': null && "x",
  "undefined || null": undefined || null, "NaN && 1": NaN && 1, '"Ann" || "Bob"': "Ann" || "Bob",
  '1 && "" && 2': 1 && "" && 2, '1 && "a" && 2': 1 && "a" && 2, '0 || "" || null': 0 || "" || null,
  'undefined ?? 0 ?? 7': undefined ?? 0 ?? 7, '" " || "x"': " " || "x", '[] || "e"': [] || "e",
};
for (const [k, v] of Object.entries(cases)) console.log(k, "->", Array.isArray(v) ? "[]" : show(v));
const user = null, prof = { addr: { zip: "20742" } };
console.log(user?.name, prof?.addr?.zip, prof.phone?.home, prof.greet?.());
console.log(typeof null, typeof [], typeof function () {}, typeof NaN, typeof undefined, typeof "5", typeof 5n, typeof class {});
console.log([] instanceof Array, [] instanceof Object, "hi" instanceof String, new String("hi") instanceof String, null instanceof Object);
// practice
let qty = 0;
const a1 = qty || 10, a2 = qty ?? 10, a3 = "false" && "yes", a4 = null || undefined, a5 = typeof (qty && "x");
console.log(a1, a2, a3, a4, a5);

console.log("== 10");
function print_squares(text, limit) {
  if (arguments.length !== print_squares.length) return "Invalid Arguments";
  if (typeof text !== "string" || typeof limit !== "number") return "Invalid Arguments";
  let result = text;
  for (let i = 1; i <= limit; i++) result += " " + i * i;
  return result;
}
console.log(print_squares("Squares:", 4), "|", print_squares("x"), "|", print_squares(5, "x"), "|", print_squares("a", 3, 9), "|", print_squares("a", "3"), "|", JSON.stringify(print_squares("a", NaN)));
function f1(a, b = 2, ...c) {}
function f2(a, b, c) {}
const f3 = (...args) => args.length;
function f4(a, b) { return arguments.length; }
console.log(f1.length, f2.length, f3.length, f3(1, 2, 3), f4(1), f4(1, 2, 3), f4.length);
function sum(...nums) { return nums.reduce((acc, n) => acc + n, 0); }
console.log(sum(), sum(1, 2, 3));
const NaNv = NaN; console.log(NaNv !== NaNv, typeof NaN === "number");
function repeat_word(word, times) {
  if (arguments.length !== repeat_word.length || typeof word !== "string" || typeof times !== "number") {
    return "Invalid Arguments";
  }
  return Array(times).fill(word).join("-");
}
console.log(repeat_word("go", 3), repeat_word("go"), repeat_word(3, "go"), repeat_word("go", 2, 1));
function strictCheck(x) { if (typeof x !== "number") throw new TypeError("Invalid Arguments"); return x; }
try { strictCheck("5"); } catch (e) { console.log(e.name + ": " + e.message); }
function pr(a, b = 10, ...rest) { return `${pr.length} ${arguments.length} ${b} ${rest.length}`; }
console.log(pr(1), "|", pr(1, undefined, 3, 4), "|", pr(1, null));

console.log("== 11");
const emps = [
  { name: "Mia", salary: 72000 },
  { name: "Ben", salary: 95000 },
  { name: "Ava", salary: 61000 },
];
emps.forEach(e => console.log(e.name));
console.log(emps.find(e => e.salary > 70000), emps.find(e => e.salary > 99000), emps.findIndex(e => e.name === "Ava"), emps.findIndex(e => e.name === "Zed"));
console.log(emps.map(e => e.name).join(", "), emps.every(e => e.salary > 60000), emps.some(e => e.salary > 90000));
console.log(emps.reduce((max, e) => e.salary > max ? e.salary : max, 0));
console.log(emps.reduce((best, e) => e.salary > best.salary ? e : best));
console.log(emps.reduce((sum, e) => sum + e.salary, 0));
function sortEmps(arr, byName) {
  return arr.sort(byName ? (a, b) => a.name.localeCompare(b.name) : (a, b) => a.salary - b.salary);
}
console.log(sortEmps(emps, true).map(e => e.name).join(" "), "|", sortEmps(emps, false).map(e => e.name).join(" "), "|", emps.map(e => e.name).join(" "));
console.log([10, 9, 1, 100].sort(), [10, 9, 1, 100].sort((a, b) => a - b));
const arr = [1, 2, 3];
console.log(arr.push(4), arr.pop(), arr.reverse(), arr);
const [first, , third] = [{ name: "Mia", salary: 72000 }, 0, { name: "Ava" }];
const { name, salary: pay, dept = "IT" } = first;
console.log(name, pay, dept, third.name);
const nums = [5, 6, 7, 8];
const [head, ...others] = nums;
console.log(head, others, Math.max(...nums), [...nums, 9]);
const raise = { ...first, salary: 80000 };
console.log(raise, first.salary);
const s = JSON.stringify({ name: "Mia", salary: 72000, hi() {} });
console.log(s, JSON.parse(s).name, typeof s);
// practice
const products = [{ item: "pen", price: 2 }, { item: "lamp", price: 30 }, { item: "mug", price: 9 }];
const priciest = products.reduce((best, p) => p.price > best.price ? p : best);
console.log(priciest);
console.log(products.filter(p => p.price < 10).map(p => p.item.toUpperCase()).join("/"));
const q = [3, 1, 2];
const r = q.sort();
r.push(9);
console.log(q, q === r);
const { item, ...restP } = products[1];
console.log(item, restP);

console.log("== 12");
const game = { name: "Chess", players: 2 };
Object.seal(game);
game.year = 2000; delete game.name; game.players = 4;
console.log(game, Object.isSealed(game), Object.isFrozen(game));
const tbl = (fn) => { const o = { a: 1 }; fn(o); o.b = 2; const d = delete o.a; o.c = 1; const o2 = { a: 1 }; fn(o2); o2.a = 5; return { add: "b" in o, del: !("a" in o), modify: o2.a === 5 }; };
console.log("preventExtensions", tbl(Object.preventExtensions), "seal", tbl(Object.seal), "freeze", tbl(Object.freeze));
const team = Object.freeze({ name: "Terps", stats: { wins: 3 } });
team.name = "X"; team.stats.wins = 10; delete team.name;
console.log(team.name, team.stats.wins);
try { (function () { "use strict"; game.year = 2000; })(); } catch (e) { console.log(e.name + ": " + e.message); }
try { (function () { "use strict"; delete game.name; })(); } catch (e) { console.log(e.name + ": " + e.message); }
const car = { make: "VW", miles: 10 };
Object.preventExtensions(car);
car.color = "red"; car.miles = 20; delete car.make;
console.log(car, Object.isExtensible(car));
const pt = Object.freeze({ x: 1 });
pt.x = 2;
const pt2 = { ...pt, x: 2 };
console.log(pt.x, pt2.x, Object.isFrozen(pt2));
