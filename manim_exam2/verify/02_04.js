// ===== 02 default pattern =====
console.log("== 02");
function Insurance(policyNumber = "None", exp = "12/31/2026") {
  this.policyNumber = policyNumber;
  this.exp = exp;
}
Insurance.prototype = {
  constructor: Insurance,
  getInfo: function () { return `Policy ${this.policyNumber} exp ${this.exp}`; },
};
const i1 = new Insurance();
console.log(i1.getInfo());
console.log(new Insurance("P7").getInfo());
function CarInsurance(policyNumber, exp, plate = "NONE") {
  Insurance.call(this, policyNumber, exp);
  this.plate = plate;
}
CarInsurance.prototype = Object.create(Insurance.prototype);
CarInsurance.prototype.constructor = CarInsurance;
CarInsurance.prototype.getInfo = function () {
  return Insurance.prototype.getInfo.call(this) + `, plate ${this.plate}`;
};
const c = new CarInsurance("A12", "6/30/2027", "8XYZ12");
console.log(c.getInfo());
console.log(c instanceof CarInsurance, c instanceof Insurance, c.constructor === CarInsurance);
const c2 = new CarInsurance("B3");
console.log(c2.getInfo());
// trap: no constructor
function A() {}
A.prototype = { hi() { return "hi"; } };
const x = new A();
console.log(x.constructor === A, x.constructor === Object, x.hi());
// per-object copies
function Slow(n) { this.n = n; this.get = function () { return this.n; }; }
console.log(new Slow(1).get === new Slow(2).get, new Insurance().getInfo === new Insurance().getInfo);
// new Parent() variant
function Truck(p, e) { Insurance.call(this, p, e); }
Truck.prototype = new Insurance();
Truck.prototype.constructor = Truck;
console.log(new Truck("T1", "1/1/2030").getInfo());
// practice Pet/Dog
function Pet(name = "Unknown", age = 0) { this.name = name; this.age = age; }
Pet.prototype.describe = function () { return `${this.name} (${this.age})`; };
function Dog(name, age, breed = "Mixed") { Pet.call(this, name, age); this.breed = breed; }
Dog.prototype = Object.create(Pet.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.describe = function () { return Pet.prototype.describe.call(this) + ` ${this.breed}`; };
console.log(new Dog("Rex", 3, "Lab").describe(), "|", new Dog().describe());

// ===== 03 prototype diagram =====
console.log("== 03");
function Boat(name) { this.name = name; }
Boat.prototype.capacity = 50;
const a = new Boat("local"), b = new Boat("small");
console.log(Object.getPrototypeOf(a) === Boat.prototype, a.__proto__ === Boat.prototype, Boat.prototype.constructor === Boat);
console.log(Object.getPrototypeOf(Boat.prototype) === Object.prototype, Object.getPrototypeOf(Object.prototype));
console.log(a.name, a.capacity, typeof a.toString, a.wings, a.hasOwnProperty("capacity"), Object.keys(a));
a.capacity = 10;
console.log(a.capacity, b.capacity, a.hasOwnProperty("capacity"));
Boat.prototype.capacity = 75;
console.log(a.capacity, b.capacity);
function Lamp(color) { this.color = color; }
Lamp.prototype.watts = 60;
const l1 = new Lamp("red"), l2 = new Lamp("blue");
l1.watts = 40;
Lamp.prototype.watts = 75;
console.log(l1.watts, l2.watts, delete l1.watts, l1.watts);

// ===== 04 class =====
console.log("== 04");
class Bike {
  static #total = 0;
  #color;
  #price;
  constructor(color = "black", price = 100) {
    this.#color = color;
    this.#price = price;
    Bike.#total++;
  }
  get color() { return this.#color; }
  set price(p) { if (p > 0) this.#price = p; }
  static getTotal() { return Bike.#total; }
  paint(c) { this.#color = c; return this; }
  info() { return `${this.#color} bike`; }
  [Symbol.toPrimitive]() { return `Bike(${this.#color}, $${this.#price})`; }
}
const bk = new Bike("red", 250);
bk.price = -5;
console.log(`${bk}`);
bk.price = 300;
console.log(`${bk}`, bk.price);
bk.paint("blue").paint("green");
console.log(`${bk}`, bk.color, Bike.getTotal());
bk.color = "pink"; // sloppy: ignored
console.log(bk.color);
try { (function () { "use strict"; bk.color = "pink"; })(); } catch (e) { console.log(e.constructor.name, e.message); }
console.log(String(bk), "" + bk, bk + "!");
class EBike extends Bike {
  #range;
  constructor(color, price, range = 40) {
    super(color, price);
    this.#range = range;
  }
  info() { return super.info() + ` with ${this.#range} mi range`; }
}
const eb = new EBike("white", 900);
console.log(eb.info(), `${eb}`, Bike.getTotal(), eb instanceof Bike);
class Bad extends Bike { constructor() { this.x = 1; super(); } }
try { new Bad(); } catch (e) { console.log(e.constructor.name + ": " + e.message); }
class DataRangeError extends Error {
  constructor(msg) { super(msg); this.name = "DataRangeError"; }
}
function setSpeed(s) {
  if (s < 0 || s > 30) throw new DataRangeError(`Speed ${s} out of range`);
  return s;
}
try { console.log(setSpeed(20)); setSpeed(45); console.log("never"); }
catch (e) { console.log(e.name + ": " + e.message); console.log(e instanceof DataRangeError, e instanceof Error); }
finally { console.log("done"); }
// practice 2 puzzle
class Ticket {
  static #count = 0;
  #seat;
  constructor(seat = "GA") { this.#seat = seat; Ticket.#count++; }
  get seat() { return this.#seat; }
  static getCount() { return Ticket.#count; }
  [Symbol.toPrimitive]() { return `Seat ${this.#seat}`; }
}
const t1 = new Ticket(), t2 = new Ticket("B12");
t1.seat = "A1";
console.log(`${t1} | ${t2} | ${Ticket.getCount()}`);
