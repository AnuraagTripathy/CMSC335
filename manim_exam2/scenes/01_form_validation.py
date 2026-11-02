from common import *

HTML = '''
<form action="./process.php" method="post">
  Name: <input type="text" id="name" name="name"><br>
  Route: <input type="text" id="route" name="route"
                value="MD-95"><br>
  <button>Submit</button>
  <button type="reset">Clear</button>
</form>
<script>
  window.onsubmit = validateRequest;
</script>
'''

JS1 = '''
function validateRequest() {
  let errors = "";

  let name = document.getElementById("name").value;
  if (name.trim() === "") {
    errors += "|No name";
  }
'''

JS2 = '''
  let [state, num] = document.getElementById("route")
                             .value.split("-");
  state = state.trim().toLowerCase();
  if (state !== "md" && state !== "va") {
    errors += "|Invalid state";
  }
  num = Number(num);
  if (isNaN(num) || num < 1 || num > 999) {
    errors += "|Invalid route";
  }
'''

JS3 = '''
  if (errors !== "") {
    alert(errors);      // ONE alert with every problem
    return false;       // false = do NOT send the form
  }
  let msg = `Request route ${state.toUpperCase()}-${num}?`;
  return window.confirm(msg);  // OK -> true, Cancel -> false
}
'''


def field(label, value, w=3.2):
    l = txt(label, 22)
    box = Rectangle(width=w, height=0.5, color=GREY_B, fill_color="#2b2e40", fill_opacity=1)
    v = (mono(value, 20) if value.strip() else txt("(only spaces)", 18, GREY_B)).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.12)
    return VGroup(l, VGroup(box, v)).arrange(RIGHT, buff=0.25)


def button(label, color="#3a86ff"):
    t = txt(label, 20)
    b = RoundedRectangle(corner_radius=0.08, width=t.width + 0.5, height=0.5, fill_color=color,
                         fill_opacity=1, stroke_width=0)
    return VGroup(b, t.move_to(b))


def dialog(title, msg, buttons):
    t = txt(title, 18, GREY_B)
    m = mono(msg, 22)
    bs = VGroup(*[button(b, "#555b75" if b == "Cancel" else "#3a86ff") for b in buttons]).arrange(RIGHT, buff=0.2)
    inner = VGroup(t, m, bs).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    bs.align_to(inner, RIGHT)
    bg = SurroundingRectangle(inner, buff=0.3, color=WHITE, fill_color="#3b3f55", fill_opacity=1, corner_radius=0.1)
    return VGroup(bg, inner)


