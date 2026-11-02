from common import *


class ArgumentValidation(ExamScene):
    def construct(self):
        self.intro(10, "Validating Function Arguments", "Short code-writing question in Problem 1",
                   say="Argument validation. Problem one often asks you to write a small function that rejects bad "
                       "input: the wrong number of arguments, or the wrong types. Here's the toolkit, and a full "
                       "worked example.")

        self.slide("fn.length vs arguments.length",
                   '''
function f1(a, b = 2, ...c) {}
function f2(a, b, c) {}
const f3 = (...args) => args.length;
function f4(a, b) { return arguments.length; }

console.log(f1.length, f2.length, f3.length);
console.log(f3(1, 2, 3), f4(1), f4(1, 2, 3), f4.length);
''',
                   "fn.length = number of\nDECLARED params, counting\nonly up to the first default\nor rest param\n\n"
                   "arguments.length = how many\nwere actually PASSED\n\n"
                   "Arrow functions have no\narguments object: use\n...args",
                   out="1 3 0\n3 1 3 2",
                   say=[("Two different counts. A function's length property is the number of parameters it "
                         "declares, but it stops counting at the first default or rest parameter. So f1's length is "
                         "just 1.", 1),
                        ("f2 declares three plain parameters, so its length is 3.", 2),
                        ("An arrow with only a rest parameter has length zero. Also, arrows have no arguments "
                         "object, so they use rest instead.", 3),
                        ("arguments dot length is different. It counts how many values were actually passed in "
                         "this call.", 4),
                        ("Let's print them all.", (6, 7))],
                   say_out="1, 3, 0 for the declared lengths. Then 3, 1, 3 for what was passed, and f4's declared "
                           "length is 2.")

        self.slide("Worked example: print_squares(text, limit)",
                   '''
function print_squares(text, limit) {
  if (arguments.length !== print_squares.length) {
    return "Invalid Arguments";        // wrong count
  }
  if (typeof text !== "string" ||
      typeof limit !== "number") {
    return "Invalid Arguments";        // wrong types
  }
  let result = text;
  for (let i = 1; i <= limit; i++) {
    result += " " + i * i;
  }
  return result;
}
''',
                   "1. check the COUNT\n\n"
                   "2. check each TYPE with\n   typeof (no isNaN needed)\n\n"
                   "3. only then do the work\n\n"
                   "typeof returns a string:\n\"number\", \"string\",\n\"boolean\", \"object\",\n\"function\", \"undefined\"",
                   say=[("Here's the worked example. print_squares takes some text and a limit, and must reject a "
                         "wrong argument count or wrong types, without using isNaN.", 1),
                        ("Check the count first. If arguments dot length doesn't equal the function's own length, "
                         "which is 2, return Invalid Arguments.", (2, 4)),
                        ("Then check each type with typeof. text must be a string and limit must be a number. Note "
                         "that it's OR here: either one being wrong is enough to reject.", (5, 8)),
                        ("Only after both checks pass do we do the actual work, adding each square to the "
                         "result.", (9, 13))])

        self.slide("Testing it",
                   '''
print_squares("Squares:", 4)
print_squares("x")            // too few
print_squares(5, "x")         // wrong types
print_squares("a", 3, 9)      // too many
print_squares("a", "3")       // "3" is a string
print_squares("a", NaN)
''',
                   None,
                   out='"Squares: 1 4 9 16"\n"Invalid Arguments"\n"Invalid Arguments"\n'
                       '"Invalid Arguments"\n"Invalid Arguments"\n"a"     (loop never runs)',
                   trap="typeof NaN is \"number\", so NaN passes a typeof check. Without isNaN: x !== x is true only for NaN.",
                   say=[("Let's test it. A valid call.", 1),
                        ("Too few arguments, wrong types, and too many arguments.", (2, 4)),
                        ("A string 3 instead of a number.", 5),
                        ("And NaN. What happens there?", 6)],
                   say_out="The good call gives Squares, 1 4 9 16. The next four are all Invalid Arguments. But NaN "
                           "slips through and returns just a, because the loop condition is false right away.",
                   say_trap="typeof NaN is number, so NaN passes a typeof check. If you have to reject it without "
                            "isNaN, use x not-equal-equal x, which is true only for NaN.")

        self.slide("Throwing instead of returning",
                   '''
function strictCheck(x) {
  if (typeof x !== "number") {
    throw new TypeError("Invalid Arguments");
  }
  return x;
}
try {
  strictCheck("5");
} catch (e) {
  console.log(e.name + ": " + e.message);
}
''',
                   "Read the question: does it\nsay RETURN a message or\nTHROW an error?\n\n"
                   "throw stops the function;\nthe caller must catch it.",
                   out="TypeError: Invalid Arguments",
                   say=[("Some questions say to throw instead of returning a message. Same check, but you throw "
                         "an error object.", (1, 6)),
                        ("Throwing stops the function immediately, and the caller has to catch it.", (7, 11))],
                   say_out="The catch prints TypeError, colon, Invalid Arguments. Read the question carefully to "
                           "see whether it wants a return or a throw.")

        self.slide("Default and rest parameters",
                   '''
function pr(a, b = 10, ...rest) {
  return `${pr.length} ${arguments.length} ${b} ${rest.length}`;
}
console.log(pr(1));
console.log(pr(1, undefined, 3, 4));
console.log(pr(1, null));

function sum(...nums) {
  return nums.reduce((acc, n) => acc + n, 0);
}
console.log(sum(), sum(1, 2, 3));
''',
                   "Default kicks in for a\nmissing arg OR undefined,\nbut NOT for null.\n\n"
                   "rest collects the extra\nargs into a real Array.\n\n"
                   "arguments still counts\neverything that was passed.",
                   out="1 1 10 0\n1 4 10 2\n1 2 null 0\n0 6",
                   trap="Passing null does not trigger a default parameter. Only undefined (or nothing) does.",
                   say=[("Default and rest parameters together. pr reports its length, the number of arguments "
                         "passed, b, and how many extras landed in rest.", (1, 3)),
                        ("We call it with one argument, then with undefined and two extras, then with null.", (4, 6)),
                        ("And rest is a real array, so sum can call reduce on it directly.", (8, 11))],
                   say_out="pr's length is always 1. With one argument, b defaults to 10. Passing undefined also "
                           "triggers the default, and rest catches 3 and 4. But null is a real value, so b is null. "
                           "And sum gives 0 and 6.",
                   say_trap="Passing null does not trigger a default parameter. Only undefined, or leaving the "
                            "argument out, does.")

        self.practice(1,
                      "Write repeat_word(word, times): if it isn't called with exactly 2 arguments, or word\n"
                      "isn't a string, or times isn't a number, return \"Invalid Arguments\". Otherwise\n"
                      "return word repeated times times, joined by \"-\".  repeat_word(\"go\", 3) -> \"go-go-go\"",
                      None,
                      '''
function repeat_word(word, times) {
  if (arguments.length !== repeat_word.length ||
      typeof word !== "string" || typeof times !== "number") {
    return "Invalid Arguments";
  }
  let result = word;
  for (let i = 1; i < times; i++) {
    result += "-" + word;
  }
  return result;
}
// repeat_word("go")  /  repeat_word(3, "go")  /  repeat_word("go", 2, 1)
//   -> "Invalid Arguments" for all three
''',
                      say_q="Write repeat_word, which takes a word and a number of times. Return Invalid Arguments "
                            "unless it's called with exactly two arguments, a string and a number. Otherwise, return "
                            "the word repeated, joined with dashes.",
                      say_a="Combine the count check and both typeof checks with OR, and return Invalid Arguments if "
                            "any of them fails. Then start with the word, and add a dash and the word for each extra "
                            "repetition. go and 3 gives go dash go dash go.",
                      answer_is_code=True)

        self.practice(2, "What does this print?",
                      '''
function m(x, y = 1, z) { return arguments.length; }
const n = (...vals) => vals.length;
console.log(m.length, m(5), m(5, 6, 7, 8), n.length, n(1, 2));
''',
                      "1 1 4 0 2\n\nm.length stops counting at the first default (y), so it is 1.",
                      say_q="What does this print?",
                      say_a="1, 1, 4, 0, 2. m's length stops at the first default, y, so it's 1, even though z comes "
                            "after. m of 5 passed one argument, and the next call passed four. n has only a rest "
                            "parameter, so its length is 0, and n of 1 2 returns 2.")

        self.outro("fn.length = declared params before the first default / rest\n"
                   "arguments.length = how many were actually passed (not in arrows)\n"
                   "typeof x !== \"number\" / \"string\" -> return \"Invalid Arguments\" (or throw)\n"
                   "NaN is typeof \"number\";  null does not trigger a default",
                   say="Recap. A function's length counts declared parameters up to the first default or rest. "
                       "arguments dot length counts what was actually passed, and arrows don't have it. Check the "
                       "count, then the types with typeof, and return Invalid Arguments or throw. And remember: NaN "
                       "is a number to typeof, and null doesn't trigger defaults.")
