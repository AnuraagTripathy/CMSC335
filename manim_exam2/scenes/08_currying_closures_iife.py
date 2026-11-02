from common import *


class CurryingClosuresIIFE(ExamScene):
    def construct(self):
        self.intro(8, "Currying, Closures, IIFE", "Asked on every exam")

        self.slide("Currying: split the arguments across calls",
                   '''
function getValue(a, b, c) {
  return a * b - c;
}

// shape (a, b)(c)
function getValueCurried(a, b) {
  return function (c) {
    return a * b - c;
  };
}

// shape (a)(b, c), arrow style
const getValueCurried2 = a => (b, c) => a * b - c;

console.log(getValue(2, 5, 3),
            getValueCurried(2, 5)(3),
            getValueCurried2(2)(5, 3));
''',
                   "Each set of parentheses in\nthe CALL = one function\nlevel in the DEFINITION.\n\n"
                   "(a, b)(c): outer takes a, b\nand RETURNS a function\nthat takes c.\n\n"
                   "Same result, different call\nshape.",
                   out="7 7 7")

        self.slide("Why it works: closures",
                   '''
const tenMinus = getValueCurried(2, 5);  // a=2, b=5 kept
console.log(tenMinus(1), tenMinus(4));

function makeCounter() {
  let count = 0;
  return () => ++count;
}
const c1 = makeCounter(), c2 = makeCounter();
console.log(c1(), c1(), c2(), c1());
''',
                   "A closure = a function plus\nthe variables of the scope\nit was created in.\n\n"
                   "Those variables stay alive\nafter the outer function\nreturns.\n\n"
                   "Each makeCounter() call\ngets its OWN count.",
                   out="9 6\n1 2 1 3",
                   trap="c1 and c2 do not share count: every call to the outer function makes a fresh closure.")

        self.slide("IIFE: Immediately Invoked Function Expression",
                   '''
// named function + a call ...
function printDoubles(num) {
  for (let i = 1; i <= num; i++) console.log(i * 2);
}
printDoubles(3);

// ... as ONE arrow-function IIFE
(num => {
  for (let i = 1; i <= num; i++) console.log(i * 2);
})(3);
''',
                   "Wrap the function in ( )\nthen call it with ( ... )\n\n"
                   "Runs once, right away; its\nvariables don't leak into\nglobal scope.\n\n"
                   "Argument goes in the LAST\nparentheses.",
                   out="2\n4\n6",
                   trap="num => {...}(3) without the wrapping parentheses is a SyntaxError.")

        self.slide("Other IIFE shapes",
                   '''
(function (msg, times) {
  console.log(msg.repeat(times));
})("ab", 3);

((msg, times) => console.log(msg.repeat(times)))("ab", 3);

// async IIFE: lets you use await at the top level
(async () => {
  const response = await fetch("data.json");
  const json = await response.json();
  console.log(json);
})();
''',
                   "Classic function IIFE and\narrow IIFE do the same.\n\n"
                   "Async IIFE: await is only\nallowed inside an async\nfunction, so wrap the code\n"
                   "in one and call it at once.",
                   out="ababab\nababab")

        self.practice(1,
                      "Given  function volume(l, w, h) { return l * w * h; }\n"
                      "write volumeA so volumeA(l)(w)(h) works, and volumeB so volumeB(l, w)(h) works.",
                      None,
                      '''
const volumeA = l => w => h => l * w * h;

function volumeB(l, w) {
  return function (h) {
    return l * w * h;
  };
}
console.log(volumeA(2)(3)(4), volumeB(2, 3)(4));   // 24 24
''', answer_is_code=True)

        self.practice(2,
                      "Rewrite as a single arrow-function IIFE (no name), then say what the closure prints.",
                      '''
function greet(name) {
  console.log("Hi " + name);
}
greet("Terp");

function makeBank(start) {
  let balance = start;
  return { deposit: amt => balance += amt, get: () => balance };
}
const acct = makeBank(10);
acct.deposit(5);
console.log(acct.get(), makeBank(0).get(), acct.balance);
''',
                      '''
(name => {
  console.log("Hi " + name);
})("Terp");

// prints: 15 0 undefined
// balance is private to the closure, so acct.balance is undefined
''', answer_is_code=True)

        self.outro("Curry: f(a, b)(c) means f returns a function of c\n"
                   "Closures keep the outer variables alive (one copy per outer call)\n"
                   "IIFE: (params => { ... })(args)\n"
                   "Async IIFE: (async () => { const r = await fetch(url); ... })();")
