from common import *


class ShortCircuit(ExamScene):
    def quiz(self, title, rows_spec, intro_say):
        """rows_spec: (expression, answer, spoken explanation). Each answer is revealed while it is explained."""
        self.header(title)
        rows = VGroup()
        for expr, ans, _ in rows_spec:
            e = mono(expr, 26)
            a = mono(ans, 26, OK)
            rows.add(VGroup(e, a))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(self.head, DOWN, buff=0.5)
        arrows = VGroup()
        w = max(r[0].width for r in rows)
        left = rows.get_left()[0]
        for r in rows:
            r[1].set_x(left + w + 1.0 + r[1].width / 2)
            arrows.add(mono("->", 26, GREY_B).move_to([left + w + 0.5, r[0].get_y(), 0]))
        VGroup(rows, arrows).set_x(0)
        with self.say(intro_say):
            self.play(*[FadeIn(r[0]) for r in rows], FadeIn(arrows))
        hl = None
        for r, (_, _, speech) in zip(rows, rows_spec):
            box = SurroundingRectangle(VGroup(r, arrows), buff=0.08, color=ACCENT).stretch_to_fit_height(r.height + 0.16).set_y(r.get_y())
            with self.say(speech):
                if hl is None:
                    hl = box
                    self.play(Create(hl), run_time=0.3)
                else:
                    self.play(Transform(hl, box), run_time=0.3)
                self.play(FadeIn(r[1], shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeOut(hl), run_time=0.3)
        self.wait(1)

    def construct(self):
        self.intro(9, "Short-Circuit Operators, typeof, instanceof", "Quick points in Problem 1",
                   say="Short-circuit operators, typeof, and instanceof. These are quick-fire points in problem one, "
                       "and the questions are designed to catch you on one or two specific values. Let's learn "
                       "exactly which ones.")

        self.slide("Truthy vs falsy", None,
                   "The ONLY falsy values:\n"
                   "   false   0   -0   0n   \"\"   null   undefined   NaN\n\n"
                   "Everything else is truthy, including:\n"
                   "   \"0\"   \"false\"   \" \"   []   {}\n\n"
                   "a && b : returns the FIRST FALSY value, or the last value if none\n"
                   "a || b : returns the FIRST TRUTHY value, or the last value if none\n"
                   "a ?? b : returns b only if a is null or undefined\n\n"
                   "They return one of the VALUES, not true/false.",
                   trap="\"0\" is a non-empty string, so it is TRUTHY: \"0\" || \"Kate\" gives \"0\".",
                   say=["Everything starts with truthy and falsy. There are only eight falsy values: false, zero, "
                        "negative zero, big int zero, the empty string, null, undefined, and NaN. Memorize that "
                        "list. Everything else is truthy, including the string zero, the string false, a string "
                        "with just a space, an empty array, and an empty object.",
                        "Now the operators. AND returns the first falsy value it sees, or the last value if they're "
                        "all truthy. OR returns the first truthy value, or the last value if none are. And the "
                        "nullish operator, double question mark, only moves to the right side when the left side is "
                        "null or undefined. The key idea: they return one of the actual values, not true or false."],
                   say_trap="The string zero is a non-empty string, so it's truthy. String zero OR Kate gives "
                            "string zero.")

        self.quiz("&& and ||",
                  [('"Mike" && 14.5', "14.5", "Mike is truthy, so AND keeps going, and returns the last value, 14.5."),
                   ('"0" || "Kate"', '"0"', "String zero is truthy, so OR stops right there and returns it."),
                   ("false && 100", "false", "false is falsy, so AND stops immediately and returns false."),
                   ('0 || "John"', '"John"', "Zero is falsy, so OR moves on, and returns John."),
                   ('null && "x"', "null", "null is falsy, so AND returns null."),
                   ('1 && "" && 2', '""', "One is truthy, then the empty string is falsy, so AND stops and returns "
                                          "the empty string."),
                   ('0 || "" || null', "null", "All three are falsy, so OR returns the last one, null.")],
                  intro_say="Try each one yourself before I reveal it.")
        self.clear()

        self.quiz("?? vs ||",
                  [('0 ?? "John"', "0", "Zero isn't null or undefined, so nullish keeps the zero."),
                   ('0 || "John"', '"John"', "But OR treats zero as falsy, and gives John."),
                   ('"" ?? "default"', '""', "Same with the empty string. Nullish keeps it."),
                   ('"" || "default"', '"default"', "OR replaces it with default."),
                   ('null ?? "x"', '"x"', "null is exactly what nullish is for, so we get x."),
                   ("undefined ?? 0 ?? 7", "0", "undefined falls through to zero, and zero is kept, so the answer "
                                                "is zero, not 7.")],
                  intro_say="Now compare nullish with OR, side by side.")
        tr = self.trap("?? only falls through on null/undefined, so 0 and \"\" are kept. Use ?? when 0 is a valid value.",
                       say="Nullish only falls through on null or undefined, so zero and the empty string are kept. "
                           "Use it when zero is a valid value, like a quantity.")
        self.clear()

        self.slide("Optional chaining ?.",
                   '''
const user = null;
const prof = { addr: { zip: "20742" } };
console.log(user?.name);        // stops at null
console.log(prof?.addr?.zip);
console.log(prof.phone?.home);  // phone is undefined
console.log(prof.greet?.());    // call only if it exists
''',
                   "a?.b gives undefined\n(instead of a TypeError)\nwhen a is null/undefined.\n\n"
                   "Also works for calls:\n  obj.method?.()",
                   out="undefined\n20742\nundefined\nundefined",
                   say=[("Optional chaining. Normally, reading a property of null throws a TypeError. With "
                         "question-mark-dot, it just stops and gives undefined.", 3),
                        ("When everything exists, it works like a normal dot.", 4),
                        ("prof dot phone is undefined, so the chain stops before home.", 5),
                        ("And it works for method calls too. greet doesn't exist, so it isn't called.", 6)],
                   say_out="undefined, 2 0 7 4 2, undefined, and undefined. No errors anywhere.")

        self.quiz("typeof quick hits",
                  [("typeof null", '"object"', "typeof null is object. That's a famous old bug in JavaScript, and "
                                               "a favorite exam question."),
                   ("typeof []", '"object"', "Arrays are objects, so typeof gives object."),
                   ("typeof function () {}", '"function"', "Functions get their own answer: function."),
                   ("typeof class {}", '"function"', "A class is really a function too."),
                   ("typeof NaN", '"number"', "NaN means not a number, but its type is number."),
                   ("typeof undefined", '"undefined"', "undefined gives the string undefined."),
                   ('typeof "5"', '"string"', "And quotes make it a string, even if it looks like a number.")],
                  intro_say="typeof always returns a string. Here are the ones people miss.")
        tr = self.trap("typeof null is \"object\" and typeof NaN is \"number\". Use Array.isArray(x) for arrays.",
                       say="typeof null is object, and typeof NaN is number. To test for an array, use "
                           "Array dot isArray.")
        self.clear()

        self.quiz("instanceof: is X.prototype on the chain?",
                  [("[] instanceof Array", "true", "An array's chain includes Array dot prototype, so true."),
                   ("[] instanceof Object", "true", "And that chain continues to Object dot prototype, so this is "
                                                    "true as well."),
                   ('"hi" instanceof String', "false   (primitive)", "A string literal is a primitive, not an "
                                                                     "object, so instanceof gives false."),
                   ('new String("hi") instanceof String', "true", "But new String makes a wrapper object, so true."),
                   ("null instanceof Object", "false", "null has no prototype chain at all, so false.")],
                  intro_say="instanceof asks one question: is this constructor's prototype somewhere on the object's "
                            "prototype chain?")
        self.clear()

        self.practice(1, "What is each value?",
                      '''
let qty = 0;
const a1 = qty || 10;
const a2 = qty ?? 10;
const a3 = "false" && "yes";
const a4 = null || undefined;
const a5 = typeof (qty && "x");
''',
                      'a1 = 10\na2 = 0\na3 = "yes"   ("false" is a non-empty string: truthy)\n'
                      'a4 = undefined   (no truthy value: returns the last one)\n'
                      'a5 = "number"   (qty && "x" is 0)',
                      say_q="What is each of these five values?",
                      say_a="a1 is 10, because zero is falsy. a2 is zero, because nullish keeps zero. a3 is yes, "
                            "because the string false is truthy. a4 is undefined, because neither is truthy, so OR "
                            "returns the last one. And a5: qty AND x stops at zero, and typeof zero is number.")

        self.practice(2, "What does this print?",
                      '''
console.log(" " || "x", NaN && 1, "Ann" || "Bob", [] || "empty");
''',
                      '" "  NaN  "Ann"  []\n\n(console shows:   NaN Ann [])\n'
                      'A space is a non-empty string (truthy); NaN is falsy; [] is truthy.',
                      say_q="What does this print?",
                      say_a="A single space, NaN, Ann, and an empty array. The space is a non-empty string, so it's "
                            "truthy. NaN is falsy, so AND returns it. Ann is truthy. And an empty array is truthy, so "
                            "OR returns the array, not the word empty.")

        self.outro("&& -> first falsy (or last);  || -> first truthy (or last)\n"
                   "?? -> right side only for null / undefined;  ?. -> undefined instead of an error\n"
                   "Falsy: false 0 -0 0n \"\" null undefined NaN   (\"0\" and [] are truthy)\n"
                   "typeof null === \"object\";  typeof NaN === \"number\"",
                   say="Recap. AND returns the first falsy value, or the last one. OR returns the first truthy value, "
                       "or the last one. Nullish only falls through on null or undefined. Optional chaining gives "
                       "undefined instead of an error. Know the eight falsy values, and remember that string zero "
                       "and empty arrays are truthy. And typeof null is object, while typeof NaN is number.")
