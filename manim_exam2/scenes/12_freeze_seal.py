from common import *


class FreezeSeal(ExamScene):
    def construct(self):
        self.intro(12, "freeze / seal / preventExtensions", "Short answer in Problem 1",
                   say="Last one: freeze, seal, and preventExtensions. It's a short answer question, and it's easy "
                       "points once you have one small table in your head.")

        # ---- the table ----
        self.header("What each one allows")
        heads = ["", "add", "delete", "modify", "read"]
        rows = [("Object.preventExtensions", ["no", "yes", "yes", "yes"]),
                ("Object.seal", ["no", "no", "yes", "yes"]),
                ("Object.freeze", ["no", "no", "no", "yes"])]
        cells = VGroup()
        for h in heads:
            cells.add(txt(h or "x", 26, ACCENT, weight=BOLD).set_opacity(1 if h else 0))
        for name, vals in rows:
            cells.add(mono(name, 24))
            for v in vals:
                cells.add(txt(v, 28, OK if v == "yes" else BAD, weight=BOLD))
        table = cells.arrange_in_grid(rows=4, cols=5, buff=(0.7, 0.45), col_alignments="lcccc")
        table.next_to(self.head, DOWN, buff=0.6)
        lines = VGroup(*[Line(table.get_left() + LEFT * 0.2, table.get_right() + RIGHT * 0.2, color=GREY_D)
                         .set_y((cells[5 * i].get_y() + cells[5 * (i + 1)].get_y()) / 2) for i in range(3)])
        with self.say("For each method, there are four questions. Can you add new properties, delete them, "
                      "modify their values, and read them?"):
            self.play(FadeIn(cells[:5]), Create(lines))
        row_says = ["preventExtensions is the mildest. You can't add new properties, but you can still delete "
                    "and modify the existing ones.",
                    "seal goes one step further. No adding and no deleting, so the set of keys is locked. But you "
                    "can still change the values.",
                    "freeze is the strictest. No adding, no deleting, and no modifying. The object is read only."]
        for i in range(3):
            with self.say(row_says[i]):
                self.play(FadeIn(cells[5 * (i + 1):5 * (i + 2)], shift=RIGHT * 0.2))
        note = txt("Each step down removes one more permission.  Check with\n"
                   "Object.isExtensible(o)   Object.isSealed(o)   Object.isFrozen(o)", 22, GREY_A)
        note.next_to(table, DOWN, buff=0.5)
        with self.say("Notice the pattern: each row down removes one more permission. Reading is always allowed. "
                      "And you can check an object's state with isExtensible, isSealed, and isFrozen."):
            self.play(FadeIn(note))
        self.wait(1)
        self.clear()

        self.slide("Exam example: Object.seal",
                   '''
const game = { name: "Chess", players: 2 };
Object.seal(game);

game.year = 2000;     // add     -> NOT allowed
delete game.name;     // delete  -> NOT allowed
game.players = 4;     // modify  -> allowed
console.log(game.name, game.players, game.year);
console.log(Object.isSealed(game), Object.isFrozen(game));
''',
                   "Sealed: the SET of keys is\nlocked, values can change.\n\n"
                   "Failed changes are silently\nignored in sloppy mode...",
                   out="Chess 4 undefined\ntrue false",
                   say=[("Here's the exam's example. We make a game object and seal it.", (1, 2)),
                        ("Adding a year is not allowed, because sealing blocks adding.", 4),
                        ("Deleting the name is not allowed either.", 5),
                        ("But changing players is fine. Sealed objects can still be modified.", 6),
                        ("In a normal, sloppy-mode script, the blocked changes don't throw. They're just silently "
                         "ignored.", (7, 8))],
                   say_out="So the name survives, players is 4, and year is undefined. It's sealed, but not frozen.")

        self.slide("...but throw in strict mode",
                   '''
"use strict";
game.year = 2000;
// TypeError: Cannot add property year, object is not extensible

delete game.name;
// TypeError: Cannot delete property 'name' of #<Object>
''',
                   None,
                   trap="Classes and modules are always strict, so a blocked change THROWS there instead of failing silently.",
                   say=[("But in strict mode, the same blocked changes throw TypeErrors.", (1, 2)),
                        ("Both the add and the delete throw.", (4, 5))],
                   say_trap="Class bodies and modules are always strict, so in code like that, a blocked change "
                            "throws instead of silently failing.")

        self.slide("preventExtensions",
                   '''
const car = { make: "VW", miles: 10 };
Object.preventExtensions(car);
car.color = "red";    // add     -> ignored
car.miles = 20;       // modify  -> allowed
delete car.make;      // delete  -> allowed
console.log(car, Object.isExtensible(car));
''',
                   None,
                   out="{ miles: 20 } false",
                   say=[("preventExtensions on a car.", (1, 2)),
                        ("Adding color is ignored, but modifying miles and deleting make are both allowed.", (3, 5))],
                   say_out="So only miles 20 is left, and isExtensible is false.")

        self.slide("freeze is SHALLOW",
                   '''
const team = Object.freeze({ name: "Terps",
                             stats: { wins: 3 } });
team.name = "X";        // ignored
team.stats.wins = 10;   // nested object is NOT frozen
delete team.name;       // ignored
console.log(team.name, team.stats.wins);
''',
                   "freeze only locks the\ntop-level properties.\n\n"
                   "team.stats still points to\nthe same (unfrozen) object,\nso its contents can change.",
                   out="Terps 10",
                   trap="Object.freeze does not freeze nested objects. Freeze each inner object too if needed.",
                   say=[("Last important detail: freeze is shallow. This team is frozen, and it has a nested stats "
                         "object.", (1, 2)),
                        ("Changing the name is ignored, and so is the delete.", (3, 5)),
                        ("But team dot stats still points to the same inner object, and that object was never "
                         "frozen. So changing wins works.", 4)],
                   say_out="Terps, and 10.",
                   say_trap="Object dot freeze does not freeze nested objects. If you need them locked too, freeze "
                            "each inner object as well.")

        self.practice(1, "After each line, is the change allowed? What is printed?",
                      '''
const pen = { color: "blue", price: 2 };
Object.freeze(pen);
pen.price = 3;
pen.brand = "Bic";
delete pen.color;
console.log(pen.color, pen.price, pen.brand, Object.isSealed(pen));
''',
                      "None of the three changes are allowed (frozen: no add, delete, or modify).\n\n"
                      "blue 2 undefined true\n\n(a frozen object also counts as sealed)",
                      say_q="The pen is frozen. For each line, is the change allowed? And what's printed?",
                      say_a="None of the three changes are allowed, because frozen means no add, no delete, and no "
                            "modify. So it prints blue, 2, undefined, and true, because a frozen object also counts "
                            "as sealed.")

        self.practice(2, "Fill in: which method gives exactly this behavior?",
                      '''
// can modify existing values: yes
// can delete properties:      yes
// can add new properties:     no
''',
                      "Object.preventExtensions(obj)",
                      say_q="Which method gives exactly this behavior? Modify yes, delete yes, add no.",
                      say_a="Object dot preventExtensions. It only blocks adding.")

        self.outro("preventExtensions: no add\n"
                   "seal: no add, no delete (modify OK)\n"
                   "freeze: no add, no delete, no modify (read only), and it is shallow\n"
                   "Sloppy mode: silently ignored.  Strict mode: TypeError",
                   say="Recap. preventExtensions blocks adding. seal blocks adding and deleting, but you can still "
                       "modify. freeze blocks all three, and it's shallow. Blocked changes are silently ignored in "
                       "sloppy mode, and throw a TypeError in strict mode. That's the whole set. Good luck on the "
                       "exam!")
