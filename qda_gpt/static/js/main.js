//main.js

// Function to get the CSRF token from the meta tag for secure form submissions
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Function to show the loader during data processing
function showLoader() {
    const loader = document.getElementById("analyze-loader");
    if (loader) {
        loader.style.display = "block";
        console.log("Loader should now be visible");
    } else {
        console.error("Loader element not found or type mismatch");
    }
}

// Function to hide the loader after processing is complete
function hideLoader() {
    const loader = document.getElementById("analyze-loader");
    if (loader) {
        loader.style.display = "none";
        console.log("Loader is now hidden");
    }
}

// Function to start fetching the analysis status from the server
function fetchStatus() {
    fetch('/analysis-status/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        updateAnalysisStatus(data.analysis_status);

        // Keep polling until the analysis is completed
        if (!data.analysis_status.includes("Analysis completed")) {
            setTimeout(fetchStatus, 500);  // Continue polling every 500ms
        } else {
            hideLoader();  // Hide the loader when the analysis is complete
        }
    })
    .catch(error => {
        console.error('Error fetching status:', error);
        hideLoader();  // Hide the loader on error to avoid it hanging indefinitely
    });
}

// Function to handle the form submission and validate the input
function handleSubmit(event) {
    var action = event.submitter.value;
    if (action === 'analyze') {
        var fileInput = document.querySelector('input[type="file"]');
        if (!fileInput.files.length) {
            alert("Please select a file.");
            event.preventDefault();
            return false;  // Prevent submission if no file is selected
        }
        fetchStatus();  // Start polling for status updates
        showLoader('analyze');   // Show loader when the form is submitted
    }
    return true;
}

// Function to handle selection of analysis type and update the UI
function selectAnalysisType(type) {
    document.getElementById('analysis_type_hidden').value = type; // Update the hidden input field with the selected type
    var buttons = document.querySelectorAll('.analysis-button');
    buttons.forEach(function(button) {
        button.classList.remove('active-button');  // Remove active state from all buttons
    });
    document.getElementById(type + '-button').classList.add('active-button');  // Add active state to the selected button

    // Update the display with the selected type and capitalize the first letter
    document.getElementById('selected-analysis-type').innerText = 'Selected analysis type: ' + type.charAt(0).toUpperCase() + type.slice(1) + ' Analysis';  // Update the display with the selected type
    console.log("[DEBUG] selectAnalysisType called with type:", type);
}


// Function to clear the session data on the server
function clearSessionData() {
    // Fetch the CSRF token from the hidden input
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send a GET request to the server to clear the session data
    fetch('/clear-session/', {
        method: 'GET',
        headers: {
            // Include the CSRF token in the request headers for security
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        // Check if the response from the server is OK (status code 200-299)
        if (response.ok) {
            // If the session was successfully cleared, redirect the user to the dashboard (root URL "/")
            window.location.href = "/";
        } else {
            console.error("[DEBUG] Failed to clear session data");
        }
    }).catch(error => {
        console.error("[DEBUG] clearSessionData error:", error);
    });
}

// Function to trigger the download of the analysis results as an Excel file
function downloadXLSX() {
    console.log("[DEBUG] downloadExcel called.");
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const fileName = `qda_${year}_${month}_${day}_${hours}${minutes}.xlsx`;

    const url = `/download_xlsx/?file_name=${fileName}`;
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const downloadUrl = window.URL.createObjectURL(blob);  // Create a URL for the blob
            const a = document.createElement('a');  // Create a temporary link element
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = fileName;  // Set the filename for the download
            document.body.appendChild(a);  // Append the link to the body
            a.click();  // Simulate a click to start the download
            window.URL.revokeObjectURL(downloadUrl);  // Clean up the URL object
            document.body.removeChild(a);  // Remove the temporary link
        })
        .catch(error => console.error('Error downloading Excel:', error));
}

// Function to show additional information in an info box
function showInfo(event, infoId) {
    event.preventDefault(); // Prevent default action
    event.stopPropagation(); // Prevent the file explorer from opening
    var infoBox = document.getElementById(infoId);
    if (infoBox.style.display === "none" || infoBox.style.display === "") {
        infoBox.style.display = "block";
    } else {
        infoBox.style.display = "none";
    }
}

// Function to hide the info box
function hideInfo(infoId) {
    var infoBox = document.getElementById(infoId);
    infoBox.style.display = "none";
}

// Function to validate the form before submission
function validateForm() {
    console.log("[DEBUG] validateForm called.");
    const fileInput = document.querySelector('input[type="file"]').files.length > 0;
    const analysisType = document.getElementById('analysis_type_hidden').value !== "";
    const promptInput = document.querySelector('textarea[name="user_prompt"]').value.trim() !== "";

    // Determine if the form is valid based on input presence
    const isValid = fileInput && analysisType && promptInput;
    const analyzeButton = document.getElementById('analyze-button');

    analyzeButton.disabled = !isValid;  // Disable the button if the form is invalid
    console.log("Analyze button disabled state:", analyzeButton.disabled);

}

