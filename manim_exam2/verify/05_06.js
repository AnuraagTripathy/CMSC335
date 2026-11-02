// ===== 05 promises =====
const files = { "images.json": { urls: ["a.png", "b.png", "c.png"] }, "temps.json": { boston: 41, austin: 77 } };
const fetch = f => Promise.resolve({ json: () => Promise.resolve(files[f]) });
const log = [];
function getImageURL(index, jsonFile) {
  return new Promise((resolve, reject) => {
    fetch(jsonFile)
      .then(response => response.json())
      .then(json => index >= json.urls.length ? reject("Invalid Index") : resolve(json.urls[index]));
  });
}
async function getImageURL2(index, jsonFile) {
  const response = await fetch(jsonFile);
  const json = await response.json();
  if (index >= json.urls.length) throw "Invalid Index";
  return json.urls[index];
}
function getTemperature(city, jsonFile) {
  return new Promise((resolve, reject) => {
    fetch(jsonFile)
      .then(r => r.json())
      .then(json => json[city] === undefined ? reject("Unknown City") : resolve(json[city]));
  });
}
function delayedSquare(x, ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => typeof x === "number" ? resolve(x * x) : reject("Not a number"), ms);
  });
}
(async () => {
  await getImageURL(1, "images.json").then(u => console.log("05 then:", u)).catch(e => console.log("05 catch:", e));
  await getImageURL(5, "images.json").then(u => console.log("05 then:", u)).catch(e => console.log("05 catch:", e));
  await getImageURL2(2, "images.json").then(u => console.log("05 await:", u));
  await getImageURL2(9, "images.json").catch(e => console.log("05 await catch:", e));
  await Promise.all([getImageURL(0, "images.json"), getImageURL(2, "images.json")]).then(u => console.log("05 all:", u));
  await Promise.all([getImageURL(0, "images.json"), getImageURL(7, "images.json")]).then(u => console.log("05 all:", u)).catch(e => console.log("05 all catch:", e));
  await getTemperature("austin", "temps.json").then(t => console.log("05 temp", t));
  await getTemperature("paris", "temps.json").catch(e => console.log("05 temp", e));
  await delayedSquare(4, 10).then(v => console.log("05 sq", v));
  await delayedSquare("4", 10).catch(e => console.log("05 sq", e));
  async function f() { return 5; }
  const pf = f();
  console.log("05 async returns", pf instanceof Promise, pf);
  const never = new Promise(res => { console.log("05 work done"); });
  setTimeout(() => console.log("05 never:", never), 5);
  await new Promise(r => setTimeout(r, 20));
  // chain
  await Promise.resolve(2).then(v => v * 10).then(v => { console.log("05 chain", v); });
  // practice 2
  console.log("--- 05 practice2");
  const p = new Promise((res, rej) => { console.log("A"); res(1); rej(2); res(3); });
  p.then(v => console.log("B", v)).catch(e => console.log("C", e));
  console.log("D");
  await new Promise(r => setTimeout(r, 20));
  // ===== 06 event loop =====
  console.log("== 06 puzzle1");
  console.log("Dog"); setTimeout(() => console.log("Cat"), 0); console.log("Lion");
  await new Promise(r => setTimeout(r, 20));
  console.log("== 06 puzzle2");
  console.log("1");
  setTimeout(() => console.log("2"), 0);
  Promise.resolve().then(() => console.log("3"));
  console.log("4");
  await new Promise(r => setTimeout(r, 20));
  console.log("== 06 practice");
  setTimeout(() => console.log("A"), 0);
  Promise.resolve().then(() => { console.log("B"); setTimeout(() => console.log("C"), 0); });
  Promise.resolve().then(() => console.log("D"));
  console.log("E");
  await new Promise(r => setTimeout(r, 30));
  console.log("== 06 trap");
  function getCount() {
    let count;
    const id = setInterval(() => { count = 10; clearInterval(id); }, 10);
    return count;
  }
  console.log(getCount());
  function getCountP() {
    return new Promise(resolve => {
      const id = setInterval(() => { clearInterval(id); resolve(10); }, 10);
    });
  }
  await getCountP().then(c => console.log(c));
  console.log("== 06 interval");
  let n = 0;
  await new Promise(done => {
    const id = setInterval(() => { n++; console.log(n); if (n === 3) { clearInterval(id); done(); } }, 5);
  });
})();
