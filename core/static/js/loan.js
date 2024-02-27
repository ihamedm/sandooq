// loan.js
document.addEventListener("DOMContentLoaded", function() {
    var amountField = document.getElementById('id_amount');
    var installmentsField = document.getElementById('id_installments');
    var installmentAmountField = document.getElementById('id_installment_amount');
    var lastInstallmentAmountField = document.getElementById('id_last_installment_amount');

    // Function to calculate last installment amount
    function calculateLastInstallmentAmount() {
        var amount = parseFloat(amountField.value) || 0;
        var installments = parseInt(installmentsField.value) || 0;
        var installmentAmount = parseFloat(installmentAmountField.value) || 0;

        var lastInstallmentAmount = amount - (installments - 1) * installmentAmount;
        // Round the last installment amount to the nearest integer
        lastInstallmentAmount = Math.floor(lastInstallmentAmount);

        lastInstallmentAmountField.value = lastInstallmentAmount;
    }

    // Attach change event listeners to form fields
    amountField.addEventListener('input', calculateLastInstallmentAmount);
    installmentsField.addEventListener('input', calculateLastInstallmentAmount);
    installmentAmountField.addEventListener('input', calculateLastInstallmentAmount);
});