// Event listener to initialize the script once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("[DEBUG] DOMContentLoaded event triggered.");
    document.getElementById('file-input').addEventListener('change', validateForm);
    document.querySelectorAll('.analysis-button').forEach(button => {
        button.addEventListener('click', validateForm);
    });
    document.querySelector('textarea[name="user_prompt"]').addEventListener('input', validateForm);

    // Add event listeners to info buttons
    document.querySelectorAll('.info-button').forEach(button => {
        button.addEventListener('click', function(event) {
            const infoId = this.getAttribute('data-info-id');
            showInfo(event, infoId);
        });
    });

    // Ensure info windows close on clicking 'X'
    document.querySelectorAll('.close').forEach(closeButton => {
        closeButton.addEventListener('click', function() {
            var infoBox = this.closest('.info-box');
            infoBox.style.display = 'none';
        });
    });

    // Prevent entire row from being clickable
    document.querySelectorAll('.form-section').forEach(section => {
        section.addEventListener('click', function(event) {
            if (event.target.tagName !== 'INPUT' && event.target.tagName !== 'TEXTAREA' && event.target.tagName !== 'BUTTON' && event.target.tagName !== 'LABEL' && event.target.className !== 'file-name') {
                event.stopPropagation();
            }
        });
    });

    // Prevent form input elements from propagating click events to their parent elements
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    });

    // Initially disable the Analyze button
    validateForm();

    // Enable the Download Excel button if deletion_results is present
    const deletionResults = document.getElementById('deletion-results').getAttribute('data-results');
    console.log("[DEBUG] Initial deletionResults:", deletionResults);
    if (deletionResults === 'true') {
        const downloadButton = document.getElementById('download-xlsx-btn');
        downloadButton.disabled = false;
        downloadButton.classList.remove('disabled-button');
        console.log("[DEBUG] Download button enabled initially.");
    }

    // Hide all info boxes initially
    var infoBoxes = document.querySelectorAll('.info-box');
    infoBoxes.forEach(function(infoBox) {
        infoBox.style.display = 'none';
    });

});

// Establish WebSocket connection to the specified path for real-time updates
let socketUrl;
if (window.location.host.includes('localhost') || window.location.host.includes('127.0.0.1')) {
    socketUrl = 'ws://127.0.0.1:8000/ws/analysis/';
} else {
    socketUrl = `wss://${window.location.host}/ws/analysis/`;
}

const socket = new WebSocket(socketUrl);

socket.onopen = function() {
    console.log('WebSocket connection opened');
    // Send a simple message to trigger the server response
    socket.send(JSON.stringify({message: 'Test message'}));
};

socket.onmessage = function(e) {
    console.log('WebSocket message received:', e.data);
    const data = JSON.parse(e.data);

    if (data.prompt_table_pairs) {
        updateResults(data.prompt_table_pairs);
    }

    if (data.flowchart_path) {
        updateFlowchart(data.flowchart_path);
    }
    if (data.analysis_status) {
        updateAnalysisStatus(data.analysis_status);
        showLoader();  // Keep loader visible for every phase of the analysis

        if (data.analysis_status.includes("Analysis completed")) {
            hideLoader();  // Hide loader when analysis is complete

            // Send the updated data to the server to update the session
            fetch('/update-session/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    prompt_table_pairs: data.prompt_table_pairs || [],
                    flowchart_path: data.flowchart_path || '',
                    analysis_status: data.analysis_status || '',
                    deletion_results: data.deletion_results || ''
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error('Failed to update session');
                }
                console.log('Session updated with new results');
            }).catch(error => {
                console.error('Error updating session:', error);
            });

        }
    }
    // Handle deletion results
    if (data.deletion_results) {
        updateDeletionResults(data.deletion_results);
    }
};

socket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};

// Function to update the analysis results and manage the collapsible sections
function updateResults(promptTablePairs, flowchartPath) {
    const resultContainer = document.getElementById('websocket-data');
    resultContainer.innerHTML = ''; // Clear previous results

    promptTablePairs.forEach((pair, index) => {
        // Create and append collapsible section for Prompt
        const promptSection = createCollapsibleSection(`Prompt ${index + 1}`, pair.prompt, `prompt-${index + 1}`);
        resultContainer.appendChild(promptSection);

        // Prepare the response content and append it inside a collapsible section
        let responseContent = '';
        pair.tables.forEach((table) => {
            responseContent += `<div class="table-name">${table.table_name}</div>`;
            responseContent += generateTableHtml(table);
        });
        const responseSection = createCollapsibleSection(`Response ${index + 1} from OpenAI Assistant`, responseContent, `response-${index + 1}`);
        resultContainer.appendChild(responseSection);
    });

    // Handle the flowchart separately
    if (flowchartPath) {
        // First, remove any existing standalone flowchart
        const existingFlowchart = document.querySelector('#websocket-data img[src="' + flowchartPath + '"]');
        if (existingFlowchart) {
            existingFlowchart.remove(); // Remove the existing flowchart if it is outside of a collapsible section
        }

        // Wrap the flowchart in a collapsible section
        const flowchartSection = createCollapsibleSection("Flowchart", `<img src="${flowchartPath}" alt="Flowchart" style="max-width: 100%; height: auto;">`, 'flowchart-section');
        resultContainer.appendChild(flowchartSection);
    }
}

