from common import *


class ThisContext(ExamScene):
    def construct(self):
        self.intro(7, "this (the context object)", "Output-prediction puzzle in Problem 1")

        self.slide("Rule 1: a plain function call",
                   '''
"use strict";
function f() {
  console.log(this);
}
f();          // plain call: nothing before the dot
''',
                   "Regular functions get this\nfrom HOW they are called.\n\n"
                   "Plain call + strict mode\n  -> this is undefined\n\n"
                   "(Without \"use strict\",\nthis would be window.)",
                   out="undefined",
                   trap="this?.x on undefined gives undefined. Plain this.x would throw a TypeError.")

        self.slide("Rule 2: method call -> the object before the dot",
                   '''
"use strict";
const car = {
  carColor: "blue",
  show() { return this?.carColor; }
};
console.log(car.show());   // this = car

const s = car.show;        // copy the function out
console.log(s());          // plain call again!
''',
                   "this is decided at CALL time,\nnot where the function was\nwritten.\n\n"
                   "s() has nothing before the\ndot, so this = undefined.",
                   out="blue\nundefined")

        self.slide("Rule 3: arrow functions have no own this",
                   '''
"use strict";
window.carColor = "red";
const show = () => console.log(this.carColor);

show();
show.call({ carColor: "blue" });
''',
                   "An arrow uses the this of\nthe place it was WRITTEN\n(lexical this).\n\n"
                   "Top level of a classic\n<script>: this is window,\nso this.carColor is \"red\".",
                   out="red\nred",
                   trap=".call / .apply / .bind can NOT change an arrow function's this.")

        self.slide("call, apply, bind (regular functions)",
                   '''
"use strict";
const p = { name: "Kim" };
function intro(greet, punct) {
  return greet + ", " + this.name + punct;
}
console.log(intro.call(p, "Hi", "!"));
console.log(intro.apply(p, ["Hello", "?"]));
const bound = intro.bind(p, "Hey");
console.log(bound("."));
''',
                   "call: run now, args one by\none\n\n"
                   "apply: run now, args in an\nArray (A for Array)\n\n"
                   "bind: does NOT run; returns\na new function with this\n(and maybe some args) fixed",
                   out="Hi, Kim!\nHello, Kim?\nHey, Kim.")

        self.slide("The exam-style puzzle",
                   '''
"use strict";
window.gameLocation = "UMD";
const loc = { gameLocation: "VA" };

function f() { console.log(this?.gameLocation); }
const g = () => console.log(this?.gameLocation);

f();
g();
g.call(loc);
''',
                   "f(): plain call, strict\n  -> this undefined\n  -> undefined\n\n"
                   "g(): arrow at top level\n  -> this = window -> UMD\n\n"
                   "g.call(loc): arrow ignores\ncall -> still UMD",
                   out="undefined\nUMD\nUMD")

        self.slide("Bonus lines for the same puzzle",
                   '''
f.call(loc);        // regular function: call works
f.bind(loc)();      // bind works too
''',
                   None,
                   out="VA\nVA")

        self.practice(1, "What does this print? (classic <script> in a browser)",
                      '''
"use strict";
window.carColor = "red";
const car = { carColor: "blue",
  show() { return this?.carColor; },
  arrow: () => this?.carColor };
const s = car.show;
console.log(car.show(), car.arrow(), s(), s.call(car));
''',
                      "blue red undefined blue\n\n"
                      "car.show(): this = car.  car.arrow(): an arrow inside an object literal still\n"
                      "uses the outer this (window).  s(): plain strict call.  s.call(car): this = car.")

        self.practice(2, "What does this print?",
                      '''
"use strict";
window.score = 10;
const game = { score: 99 };
function a() { return this?.score; }
const b = () => this?.score;
const c = a.bind(game);
console.log(a(), b(), c(), b.apply(game), a.call(game));
''',
                      "undefined 10 99 10 99")

        self.outro("Regular function: this = object before the dot; plain call in strict -> undefined\n"
                   "Arrow function: this from where it was written (top level -> window)\n"
                   "call(obj, a, b) / apply(obj, [a, b]) run now; bind(obj) returns a new function\n"
                   "None of them change an arrow's this")
