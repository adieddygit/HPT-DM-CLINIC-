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

// Add event listener for adding more lab investigations
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

    // Add new input group before the "Add Another" button
    investigationGroup.insertBefore(newInputGroup, document.getElementById('add-more'));
});

// Add event listener for removing the last lab investigation group
document.getElementById('delete').addEventListener('click', function() {
    const investigationGroup = document.getElementById('lab-investigation-group');
    const inputGroups = investigationGroup.getElementsByClassName('input-group');

    if (inputGroups.length > 0) {
        investigationGroup.removeChild(inputGroups[inputGroups.length - 1]);
    }
});

// Add event listener for adding more radiograph investigations
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

    // Add new input group before the "Add Another" button
    radiographGroup.insertBefore(newRadiographGroup, document.getElementById('add-more-radiograph'));
});

// Add event listener for removing the last radiograph investigation group
document.getElementById('delete-radiograph').addEventListener('click', function() {
    const radiographGroup = document.getElementById('radiograph-investigation-group');
    const inputGroups = radiographGroup.getElementsByClassName('input-group');

    if (inputGroups.length > 0) {
        radiographGroup.removeChild(inputGroups[inputGroups.length - 1]);
    }
});


document.getElementById('signlog').addEventListener('submit', function(event){
event.preventDefault()
let errors = []

let username = document.getElementById('username').value
let email = document.getElementById('email').value
let password = document.getElementById('password').value

if (username.length <3){
    errors.push('Username must be at least 3 characters long')
}

let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if(!emailPattern.test(email)){
    errors.push('Please enter a valid email address. !')
}

if(password.length < 6){
    errors.push('Password must be at least 6 characters long !')
}else if(!/^[a-zA-Z]+@,%#&\*\.\+\-[0-9]+$/.test(password)){
    errors.push('Password must include alphanumerics and allows symbols !')
}

if (errors.length >0){
    document.getElementById('error').innerHTML = errors.join('<br/>')
    document.getElementById('error').style.color = 'red' 
}

})