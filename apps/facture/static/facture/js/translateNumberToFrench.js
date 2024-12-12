const numberToFrench = (number) => {
  const ones = [
    "", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
    "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"
  ];
  const tens = [
    "", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingts", "quatre-vingt-dix"
  ];
  const thousands = ["", "mille", "million", "milliard"]; // You can add more if needed

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
      // Handle large numbers, thousands, millions, billions, etc.
      let numberString = "";
      let scaleIndex = 0;

      // Process each group of three digits
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

  if (number < 0) return "moins " + convertNumber(Math.abs(number));
  const result = convertNumber(number);

  // Capitalize the first letter of the result
  return result.toUpperCase() + ' MAD';
};

