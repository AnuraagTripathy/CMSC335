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
    def run_puzzle(self, title, lines, steps, intro_say):
        """steps: ("say", caption, speech) starts a narrated group; the steps after it run during the speech."""
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
        with self.say(intro_say):
            self.play(FadeIn(cg), FadeIn(stack), FadeIn(micro), FadeIn(macro), FadeIn(cons_box), FadeIn(cons_t))
        S, MI, MA, C = [], [], [], []
        st8 = {"hl": None, "cap": None}

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

        def do(st):
            kind, arg = st[0], st[1] if len(st) > 1 else None
            if kind == "line":
                new = SurroundingRectangle(code_lines[arg], color=ACCENT, buff=0.06)
                hl = st8["hl"]
                self.play(Create(new) if hl is None else Transform(hl, new), run_time=0.4)
                if hl is None:
                    st8["hl"] = new
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

        groups, cur = [], (None, None, [])
        for st in steps:
            if st[0] == "say":
                groups.append(cur)
                cur = (st[1], st[2], [])
            else:
                cur[2].append(st)
        groups.append(cur)
        for caption, speech, actions in groups:
            if speech is None:
                for a in actions:
                    do(a)
                continue
            with self.say(speech):
                new = txt(textwrap.fill(caption, 52), 21, GREY_A).move_to([3.2, -3.1, 0])
                if new.width > 7.6:
                    new.scale_to_fit_width(7.6)
                if st8["cap"] is None:
                    self.play(FadeIn(new))
                else:
                    self.play(FadeOut(st8["cap"]), FadeIn(new))
                st8["cap"] = new
                for a in actions:
                    do(a)
        self.wait(2)
        self.clear()

    def construct(self):
        self.intro(6, "The Event Loop", "Output-order puzzles + the setInterval return trap",
                   say="The event loop. This is where those, what order does this print, questions come from. Once "
                       "you see the three places code waits, these puzzles become mechanical.")

        self.slide("Three places code waits", None,
                   "Call stack: what is running RIGHT NOW (one thing at a time)\n\n"
                   "Macrotask queue: setTimeout / setInterval callbacks, events\n\n"
                   "Microtask queue: promise reactions (.then / .catch / await resumes),\n"
                   "  e.g. what runs after fetch resolves\n\n"
                   "The loop: run the whole script -> drain ALL microtasks ->\n"
                   "  take ONE macrotask -> drain ALL microtasks -> repeat",
                   say=["JavaScript runs one thing at a time, on the call stack. Anything that has to wait goes into "
                        "one of two queues. The macrotask queue holds timer callbacks from setTimeout and "
                        "setInterval, plus events. The microtask queue holds promise reactions, like dot then "
                        "callbacks, and the code that runs after fetch resolves.",
                        "And here's the rule that decides every puzzle. First, the whole script runs. Then every "
                        "microtask runs, until that queue is empty. Only then does the loop take one macrotask. "
                        "After it, all microtasks again, and repeat."])

        self.run_puzzle("Puzzle 1",
                        ['console.log("Dog");', 'setTimeout(() => console.log("Cat"), 0);', 'console.log("Lion");'],
                        [("say", "The script itself runs on the call stack, top to bottom.",
                          "The script goes on the call stack and runs top to bottom. Line one logs Dog right away."),
                         ("push", "script"),
                         ("line", 0), ("push", 'log("Dog")'), ("log", "Dog"), ("pop",),
                         ("say", "setTimeout only REGISTERS the callback. After 0 ms it waits in the macrotask queue.",
                          "Line two is setTimeout with zero milliseconds. It doesn't run the callback. It only "
                          "registers it, and after zero milliseconds the callback goes into the macrotask queue, "
                          "where it has to wait its turn."),
                         ("line", 1), ("push", "setTimeout(...)"),
                         ("macro", '() => log("Cat")'), ("pop",),
                         ("say", "The script keeps going: Lion is logged.",
                          "The script keeps going, and line three logs Lion. Now the script is finished, and "
                          "the stack is empty."),
                         ("line", 2), ("push", 'log("Lion")'), ("log", "Lion"), ("pop",),
                         ("pop",),
                         ("say", "Stack empty, no microtasks: the loop takes the next macrotask.",
                          "There are no microtasks, so the loop takes the next macrotask, and finally logs Cat."),
                         ("run_macro",), ("log", "Cat"), ("pop",),
                         ("say", "Output: Dog Lion Cat. A 0 ms timeout still waits for the script to finish.",
                          "So the output is Dog, Lion, Cat. A zero millisecond timeout still waits for all the "
                          "synchronous code to finish.")],
                        intro_say="Puzzle one. On the left is the code, in the middle the call stack and the two "
                                  "queues, and on the bottom left, the console.")

        self.run_puzzle("Puzzle 2: promises vs setTimeout",
                        ['console.log("1");', 'setTimeout(() => console.log("2"), 0);',
                         'Promise.resolve().then(() => console.log("3"));', 'console.log("4");'],
                        [("say", "1 is logged; the timer callback goes to the macrotask queue.",
                          "Now let's mix in a promise. One is logged immediately. The timeout's callback goes to "
                          "the macrotask queue, exactly like before."),
                         ("push", "script"),
                         ("line", 0), ("log", "1"),
                         ("line", 1), ("macro", '() => log("2")'),
                         ("say", "The promise is already resolved, so its .then callback goes to the MICROtask queue.",
                          "Promise dot resolve gives an already resolved promise, so its then callback goes "
                          "straight into the microtask queue."),
                         ("line", 2),
                         ("micro", '() => log("3")'),
                         ("say", "4 is logged; the script is done.",
                          "Then four is logged, and the script is done."),
                         ("line", 3), ("log", "4"),
                         ("pop",),
                         ("say", "Script done. ALL microtasks run before the next macrotask.",
                          "Now the key rule. All microtasks run before the next macrotask. So three prints next, "
                          "and only after that does the timer's callback get to print two."),
                         ("run_micro",), ("log", "3"), ("pop",),
                         ("run_macro",), ("log", "2"), ("pop",),
                         ("say", "Output: 1 4 3 2. Synchronous first, then microtasks, then macrotasks.",
                          "One, four, three, two. Synchronous code first, then microtasks, then macrotasks.")],
                        intro_say="Puzzle two mixes a promise with setTimeout.")

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
                   trap="A function can't return a value that is assigned later inside setTimeout / setInterval.",
                   say=[("Here's a trap the exam has used. getCount declares count, and sets up an interval that "
                         "will set count to 10.", (1, 6)),
                        ("But the return happens right now, during the script. The interval callback can't run "
                         "until the stack is empty, which is long after getCount has already returned.", 7)],
                   say_out="So it prints undefined. The fix is to return a promise and call resolve with 10 inside "
                           "the callback.",
                   say_trap="A function can't return a value that only gets assigned later, inside a setTimeout or "
                            "setInterval callback.")

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
                   out="1   (after 1 s)\n2   (after 2 s)\n3   (after 3 s, then stops)",
                   say=[("setInterval runs its callback again and again, every given number of milliseconds. It "
                         "returns an id, so save it.", 2),
                        ("Each time, we bump n and log it.", (3, 4)),
                        ("When n hits 3, clearInterval with that id stops it. setTimeout, by contrast, runs only "
                         "once, and clearTimeout cancels it.", (5, 7))],
                   say_out="So we get 1, 2, and 3, one second apart, and then it stops.")

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
                      "they were queued: A (queued by the script), C (queued later, inside B).",
                      say_q="What does this print, in order?",
                      say_a="E, B, D, A, C. E is the only synchronous log, so it's first. Then the microtasks, in the "
                            "order they were queued: B, then D. While B ran, it queued another timer, C. Now the "
                            "macrotasks run in order: A was queued by the script, so it goes before C.")

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
''',
                      say_q="Fix getCount so the caller can actually get the 10, and show how to call it.",
                      say_a="Return a new Promise. Inside the interval callback, clear the interval and call resolve "
                            "with 10. The caller can't get a plain value back, so it uses dot then to receive the "
                            "count.",
                      answer_is_code=True)

        self.outro("Sync code first (the whole script)\n"
                   "Then ALL microtasks (promise .then / await)\n"
                   "Then ONE macrotask (setTimeout / setInterval), then microtasks again...\n"
                   "Values set in a timer callback can't be returned directly: use a Promise",
                   say="Recap. All the synchronous code runs first. Then all the microtasks, meaning promise "
                       "callbacks. Then one macrotask, like a timer callback, and then microtasks again. And a value "
                       "set inside a timer callback can't be returned directly. Wrap it in a promise.")
