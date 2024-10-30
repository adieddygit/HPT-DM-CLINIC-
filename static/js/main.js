// Toggle the Side Navigation
// function toggleNav() {
//     const sidenav = document.getElementById("mySidenav");
//     if (sidenav.style.width === "250px") {
//         sidenav.style.width = "0";
//     } else {
//         sidenav.style.width = "250px";
//     }
// }

// Toggle the Side Navigation
function toggleNav() {
    const sidenav = document.getElementById("mySidenav");
    const mainContent = document.querySelector(".main-content");
    
    if (sidenav.style.width === "220px") {
        sidenav.style.width = "0";
        mainContent.classList.remove("sidenav-open");
    } else {
        sidenav.style.width = "220px";
        mainContent.classList.add("sidenav-open");
    }
}

document.getElementById('add-more').addEventListener('click', function() {
    const investigationGroup = document.getElementById('lab-investigation-group');
    
    // Create a new div for the additional input group
    const newInputGroup = document.createElement('div');
    newInputGroup.classList.add('input-group');

    // Create new input for Investigation Type
    const newInvestigationInput = document.createElement('input');
    newInvestigationInput.type = 'text';
    newInvestigationInput.name = 'lab_investigation_type[]';
    newInvestigationInput.placeholder = 'Enter Investigation';
    newInvestigationInput.required = true;

    // Create new input for Investigation Result
    const newResultInput = document.createElement('input');
    newResultInput.type = 'text';
    newResultInput.name = 'lab_investigation_result[]';
    newResultInput.placeholder = 'Enter Result';
    newResultInput.required = true;

    // Append inputs to the new div
    newInputGroup.appendChild(newInvestigationInput);
    newInputGroup.appendChild(newResultInput);

    // Add new input group before the button
    investigationGroup.insertBefore(newInputGroup, document.getElementById('add-more'));
});

document.getElementById('add-more-radiograph').addEventListener('click', function() {
    const radiographGroup = document.getElementById('radiograph-investigation-group');
    
    // Create a new div for the additional input group
    const newRadiographGroup = document.createElement('div');
    newRadiographGroup.classList.add('input-group');

    // Create new input for Radiograph Investigation Type
    const newRadiographInput = document.createElement('input');
    newRadiographInput.type = 'text';
    newRadiographInput.name = 'radiograph_investigation_type[]';
    newRadiographInput.placeholder = 'Enter Investigation';
    newRadiographInput.required = true;

    // Create new input for Radiograph Investigation Result
    const newRadiographResultInput = document.createElement('input');
    newRadiographResultInput.type = 'text';
    newRadiographResultInput.name = 'radiograph_investigation_result[]';
    newRadiographResultInput.placeholder = 'Enter Result';
    newRadiographResultInput.required = true;

    // Append inputs to the new div
    newRadiographGroup.appendChild(newRadiographInput);
    newRadiographGroup.appendChild(newRadiographResultInput);

    // Add new input group before the button
    radiographGroup.insertBefore(newRadiographGroup, document.getElementById('add-more-radiograph'));
});