// Create a collapsible section with the provided title, content, and id
function createCollapsibleSection(title, content, id) {
    // Create a div element that will contain the entire collapsible section
    const sectionDiv = document.createElement('div');
    sectionDiv.classList.add('collapsible-section');

    // Create a header div that will serve as the clickable element to toggle the content
    const headerDiv = document.createElement('div');
    headerDiv.classList.add('collapsible-header');

    // Set the header's HTML to include the title and an arrow icon indicating it's collapsible
    headerDiv.innerHTML = `<span class="arrow-icon">&#9660;</span><strong>${title}</strong>`;
    // Add a data attribute to link this header to its corresponding content section
    headerDiv.setAttribute('data-target', `#collapsible-content-${id}`);

    // Create a content div that will hold the actual content of the collapsible section
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('collapsible-content');
    contentDiv.id = `collapsible-content-${id}`;
    contentDiv.style.display = 'none';
    contentDiv.innerHTML = content;

    // Append the header and content divs to the main section div
    sectionDiv.appendChild(headerDiv);
    sectionDiv.appendChild(contentDiv);

    // Add click event to toggle visibility
    headerDiv.addEventListener('click', function () {
        const contentElement = document.querySelector(this.getAttribute('data-target'));
        if (contentElement.style.display === 'none') {
            contentElement.style.display = 'block';
            this.querySelector('.arrow-icon').innerHTML = '&#9650;'; // Change to up arrow
        } else {
            contentElement.style.display = 'none';
            this.querySelector('.arrow-icon').innerHTML = '&#9660;'; // Change to down arrow
        }
    });

    return sectionDiv;
}

// Function to generate HTML for a table given the data
function generateTableHtml(table) {
    let html = `<table class="generated-table"><thead><tr>`;

    // Loop through the columns array to create each table header cell
    table.columns.forEach(column => {
        html += `<th>${column}</th>`;  // Add each column header
    });
    html += `</tr></thead><tbody>`;  // Close the header row and open the table body

    // Loop through the data array to create each row of the table
    table.data.forEach(row => {
        html += `<tr>`;  // Start a new row
        row.forEach(cell => {
            html += `<td>${cell}</td>`;  // Add each cell value within the row
        });
        html += `</tr>`;  // Close the current row
    });
    html += `</tbody></table>`;  // Close the table body and the table itself

    return html;
}

// Function to update the deletion results and enable the download button
function updateDeletionResults(deletionResults) {
    const deletionContainer = document.getElementById('deletion-results');
    if (deletionContainer) {
        deletionContainer.innerHTML = `<strong>OpenAI API call termination status:</strong> ${deletionResults}`;
        deletionContainer.classList.add('left-align');
        deletionContainer.setAttribute('data-results', 'true');  // Set a flag to indicate results are available
        const downloadButton = document.getElementById('download-xlsx-btn');
        downloadButton.disabled = false;
        downloadButton.classList.remove('disabled-button');  // Enable the download button
        console.log("[DEBUG] Deletion results displayed.");
    } else {
        console.error("[DEBUG] Element with ID 'deletion-results' not found.");
    }
}

// Function to update the flowchart display
function updateFlowchart(flowchartPath) {
    // Ensure that we are only handling the flowchart inside a collapsible section
    const resultContainer = document.getElementById('websocket-data');

    // Remove any existing flowchart (if directly added before)
    const existingFlowchart = document.querySelector('#websocket-data img[src="' + flowchartPath + '"]');
    if (existingFlowchart) {
        existingFlowchart.remove();
    }

    // Now handle the flowchart inside the collapsible section
    if (flowchartPath && flowchartPath.trim() !== '') {
        const flowchartSection = createCollapsibleSection("Flowchart", `<img src="${flowchartPath}" alt="Flowchart" style="max-width: 100%; height: auto;">`, 'flowchart-section');
        resultContainer.appendChild(flowchartSection);
    }
}

// Function to update the analysis status display
function updateAnalysisStatus(status) {
    const statusContainer = document.getElementById('analysis-status');
    if (statusContainer) {
        statusContainer.innerText = status || "No status available";
        console.log('[DEBUG] Updated status:', status);
    } else {
        console.error("[DEBUG] Element with ID 'analysis-status' not found.");
    }
}




