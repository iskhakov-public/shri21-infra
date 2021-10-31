test("unit tests", () => {
  expect(1 + 2).toBe(3);
});

test("hermione tests", () => {
  expect(2 * 2).toBe(4);
});

test("e2e tests", () => {
  expect(1).toBe(1);
});

test("laws of physics", () => {
  expect(true).toBe(true);
});

test("1 + 1 = 2?", () => {
  expect(Math.log10(Math.pow(1 + 1, 10) * 21.5) / 2.174213).toBeLessThan(2);
});
