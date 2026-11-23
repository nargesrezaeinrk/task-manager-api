document.addEventListener("DOMContentLoaded", () => {

    const plannerForm = document.getElementById("planner-form");

    if (!plannerForm) {
        return;
    }

    const modal = document.getElementById("unsaved-modal");

    const cancelButton = document.getElementById("cancel-changes");
    const saveAndContinueButton = document.getElementById("save-and-continue");
    const discardButton = document.getElementById("discard-changes");
    const stayButton = document.getElementById("stay-on-page");

    const textareas = plannerForm.querySelectorAll("textarea");

    let originalValues = {};
    let pendingAction = null;
    let isSaving = false;


    // Store the original values of all textareas.

    function saveOriginalValues() {

        originalValues = {};

        textareas.forEach((textarea) => {
            originalValues[textarea.name] = textarea.value;
        });

    }


    // Check whether any textarea has changed.

    function hasUnsavedChanges() {

        return Array.from(textareas).some((textarea) => {
            return textarea.value !== originalValues[textarea.name];
        });

    }


    // Restore all textareas to their original values.

    function discardChanges() {

        textareas.forEach((textarea) => {
            textarea.value = originalValues[textarea.name];
        });

    }


    // Open the confirmation modal.

    function openModal(action) {

        pendingAction = action;
        modal.hidden = false;

    }


    // Close the confirmation modal.

    function closeModal() {

        modal.hidden = true;
        pendingAction = null;

    }


    // Navigate to the action that was originally requested.

    function continueNavigation() {

        if (!pendingAction) {
            return;
        }

        const action = pendingAction;

        closeModal();

        if (action.type === "link") {
            window.location.href = action.url;
        }

        if (action.type === "form") {
            action.form.submit();
        }

    }


    // Intercept links inside the planner layout.

    document.querySelectorAll(".planner-layout a").forEach((link) => {

        link.addEventListener("click", (event) => {

            if (
                event.defaultPrevented ||
                event.button !== 0 ||
                event.ctrlKey ||
                event.metaKey ||
                event.shiftKey ||
                event.altKey ||
                link.target === "_blank"
            ) {
                return;
            }

            if (!hasUnsavedChanges()) {
                return;
            }

            event.preventDefault();

            openModal({
                type: "link",
                url: link.href,
            });

        });

    });


    // Intercept the Add New Week form.

    document.querySelectorAll(".add-week-form").forEach((form) => {

        form.addEventListener("submit", (event) => {

            if (!hasUnsavedChanges()) {
                return;
            }

            event.preventDefault();

            openModal({
                type: "form",
                form: form,
            });

        });

    });


    // Cancel Changes.

    cancelButton.addEventListener("click", () => {

        if (!hasUnsavedChanges()) {
            return;
        }

        discardChanges();

    });


    // Save and Continue.

    saveAndContinueButton.addEventListener("click", async () => {

        if (!pendingAction || isSaving) {
            return;
        }

        isSaving = true;
        saveAndContinueButton.disabled = true;

        try {

            const formData = new FormData(plannerForm);

            const response = await fetch(plannerForm.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (!response.ok) {
                throw new Error("The planner could not be saved.");
            }

            const result = await response.json();

            if (!result.success) {
                throw new Error("The planner could not be saved.");
            }

            continueNavigation();

        } catch (error) {

            console.error(error);

            alert("Your changes could not be saved. Please try again.");

        } finally {

            isSaving = false;
            saveAndContinueButton.disabled = false;

        }

    });


    // Discard Changes and Continue.

    discardButton.addEventListener("click", () => {

        discardChanges();
        continueNavigation();

    });


    // Stay on This Week.

    stayButton.addEventListener("click", () => {

        closeModal();

    });


    // Warn before refreshing or closing the browser tab.

    window.addEventListener("beforeunload", (event) => {

        if (hasUnsavedChanges()) {

            event.preventDefault();
            event.returnValue = "";

        }

    });


    // Save initial values.

    saveOriginalValues();

});