var d3 = require('d3')

module.exports = {
  hello: hello,
  moreThings: moreThings
}

function hello () {
  return "hello"
}


function moreThings(x) {
  return (x == 8) ? 10 : 7;
}

