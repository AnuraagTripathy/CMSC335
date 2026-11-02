from common import *


class FreezeSeal(ExamScene):
    def construct(self):
        self.intro(12, "freeze / seal / preventExtensions", "Short answer in Problem 1")

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
        self.play(FadeIn(cells[:5]), Create(lines))
        for i in range(3):
            self.play(FadeIn(cells[5 * (i + 1):5 * (i + 2)], shift=RIGHT * 0.2))
            self.wait(2.5)
        note = txt("Each step down removes one more permission.  Check with\n"
                   "Object.isExtensible(o)   Object.isSealed(o)   Object.isFrozen(o)", 22, GREY_A)
        note.next_to(table, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(7)
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
                   out="Chess 4 undefined\ntrue false")

        self.slide("...but throw in strict mode",
                   '''
"use strict";
game.year = 2000;
// TypeError: Cannot add property year, object is not extensible

delete game.name;
// TypeError: Cannot delete property 'name' of #<Object>
''',
                   None,
                   trap="Classes and modules are always strict, so a blocked change THROWS there instead of failing silently.")

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
                   out="{ miles: 20 } false")

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
                   trap="Object.freeze does not freeze nested objects. Freeze each inner object too if needed.")

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
                      "blue 2 undefined true\n\n(a frozen object also counts as sealed)")

        self.practice(2, "Fill in: which method gives exactly this behavior?",
                      '''
// can modify existing values: yes
// can delete properties:      yes
// can add new properties:     no
''',
                      "Object.preventExtensions(obj)")

        self.outro("preventExtensions: no add\n"
                   "seal: no add, no delete (modify OK)\n"
                   "freeze: no add, no delete, no modify (read only), and it is shallow\n"
                   "Sloppy mode: silently ignored.  Strict mode: TypeError")
