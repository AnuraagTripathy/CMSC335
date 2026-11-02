from common import *

EMPS = '''const emps = [
  { name: "Mia", salary: 72000 },
  { name: "Ben", salary: 95000 },
  { name: "Ava", salary: 61000 },
];
'''


class ArrayMethods(ExamScene):
    def construct(self):
        self.intro(11, "Array Methods on Arrays of Objects", "~38 pts on older exams; + destructuring, spread, JSON",
                   say="Array methods on arrays of objects. On the older exams this was a whole problem, around 38 "
                       "points, and the same methods still show up in other problems. We'll also cover destructuring, "
                       "spread, and JSON.")

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
                   out="Mia\nBen\nAva\n{ name: 'Mia', salary: 72000 }\nundefined\n2 -1\ntrue true",
                   say=[("Our data is an array of employee objects, each with a name and a salary.", (1, 5)),
                        ("forEach runs a function for every item. It returns undefined, so it's only for side "
                         "effects, like logging.", 7),
                        ("find returns the first item that matches, the whole object, or undefined if nothing "
                         "matches.", (8, 9)),
                        ("findIndex returns the index of the first match instead, or negative one.", (10, 11)),
                        ("every asks whether all items pass the test. some asks whether at least one does.",
                         (12, 13))],
                   say_out="The three names, then Mia's whole object, then undefined because nobody earns over "
                           "99 thousand, then 2 and negative 1, and true true.")

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
                   out="Mia, Ben, Ava\n95000\n{ name: 'Ben', salary: 95000 }\n228000",
                   say=[("map builds a new array of the same length, here just the names, and join glues them into "
                         "one string with a separator.", 1),
                        ("reduce is the one to really practice. It carries an accumulator through the array. "
                         "Whatever your callback returns becomes the accumulator for the next item. For a maximum "
                         "value, start at zero and keep the bigger salary.", (3, 5)),
                        ("For the maximum object, leave out the initial value. Then the accumulator starts as the "
                         "first employee, and you keep whichever object has the higher salary.", (7, 9)),
                        ("And a sum is the classic: start at zero and add each salary.", 11)],
                   say_out="Mia, Ben, Ava. Then 95000, Ben's whole object, and the total, 228000.")

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
                   trap="sort() changes the original array, and with no comparator it compares as STRINGS.",
                   say=[("Sorting. The exam likes a boolean parameter that picks the sort order or the sort key. "
                         "The comparator returns a negative number to put a first, and a positive number to put b "
                         "first.", (1, 5)),
                        ("For strings, use localeCompare. For numbers, just subtract: a's salary minus b's salary "
                         "sorts ascending, and b minus a sorts descending.", (3, 4)),
                        ("Now we sort by name, then by salary, and then print the original array.", (6, 8)),
                        ("And finally, numbers with and without a comparator.", (10, 11))],
                   say_out="By name: Ava, Ben, Mia. By salary: Ava, Mia, Ben. And look, the original array changed "
                           "too. Without a comparator, the numbers sort as strings, so 100 comes before 9.",
                   say_trap="sort changes the original array, and without a comparator it compares the values as "
                            "strings.")

        self.slide("push, pop, reverse",
                   '''
const arr = [1, 2, 3];
console.log(arr.push(4));    // returns the NEW LENGTH
console.log(arr.pop());      // returns the removed item
arr.reverse();               // in place
console.log(arr);
''',
                   None,
                   out="4\n4\n[ 3, 2, 1 ]",
                   say=[("Quick return values. push returns the new length, not the array.", 2),
                        ("pop returns the item it removed.", 3),
                        ("And reverse flips the array in place.", (4, 5))],
                   say_out="4, then 4 again, the removed item, and then 3, 2, 1.")

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
                   trap="Same ... syntax: on the LEFT of = (or in params) it is rest; on the right / in a call it is spread.",
                   say=[("Array destructuring pulls items out by position. An empty spot between commas skips one.",
                         2),
                        ("Object destructuring pulls properties out by name. salary colon pay renames it, and dept "
                         "equals IT gives a default because first has no dept.", (3, 4)),
                        ("Three dots on the left side is rest. It collects whatever's left into an array.", (6, 8)),
                        ("Three dots on the right side, or in a call, is spread. It expands an array into separate "
                         "values.", 9),
                        ("Spread works on objects too. This copies first and overrides the salary, without changing "
                         "the original.", (11, 12))],
                   say_out="Mia, 72000, and IT. Then 5 and the rest, 6 7 8. Max is 8, and the new array ends in 9. "
                           "And the copy has 80000, while first still has 72000.",
                   say_trap="It's the same three dots. On the left of an equals sign, or in a parameter list, it's "
                            "rest. On the right, or in a function call, it's spread.")

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
                   out='{"name":"Mia","salary":72000} string\nMia',
                   say=[("JSON dot stringify turns an object into a string. The keys get double quotes, and "
                         "functions are dropped completely.", (1, 3)),
                        ("JSON dot parse goes the other way, turning the string back into an object.", 4)],
                   say_out="The string has no hi method, its type is string, and parsing it back gives us Mia.")

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
''',
                      say_q="products is an array of objects with an item and a price. Write getMostExpensive using "
                            "reduce, returning the whole object. And write sortProducts, which sorts by price, "
                            "ascending when the boolean is true and descending otherwise.",
                      say_a="For the max, reduce with no initial value and keep whichever object has the higher "
                            "price. For sorting, use the boolean to pick the comparator: a minus b for ascending, "
                            "b minus a for descending.",
                      answer_is_code=True)

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
                      "sort returns the SAME array, so pushing to r changes q too.",
                      say_q="What does this print?",
                      say_a="First, filter keeps the pen and the mug, map uppercases them, and join gives PEN slash "
                            "MUG. Next, sort returns the same array, not a copy, so pushing 9 onto r also changes q, "
                            "and q triple-equals r is true. Finally, item is lamp, and rest collects the remaining "
                            "property, price 30.")

        self.outro("find -> item | undefined;  findIndex -> index | -1;  every / some -> boolean\n"
                   "map -> new array;  reduce((acc, x) => ..., init) for max / sum\n"
                   "sort mutates: (a, b) => a.n - b.n  or  a.s.localeCompare(b.s)\n"
                   "[a, ...rest] = arr;  {x, y: alias = def} = obj;  {...obj};  JSON.stringify/parse",
                   say="Recap. find gives an item or undefined, findIndex gives an index or negative one, and every "
                       "and some give booleans. map makes a new array, and reduce handles max and sum. sort changes "
                       "the array, so use subtraction for numbers and localeCompare for strings. And know your "
                       "destructuring, rest versus spread, and JSON stringify and parse.")
