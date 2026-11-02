from common import *


class PromisesFetch(ExamScene):
    def construct(self):
        self.intro(5, "Promises + fetch (without await)", "~30 of 200 pts on the last exam")

        self.slide("Promise states",
                   '''
const p = new Promise((resolve, reject) => {
  // do the work...
  resolve(value);   // -> fulfilled
  // or
  reject(reason);   // -> rejected
});
''',
                   "pending -> fulfilled\npending -> rejected\n\n"
                   "Settles only ONCE: later\nresolve/reject calls are\nignored.\n\n"
                   ".then(onFulfilled)\n.catch(onRejected)")

        self.slide("Pending forever",
                   '''
const never = new Promise(resolve => {
  console.log("work done");
  // forgot to call resolve(...)
});
setTimeout(() => console.log(never), 5);
''',
                   None,
                   out="work done\nPromise { <pending> }",
                   trap="Finishing the work does not settle a promise. Only calling resolve or reject does.")

        self.slide("The exam problem: getImageURL",
                   '''
function getImageURL(index, jsonFile) {
  return new Promise((resolve, reject) => {
    fetch(jsonFile)
      .then(response => response.json())
      .then(json => index >= json.urls.length
                      ? reject("Invalid Index")
                      : resolve(json.urls[index]));
  });
}
''',
                   "images.json:\n{ \"urls\": [\"a.png\",\n  \"b.png\", \"c.png\"] }\n\n"
                   "fetch returns a promise of\na Response\n\n"
                   "response.json() returns\nANOTHER promise (of the\nparsed object)\n\n"
                   "resolve/reject come from the\nouter new Promise")

        self.slide("Using it with .then().catch()",
                   '''
getImageURL(1, "images.json")
  .then(url => console.log("then:", url))
  .catch(err => console.log("catch:", err));

getImageURL(5, "images.json")
  .then(url => console.log("then:", url))
  .catch(err => console.log("catch:", err));
''',
                   "In a page you would do\n  img.src = url\ninside the then.\n\n"
                   "Index 5 is past the end, so\nreject runs and .catch gets\n\"Invalid Index\".",
                   out="then: b.png\ncatch: Invalid Index\n(two separate fetches: with a real network the lines may swap)",
                   trap="Write return new Promise(...). Without the return the caller gets undefined, and .then on it throws a TypeError.")

        self.slide(".then() returns a new promise",
                   '''
Promise.resolve(2)
  .then(v => v * 10)        // returns 20 -> next then
  .then(v => console.log(v));

async function f() { return 5; }
console.log(f());           // NOT 5
f().then(v => console.log(v));
''',
                   "Whatever a then callback\nreturns becomes the value\nfor the next then.\n\n"
                   "An async function ALWAYS\nreturns a promise.",
                   out="Promise { 5 }   (Chrome: Promise {<fulfilled>: 5})\n5\n20   (the 2-step chain needs one extra microtask turn)")

        self.slide("The async/await equivalent",
                   '''
async function getImageURL2(index, jsonFile) {
  const response = await fetch(jsonFile);
  const json = await response.json();
  if (index >= json.urls.length) {
    throw "Invalid Index";      // = reject
  }
  return json.urls[index];      // = resolve
}
getImageURL2(9, "images.json")
  .catch(e => console.log(e));
''',
                   "await pauses this function\nuntil the promise settles\n\n"
                   "return value -> fulfilled\nthrow -> rejected\n\n"
                   "If the exam says \"no await\",\nuse the .then version!",
                   out="Invalid Index")

        self.slide("Promise.all",
                   '''
Promise.all([getImageURL(0, "images.json"),
             getImageURL(2, "images.json")])
  .then(urls => console.log(urls));

Promise.all([getImageURL(0, "images.json"),
             getImageURL(7, "images.json")])
  .then(urls => console.log(urls))
  .catch(e => console.log("failed:", e));
''',
                   "Waits for ALL; results come\nback in the SAME order as\nthe input array\n\n"
                   "If ANY one rejects, the\nwhole thing rejects",
                   out="[ 'a.png', 'c.png' ]\nfailed: Invalid Index\n(the two Promise.all calls run independently)")

        self.slide("Callback / setTimeout -> promise",
                   '''
function delayedSquare(x, ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (typeof x === "number") resolve(x * x);
      else reject("Not a number");
    }, ms);
  });
}
delayedSquare(4, 1000).then(v => console.log(v));
delayedSquare("4", 1000).catch(e => console.log(e));

const wait = ms => new Promise(res => setTimeout(res, ms));
''',
                   "Recipe:\n1. return new Promise(...)\n2. start the async task\n"
                   "3. in ITS callback, call\n   resolve(result) or\n   reject(error)",
                   out="16\nNot a number   (after 1 second)")

        self.practice(1,
                      "Without await, write getTemperature(city, jsonFile) that returns a promise.\n"
                      "The JSON looks like { \"boston\": 41, \"austin\": 77 }. Resolve with the temperature,\n"
                      "or reject with \"Unknown City\" if the city isn't in the file. Then use it with then/catch.",
                      None,
                      '''
function getTemperature(city, jsonFile) {
  return new Promise((resolve, reject) => {
    fetch(jsonFile)
      .then(response => response.json())
      .then(json => json[city] === undefined
                      ? reject("Unknown City")
                      : resolve(json[city]));
  });
}
getTemperature("austin", "temps.json")
  .then(t => console.log(t))        // 77
  .catch(e => console.log(e));      // ("paris" -> Unknown City)
''', answer_is_code=True)

        self.practice(2, "What does this print, in order?",
                      '''
const p = new Promise((res, rej) => {
  console.log("A");
  res(1); rej(2); res(3);
});
p.then(v => console.log("B", v)).catch(e => console.log("C", e));
console.log("D");
''',
                      "A\nD\nB 1\n\nThe executor runs immediately (A). The promise settles once, with 1;\n"
                      "rej(2) and res(3) are ignored. then callbacks run after the current code (D first).")

        self.outro("return new Promise((resolve, reject) => { ... })\n"
                   "fetch(f).then(r => r.json()).then(json => cond ? reject(..) : resolve(..))\n"
                   "Use it: p.then(value => ...).catch(err => ...)\n"
                   "async fn always returns a promise; Promise.all keeps order, fails fast")
