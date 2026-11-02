from common import *


class ShortCircuit(ExamScene):
    def quiz(self, title, pairs):
        """Show expressions, then reveal each answer one by one."""
        self.header(title)
        rows = VGroup()
        for expr, ans in pairs:
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
        self.play(*[FadeIn(r[0]) for r in rows], FadeIn(arrows))
        self.wait(4)
        for r in rows:
            self.play(FadeIn(r[1], shift=LEFT * 0.2), run_time=0.5)
            self.wait(1.6)
        self.wait(2)

    def construct(self):
        self.intro(9, "Short-Circuit Operators, typeof, instanceof", "Quick points in Problem 1")

        self.slide("Truthy vs falsy", None,
                   "The ONLY falsy values:\n"
                   "   false   0   -0   0n   \"\"   null   undefined   NaN\n\n"
                   "Everything else is truthy, including:\n"
                   "   \"0\"   \"false\"   \" \"   []   {}\n\n"
                   "a && b : returns the FIRST FALSY value, or the last value if none\n"
                   "a || b : returns the FIRST TRUTHY value, or the last value if none\n"
                   "a ?? b : returns b only if a is null or undefined\n\n"
                   "They return one of the VALUES, not true/false.",
                   trap="\"0\" is a non-empty string, so it is TRUTHY: \"0\" || \"Kate\" gives \"0\".")

        self.quiz("&& and ||", [('"Mike" && 14.5', "14.5"), ('"0" || "Kate"', '"0"'),
                                ("false && 100", "false"), ('0 || "John"', '"John"'),
                                ('null && "x"', "null"), ('1 && "" && 2', '""'),
                                ('0 || "" || null', "null")])
        self.clear()

        self.quiz("?? vs ||", [('0 ?? "John"', "0"), ('0 || "John"', '"John"'),
                               ('"" ?? "default"', '""'), ('"" || "default"', '"default"'),
                               ('null ?? "x"', '"x"'), ("undefined ?? 0 ?? 7", "0")])
        tr = self.trap("?? only falls through on null/undefined, so 0 and \"\" are kept. Use ?? when 0 is a valid value.")
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
                   out="undefined\n20742\nundefined\nundefined")

        self.quiz("typeof quick hits", [("typeof null", '"object"'), ("typeof []", '"object"'),
                                        ("typeof function () {}", '"function"'), ("typeof class {}", '"function"'),
                                        ("typeof NaN", '"number"'), ("typeof undefined", '"undefined"'),
                                        ('typeof "5"', '"string"')])
        tr = self.trap("typeof null is \"object\" and typeof NaN is \"number\". Use Array.isArray(x) for arrays.")
        self.clear()

        self.quiz("instanceof: is X.prototype on the chain?",
                  [("[] instanceof Array", "true"), ("[] instanceof Object", "true"),
                   ('"hi" instanceof String', "false   (primitive)"),
                   ('new String("hi") instanceof String', "true"), ("null instanceof Object", "false")])
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
                      'a5 = "number"   (qty && "x" is 0)')

        self.practice(2, "What does this print?",
                      '''
console.log(" " || "x", NaN && 1, "Ann" || "Bob", [] || "empty");
''',
                      '" "  NaN  "Ann"  []\n\n(console shows:   NaN Ann [])\n'
                      'A space is a non-empty string (truthy); NaN is falsy; [] is truthy.')

        self.outro("&& -> first falsy (or last);  || -> first truthy (or last)\n"
                   "?? -> right side only for null / undefined;  ?. -> undefined instead of an error\n"
                   "Falsy: false 0 -0 0n \"\" null undefined NaN   (\"0\" and [] are truthy)\n"
                   "typeof null === \"object\";  typeof NaN === \"number\"")
