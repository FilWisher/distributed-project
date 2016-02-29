module.exports = {
  hello: hello,
  moreThings: moreThings
}

function hello () {
  return "hello"
}


function moreThings(x) {
  return (x == 8) ? 10 : 7;
  //return 7
}
