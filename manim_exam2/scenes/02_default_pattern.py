from common import *


class DefaultPattern(ExamScene):
    def construct(self):
        self.intro(2, "Custom Types: the Default Pattern + Inheritance",
                   "40-48 of 200 pts  (no class / extends / super allowed)",
                   say="Next up: custom types with the Default Pattern. This problem is worth 40 to 48 points, and "
                       "the catch is that you can't use class, extends, or super. You build everything from plain "
                       "functions and prototypes.")

        self.slide("Step 1: the constructor function",
                   '''
function Insurance(policyNumber = "None",
                   exp = "12/31/2026") {
  this.policyNumber = policyNumber;
  this.exp = exp;
}

const i1 = new Insurance();
const i2 = new Insurance("P7");
''',
                   "A regular function, called\nwith new\n\n"
                   "this = the brand-new object\n\n"
                   "Default params fill in any\n"
                   "argument that is missing\n(undefined)\n\n"
                   "ONLY data goes here",
                   out='i1 -> { policyNumber: "None", exp: "12/31/2026" }\n'
                       'i2 -> { policyNumber: "P7",   exp: "12/31/2026" }',
                   say=[("Step one is the constructor. It's just a regular function, with a capital letter by "
                         "convention. The exam usually asks for default values, so put them right in the "
                         "parameter list.", (1, 2)),
                        ("When you call it with new, JavaScript creates a brand-new empty object and makes this "
                         "point to it. So these two lines store the data on the new object.", (3, 4)),
                        ("Only data goes in the constructor. Methods go somewhere else, and you'll see why in a "
                         "second.", (7, 8))],
                   say_out="i1 passed nothing, so both defaults kick in. i2 passed only the policy number, so "
                           "the expiration date still falls back to its default.")

        self.slide("Step 2: methods go on the prototype",
                   '''
// Option A: replace the whole prototype object
Insurance.prototype = {
  constructor: Insurance,      // put it back!
  getInfo: function () {
    return `Policy ${this.policyNumber}` +
           ` exp ${this.exp}`;
  }
};

// Option B: add one method at a time
Insurance.prototype.getInfo = function () {
  return `Policy ${this.policyNumber}` +
         ` exp ${this.exp}`;
};
''',
                   "Why the prototype?\n"
                   "Every object shares ONE copy\n"
                   "of each method.\n\n"
                   "this.getInfo = function(){}\n"
                   "inside the constructor makes\n"
                   "a NEW copy for every object\n"
                   "(wastes memory).",
                   out='new Insurance().getInfo()  ->  "Policy None exp 12/31/2026"',
                   trap="Option A replaces the prototype object, so constructor is lost unless you write constructor: Insurance.",
                   say=["Step two: methods go on the prototype. Why? Every object made by Insurance shares the "
                        "same prototype, so there's exactly one copy of each method. If you wrote this dot getInfo "
                        "equals a function inside the constructor, every single object would get its own copy, "
                        "and that wastes memory. The exam likes to ask about exactly that.",
                        ("There are two ways to do it. Option A replaces the entire prototype with an object "
                         "literal that holds all the methods.", (2, 8)),
                        ("Look at this line. Because we threw away the original prototype object, we lost its "
                         "constructor property, so we have to put it back by hand.", 3),
                        ("Option B adds one method at a time to the existing prototype. Nothing gets replaced, "
                         "so constructor stays intact.", (11, 14))],
                   say_out="Either way, any Insurance object can call getInfo, and this refers to the object it "
                           "was called on.",
                   say_trap="If you replace the prototype with an object literal, the constructor property is gone "
                            "unless you write constructor colon Insurance yourself.")

        self.slide("Proof: the constructor trap",
                   '''
function A() {}
A.prototype = { hi() { return "hi"; } };   // no constructor
const x = new A();
console.log(x.constructor === A, x.constructor === Object, x.hi());

function Slow(n) { this.n = n; this.get = function () { return this.n; }; }
console.log(new Slow(1).get === new Slow(2).get);
console.log(new Insurance().getInfo === new Insurance().getInfo);
''',
                   None,
                   out="false true hi\nfalse     <- two separate copies\ntrue      <- one shared copy on the prototype",
                   say=[("Let's prove both claims. Here A's prototype is replaced without a constructor property. "
                         "So when we ask x for its constructor, the lookup goes past A's prototype all the way to "
                         "Object dot prototype.", (1, 4)),
                        ("And here, Slow defines get inside the constructor, so two Slow objects have two different "
                         "get functions. Insurance objects share one getInfo.", (6, 8))],
                   say_out="So x dot constructor is Object, not A. The two Slow methods are different functions, "
                           "and the two Insurance methods are the very same function.")

        self.slide("Step 3: the child type",
                   '''
function CarInsurance(policyNumber, exp, plate = "NONE") {
  Insurance.call(this, policyNumber, exp);   // parent sets its fields
  this.plate = plate;                        // child's own field
}

CarInsurance.prototype = Object.create(Insurance.prototype);
// (older style: CarInsurance.prototype = new Insurance();)
CarInsurance.prototype.constructor = CarInsurance;
''',
                   None,
                   trap="Forgetting CarInsurance.prototype.constructor = CarInsurance leaves constructor pointing at Insurance.",
                   say=[("Step three, inheritance. The child constructor takes the parent's parameters plus its own.",
                         1),
                        ("Insurance dot call, with this as the first argument, runs the parent constructor on the "
                         "new child object. That sets policyNumber and exp. This is the default-pattern version of "
                         "calling super.", 2),
                        ("Then the child sets its own field.", 3),
                        ("Next, link the prototypes. Object dot create makes a new empty object whose proto is "
                         "Insurance dot prototype, so every car insurance object can find getInfo. Some answer keys "
                         "use new Insurance here instead, and that works too.", (6, 7)),
                        ("And finally, repair the constructor so it points at CarInsurance.", 8)],
                   say_trap="If you forget to reset the constructor, CarInsurance objects report Insurance as their "
                            "constructor, because they inherit it from the parent's prototype.")

        self.slide("What each line does",
                   None,
                   "Insurance.call(this, p, e)\n"
                   "   runs the parent constructor on THIS new object  (the 'super(...)' of the default pattern)\n\n"
                   "Object.create(Insurance.prototype)\n"
                   "   new empty object whose __proto__ is Insurance.prototype, so children inherit getInfo\n\n"
                   "CarInsurance.prototype.constructor = CarInsurance\n"
                   "   repairs constructor, which Object.create's object would otherwise inherit from Insurance",
                   say=["Here are those three lines one more time, because you'll write them on every exam. Call "
                        "copies the parent's fields onto the child. Object dot create links the prototypes so the "
                        "child inherits methods. And resetting constructor fixes the one thing Object dot create "
                        "breaks."])

        self.slide("Step 4: overriding and calling the parent's version",
                   '''
CarInsurance.prototype.getInfo = function () {
  return Insurance.prototype.getInfo.call(this) +
         `, plate ${this.plate}`;
};

const c = new CarInsurance("A12","6/30/2027","8XYZ12");
console.log(c.getInfo());
console.log(c instanceof CarInsurance,
            c instanceof Insurance,
            c.constructor === CarInsurance);
console.log(new CarInsurance("B3").getInfo());
''',
                   "Parent.prototype.method\n  .call(this) is the\n"
                   "default-pattern version of\n  super.method()\n\n"
                   "Add child methods AFTER the\n"
                   "Object.create line, or they\nget wiped out",
                   out="Policy A12 exp 6/30/2027, plate 8XYZ12\n"
                       "true true true\n"
                       "Policy B3 exp 12/31/2026, plate NONE",
                   say=[("Step four, overriding. Put a getInfo on the child's prototype. Lookup finds this one "
                         "first, so it wins over the parent's.", 1),
                        ("To reuse the parent's version, grab it from Insurance dot prototype and call it with "
                         "this. That's the default-pattern version of super dot getInfo. Then append the plate.",
                         (2, 3)),
                        ("One ordering rule: add child methods after the Object dot create line. Otherwise, the "
                         "assignment replaces the prototype and wipes them out.", None),
                        ("Now let's test it, including a car insurance made with only a policy number.", (6, 11))],
                   say_out="The override works, instanceof is true for both the child and the parent, the "
                           "constructor is correct, and the missing expiration date fell back to the parent's "
                           "default, because undefined was passed through call.")

        self.practice(1,
                      "Using the Default Pattern (no class), define Pet(name = \"Unknown\", age = 0)\n"
                      "with a prototype method describe() returning \"name (age)\". Then define Dog\n"
                      "(extra breed = \"Mixed\") that inherits from Pet and overrides describe()\n"
                      "to append the breed, reusing Pet's describe().",
                      None,
                      '''
function Pet(name = "Unknown", age = 0) {
  this.name = name;
  this.age = age;
}
Pet.prototype.describe = function () { return `${this.name} (${this.age})`; };

function Dog(name, age, breed = "Mixed") {
  Pet.call(this, name, age);
  this.breed = breed;
}
Dog.prototype = Object.create(Pet.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.describe = function () {
  return Pet.prototype.describe.call(this) + ` ${this.breed}`;
};
// new Dog("Rex", 3, "Lab").describe() -> "Rex (3) Lab"
// new Dog().describe()                -> "Unknown (0) Mixed"
''',
                      say_q="Using the Default Pattern, with no class keyword, define Pet with a name and an age, "
                            "both with defaults, and a describe method on the prototype. Then define Dog, which adds "
                            "a breed, inherits from Pet, and overrides describe to add the breed while reusing Pet's "
                            "version.",
                      say_a="The Pet constructor stores the data, and describe goes on the prototype. For Dog, call "
                            "Pet with this to set name and age, then set breed. Link the prototypes with Object dot "
                            "create, restore the constructor, and only then add the override, which calls Pet's "
                            "describe with this and appends the breed.",
                      answer_is_code=True)

        self.practice(2, "What does this print?",
                      '''
function Song(title) { this.title = title; }
Song.prototype = { play() { return "playing " + this.title; } };
const s = new Song("Fight");
console.log(s.play(), s.constructor === Song);
''',
                      'playing Fight false\n\nThe prototype object was replaced without constructor: Song,\n'
                      'so s.constructor is found further up the chain: Object.',
                      say_q="What does this print?",
                      say_a="It prints playing Fight, then false. play works fine because it's on the prototype. "
                            "But the prototype was replaced without a constructor property, so s dot constructor is "
                            "found further up the chain, on Object dot prototype, and it's Object, not Song.")

        self.outro("Data in the constructor:  this.x = x  (with default params)\n"
                   "Methods on Type.prototype: one shared copy\n"
                   "Child: Parent.call(this, ...)  +  Object.create(Parent.prototype)\n"
                   "Always restore .constructor;  override with Parent.prototype.m.call(this)",
                   say="Recap. Data goes in the constructor, with default parameters. Methods go on the prototype, "
                       "so there's one shared copy. For a child, call the parent with this, link the prototypes with "
                       "Object dot create, restore the constructor, and override by calling the parent's method "
                       "with call this.")
