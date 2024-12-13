/* jshint esversion: 6 */

const numberToFrench = (number) => {
  "use strict";
  const ones = [
    "", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
    "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"
  ];
  const tens = [
    "", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingts", "quatre-vingt-dix"
  ];
  const thousands = ["", "mille", "million", "milliard"]; // Extend as needed

  const convertNumber = (num) => {
    if (num < 20) {
      return ones[num];
    } else if (num < 100) {
      const tensPart = Math.floor(num / 10);
      const onesPart = num % 10;
      return onesPart === 0 ? tens[tensPart] : tens[tensPart] + (onesPart === 1 && tensPart === 8 ? "-et-un" : "-" + ones[onesPart]);
    } else if (num < 1000) {
      const hundredsPart = Math.floor(num / 100);
      const remainder = num % 100;
      return hundredsPart === 1 ? "cent" + (remainder > 0 ? " " + convertNumber(remainder) : "") : ones[hundredsPart] + " cent" + (remainder > 0 ? " " + convertNumber(remainder) : "");
    } else {
      let numberString = "";
      let scaleIndex = 0;

      while (num > 0) {
        const group = num % 1000;
        if (group > 0) {
          const groupString = convertNumber(group);
          numberString = groupString + (thousands[scaleIndex] ? " " + thousands[scaleIndex] : "") + (numberString ? " " + numberString : "");
        }
        num = Math.floor(num / 1000);
        scaleIndex++;
      }

      return numberString;
    }
  };

  if (number < 0){
     return "MOINS " + numberToFrench(Math.abs(number));
  }

  const [integerPart, fractionalPart] = number.toString().split(".");
  let result = convertNumber(parseInt(integerPart, 10));

  if (fractionalPart) {
    const fractionalWords = fractionalPart
      .split("")
      .map(digit => ones[parseInt(digit, 10)])
      .join(" ");
    result += " virgule " + fractionalWords;
  }

  // Capitalize the first letter of the result and append "MAD"
  return result.toUpperCase() + " MAD";
};
