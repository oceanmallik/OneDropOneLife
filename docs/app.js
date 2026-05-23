// docs/app.js

let allDonors = [];

// 1. Fetch JSON data from the docs directory
async function fetchDonorData() {
    try {
        // Pulls from the file generated from your published CSV link
        const response = await fetch('./donors.json');
        allDonors = await response.json();
        
        // Display data immediately upon load
        filterAndSortDonors();
    } catch (error) {
        console.error("Error reading donor database:", error);
        document.getElementById('donorGrid').innerHTML = 
            `<p class="status-message">Failed to load donor profiles. Verify that donors.json exists inside your docs folder.</p>`;
    }
}

// 2. Main Filtering and Sorting controller
function filterAndSortDonors() {
    const bloodSelection = document.getElementById('bloodFilter').value;
    const locationSortSelection = document.getElementById('locationSort').value;
    
    // Process A: Dropdown Filter rule
    let processedDonors = allDonors.filter(donor => {
        if (bloodSelection === "All") return true;
        return donor["Blood Group"] === bloodSelection;
    });

    // Process B: Text-based Alphabetical sorting for Addresses
    if (locationSortSelection === "ASC") {
        processedDonors.sort((a, b) => a.Address.localeCompare(b.Address));
    } else if (locationSortSelection === "DESC") {
        processedDonors.sort((a, b) => b.Address.localeCompare(a.Address));
    }

    // Process C: Print update to DOM
    renderCards(processedDonors);
}

// 3. Render raw dynamic cards matching requested variables
function renderCards(donorList) {
    const grid = document.getElementById('donorGrid');
    grid.innerHTML = ''; // Wipe out previous state

    if (donorList.length === 0) {
        grid.innerHTML = '<p class="status-message">No donor records found matching the selection criteria.</p>';
        return;
    }

    donorList.forEach((donor, index) => {
        const phone = donor["Contact Number"] || "Not available";
        const hasPhone = phone !== "Not available";
        // Structure strictly contains: Name, ID, Blood Group, Address, Contact Number
        const cardHTML = `
            <article class="donor-record-card" style="--card-index: ${index};">
                <div class="donor-record-header">
                    <h3>${donor.Name}</h3>
                    <span class="blood-pill">${donor["Blood Group"]}</span>
                </div>
                <div class="donor-record-meta">
                    <p><strong>Student ID:</strong> ${donor.ID}</p>
                    <p><strong>Location:</strong> ${donor.Address}</p>
                    <p><strong>Contact:</strong> ${phone}</p>
                </div>
                ${hasPhone
                    ? `<a class="button button-primary donor-call" href="tel:${phone}">Call Donor</a>`
                    : `<span class="button button-secondary donor-call donor-call-disabled" aria-disabled="true">Contact Unavailable</span>`}
            </article>
        `;
        grid.innerHTML += cardHTML;
    });
}

// Boot up application
window.onload = fetchDonorData;