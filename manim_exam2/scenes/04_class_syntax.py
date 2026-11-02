from common import *


class ClassSyntax(ExamScene):
    def construct(self):
        self.intro(4, "Classes with the class Keyword", "34-40 of 200 pts  (+ custom errors)")

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
                   trap="Reading b.#color outside the class is a SyntaxError. Use a getter instead.")

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
                   "return this lets you write\n  b.paint(\"blue\").paint(\"green\")")

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
                   out="Bike(red, $250)\nBike(green, $300) green 1")

        self.slide("Getter / setter traps",
                   '''
console.log(b.price);   // set price exists, get price does not
b.color = "pink";       // get color exists, set color does not
console.log(b.color);
''',
                   None,
                   out="undefined\ngreen     (assignment ignored; TypeError in strict mode / modules)",
                   trap="A setter with no getter reads as undefined. A getter with no setter can't be assigned.")

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
                   trap="Using this before super() throws ReferenceError. A child can't read the parent's #private fields.")

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
                   out="20\nDataRangeError: Speed 45 out of range\ntrue true\ndone")

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
''', answer_is_code=True)

        self.practice(2, "What does this print? (Ticket has only a getter for seat)",
                      '''
const t1 = new Ticket(), t2 = new Ticket("B12");
t1.seat = "A1";
console.log(`${t1.seat} | ${t2.seat} | ${Ticket.getCount()}`);
''',
                      "GA | B12 | 2\n\nt1.seat = \"A1\" is ignored (no setter), and the static\n"
                      "count was bumped once per new Ticket.")

        self.outro("#private fields, static #total, ClassName.#total++ in the constructor\n"
                   "get x() / set x(v) with validation; static methods; return this to chain\n"
                   "[Symbol.toPrimitive]() so `${obj}` prints nicely\n"
                   "extends + super(...) first + super.method();  class MyError extends Error")
