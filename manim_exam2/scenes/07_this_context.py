from common import *


class ThisContext(ExamScene):
    def construct(self):
        self.intro(7, "this (the context object)", "Output-prediction puzzle in Problem 1",
                   say="Let's talk about this, the context object. There's almost always an output puzzle about it "
                       "in problem one. The good news: three rules cover every case.")

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
                   trap="this?.x on undefined gives undefined. Plain this.x would throw a TypeError.",
                   say=[("Rule one. For a regular function, this isn't decided when you write the function. It's "
                         "decided by how you call it.", (2, 4)),
                        ("Here f is called plainly, with nothing before a dot. In strict mode, that means this is "
                         "undefined. Without use strict, it would be the window object instead.", 5)],
                   say_out="So it prints undefined.",
                   say_trap="The exam code often writes this question-mark-dot x. On undefined, that safely gives "
                            "undefined. Plain this dot x would throw a TypeError instead.")

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
                   out="blue\nundefined",
                   say=[("Rule two. When you call a function as a method, with an object before the dot, this is "
                         "that object. So car dot show gives blue.", (4, 6)),
                        ("But watch this. We copy the function into a variable s, and call s with nothing before "
                         "the dot. It's the same function, but now it's a plain call again.", (8, 9))],
                   say_out="So we get blue, and then undefined. The object that owns the function doesn't matter. "
                           "Only the call site does.")

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
                   trap=".call / .apply / .bind can NOT change an arrow function's this.",
                   say=[("Rule three. Arrow functions don't have their own this. They use the this of the place "
                         "where they were written.", 3),
                        ("This arrow was written at the top level of a classic script, where this is window. And we "
                         "set window dot carColor to red.", 2),
                        ("So calling it gives red. And even call, with a different object, doesn't change it.",
                         (5, 6))],
                   say_out="Red, and red again.",
                   say_trap="Call, apply, and bind cannot change an arrow function's this. They're simply ignored for "
                            "that purpose.")

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
                   out="Hi, Kim!\nHello, Kim?\nHey, Kim.",
                   say=[("For regular functions, you can set this explicitly. Here intro uses this dot name.",
                         (3, 5)),
                        ("call runs the function now. The first argument becomes this, and the rest are passed "
                         "one by one.", 6),
                        ("apply also runs it now, but takes the arguments as an array. A for apply, A for array.", 7),
                        ("bind doesn't run anything. It returns a new function with this locked in, and here the "
                         "first argument locked in too. Then we call that new function later.", (8, 9))])

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
                   out="undefined\nUMD\nUMD",
                   say=[("Now the exam-style puzzle. We set window dot gameLocation to U M D, and make an object "
                         "with V A.", (2, 3)),
                        ("f is a regular function, and g is an arrow, and both print this dot gameLocation.", (5, 6)),
                        ("f is a plain call in strict mode, so this is undefined, and the optional chain gives "
                         "undefined.", 8),
                        ("g is an arrow written at the top level, so this is window, and that's U M D.", 9),
                        ("And g dot call with loc? Arrows ignore call. Still U M D.", 10)],
                   say_out="undefined, U M D, U M D.")

        self.slide("Bonus lines for the same puzzle",
                   '''
f.call(loc);        // regular function: call works
f.bind(loc)();      // bind works too
''',
                   None,
                   out="VA\nVA",
                   say=[("For contrast, f is a regular function, so call and bind do work on it.", (1, 2))],
                   say_out="Both print V A.")

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
                      "uses the outer this (window).  s(): plain strict call.  s.call(car): this = car.",
                      say_q="What does this print? Assume it's a classic script in a browser.",
                      say_a="Blue, red, undefined, blue. car dot show is a method call, so this is car. car dot "
                            "arrow is an arrow, and even inside an object literal it uses the outer this, which is "
                            "window, so red. s is a plain call in strict mode, so undefined. And s dot call with car "
                            "sets this back to car.")

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
                      "undefined 10 99 10 99",
                      say_q="What does this print?",
                      say_a="undefined, 10, 99, 10, 99. a is a plain strict call. b is an arrow, so it uses window, "
                            "10. c is bound to game, 99. apply can't change an arrow, so 10 again. And a dot call "
                            "with game gives 99.")

        self.outro("Regular function: this = object before the dot; plain call in strict -> undefined\n"
                   "Arrow function: this from where it was written (top level -> window)\n"
                   "call(obj, a, b) / apply(obj, [a, b]) run now; bind(obj) returns a new function\n"
                   "None of them change an arrow's this",
                   say="Recap. For a regular function, this is the object before the dot, and a plain call in "
                       "strict mode gives undefined. For an arrow, this comes from where it was written, which at "
                       "the top level is window. Call and apply run the function now with a chosen this. Bind returns "
                       "a new function. And none of them change an arrow's this.")
