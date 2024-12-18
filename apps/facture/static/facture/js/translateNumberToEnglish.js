/* jshint esversion: 6 */

const numberToEnglish = (number) => {
  "use strict";
  const ones = [
    "",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
  ];
  const tens = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
  ];
  const thousands = [
    "",
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
  ];

  const convertNumber = (num) => {
    if (num < 20) {
      return ones[num];
    } else if (num < 100) {
      const tensPart = Math.floor(num / 10);
      const onesPart = num % 10;
      return tens[tensPart] + (onesPart > 0 ? "-" + ones[onesPart] : "");
    } else if (num < 1000) {
      const hundredsPart = Math.floor(num / 100);
      const remainder = num % 100;
      return (
        ones[hundredsPart] +
        " hundred" +
        (remainder > 0 ? " " + convertNumber(remainder) : "")
      );
    } else {
      let numberString = "";
      let scaleIndex = 0;

      while (num > 0) {
        const group = num % 1000;
        if (group > 0) {
          const groupString = convertNumber(group);
          numberString =
            groupString +
            (thousands[scaleIndex] ? " " + thousands[scaleIndex] : "") +
            (numberString ? " " + numberString : "");
        }
        num = Math.floor(num / 1000);
        scaleIndex++;
      }

      return numberString;
    }
  };

  if (number < 0) {
    return "minus " + numberToEnglish(Math.abs(number));
  }

  const [integerPart, fractionalPart] = number.toString().split(".");
  let result = convertNumber(parseInt(integerPart, 10));

  // Check for fractional part and add only if it's not zero
  if (fractionalPart && parseInt(fractionalPart, 10) > 0) {
    const fractionalWords = fractionalPart
      .split("")
      .map((digit) => ones[parseInt(digit, 10)])
      .join(" ");
    result += " point " + fractionalWords;
  }

  // Capitalize the first letter of the result
  return result.toUpperCase() + ' DOLLARS';
};
