from common import *


class ArgumentValidation(ExamScene):
    def construct(self):
        self.intro(10, "Validating Function Arguments", "Short code-writing question in Problem 1")

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
                   out="1 3 0\n3 1 3 2")

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
                   "typeof returns a string:\n\"number\", \"string\",\n\"boolean\", \"object\",\n\"function\", \"undefined\"")

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
                   trap="typeof NaN is \"number\", so NaN passes a typeof check. Without isNaN: x !== x is true only for NaN.")

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
                   out="TypeError: Invalid Arguments")

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
                   trap="Passing null does not trigger a default parameter. Only undefined (or nothing) does.")

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
''', answer_is_code=True)

        self.practice(2, "What does this print?",
                      '''
function m(x, y = 1, z) { return arguments.length; }
const n = (...vals) => vals.length;
console.log(m.length, m(5), m(5, 6, 7, 8), n.length, n(1, 2));
''',
                      "1 1 4 0 2\n\nm.length stops counting at the first default (y), so it is 1.")

        self.outro("fn.length = declared params before the first default / rest\n"
                   "arguments.length = how many were actually passed (not in arrows)\n"
                   "typeof x !== \"number\" / \"string\" -> return \"Invalid Arguments\" (or throw)\n"
                   "NaN is typeof \"number\";  null does not trigger a default")
