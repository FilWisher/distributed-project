test("heh", function() {
  equal(1, 1, "passed")
})

test("hello returns hello", function () {
  equal(hello(), "hello", "it does")
})

test("moreThings return 7", function () {
  equal(moreThings(), 7, "it does")
})