class FormValidation(ExamScene):
    def construct(self):
        self.intro(1, "Form + JavaScript Validation", "Biggest problem on the exam: 46-78 of 200 pts")

        self.slide("The HTML side", HTML,
                   "action = where data goes\n"
                   "method=\"post\" = how it's sent\n\n"
                   "name=\"...\" is the key the\n"
                   "server receives (id is for JS)\n\n"
                   "value=\"MD-95\" = default text\n\n"
                   "A bare <button> is a SUBMIT\n"
                   "button by default\n"
                   "type=\"reset\" clears the form",
                   trap="A <button> with no type submits the form. Use type=\"reset\" to clear, type=\"button\" for neither.")

        self.slide("Hooking up validation",
                   "window.onsubmit = validateRequest;   // no ()!\n\n"
                   "function validateRequest() {\n"
                   "  // ...checks...\n"
                   "  return false;   // blocks submission\n"
                   "  return true;    // form is sent to action\n"
                   "}",
                   "Assign the function itself.\n"
                   "validateRequest() with parens\n"
                   "would call it immediately and\n"
                   "assign its return value.\n\n"
                   "The return value decides\n"
                   "whether the form is sent.",
                   trap="window.onsubmit = validateRequest(); is wrong: it runs once on page load.")

        # ---- the worked problem ----------------------------------------
        self.header("Worked problem (exam style)")
        spec = txt("Requirements:\n"
                   "1. Name must not be blank (spaces only counts as blank)\n"
                   "2. Route is STATE-NUMBER, e.g. MD-95\n"
                   "     state must be md or va (any case)\n"
                   "     number must be a number from 1 to 999\n"
                   "3. Show ONE alert listing every error, e.g. |No name|Invalid state\n"
                   "4. If valid, ask for confirmation; send only if user clicks OK", 24)
        spec.next_to(self.head, DOWN, buff=0.5)
        self.play(Write(spec), run_time=3)
        self.wait(10)
        self.clear()

        self.slide("Step 1: start the error string, check blank",
                   JS1,
                   ".value is always a STRING\n\n"
                   "trim() removes leading and\n"
                   "trailing spaces, so \"   \"\n"
                   "becomes \"\" and is caught\n\n"
                   "errors += builds up the\n"
                   "message; don't alert yet",
                   trap="Checking name === \"\" alone misses an input of only spaces. Use name.trim() === \"\".")

        self.slide("Step 2: split the dash-separated value", JS2,
                   "\"MD-95\".split(\"-\")\n  -> [\"MD\", \"95\"]\n"
                   "Array destructuring:\n  state = \"MD\", num = \"95\"\n\n"
                   "toLowerCase() so MD, Md,\n md all match\n\n"
                   "Number(\"95\") -> 95\n"
                   "Number(\"95a\") -> NaN",
                   out='Number("")        -> 0      (caught by num < 1)\n'
                       'Number(" 95 ")    -> 95\n'
                       'Number(undefined) -> NaN    (input had no dash)')

        self.slide("Step 3: one alert, or confirm", JS3,
                   "If any error was added:\n alert once, return false\n\n"
                   "Otherwise return what\n"
                   "confirm() returns:\n"
                   " OK -> true -> sent\n"
                   " Cancel -> false -> not sent",
                   trap="return window.confirm(msg). Without the return, the form is sent even after Cancel.")

        # ---- simulate two submissions -----------------------------------
        self.header("Run it: bad input")
        f1 = field("Name:", "   ")
        f2 = field("Route:", "ny-95")
        bts = VGroup(button("Submit"), button("Clear", "#555b75")).arrange(RIGHT, buff=0.3)
        form = VGroup(f1, f2, bts).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=1).shift(UP * 0.5)
        self.play(FadeIn(form))
        self.wait(1)
        self.play(Indicate(bts[0]))
        trace = txt('name.trim() === ""  ->  "|No name"\n'
                    'state = "ny"  ->  "|Invalid state"\n'
                    'num = 95  ->  OK', 22).to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        self.play(Write(trace), run_time=2)
        self.wait(3)
        d = dialog("This page says", "|No name|Invalid state", ["OK"]).next_to(trace, DOWN, buff=0.5)
        self.play(FadeIn(d, scale=0.9))
        res = txt("return false  ->  form NOT sent", 24, BAD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(res))
        self.wait(4)
        self.clear()

        self.header("Run it: good input")
        f1 = field("Name:", "Ann")
        f2 = field("Route:", " Md-95 ")
        bts = VGroup(button("Submit"), button("Clear", "#555b75")).arrange(RIGHT, buff=0.3)
        form = VGroup(f1, f2, bts).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=1).shift(UP * 0.5)
        self.play(FadeIn(form))
        self.play(Indicate(bts[0]))
        d = dialog("This page says", "Request route MD-95?", ["OK", "Cancel"]).to_edge(RIGHT, buff=0.8)
        self.play(FadeIn(d, scale=0.9))
        self.wait(2)
        self.play(Indicate(d[1][2][0]))
        res = txt("OK -> confirm returns true -> POST to ./process.php\nCancel -> false -> stays on page", 24, OK).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(res))
        self.wait(5)
        self.clear()

        self.practice(1,
                      "Field id=\"room\" holds BUILDING,ROOM (comma-separated), e.g. AVW,1112.\n"
                      "Write the checks: building not blank -> \"|No building\";\n"
                      "room must be a number from 1000 to 4999 -> \"|Invalid room\".",
                      None,
                      '''
let errors = "";
let [bldg, room] = document.getElementById("room").value.split(",");
if (bldg === undefined || bldg.trim() === "") {
  errors += "|No building";
}
room = Number(room);
if (isNaN(room) || room < 1000 || room > 4999) {
  errors += "|Invalid room";
}
// " ,2000" -> "|No building"      "IRB" -> "|Invalid room"
// "IRB, 2120 " -> ""  (Number trims spaces)
''', answer_is_code=True)

        self.practice(2,
                      "The user enters MD95 (no dash) and a valid name, then clicks Submit.\n"
                      "Using validateRequest from this video: what does the alert say,\n"
                      "and is the form sent?",
                      None,
                      '"MD95".split("-") -> ["MD95"], so state = "md95", num = undefined\n\n'
                      'alert shows:  |Invalid state|Invalid route\n'
                      'return false -> the form is NOT sent')

        self.outro("window.onsubmit = fn  (no parentheses)\n"
                   "Read .value, then split / trim / toLowerCase / Number\n"
                   "isNaN(num) || out of range  ->  add to error string\n"
                   "Errors: one alert, return false.  Else: return window.confirm(msg)")
