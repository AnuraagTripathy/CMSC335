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
        self.intro(1, "Form + JavaScript Validation", "Biggest problem on the exam: 46-78 of 200 pts",
                   say="Hey! Let's start with the single biggest problem on Exam 2: a form plus JavaScript "
                       "validation. It's worth anywhere from 46 to 78 points, so if you only master one thing, "
                       "make it this one.")

        self.slide("The HTML side", HTML,
                   "action = where data goes\n"
                   "method=\"post\" = how it's sent\n\n"
                   "name=\"...\" is the key the\n"
                   "server receives (id is for JS)\n\n"
                   "value=\"MD-95\" = default text\n\n"
                   "A bare <button> is a SUBMIT\n"
                   "button by default\n"
                   "type=\"reset\" clears the form",
                   trap="A <button> with no type submits the form. Use type=\"reset\" to clear, type=\"button\" for neither.",
                   say=[("First, the HTML. The form tag's action says where the data goes, here process dot PHP, "
                         "and method equals post says how it's sent.", 1),
                        ("Each input gets two attributes that look alike but do different jobs. The name is the key "
                         "the server receives. The id is what your JavaScript uses with getElementById.", (2, 3)),
                        ("And value gives the field its starting text, so the route box already says M D dash 95.", 4),
                        ("Now the buttons. A plain button tag with no type is a submit button by default. "
                         "Type equals reset clears the form back to its default values.", (5, 6)),
                        ("Finally, the script hooks our validation function to the submit event.", (8, 10))],
                   say_trap="A button with no type attribute submits the form. If you want it to clear, write type "
                            "equals reset. If you want it to do neither, write type equals button.")

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
                   trap="window.onsubmit = validateRequest(); is wrong: it runs once on page load.",
                   say=[("Look closely at this line. We assign the function itself to window dot onsubmit. "
                         "No parentheses. The browser will call it for us when the user submits.", 1),
                        ("Inside, the return value is the whole game. Return false, and the submission is "
                         "blocked. The page just stays put.", 5),
                        ("Return true, and the form is sent to the action URL.", 6)],
                   say_trap="If you write validateRequest with parentheses, the function runs once, right when the "
                            "page loads, and onsubmit gets its return value instead of the function. That costs points.")

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
        with self.say("Here's a problem written the way the exam writes them. Read the requirements carefully, "
                      "because every bullet is a check you'll be graded on. One: the name can't be blank, and a "
                      "name made of only spaces counts as blank. Two: the route is a state, a dash, and a number. "
                      "The state must be M D or V A in any capitalization, and the number must be between 1 and 999. "
                      "Three: show one alert that lists every error, not one alert per error. And four: if "
                      "everything's valid, ask the user to confirm, and only send if they click OK."):
            self.play(Write(spec), run_time=3)
        self.wait(1)
        self.clear()

        self.slide("Step 1: start the error string, check blank",
                   JS1,
                   ".value is always a STRING\n\n"
                   "trim() removes leading and\n"
                   "trailing spaces, so \"   \"\n"
                   "becomes \"\" and is caught\n\n"
                   "errors += builds up the\n"
                   "message; don't alert yet",
                   trap="Checking name === \"\" alone misses an input of only spaces. Use name.trim() === \"\".",
                   say=[("Step one. We start with an empty error string. The plan is to collect every problem "
                         "in here, and only alert once at the end.", 2),
                        ("Then we read the name field's value. Remember, dot value is always a string, even "
                         "when the user typed digits.", 4),
                        ("We trim it, which removes spaces from both ends, and compare it to the empty string. "
                         "If it's blank, we tack on, bar, No name.", (5, 7))],
                   say_trap="Comparing the name to an empty string without trim misses an input of just spaces. "
                            "Always trim first.")

        self.slide("Step 2: split the dash-separated value", JS2,
                   "\"MD-95\".split(\"-\")\n  -> [\"MD\", \"95\"]\n"
                   "Array destructuring:\n  state = \"MD\", num = \"95\"\n\n"
                   "toLowerCase() so MD, Md,\n md all match\n\n"
                   "Number(\"95\") -> 95\n"
                   "Number(\"95a\") -> NaN",
                   out='Number("")        -> 0      (caught by num < 1)\n'
                       'Number(" 95 ")    -> 95\n'
                       'Number(undefined) -> NaN    (input had no dash)',
                   say=[("Step two, the route. Split on the dash turns M D dash 95 into an array of two strings, "
                         "and array destructuring drops them straight into state and num.", (1, 2)),
                        ("We trim the state and lowercase it. That way capital M D, lowercase m d, and mixed "
                         "case all compare equal to lowercase m d.", 3),
                        ("If it's neither m d nor v a, add, Invalid state. Notice it's AND here: the state is bad "
                         "only if it's not m d and also not v a.", (4, 6)),
                        ("For the number, convert with Number. Then check isNaN first, and then the range. "
                         "If any of those fail, add, Invalid route.", (7, 10))],
                   say_out="A few Number facts worth memorizing. Number of an empty string is zero, which the less "
                           "than one check catches. Number ignores surrounding spaces. And if the user typed no dash "
                           "at all, num is undefined, and Number of undefined is NaN.")

        self.slide("Step 3: one alert, or confirm", JS3,
                   "If any error was added:\n alert once, return false\n\n"
                   "Otherwise return what\n"
                   "confirm() returns:\n"
                   " OK -> true -> sent\n"
                   " Cancel -> false -> not sent",
                   trap="return window.confirm(msg). Without the return, the form is sent even after Cancel.",
                   say=[("Step three. If the error string isn't empty, show it in one alert and return false, "
                         "so nothing is sent.", (1, 4)),
                        ("Otherwise, build the confirmation message and return whatever window dot confirm "
                         "returns. Confirm gives true when the user clicks OK and false for Cancel, which is exactly "
                         "the value onsubmit needs.", (5, 6))],
                   say_trap="You have to return the result of confirm. If you just call confirm without returning it, "
                            "the function returns undefined, and the form gets sent even if the user clicked Cancel.")

        # ---- simulate two submissions -----------------------------------
        self.header("Run it: bad input")
        f1 = field("Name:", "   ")
        f2 = field("Route:", "ny-95")
        bts = VGroup(button("Submit"), button("Clear", "#555b75")).arrange(RIGHT, buff=0.3)
        form = VGroup(f1, f2, bts).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=1).shift(UP * 0.5)
        with self.say("Let's run it. The user typed only spaces for the name, and N Y dash 95 for the route, "
                      "then clicks Submit."):
            self.play(FadeIn(form))
            self.play(Indicate(bts[0]))
        trace = txt('name.trim() === ""  ->  "|No name"\n'
                    'state = "ny"  ->  "|Invalid state"\n'
                    'num = 95  ->  OK', 22).to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        with self.say("Trimming the name gives an empty string, so we add No name. The state is n y, which "
                      "isn't m d or v a, so we add Invalid state. And 95 is in range, so the number is fine."):
            self.play(Write(trace), run_time=2)
        d = dialog("This page says", "|No name|Invalid state", ["OK"]).next_to(trace, DOWN, buff=0.5)
        res = txt("return false  ->  form NOT sent", 24, BAD).to_edge(DOWN, buff=0.6)
        with self.say("So the user sees one alert with both errors, and since we return false, the form is not sent."):
            self.play(FadeIn(d, scale=0.9))
            self.play(FadeIn(res))
        self.wait(1)
        self.clear()

        self.header("Run it: good input")
        f1 = field("Name:", "Ann")
        f2 = field("Route:", " Md-95 ")
        bts = VGroup(button("Submit"), button("Clear", "#555b75")).arrange(RIGHT, buff=0.3)
        form = VGroup(f1, f2, bts).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=1).shift(UP * 0.5)
        d = dialog("This page says", "Request route MD-95?", ["OK", "Cancel"]).to_edge(RIGHT, buff=0.8)
        with self.say("Now a good one: Ann, and Md dash 95 with some extra spaces. The trim and the "
                      "lowercase take care of those, so there are no errors, and the confirm box pops up."):
            self.play(FadeIn(form))
            self.play(Indicate(bts[0]))
            self.play(FadeIn(d, scale=0.9))
        res = txt("OK -> confirm returns true -> POST to ./process.php\nCancel -> false -> stays on page", 24, OK).to_edge(DOWN, buff=0.6)
        with self.say("Click OK, confirm returns true, and the form is posted to process dot PHP. "
                      "Click Cancel, it returns false, and the user stays on the page."):
            self.play(Indicate(d[1][2][0]))
            self.play(FadeIn(res))
        self.wait(1)
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
''',
                      say_q="A field with id room holds a building and a room separated by a comma, like A V W comma "
                            "1112. Write the two checks: the building can't be blank, and the room must be a number "
                            "from 1000 to 4999.",
                      say_a="Same pattern as before, just splitting on a comma. Destructure into building and room. "
                            "If the building is blank after trimming, add No building. Then convert the room with "
                            "Number, and if it's NaN or out of range, add Invalid room. Notice that if the user types "
                            "only I R B, room is undefined, Number makes it NaN, and the check still catches it.",
                      answer_is_code=True)

        self.practice(2,
                      "The user enters MD95 (no dash) and a valid name, then clicks Submit.\n"
                      "Using validateRequest from this video: what does the alert say,\n"
                      "and is the form sent?",
                      None,
                      '"MD95".split("-") -> ["MD95"], so state = "md95", num = undefined\n\n'
                      'alert shows:  |Invalid state|Invalid route\n'
                      'return false -> the form is NOT sent',
                      say_q="The user forgets the dash and types M D 95, with a valid name. Using our "
                            "validateRequest, what does the alert say, and is the form sent?",
                      say_a="Splitting on a dash that isn't there gives a one-element array. So state is the whole "
                            "string, m d 95, which is an invalid state. And num is undefined, so Number gives NaN, "
                            "which is an invalid route. The alert shows both errors, we return false, and the form is "
                            "not sent.")

        self.outro("window.onsubmit = fn  (no parentheses)\n"
                   "Read .value, then split / trim / toLowerCase / Number\n"
                   "isNaN(num) || out of range  ->  add to error string\n"
                   "Errors: one alert, return false.  Else: return window.confirm(msg)",
                   say="To recap. Hook it up with window dot onsubmit equals the function, no parentheses. Read "
                       "each value, then split, trim, lowercase, and convert with Number. Check isNaN and the range, "
                       "and add each problem to one error string. If there are errors, one alert and return false. "
                       "Otherwise, return window dot confirm. Nail this, and you've locked in the biggest chunk of "
                       "the exam.")
