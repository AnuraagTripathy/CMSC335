from common import *


class ClassSyntax(ExamScene):
    def construct(self):
        self.intro(4, "Classes with the class Keyword", "34-40 of 200 pts  (+ custom errors)",
                   say="Now the class keyword. This problem is worth 34 to 40 points, and it checks a specific "
                       "list of features: private fields, a static counter, getters and setters, toPrimitive, "
                       "inheritance, and custom errors. Let's go through every one.")

        self.slide("Fields, static, and the constructor",
                   '''
class Bike {
  static #total = 0;    // one counter for the class
  #color;               // private: only code inside
  #price;               //   the class can touch these

  constructor(color = "black", price = 100) {
    this.#color = color;
    this.#price = price;
    Bike.#total++;      // count every Bike created
  }
}
''',
                   "#name = private field.\nDeclare it in the class body\nbefore using it.\n\n"
                   "static = belongs to the class,\nnot to each object.\n\n"
                   "Use ClassName.#total (not\nthis.#total) for statics.",
                   trap="Reading b.#color outside the class is a SyntaxError. Use a getter instead.",
                   say=[("Here's a Bike class. A static field belongs to the class itself, not to each bike. "
                         "We'll use it to count how many bikes were created. The hash sign makes it private.", 2),
                        ("These two are private instance fields. The hash is part of the name, and you have to "
                         "declare them in the class body before you use them. Only code inside the class can read "
                         "or write them.", (3, 4)),
                        ("The constructor takes default parameters, just like a function, and stores them in the "
                         "private fields.", (6, 8)),
                        ("Then it bumps the counter. Notice it's Bike dot hash total, not this dot hash total. "
                         "Statics live on the class, so you reach them through the class name.", 9)],
                   say_trap="Trying to read b dot hash color from outside the class is a syntax error. If outside "
                            "code needs the value, you provide a getter.")

        self.slide("Getters, setters with validation, static methods",
                   '''
  get color() { return this.#color; }

  set price(p) {
    if (p > 0) {          // validate before storing
      this.#price = p;
    }
  }

  static getTotal() { return Bike.#total; }

  paint(c) {
    this.#color = c;
    return this;          // enables chaining
  }
''',
                   "Used like properties, no ():\n  b.color\n  b.price = 300\n\n"
                   "static method is called on\nthe class: Bike.getTotal()\n\n"
                   "return this lets you write\n  b.paint(\"blue\").paint(\"green\")",
                   say=[("A getter looks like a method with get in front, but you use it like a property, with no "
                         "parentheses. b dot color runs this and returns the private color.", 1),
                        ("A setter runs when you assign. b dot price equals 300 calls this with p equal to 300. "
                         "The exam almost always wants validation here: only store the value if it's positive. "
                         "Otherwise, quietly ignore it.", (3, 7)),
                        ("A static method is called on the class, Bike dot getTotal, not on an object.", 9),
                        ("And returning this from a method lets you chain calls, like paint blue, then paint green, "
                         "in one expression.", (11, 14))])

        self.slide("Symbol.toPrimitive: the course's toString()",
                   '''
  [Symbol.toPrimitive]() {
    return `Bike(${this.#color}, $${this.#price})`;
  }
}

const b = new Bike("red", 250);
b.price = -5;               // rejected by the setter
console.log(`${b}`);
b.price = 300;
b.paint("blue").paint("green");
console.log(`${b}`, b.color, Bike.getTotal());
''',
                   "Square brackets: the method\nname is the Symbol value.\n\n"
                   "Template literals and + call\nit automatically.\n\n"
                   "$${...} prints a literal $\nfollowed by the value.",
                   out="Bike(red, $250)\nBike(green, $300) green 1",
                   say=[("This is the course's version of Java's toString. The method's name is the symbol "
                         "Symbol dot toPrimitive, which is why it's in square brackets. Whenever the object is "
                         "used in a template literal or with plus, JavaScript calls this.", (1, 3)),
                        ("The double dollar sign is just a literal dollar sign, followed by the dollar-brace that "
                         "inserts the price.", 2),
                        ("Now let's use it. We make a red bike for 250, then try to set the price to negative 5.",
                         (6, 8)),
                        ("Then a valid price, two chained paints, and print again with the getter and the static "
                         "count.", (9, 11))],
                   say_out="The negative price was rejected by the setter, so it still says 250. After the "
                           "update and the chain, it's a green bike for 300, and exactly one bike has been made.")

        self.slide("Getter / setter traps",
                   '''
console.log(b.price);   // set price exists, get price does not
b.color = "pink";       // get color exists, set color does not
console.log(b.color);
''',
                   None,
                   out="undefined\ngreen     (assignment ignored; TypeError in strict mode / modules)",
                   trap="A setter with no getter reads as undefined. A getter with no setter can't be assigned.",
                   say=[("Two classic output questions. Bike has a setter for price, but no getter. So what does "
                         "reading b dot price give?", 1),
                        ("And color has a getter but no setter. So what happens when we assign pink to it?", (2, 3))],
                   say_out="Reading price gives undefined, because there's no getter to run. And the assignment "
                           "to color is ignored, so it's still green. In strict mode, or in a module, that assignment "
                           "would throw a TypeError instead.")

        self.slide("Inheritance: extends and super",
                   '''
class EBike extends Bike {
  #range;
  constructor(color, price, range = 40) {
    super(color, price);    // MUST come before this
    this.#range = range;
  }
  info() {                  // Bike has: info() {
    return super.info() +   //   return `${this.#color} bike`; }
           ` with ${this.#range} mi range`;
  }
}
const e = new EBike("white", 900);
console.log(e.info(), `${e}`, Bike.getTotal());
''',
                   "super(...) runs the parent\nconstructor\n\n"
                   "super.info() calls the\nparent's version of a method\n\n"
                   "toPrimitive is inherited too\n\n"
                   "Bike.#total also counted\nthe EBike (b + e = 2)",
                   out="white bike with 40 mi range Bike(white, $900) 2",
                   trap="Using this before super() throws ReferenceError. A child can't read the parent's #private fields.",
                   say=[("Inheritance: EBike extends Bike and adds its own private range.", (1, 2)),
                        ("In the child's constructor, call super first. super runs the parent constructor, which "
                         "sets color and price and bumps the counter. Only after that can you use this.", (3, 6)),
                        ("To override a method and still reuse the parent's version, call super dot info. Bike's "
                         "info returns color, then bike, and we append the range.", (7, 10)),
                        ("Then we make a white e-bike and print it.", (12, 13))],
                   say_out="The override works. toPrimitive is inherited, so the template literal still prints "
                           "nicely. And the total is 2, because the e-bike went through Bike's constructor too.",
                   say_trap="Touching this before calling super throws a ReferenceError. And a child class can't "
                            "read the parent's private hash fields, which is why EBike uses super dot info instead "
                            "of reading the color directly.")

        self.slide("Custom errors: extends Error",
                   '''
class DataRangeError extends Error {
  constructor(msg) {
    super(msg);                 // sets message
    this.name = "DataRangeError";
  }
}
function setSpeed(s) {
  if (s < 0 || s > 30) {
    throw new DataRangeError(`Speed ${s} out of range`);
  }
  return s;
}
try {
  console.log(setSpeed(20));
  setSpeed(45);
  console.log("never");
} catch (e) {
  console.log(e.name + ": " + e.message);
  console.log(e instanceof DataRangeError, e instanceof Error);
} finally {
  console.log("done");
}
''',
                   None,
                   out="20\nDataRangeError: Speed 45 out of range\ntrue true\ndone",
                   say=[("Older exams also ask for a custom error. Extend Error, pass the message to super, which "
                         "sets e dot message, and set this dot name to the class name.", (1, 6)),
                        ("Then throw it when a value is out of range.", (7, 12)),
                        ("In the try block, the first call works. The second call throws, so the line after it "
                         "never runs. Control jumps to catch.", (13, 17)),
                        ("Catch prints the name and the message, and checks instanceof. And finally runs no matter "
                         "what.", (17, 22))],
                   say_out="So we get 20, then DataRangeError colon Speed 45 out of range, then true true, because "
                           "the error is both a DataRangeError and an Error, and finally, done. Never is never "
                           "printed.")

        self.practice(1,
                      "Write class Ticket: private #seat; static private #count; constructor(seat = \"GA\",\n"
                      "price = 20) that bumps the count; get seat(); set price(p) that only accepts p > 0;\n"
                      "static getCount(); and toPrimitive so `${t}` gives \"Seat GA ($20)\".",
                      None,
                      '''
class Ticket {
  static #count = 0;
  #seat;
  #price;
  constructor(seat = "GA", price = 20) {
    this.#seat = seat;
    this.#price = price;
    Ticket.#count++;
  }
  get seat() { return this.#seat; }
  set price(p) { if (p > 0) this.#price = p; }
  static getCount() { return Ticket.#count; }
  [Symbol.toPrimitive]() { return `Seat ${this.#seat} ($${this.#price})`; }
}
''',
                      say_q="Write a Ticket class with a private seat, a private static count, a constructor with "
                            "default seat G A and price 20 that bumps the count, a seat getter, a price setter that "
                            "only accepts positive values, a static getCount, and toPrimitive so the template "
                            "literal gives Seat G A, dollar 20.",
                      say_a="Declare the static count and the private fields first. The constructor stores both "
                            "values and does Ticket dot hash count plus plus. The getter returns the seat. The "
                            "setter checks p greater than zero before storing. getCount is static. And toPrimitive "
                            "returns the template string, with a double dollar sign for the literal dollar.",
                      answer_is_code=True)

        self.practice(2, "What does this print? (Ticket has only a getter for seat)",
                      '''
const t1 = new Ticket(), t2 = new Ticket("B12");
t1.seat = "A1";
console.log(`${t1.seat} | ${t2.seat} | ${Ticket.getCount()}`);
''',
                      "GA | B12 | 2\n\nt1.seat = \"A1\" is ignored (no setter), and the static\n"
                      "count was bumped once per new Ticket.",
                      say_q="Using that Ticket class, which has only a getter for seat, what does this print?",
                      say_a="G A, B 12, and 2. Assigning A 1 to t1 dot seat does nothing, because there's no "
                            "setter, so t1 keeps the default G A. And the static count went up once for each new "
                            "Ticket.")

        self.outro("#private fields, static #total, ClassName.#total++ in the constructor\n"
                   "get x() / set x(v) with validation; static methods; return this to chain\n"
                   "[Symbol.toPrimitive]() so `${obj}` prints nicely\n"
                   "extends + super(...) first + super.method();  class MyError extends Error",
                   say="Recap. Private fields with a hash, a static counter bumped with the class name in the "
                       "constructor, getters and setters with validation, static methods, and return this for "
                       "chaining. Symbol dot toPrimitive makes template literals print your object. For inheritance, "
                       "call super first, and use super dot method to reuse the parent. And custom errors extend "
                       "Error and set their name.")
