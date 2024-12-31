/* jshint esversion: 6 */
document.addEventListener("DOMContentLoaded", function () {
  // Prefill created_date field
  var createdDateContainer = document.getElementById("created-date-container");
  var createdDateValue = createdDateContainer
    ? createdDateContainer.getAttribute("data-created-date")
    : null;

  if (createdDateValue) {
    var createdDateInput = document.getElementById("id_created_date");
    if (createdDateInput) {
      createdDateInput.value = createdDateValue;
      console.log("Prefilling created_date with value:", createdDateValue);
      console.log("Created Date Value after setting:", createdDateInput.value);
    } else {
      console.error("Created date input field not found.");
    }
  } else {
    console.error("No created_date value found.");
  }

  // Prefill date_regulations field
  var regulationsDateContainer = document.getElementById(
    "date-regulations-container",
  );
  var regulationsDateValue = regulationsDateContainer
    ? regulationsDateContainer.getAttribute("data-regulations-date")
    : null;

  if (regulationsDateValue) {
    var regulationsDateInput = document.getElementById("id_date_regulations");
    if (regulationsDateInput) {
      regulationsDateInput.value = regulationsDateValue;
      console.log(
        "Prefilling date_regulations with value:",
        regulationsDateValue,
      );
      console.log(
        "Date Regulations Value after setting:",
        regulationsDateInput.value,
      );
    } else {
      console.error("Date regulations input field not found.");
    }
  } else {
    console.error("No date_regulations value found.");
  }
});
document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  const montantTtcInput = document.getElementById("id_montant_ttc");
  const montantHtInput = document.getElementById("id_montant_ht");
  const montantTvaInput = document.getElementById("id_montant_tva");

  // Update dependent values based on active field
  const updateValues = () => {
    const montantTtc = parseFloat(montantTtcInput.value) || 0;
    const montantHt = parseFloat(montantHtInput.value) || 0;
    const montantTva = parseFloat(montantTvaInput.value) || 0;

    if (
      document.activeElement === montantHtInput ||
      document.activeElement === montantTvaInput
    ) {
      if (!montantTtcInput.value && montantHt !== 0 && montantTva !== 0) {
        montantTtcInput.value = (montantHt + montantTva).toFixed(2);
      }
    }

    if (
      document.activeElement === montantTtcInput ||
      document.activeElement === montantHtInput
    ) {
      if (!montantTvaInput.value && montantTtc !== 0 && montantHt !== 0) {
        montantTvaInput.value = (montantTtc - montantHt).toFixed(2);
      }
    }

    if (
      document.activeElement === montantTtcInput ||
      document.activeElement === montantTvaInput
    ) {
      if (!montantHtInput.value && montantTtc !== 0 && montantTva !== 0) {
        montantHtInput.value = (montantTtc - montantTva).toFixed(2);
      }
    }
  };

  // Recheck all values when any input is changed
  const recheckValues = () => {
    const montantTtc = parseFloat(montantTtcInput.value) || 0;
    const montantHt = parseFloat(montantHtInput.value) || 0;
    const montantTva = parseFloat(montantTvaInput.value) || 0;

    if (montantTtc && montantHt && !montantTva) {
      montantTvaInput.value = (montantTtc - montantHt).toFixed(2);
    }
    if (montantTtc && montantTva && !montantHt) {
      montantHt.value = (montantTtc - montantTva).toFixed(2);
    }
    if (montantTva && montantHt && !montantTtc) {
      montantTtc.value = (montantTva + montantHt).toFixed(2);
    }
  };

  // Event listeners for all inputs
  [montantTtcInput, montantHtInput, montantTvaInput].forEach((input) => {
    input.addEventListener("input", () => {
      updateValues();
      recheckValues();
    });

    input.addEventListener("focus", () => {
      input.value = "";
    });
  });
});
