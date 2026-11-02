from common import *


class PromisesFetch(ExamScene):
    def construct(self):
        self.intro(5, "Promises + fetch (without await)", "~30 of 200 pts on the last exam",
                   say="Promises and fetch, without await. On the last exam this was a 30 point problem, and the "
                       "twist is that you have to write it with dot then instead of await. Let's make sure that feels "
                       "natural.")

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
                   ".then(onFulfilled)\n.catch(onRejected)",
                   say=[("A promise is an object that stands for a result that isn't ready yet. You create one "
                         "with new Promise, and pass it a function that receives two callbacks, resolve and reject.",
                         1),
                        ("Every promise starts out pending. Calling resolve moves it to fulfilled, with a value.",
                         (2, 3)),
                        ("Calling reject moves it to rejected, with a reason.", (4, 5)),
                        ("And it settles only once. After the first resolve or reject, any later calls are simply "
                         "ignored. To react to the result, you use dot then for success and dot catch for failure.",
                         None)])

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
                   trap="Finishing the work does not settle a promise. Only calling resolve or reject does.",
                   say=[("Here's a question the exam likes. This promise's function runs and logs work done, but "
                         "never calls resolve.", (1, 4)),
                        ("A little later we print the promise. What state is it in?", 5)],
                   say_out="It's still pending. And it'll stay pending forever.",
                   say_trap="Doing the work doesn't settle a promise. The only things that settle it are calling "
                            "resolve or calling reject.")

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
                   "resolve/reject come from the\nouter new Promise",
                   say=[("Here's the actual exam problem. getImageURL takes an index and a JSON file name, and "
                         "it has to return a promise. So the very first thing we write is return new Promise.",
                         (1, 2)),
                        ("Inside, we fetch the file. fetch itself returns a promise of a response object.", 3),
                        ("Calling response dot json returns another promise, this time of the parsed object. "
                         "Returning it from the then means the next then receives the parsed JSON.", 4),
                        ("Now the decision. If the index is past the end of the urls array, call reject with "
                         "Invalid Index. Otherwise, resolve with the URL at that index. Those resolve and reject "
                         "are the ones from our outer new Promise, so they settle the promise we returned.",
                         (5, 7))])

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
                   trap="Write return new Promise(...). Without the return the caller gets undefined, and .then on it throws a TypeError.",
                   say=[("Using it looks like this. Index 1 is valid, so then receives the URL. In a real page, "
                         "you'd set an image's src to that URL right here.", (1, 3)),
                        ("Index 5 is past the end, so the promise rejects, the then is skipped, and catch gets "
                         "the message.", (5, 7))],
                   say_out="So we see b dot png, and Invalid Index. One honest note: these are two separate "
                           "fetches, so with a real network the two lines could come out in either order.",
                   say_trap="Don't forget the word return in front of new Promise. Without it, the function returns "
                            "undefined, and calling dot then on undefined throws a TypeError.")

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
                   out="Promise { 5 }   (Chrome: Promise {<fulfilled>: 5})\n5\n20   (the 2-step chain needs one extra microtask turn)",
                   say=[("Two facts that show up in output questions. First, dot then itself returns a new promise. "
                         "Whatever the callback returns becomes the value for the next then. Here 2 times 10 "
                         "passes 20 down the chain.", (1, 3)),
                        ("Second, an async function always returns a promise, even if you return a plain number. "
                         "So logging f of nothing doesn't print 5.", (5, 6)),
                        ("To actually get the 5, you use dot then.", 7)],
                   say_out="The first line is the promise object itself. Then 5, and then 20. The 20 comes last "
                           "because that chain has two steps, and each step waits one extra turn.")

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
                   out="Invalid Index",
                   say=[("For comparison, here's the same function with async and await. await pauses this "
                         "function until the promise settles and hands you the value.", (1, 3)),
                        ("Throwing inside an async function rejects its promise, and returning a value fulfills "
                         "it.", (4, 7)),
                        ("This version is shorter, but read the question. If it says no await, you must write the "
                         "dot then version.", (9, 10))],
                   say_out="Index 9 is too big, so the throw rejects the promise, and catch prints Invalid Index.")

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
                   out="[ 'a.png', 'c.png' ]\nfailed: Invalid Index\n(the two Promise.all calls run independently)",
                   say=[("Promise dot all takes an array of promises and waits for all of them. The results come "
                         "back as an array, in the same order as the input, no matter which one finished first.",
                         (1, 3)),
                        ("But if any one of them rejects, the whole thing rejects, and you land in catch.", (5, 8))],
                   say_out="The first gives a dot png and c dot png, in order. The second fails because index 7 is "
                           "invalid.")

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
                   out="16\nNot a number   (after 1 second)",
                   say=[("Last pattern: turning a callback-style function, like setTimeout, into one that returns a "
                         "promise. Step one, return new Promise.", (1, 2)),
                        ("Step two, start the async task. Step three, inside that task's callback, call resolve "
                         "with the result, or reject with an error.", (3, 6)),
                        ("Now callers can use then and catch.", (9, 10)),
                        ("And the smallest version of this idea is a wait function that resolves after some "
                         "milliseconds.", 12)],
                   say_out="After one second, 16 for the number, and Not a number for the string.")

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
''',
                      say_q="Without await, write getTemperature, which takes a city and a JSON file and returns a "
                            "promise. Resolve with the city's temperature, or reject with Unknown City if the city "
                            "isn't in the file. Then show how to use it.",
                      say_a="Same shape as getImageURL. Return new Promise, fetch the file, convert with response "
                            "dot json, and then decide. If json of city is undefined, reject with Unknown City. "
                            "Otherwise, resolve with the temperature. Then the caller uses then and catch.",
                      answer_is_code=True)

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
                      "rej(2) and res(3) are ignored. then callbacks run after the current code (D first).",
                      say_q="What does this print, in order?",
                      say_a="A, then D, then B 1. The function passed to new Promise runs immediately, so A prints "
                            "first. The promise settles once, with 1, so reject 2 and resolve 3 are ignored. Then "
                            "callbacks always wait until the current code finishes, so D prints before B.")

        self.outro("return new Promise((resolve, reject) => { ... })\n"
                   "fetch(f).then(r => r.json()).then(json => cond ? reject(..) : resolve(..))\n"
                   "Use it: p.then(value => ...).catch(err => ...)\n"
                   "async fn always returns a promise; Promise.all keeps order, fails fast",
                   say="Recap. Return new Promise, with resolve and reject. Fetch, convert with response dot json, "
                       "then decide whether to reject or resolve. Callers use then and catch. An async function "
                       "always returns a promise. And Promise dot all keeps the input order, but fails as soon as "
                       "one promise rejects.")
