function hideElement(element) {
    document.getElementById(element + "-div").hidden = true;
    document.getElementById(element).required = false;
    document.getElementById(element).value = "";
}

function showElement(element) {
    document.getElementById(element + "-div").hidden = false;
    document.getElementById(element).required = true;
}

function changedSelection() {
    let selectBox = document.getElementById("exercise-type");
    let value = selectBox.value;
    if (value === "Running" || value === "Biking" || value === "Swimming") {
        showElement("distance");
        showElement("duration");
        hideElement("reps");
        hideElement("weight");
        hideElement("sets");
    } else if (value === "Weights") {
        showElement("reps");
        showElement("weight");
        showElement("sets");
        hideElement("distance");
        hideElement("duration");
    } else if (value === "Yoga") {
        showElement("duration");
        hideElement("reps");
        hideElement("weight");
        hideElement("sets");
        hideElement("distance");
    } else if (value === "Other") {
        hideElement("reps");
        hideElement("weight");
        hideElement("sets");
        hideElement("distance");
        hideElement("duration");
    }
}