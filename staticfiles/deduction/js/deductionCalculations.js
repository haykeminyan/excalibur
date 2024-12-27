/* jshint esversion: 6 */

document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  const montantTtcInput = document.getElementById("id_montant_ttc");
  const montantHtInput = document.getElementById("id_montant_ht");
  const montantTvaInput = document.getElementById("id_montant_tva");

  // Update dependent values based on active field
  const updateValues = () => {
    const montantTtc = parseFloat(montantTtcInput.value) || 0;
    const montantHt = parseFloat(montantHtInput.value) || 0;
    const montantTva =
      parseFloat(montantTvaInput.value) || 0;

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
  [
    montantTtcInput,
    montantHtInput,
    montantTvaInput,
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
