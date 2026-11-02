from common import *


def column(title, x, color):
    box = Rectangle(width=2.4, height=4.1, color=color).move_to([x, -0.15, 0])
    t = txt(title, 20, color, weight=BOLD).next_to(box, UP, buff=0.12)
    return VGroup(box, t)


def item(label, color):
    t = mono(label, 16)
    r = RoundedRectangle(corner_radius=0.08, width=2.2, height=0.48, fill_color=color, fill_opacity=0.35,
                         color=color)
    if t.width > 2.0:
        t.scale_to_fit_width(2.0)
    return VGroup(r, t.move_to(r))


class EventLoop(ExamScene):
    def run_puzzle(self, title, lines, steps):
        self.header(title)
        code_lines = VGroup(*[mono(l, 19) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        if code_lines.width > 5.6:
            code_lines.scale_to_fit_width(5.6)
        code_bg = SurroundingRectangle(code_lines, color=GREY_B, buff=0.2, corner_radius=0.08)
        cg = VGroup(code_bg, code_lines).to_corner(UL, buff=0.4).shift(DOWN * 0.8)
        stack = column("Call Stack", 0.6, BLUE_C)
        micro = column("Microtasks", 3.2, PURPLE_B)
        macro = column("Macrotasks", 5.8, ORANGE)
        cons_box = Rectangle(width=5.9, height=2.2, color=OK).to_corner(DL, buff=0.35)
        cons_t = txt("Console", 20, OK, weight=BOLD).next_to(cons_box, UP, buff=0.1, aligned_edge=LEFT)
        self.play(FadeIn(cg), FadeIn(stack), FadeIn(micro), FadeIn(macro), FadeIn(cons_box), FadeIn(cons_t))
        S, MI, MA, C = [], [], [], []
        hl = None
        cap = None

        def place(lst, col, from_bottom):
            box = col[0]
            anims = []
            for i, m in enumerate(lst):
                if from_bottom:
                    target = box.get_bottom() + UP * (0.35 + 0.55 * i)
                else:
                    target = box.get_top() + DOWN * (0.35 + 0.55 * i)
                anims.append(m.animate.move_to(target))
            return anims

        for st in steps:
            kind, arg = st[0], st[1] if len(st) > 1 else None
            if kind == "line":
                new = SurroundingRectangle(code_lines[arg], color=ACCENT, buff=0.06)
                self.play(Create(new) if hl is None else Transform(hl, new), run_time=0.4)
                if hl is None:
                    hl = new
            elif kind == "say":
                new = txt(textwrap.fill(arg, 52), 21, GREY_A).move_to([3.2, -3.1, 0])
                if new.width > 7.6:
                    new.scale_to_fit_width(7.6)
                if cap is None:
                    self.play(FadeIn(new))
                else:
                    self.play(FadeOut(cap), FadeIn(new))
                cap = new
                self.wait(read_time(arg))
            elif kind == "push":
                m = item(arg, BLUE_C).move_to(stack[0].get_top() + UP * 0.3)
                S.append(m)
                self.play(FadeIn(m), *place(S, stack, True), run_time=0.5)
            elif kind == "pop":
                m = S.pop()
                self.play(FadeOut(m, shift=UP * 0.3), run_time=0.4)
            elif kind in ("micro", "macro"):
                lst, col, color = (MI, micro, PURPLE_B) if kind == "micro" else (MA, macro, ORANGE)
                m = item(arg, color).move_to(stack[0].get_center())
                lst.append(m)
                self.play(FadeIn(m), *place(lst, col, False), run_time=0.7)
            elif kind in ("run_micro", "run_macro"):
                lst, col = (MI, micro) if kind == "run_micro" else (MA, macro)
                m = lst.pop(0)
                S.append(m)
                self.play(m.animate.move_to(stack[0].get_bottom() + UP * (0.35 + 0.55 * (len(S) - 1))),
                          *place(lst, col, False), run_time=0.8)
            elif kind == "log":
                t = mono(arg, 22, OK)
                C.append(t)
                t.move_to(cons_box.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.35)
                t.shift(RIGHT * 1.1 * (len(C) - 1))
                self.play(FadeIn(t, scale=1.3), run_time=0.5)
            elif kind == "wait":
                self.wait(arg)
        self.wait(3)
        self.clear()

    def construct(self):
        self.intro(6, "The Event Loop", "Output-order puzzles + the setInterval return trap")

        self.slide("Three places code waits", None,
                   "Call stack: what is running RIGHT NOW (one thing at a time)\n\n"
                   "Macrotask queue: setTimeout / setInterval callbacks, events\n\n"
                   "Microtask queue: promise reactions (.then / .catch / await resumes),\n"
                   "  e.g. what runs after fetch resolves\n\n"
                   "The loop: run the whole script -> drain ALL microtasks ->\n"
                   "  take ONE macrotask -> drain ALL microtasks -> repeat")

        self.run_puzzle("Puzzle 1",
                        ['console.log("Dog");', 'setTimeout(() => console.log("Cat"), 0);', 'console.log("Lion");'],
                        [("say", "The script itself runs on the call stack, top to bottom."),
                         ("push", "script"),
                         ("line", 0), ("push", 'log("Dog")'), ("log", "Dog"), ("pop",),
                         ("line", 1), ("push", "setTimeout(...)"),
                         ("say", "setTimeout only REGISTERS the callback. After 0 ms it waits in the macrotask queue."),
                         ("macro", '() => log("Cat")'), ("pop",),
                         ("line", 2), ("push", 'log("Lion")'), ("log", "Lion"), ("pop",),
                         ("pop",),
                         ("say", "Stack empty, no microtasks: the loop takes the next macrotask."),
                         ("run_macro",), ("log", "Cat"), ("pop",),
                         ("say", "Output: Dog Lion Cat. A 0 ms timeout still waits for the script to finish.")])

        self.run_puzzle("Puzzle 2: promises vs setTimeout",
                        ['console.log("1");', 'setTimeout(() => console.log("2"), 0);',
                         'Promise.resolve().then(() => console.log("3"));', 'console.log("4");'],
                        [("push", "script"),
                         ("line", 0), ("log", "1"),
                         ("line", 1), ("macro", '() => log("2")'),
                         ("line", 2),
                         ("say", "The promise is already resolved, so its .then callback goes to the MICROtask queue."),
                         ("micro", '() => log("3")'),
                         ("line", 3), ("log", "4"),
                         ("pop",),
                         ("say", "Script done. ALL microtasks run before the next macrotask."),
                         ("run_micro",), ("log", "3"), ("pop",),
                         ("run_macro",), ("log", "2"), ("pop",),
                         ("say", "Output: 1 4 3 2. Synchronous first, then microtasks, then macrotasks.")])

        self.slide("The return-value trap",
                   '''
function getCount() {
  let count;
  const id = setInterval(() => {
    count = 10;
    clearInterval(id);
  }, 100);
  return count;      // runs NOW, callback runs later
}
console.log(getCount());
''',
                   "return happens during the\nscript; the callback can't\nrun until the stack is empty.\n\n"
                   "Fix: return a Promise and\nresolve(10) inside the\ncallback.",
                   out="undefined",
                   trap="A function can't return a value that is assigned later inside setTimeout / setInterval.")

        self.slide("setInterval + clearInterval",
                   '''
let n = 0;
const id = setInterval(() => {
  n++;
  console.log(n);
  if (n === 3) {
    clearInterval(id);   // stop it
  }
}, 1000);
''',
                   "setInterval repeats every\nms until clearInterval(id)\n\n"
                   "setTimeout runs once\n(clearTimeout cancels it)\n\n"
                   "Keep the returned id!",
                   out="1   (after 1 s)\n2   (after 2 s)\n3   (after 3 s, then stops)")

        self.practice(1, "What does this print, in order?",
                      '''
setTimeout(() => console.log("A"), 0);
Promise.resolve().then(() => {
  console.log("B");
  setTimeout(() => console.log("C"), 0);
});
Promise.resolve().then(() => console.log("D"));
console.log("E");
''',
                      "E B D A C\n\nE is synchronous. Microtasks B then D. Then macrotasks in the order\n"
                      "they were queued: A (queued by the script), C (queued later, inside B).")

        self.practice(2, "Fix getCount so the caller can get the 10. Show how to call it.",
                      None,
                      '''
function getCount() {
  return new Promise(resolve => {
    const id = setInterval(() => {
      clearInterval(id);
      resolve(10);
    }, 100);
  });
}
getCount().then(count => console.log(count));   // 10
''', answer_is_code=True)

        self.outro("Sync code first (the whole script)\n"
                   "Then ALL microtasks (promise .then / await)\n"
                   "Then ONE macrotask (setTimeout / setInterval), then microtasks again...\n"
                   "Values set in a timer callback can't be returned directly: use a Promise")
