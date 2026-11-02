from common import *

SRC = '''
function Boat(name) {
  this.name = name;
}
Boat.prototype.capacity = 50;
const a = new Boat("local"),
      b = new Boat("small");
'''


def box(title, rows, color, w=3.0):
    t = txt(title, 22, color, weight=BOLD)
    rs = VGroup(*[mono(r, 18) for r in rows]) if rows else VGroup()
    if rows:
        rs.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    content = VGroup(t, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.15) if rows else t
    r = RoundedRectangle(corner_radius=0.1, width=max(w, content.width + 0.4), height=content.height + 0.4,
                         color=color, fill_color=color, fill_opacity=0.12)
    content.move_to(r)
    g = VGroup(r, content)
    g.rows = rs
    return g


def arrow(m1, m2, label, color=GREY_A, angle=0, lpos=0.5, side=UP):
    a = CurvedArrow(m1, m2, angle=angle, color=color, stroke_width=3, tip_length=0.2) if angle else \
        Arrow(m1, m2, buff=0.05, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.12)
    l = mono(label, 16, color)
    l.move_to(a.point_from_proportion(lpos)).shift(side * 0.25)
    return VGroup(a, l)


class PrototypeDiagram(ExamScene):
    def construct(self):
        self.intro(3, "The Prototype Diagram", "10-14 of 200 pts: draw every arrow",
                   say="This one is a drawing question, worth 10 to 14 points: the prototype diagram. The points are "
                       "in the arrows, so let's build the diagram one arrow at a time and talk about why each one "
                       "is there.")

        self.header("The code you'll be given")
        c = code(SRC, w=8)
        c.next_to(self.head, DOWN, buff=0.5)
        n = txt("Draw: the function, its prototype object, both instances,\n"
                "and every prototype / constructor / __proto__ link up to null.", 24)
        n.next_to(c, DOWN, buff=0.5)
        with self.say("Here's typical exam code. A constructor function Boat that stores a name, a capacity "
                      "property added to Boat dot prototype, and two boats made with new."):
            self.play(FadeIn(c))
            hl = self.highlight(c, (1, 3))
            hl = self.highlight(c, 4, hl)
            hl = self.highlight(c, (5, 6), hl)
        with self.say("You need to draw the function, its prototype object, both instances, and every "
                      "prototype, constructor, and proto link, all the way up to null."):
            self.play(FadeOut(hl), Write(n))
        self.play(FadeOut(n), FadeOut(self.head))
        self.head = None
        self.play(c.animate.scale(0.55).to_edge(LEFT, buff=0.25).set_y(-0.9))

        boat = box("Boat  (function)", ["prototype"], BLUE_C).move_to([-4.6, 2.2, 0])
        proto = box("Boat.prototype", ["capacity: 50", "constructor", "__proto__"], ACCENT).move_to([0.2, 2.2, 0])
        A = box("a", ['name: "local"', "__proto__"], OK, w=2.6).move_to([4.9, 2.7, 0])
        B = box("b", ['name: "small"', "__proto__"], OK, w=2.6).move_to([4.9, 0.6, 0])
        objp = box("Object.prototype", ["toString, hasOwnProperty...", "__proto__"], PURPLE_B).move_to([0.2, -0.7, 0])
        nul = box("null", None, GREY_B, w=1.4).move_to([0.2, -2.5, 0])

        a1 = arrow(boat.get_right() + UP * 0.25, proto.get_left() + UP * 0.25, "prototype", BLUE_C)
        cap = txt("Every function gets a prototype object.\nBoat.prototype.capacity = 50 puts\ncapacity THERE, not on a or b.", 22)
        cap.to_corner(DR, buff=0.4)
        with self.say("Start with Boat itself. Functions are objects too, and every function automatically gets "
                      "a property called prototype that points to a separate object, Boat dot prototype. "
                      "The capacity line puts capacity on that object, not on a or b."):
            self.play(FadeIn(boat))
            self.play(FadeIn(proto), GrowFromEdge(a1, LEFT))
            self.play(FadeIn(cap))
        a2 = arrow(proto.get_left() + DOWN * 0.35, boat.get_right() + DOWN * 0.35, "constructor", ACCENT, side=DOWN)
        with self.say("The prototype object has a constructor property that points right back to Boat. "
                      "So you get a pair of arrows: prototype going out, constructor coming back."):
            self.play(GrowFromEdge(a2, RIGHT))
            self.play(Transform(cap, txt("Boat.prototype.constructor\npoints back to Boat.", 22).to_corner(DR, buff=0.4)))

        a3 = arrow(A.get_left(), proto.get_right() + UP * 0.3, "__proto__", OK)
        a4 = arrow(B.get_left(), proto.get_right() + DOWN * 0.3, "__proto__", OK, side=DOWN)
        with self.say("Now the instances. new Boat makes a fresh object and runs the constructor, so a and b each "
                      "get their own name. And new also sets each object's hidden proto link to Boat dot prototype. "
                      "That link is how they'll find capacity."):
            self.play(FadeIn(A), FadeIn(B))
            self.play(GrowFromEdge(a3, RIGHT), GrowFromEdge(a4, RIGHT))
            self.play(Transform(cap, txt("new Boat(...) makes an object with\nits OWN name, whose __proto__ is\nBoat.prototype.", 22).to_corner(DR, buff=0.4)))

        a5 = arrow(proto.get_bottom(), objp.get_top(), "__proto__", PURPLE_B, side=RIGHT * 2.6)
        a6 = arrow(objp.get_bottom(), nul.get_top(), "__proto__", GREY_B, side=RIGHT * 2.6)
        with self.say("Don't stop there. Boat dot prototype is itself a plain object, so its proto is Object dot "
                      "prototype, where methods like toString live. And Object dot prototype's proto is null. "
                      "That's the end of the chain, and the exam expects you to draw it."):
            self.play(FadeIn(objp), GrowFromEdge(a5, UP))
            self.play(FadeIn(nul), GrowFromEdge(a6, UP))
            self.play(Transform(cap, txt("Boat.prototype is a plain object, so\nits __proto__ is Object.prototype,\nwhose __proto__ is null (end).", 22).to_corner(DR, buff=0.4)))
        self.play(FadeOut(cap))
        tr = self.trap("The instances have NO prototype property and NO capacity of their own. Only the function has .prototype; objects have __proto__.",
                       say="Don't draw a prototype property or a capacity inside a or b. Only the function has a "
                           "prototype property. Ordinary objects have a proto link instead.")
        self.play(FadeOut(tr))

        # ---- property lookup ----
        def lookup(expr, path, result, note, speech):
            q = mono(expr, 26, ACCENT)
            r = mono(f"-> {result}", 26, OK).next_to(q, RIGHT, buff=0.3)
            nt = txt(note, 20, GREY_A).next_to(VGroup(q, r), DOWN, buff=0.15, aligned_edge=LEFT)
            VGroup(q, r, nt).to_corner(DR, buff=0.4)
            with self.say(speech):
                self.play(FadeIn(q))
                dot = Dot(path[0].get_center(), color=RED, radius=0.12)
                self.play(FadeIn(dot), Indicate(path[0], color=RED))
                for m in path[1:]:
                    self.play(dot.animate.move_to(m.get_center()), run_time=0.8)
                    self.play(Indicate(m, color=RED), run_time=0.6)
                self.play(FadeIn(r), FadeIn(nt))
            self.wait(1)
            self.play(FadeOut(q), FadeOut(r), FadeOut(dot), FadeOut(nt))

        lookup("a.name", [A], '"local"', "found on a itself\n(own property)",
               "Now, why does this matter? Property lookup. For a dot name, JavaScript checks a first, finds name "
               "right there, and returns local.")
        lookup("a.capacity", [A, proto], "50", "not on a, so follow\n__proto__ to Boat.prototype",
               "For a dot capacity, it's not on a, so JavaScript follows the proto arrow to Boat dot prototype, and "
               "finds 50.")
        lookup("a.toString", [A, proto, objp], "function", "found two levels up,\non Object.prototype",
               "a dot toString isn't on a or on Boat dot prototype, so it keeps climbing and finds it on Object dot "
               "prototype.")
        lookup("a.wings", [A, proto, objp, nul], "undefined", "reached null: not found,\nso undefined (no error)",
               "And a dot wings walks the whole chain, hits null, and gives undefined. Not an error, just undefined.")

        # shadowing
        q = mono("a.capacity = 10;", 26, ACCENT)
        nt = txt("Assignment creates an OWN property on a\n(it shadows the prototype's).\n"
                 "a.capacity -> 10\nb.capacity -> 50 (from Boat.prototype)", 20, GREY_A)
        nt.next_to(q, DOWN, buff=0.15, aligned_edge=LEFT)
        VGroup(q, nt).to_corner(DR, buff=0.4)
        newA = box("a", ['name: "local"', "capacity: 10", "__proto__"], OK, w=2.6).move_to(A).align_to(A, UP)
        with self.say("What if we assign a dot capacity equals 10? Assignment never walks the chain. It creates "
                      "a new own property on a, which shadows the prototype's value. So a dot capacity is 10, but "
                      "b still finds 50 on the prototype."):
            self.play(FadeIn(q))
            self.play(Transform(A, newA))
            self.play(FadeIn(nt))
        q2 = mono("Boat.prototype.capacity = 75;", 24, ACCENT).move_to(q).to_edge(RIGHT, buff=0.4)
        newP = box("Boat.prototype", ["capacity: 75", "constructor", "__proto__"], ACCENT).move_to(proto)
        nt2 = txt("Changing the prototype affects every\nobject that doesn't shadow it:\n"
                  "b.capacity -> 75\na.capacity is still 10", 20, GREY_A).next_to(q2, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.say("And if we change the prototype's capacity to 75, every object that doesn't shadow it sees "
                      "the change instantly. b now gives 75, while a still says 10."):
            self.play(Transform(q, q2), Transform(proto, newP), Transform(nt, nt2))
        self.wait(1)
        self.clear(keep_head=False)

        self.practice(1, "Draw the prototype diagram (list every box and arrow) for:",
                      '''
function Lamp(color) { this.color = color; }
Lamp.prototype.watts = 60;
const x = new Lamp("red");
''',
                      "Boxes: Lamp (function), Lamp.prototype {watts: 60}, x {color: \"red\"},\n"
                      "       Object.prototype, null\n\n"
                      "Lamp --prototype--> Lamp.prototype\n"
                      "Lamp.prototype --constructor--> Lamp\n"
                      "x --__proto__--> Lamp.prototype\n"
                      "Lamp.prototype --__proto__--> Object.prototype --__proto__--> null",
                      say_q="Draw the prototype diagram for this Lamp code. List every box and every arrow.",
                      say_a="Five boxes: the Lamp function, Lamp dot prototype holding watts 60, x holding its own "
                            "color, Object dot prototype, and null. The arrows: Lamp's prototype goes to Lamp dot "
                            "prototype, whose constructor points back to Lamp. x's proto goes to Lamp dot prototype. "
                            "Then Lamp dot prototype's proto goes to Object dot prototype, and that goes to null.")

        self.practice(2, "What does this print?",
                      '''
function Lamp(color) { this.color = color; }
Lamp.prototype.watts = 60;
const l1 = new Lamp("red"), l2 = new Lamp("blue");
l1.watts = 40;
Lamp.prototype.watts = 75;
console.log(l1.watts, l2.watts);
delete l1.watts;
console.log(l1.watts);
''',
                      "40 75\n75\n\nl1 has its own watts (40) until it is deleted;\n"
                      "then lookup falls back to Lamp.prototype (75).",
                      say_q="What does this print?",
                      say_a="First line: 40 and 75. l1 has its own watts of 40, which shadows the prototype, and l2 "
                            "sees the updated prototype value of 75. After deleting l1's own watts, lookup falls back "
                            "to the prototype, so the second line prints 75.")

        self.outro("Function --prototype--> F.prototype --constructor--> Function\n"
                   "instance --__proto__--> F.prototype --__proto__--> Object.prototype --> null\n"
                   "Own properties (this.x) live in the instance box\n"
                   "Lookup walks __proto__ links; not found at null -> undefined",
                   say="Recap. The function's prototype arrow goes to its prototype object, and constructor comes "
                       "back. Each instance has a proto arrow to that prototype object, which links to Object dot "
                       "prototype, then null. Own properties live in the instance box. And lookup simply walks the "
                       "proto arrows until it finds the property, or reaches null and gives undefined.")
