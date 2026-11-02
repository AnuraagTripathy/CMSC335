// mock DOM to test validateRequest logic
let fields = {}, alerts = [], confirmAnswer = true;
const document = { getElementById: id => ({ value: fields[id] }) };
const alert = m => alerts.push(m);
const window = { confirm: m => { alerts.push("CONFIRM:" + m); return confirmAnswer; } };
function validateRequest() {
  let errors = "";
  let name = document.getElementById("name").value;
  if (name.trim() === "") {
    errors += "|No name";
  }
  let [state, num] = document.getElementById("route").value.split("-");
  state = state.trim().toLowerCase();
  if (state !== "md" && state !== "va") {
    errors += "|Invalid state";
  }
  num = Number(num);
  if (isNaN(num) || num < 1 || num > 999) {
    errors += "|Invalid route";
  }
  if (errors !== "") {
    alert(errors);
    return false;
  }
  return window.confirm(`Request route ${state.toUpperCase()}-${num}?`);
}
for (const [n, r] of [["  ", "ny-95"], ["Ann", "MD-abc"], ["Ann", "va-1000"], ["Ann", "MD95"], ["Ann", " Md - 95 "], ["Ann", "MD-"], ["Bo", "VA-66"]]) {
  fields = { name: n, route: r }; alerts = [];
  const ret = validateRequest();
  console.log(JSON.stringify(n), JSON.stringify(r), "->", ret, alerts);
}
console.log(Number(""), Number(" 95 "), Number("95a"), Number(undefined), "MD95".split("-"));
// practice: "lat,long" style -> "Room: AVW,1112"
function checkRoom(v) {
  let errors = "";
  let [bldg, room] = v.split(",");
  if (bldg === undefined || bldg.trim() === "") errors += "|No building";
  room = Number(room);
  if (isNaN(room) || room < 1000 || room > 4999) errors += "|Invalid room";
  return errors;
}
for (const v of ["AVW,1112", " ,2000", "IRB", "IRB,5000", "IRB, 2120 "]) console.log(JSON.stringify(v), "->", JSON.stringify(checkRoom(v)));
