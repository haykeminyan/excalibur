/* jshint esversion: 6 */
document.addEventListener("DOMContentLoaded", function () {
  // Get the data-created-date attribute from the container
  var createdDateContainer = document.getElementById("created-date-container");
  var createdDateValue = createdDateContainer
    ? createdDateContainer.getAttribute("data-created-date")
    : null;

  console.log("Prefilling created_date with value:", createdDateValue);

  // Now, set the value of the input field if available
  var createdDateInput = document.getElementById("id_created_date");
  if (createdDateInput && createdDateValue) {
    createdDateInput.value = createdDateValue; // Prefill the field with the value from data attribute
    console.log("Created Date Value after setting:", createdDateInput.value);
  } else {
    console.error("Created date input field or value not found.");
  }
});
document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  const percentStep = document.getElementById("id_percent");
  percentStep.step = 0.01;
  percentStep.min = 0.1;
  percentStep.max = 1;
});

document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  const quantityInput = document.getElementById("id_quantity");
  const percentInput = document.getElementById("id_percent");
  const quantityAfterPercentInput = document.getElementById(
    "id_quantity_after_percent",
  );
  const totalTaxInput = document.getElementById("id_total_tax");
  const netPayInput = document.getElementById("id_net_pay");
  const totalSumEnInput = document.getElementById("id_total_sum_en");

  // Update dependent values based on active field
  const updateValues = () => {
    const quantity = parseFloat(quantityInput.value) || 0;
    const percent = parseFloat(percentInput.value) || 0;
    const quantityAfterPercent =
      parseFloat(quantityAfterPercentInput.value) || 0;
    const netPay = parseFloat(netPayInput.value) || 0;
    const totalTax = parseFloat(totalTaxInput.value) || 0;
    if (
      document.activeElement === quantityInput ||
      document.activeElement === percentInput
    ) {
      if (!quantityAfterPercentInput.value && quantity !== 0 && percent !== 0) {
        quantityAfterPercentInput.value = (quantity * percent).toFixed(2);
      }
    }

    if (
      document.activeElement === quantityInput ||
      document.activeElement === quantityAfterPercentInput
    ) {
      if (!percentInput.value && quantityAfterPercent !== 0 && quantity !== 0) {
        percentInput.value = (quantityAfterPercent / quantity).toFixed(2);
      }
    }

    if (
      document.activeElement === percentInput ||
      document.activeElement === quantityAfterPercentInput
    ) {
      if (!quantityInput.value && quantityAfterPercent !== 0 && percent !== 0) {
        quantityInput.value = (quantityAfterPercent / percent).toFixed(2);
      }
    }

    if (
      document.activeElement === netPayInput ||
      document.activeElement === totalTaxInput ||
      document.activeElement === quantityAfterPercentInput
    ) {
      if (quantityAfterPercent !== 0 && totalTax) {
        netPayInput.value = (quantityAfterPercent - totalTax).toFixed(2);
      } else if (quantityAfterPercent !== 0 && netPay) {
        totalTaxInput.value = (quantityAfterPercent - netPay).toFixed(2);
      } else if (totalTax !== 0 && netPay) {
        quantityAfterPercentInput.value = (netPay + totalTax).toFixed(2);
      }
    }

    totalSumEnInput.value = numberToEnglish(netPayInput.value);
  };

  // Recheck all values when any input is changed
  const recheckValues = () => {
    const quantity = parseFloat(quantityInput.value) || 0;
    const percent = parseFloat(percentInput.value) || 0;
    const quantityAfterPercent =
      parseFloat(quantityAfterPercentInput.value) || 0;
    const totalTax = parseFloat(totalTaxInput.value) || 0;
    const netPay = parseFloat(netPayInput.value) || 0;

    if (quantity && percent && !quantityAfterPercent) {
      quantityAfterPercentInput.value = (quantity * percent).toFixed(2);
    }
    if (percent && quantityAfterPercent && !quantity) {
      quantityInput.value = (quantityAfterPercent / percent).toFixed(2);
    }
    if (quantity && quantityAfterPercent && !percent) {
      percentInput.value = (quantityAfterPercent / quantity).toFixed(2);
    }
    if (quantityAfterPercent !== 0 && totalTax) {
      netPayInput.value = (quantityAfterPercent - totalTax).toFixed(2);
    } else if (quantityAfterPercent !== 0 && netPay) {
      totalTaxInput.value = (quantityAfterPercent - netPay).toFixed(2);
    } else if (totalTax !== 0 && netPay) {
      quantityAfterPercentInput.value = (netPay + totalTax).toFixed(2);
    }
    totalSumEnInput.value = numberToEnglish(netPayInput.value);
  };

  // Event listeners for all inputs
  [
    quantityInput,
    percentInput,
    quantityAfterPercentInput,
    totalTaxInput,
    netPayInput,
  ].forEach((input) => {
    input.addEventListener("input", () => {
      updateValues();
      recheckValues();
    });

    input.addEventListener("focus", () => {
      input.value = "";
    });
  });
});
