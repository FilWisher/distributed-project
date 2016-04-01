var test = require('tape')
var main = require('../assets/main.js')

test('that this works', function(t) {
  
  main.hello()
  t.equals(1, 1, 'it does')
  t.end()
})

test('that this works', function(t) {
  
  main.moreThings()
  main.moreThings(8)
  t.equals(1, 1, 'it does')
  t.end()
})
