/* jshint esversion: 6 */

document.addEventListener("DOMContentLoaded", () => {
    "use strict";
    const percentStep = document.getElementById('id_percent');
    percentStep.step = 0.01;
    percentStep.min = 0.1;
    percentStep.max = 1;
});


document.addEventListener("DOMContentLoaded", () => {
    "use strict";
    const quantityInput = document.getElementById("id_quantity");
    const percentInput = document.getElementById("id_percent");
    const quantityAfterPercentInput = document.getElementById("id_quantity_after_percent");
    const totalHtInput = document.getElementById('id_tax_ht');
    const totalTaxInput = document.getElementById('id_total_tax');
    const totalTtcInput = document.getElementById('id_total_ttc');
    const netPayInput = document.getElementById('id_net_pay');
    const totalSumFrInput =  document.getElementById('id_total_sum_fr');

    // Update dependent values based on active field
    const updateValues = () => {
        const quantity = parseFloat(quantityInput.value) || 0;
        const percent = parseFloat(percentInput.value) || 0;
        const quantityAfterPercent = parseFloat(quantityAfterPercentInput.value) || 0;

        if (document.activeElement === quantityInput || document.activeElement === percentInput) {
            if (!quantityAfterPercentInput.value && quantity !== 0 && percent !== 0) {
                 quantityAfterPercentInput.value = (quantity * percent).toFixed(2);
            }

        }

        if (document.activeElement === quantityInput || document.activeElement === quantityAfterPercentInput) {
            if (!percentInput.value && quantityAfterPercent !== 0 && quantity !== 0) {
             percentInput.value = (quantityAfterPercent / quantity).toFixed(2);
            }
        }

        if (document.activeElement === percentInput || document.activeElement === quantityAfterPercentInput) {
            if (!quantityInput.value && quantityAfterPercent !== 0 && percent !== 0) {
             quantityInput.value = (quantityAfterPercent / percent).toFixed(2);
            }
        }
        totalHtInput.value = totalTtcInput.value = netPayInput.value = quantityAfterPercentInput.value;
        totalSumFrInput.value = numberToFrench(totalHtInput.value);
        totalTaxInput.value = (quantityAfterPercentInput.value / 6).toFixed(2);

    };

    // Recheck all values when any input is changed
    const recheckValues = () => {
        const quantity = parseFloat(quantityInput.value) || 0;
        const percent = parseFloat(percentInput.value) || 0;
        const quantityAfterPercent = parseFloat(quantityAfterPercentInput.value) || 0;
                const totalHt = parseFloat(totalHtInput.value) || 0;

        if (quantity && percent && !quantityAfterPercent) {
            quantityAfterPercentInput.value = (quantity * percent).toFixed(2);
        }
        if (percent && quantityAfterPercent && !quantity) {
            quantityInput.value = (quantityAfterPercent / percent).toFixed(2);
        }
        if (quantity && quantityAfterPercent && !percent) {
            percentInput.value = (quantityAfterPercent / quantity).toFixed(2);
        }
        totalHtInput.value = totalTtcInput.value = netPayInput.value = quantityAfterPercentInput.value;
        totalSumFrInput.value = numberToFrench(totalHtInput.value);
        totalTaxInput.value = (quantityAfterPercentInput.value / 6).toFixed(2);

    };

    // Event listeners for all inputs
    [quantityInput, percentInput, quantityAfterPercentInput, totalHtInput].forEach(input => {
        input.addEventListener("input", () => {
            updateValues();
            recheckValues();
        });

        input.addEventListener("focus", () => {
            input.value = '';
        });
    });
});
