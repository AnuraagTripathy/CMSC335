from common import *

EMPS = '''const emps = [
  { name: "Mia", salary: 72000 },
  { name: "Ben", salary: 95000 },
  { name: "Ava", salary: 61000 },
];
'''


class ArrayMethods(ExamScene):
    def construct(self):
        self.intro(11, "Array Methods on Arrays of Objects", "~38 pts on older exams; + destructuring, spread, JSON")

        self.slide("Search and test",
                   EMPS + '''
emps.forEach(e => console.log(e.name));
console.log(emps.find(e => e.salary > 70000));
console.log(emps.find(e => e.salary > 99000));
console.log(emps.findIndex(e => e.name === "Ava"),
            emps.findIndex(e => e.name === "Zed"));
console.log(emps.every(e => e.salary > 60000),
            emps.some(e => e.salary > 90000));
''',
                   "forEach: run for each item,\nreturns undefined\n\n"
                   "find: first MATCHING ITEM\nor undefined\n\n"
                   "findIndex: its index or -1\n\n"
                   "every: all pass?\nsome: at least one passes?",
                   out="Mia\nBen\nAva\n{ name: 'Mia', salary: 72000 }\nundefined\n2 -1\ntrue true")

        self.slide("map, join, reduce",
                   '''
console.log(emps.map(e => e.name).join(", "));

// max VALUE: start the accumulator at 0
console.log(emps.reduce((max, e) =>
  e.salary > max ? e.salary : max, 0));

// max OBJECT: no initial value -> starts with emps[0]
console.log(emps.reduce((best, e) =>
  e.salary > best.salary ? e : best));

console.log(emps.reduce((sum, e) => sum + e.salary, 0));
''',
                   "map: new array, same length\n\n"
                   "join(sep): array -> string\n\n"
                   "reduce((acc, item) => newAcc,\n        initial)\n"
                   "whatever you return becomes\nacc for the next item",
                   out="Mia, Ben, Ava\n95000\n{ name: 'Ben', salary: 95000 }\n228000")

        self.slide("sort with a comparator",
                   '''
function sortEmps(arr, byName) {
  return arr.sort(byName
    ? (a, b) => a.name.localeCompare(b.name)
    : (a, b) => a.salary - b.salary);
}
console.log(sortEmps(emps, true).map(e => e.name));
console.log(sortEmps(emps, false).map(e => e.name));
console.log(emps.map(e => e.name));

console.log([10, 9, 1, 100].sort());
console.log([10, 9, 1, 100].sort((a, b) => a - b));
''',
                   "Comparator returns:\n negative -> a first\n positive -> b first\n\n"
                   "Numbers: a.salary - b.salary\n(b - a for descending)\n\n"
                   "Strings: a.name\n  .localeCompare(b.name)",
                   out="[ 'Ava', 'Ben', 'Mia' ]\n[ 'Ava', 'Mia', 'Ben' ]\n[ 'Ava', 'Mia', 'Ben' ]   <- original changed!\n"
                       "[ 1, 10, 100, 9 ]\n[ 1, 9, 10, 100 ]",
                   trap="sort() changes the original array, and with no comparator it compares as STRINGS.")

        self.slide("push, pop, reverse",
                   '''
const arr = [1, 2, 3];
console.log(arr.push(4));    // returns the NEW LENGTH
console.log(arr.pop());      // returns the removed item
arr.reverse();               // in place
console.log(arr);
''',
                   None,
                   out="4\n4\n[ 3, 2, 1 ]")

        self.slide("Destructuring, spread, rest",
                   '''
// emps in its ORIGINAL order (Mia, Ben, Ava)
const [first, , third] = emps;          // skip with a comma
const { name, salary: pay, dept = "IT" } = first;
console.log(name, pay, dept);

const nums = [5, 6, 7, 8];
const [head, ...others] = nums;         // rest: collects
console.log(head, others);
console.log(Math.max(...nums), [...nums, 9]);   // spread

const raise = { ...first, salary: 80000 };  // copy + override
console.log(raise, first.salary);
''',
                   None,
                   out="Mia 72000 IT\n5 [ 6, 7, 8 ]\n8 [ 5, 6, 7, 8, 9 ]\n{ name: 'Mia', salary: 80000 } 72000",
                   trap="Same ... syntax: on the LEFT of = (or in params) it is rest; on the right / in a call it is spread.")

        self.slide("JSON.stringify / JSON.parse",
                   '''
const s = JSON.stringify({ name: "Mia", salary: 72000,
                           hi() {} });
console.log(s, typeof s);
console.log(JSON.parse(s).name);
''',
                   "stringify: object -> string\n(keys get double quotes)\n\n"
                   "parse: string -> object\n\n"
                   "Functions are dropped.",
                   out='{"name":"Mia","salary":72000} string\nMia')

        self.practice(1,
                      "products is an array of { item, price }. Write getMostExpensive(arr) using reduce\n"
                      "(return the object), and sortProducts(arr, ascending) that sorts by price,\n"
                      "ascending when the boolean is true and descending otherwise.",
                      None,
                      '''
function getMostExpensive(arr) {
  return arr.reduce((best, p) => p.price > best.price ? p : best);
}

function sortProducts(arr, ascending) {
  return arr.sort(ascending ? (a, b) => a.price - b.price
                            : (a, b) => b.price - a.price);
}
''', answer_is_code=True)

        self.practice(2, "What does this print?",
                      '''
const products = [{ item: "pen", price: 2 }, { item: "lamp", price: 30 },
                  { item: "mug", price: 9 }];
console.log(products.filter(p => p.price < 10)
                    .map(p => p.item.toUpperCase()).join("/"));
const q = [3, 1, 2];
const r = q.sort();
r.push(9);
console.log(q, q === r);
const { item, ...restP } = products[1];
console.log(item, restP);
''',
                      "PEN/MUG\n[ 1, 2, 3, 9 ] true\nlamp { price: 30 }\n\n"
                      "sort returns the SAME array, so pushing to r changes q too.")

        self.outro("find -> item | undefined;  findIndex -> index | -1;  every / some -> boolean\n"
                   "map -> new array;  reduce((acc, x) => ..., init) for max / sum\n"
                   "sort mutates: (a, b) => a.n - b.n  or  a.s.localeCompare(b.s)\n"
                   "[a, ...rest] = arr;  {x, y: alias = def} = obj;  {...obj};  JSON.stringify/parse")
