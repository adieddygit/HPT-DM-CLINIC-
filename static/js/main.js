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

