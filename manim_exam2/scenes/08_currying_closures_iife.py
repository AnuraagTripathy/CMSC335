from common import *


class CurryingClosuresIIFE(ExamScene):
    def construct(self):
        self.intro(8, "Currying, Closures, IIFE", "Asked on every exam",
                   say="Currying, closures, and I I F Es. Some version of these shows up on every single exam, "
                       "usually as a short rewrite question. They're quick points once the pattern clicks.")

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
                   out="7 7 7",
                   say=[("Here's a normal function of three arguments: a times b minus c.", (1, 3)),
                        ("Currying means splitting those arguments across separate calls. For the shape a comma b, "
                         "then c, the outer function takes a and b, and returns a new function that takes c.",
                         (6, 10)),
                        ("The trick: count the sets of parentheses in the call. Each set is one level of function "
                         "in the definition.", None),
                        ("For the shape a, then b comma c, the arrow version is very compact. a arrow, b comma c "
                         "arrow, and the expression.", 13),
                        ("Let's call all three with 2, 5, and 3.", (15, 17))],
                   say_out="All three give 7. Same math, different call shapes.")

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
                   trap="c1 and c2 do not share count: every call to the outer function makes a fresh closure.",
                   say=[("Why does currying work? Closures. When getValueCurried returns the inner function, that "
                         "inner function keeps a and b alive, even though the outer call is over. So tenMinus "
                         "remembers 2 and 5.", (1, 2)),
                        ("A classic closure example: makeCounter keeps a private count, and returns an arrow that "
                         "increments it.", (4, 7)),
                        ("We make two counters, and call them in a mixed order.", (8, 9))],
                   say_out="tenMinus gives 9 and 6. And the counters print 1, 2, 1, 3.",
                   say_trap="c1 and c2 do not share a count. Every call to makeCounter creates a fresh count "
                            "variable, so c2 starts over at 1.")

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
                   trap="num => {...}(3) without the wrapping parentheses is a SyntaxError.",
                   say=[("An I I F E is an immediately invoked function expression. The exam gives you a named "
                         "function and a call, like this, and asks you to rewrite them as one expression.", (1, 5)),
                        ("Wrap the function in parentheses, then call it right away with another set of "
                         "parentheses. The argument, 3, goes in that last set. It runs once, immediately, and its "
                         "variables don't leak into the global scope.", (8, 10))],
                   say_out="Both versions print 2, 4, 6.",
                   say_trap="If you leave off the parentheses around the arrow function, it's a syntax error.")

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
                   out="ababab\nababab",
                   say=[("The classic function keyword version works the same way.", (1, 3)),
                        ("And here's the arrow version on a single line.", 5),
                        ("The async I I F E is worth memorizing. await is only allowed inside an async function, so "
                         "you wrap the code in an async arrow function and call it immediately. That lets you write "
                         "await fetch at the top level of a script.", (7, 12))],
                   say_out="The first two each print a b three times.")

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
''',
                      say_q="Given a volume function of length, width, and height, write volumeA so you call it with "
                            "three separate sets of parentheses, and volumeB so you call it with length and width "
                            "together, then height.",
                      say_a="volumeA has three levels, so three arrows: l arrow w arrow h arrow the product. volumeB "
                            "has two levels: the outer function takes l and w, and returns a function of h. Both give "
                            "24 for 2, 3, and 4.",
                      answer_is_code=True)

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
''',
                      say_q="Rewrite greet and its call as a single arrow function I I F E, with no name. Then, what "
                            "does the bank closure print?",
                      say_a="Wrap an arrow that takes name in parentheses, and call it right away with Terp. For the "
                            "bank: 10 plus 5 gives 15, a new bank starting at 0 gives 0, and acct dot balance is "
                            "undefined, because balance is a variable inside the closure, not a property of the "
                            "object.",
                      answer_is_code=True)

        self.outro("Curry: f(a, b)(c) means f returns a function of c\n"
                   "Closures keep the outer variables alive (one copy per outer call)\n"
                   "IIFE: (params => { ... })(args)\n"
                   "Async IIFE: (async () => { const r = await fetch(url); ... })();",
                   say="Recap. Curried calls like f of a b, then c, mean f returns a function of c. Closures keep "
                       "the outer variables alive, with a fresh copy for each outer call. An I I F E is a function "
                       "wrapped in parentheses and called right away. And the async I I F E lets you use await "
                       "at the top level.")
