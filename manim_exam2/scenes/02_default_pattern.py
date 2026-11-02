from common import *


class DefaultPattern(ExamScene):
    def construct(self):
        self.intro(2, "Custom Types: the Default Pattern + Inheritance",
                   "40-48 of 200 pts  (no class / extends / super allowed)")

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
                       'i2 -> { policyNumber: "P7",   exp: "12/31/2026" }')

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
                   trap="Option A replaces the prototype object, so constructor is lost unless you write constructor: Insurance.")

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
                   out="false true hi\nfalse     <- two separate copies\ntrue      <- one shared copy on the prototype")

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
                   trap="Forgetting CarInsurance.prototype.constructor = CarInsurance leaves constructor pointing at Insurance.")

        self.slide("What each line does",
                   None,
                   "Insurance.call(this, p, e)\n"
                   "   runs the parent constructor on THIS new object  (the 'super(...)' of the default pattern)\n\n"
                   "Object.create(Insurance.prototype)\n"
                   "   new empty object whose __proto__ is Insurance.prototype, so children inherit getInfo\n\n"
                   "CarInsurance.prototype.constructor = CarInsurance\n"
                   "   repairs constructor, which Object.create's object would otherwise inherit from Insurance")

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
                       "Policy B3 exp 12/31/2026, plate NONE")

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
''', answer_is_code=True)

        self.practice(2, "What does this print?",
                      '''
function Song(title) { this.title = title; }
Song.prototype = { play() { return "playing " + this.title; } };
const s = new Song("Fight");
console.log(s.play(), s.constructor === Song);
''',
                      'playing Fight false\n\nThe prototype object was replaced without constructor: Song,\n'
                      'so s.constructor is found further up the chain: Object.')

        self.outro("Data in the constructor:  this.x = x  (with default params)\n"
                   "Methods on Type.prototype: one shared copy\n"
                   "Child: Parent.call(this, ...)  +  Object.create(Parent.prototype)\n"
                   "Always restore .constructor;  override with Parent.prototype.m.call(this)")
