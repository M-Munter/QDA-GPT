//main.js

// Function to get the CSRF token from the meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function showLoader() {
    const loader = document.getElementById("analyze-loader");
    if (loader) {
        loader.style.display = "block";
        console.log("Loader should now be visible");  // Debugging statement
    } else {
        console.error("Loader element not found or type mismatch");  // Debugging in case of issues
    }
}


function hideLoader() {
    const loader = document.getElementById("analyze-loader");
    if (loader) {
        loader.style.display = "none";
        console.log("Loader is now hidden");  // Debugging statement
    }
}


// Start fetching the analysis status
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
            setTimeout(fetchStatus, 500);  // Continue polling
        } else {
            hideLoader();  // Hide the loader when the analysis is complete
        }
    })
    .catch(error => {
        console.error('Error fetching status:', error);
        hideLoader();  // Hide the loader on error to avoid it hanging indefinitely
    });
}



function handleSubmit(event) {
    var action = event.submitter.value;
    if (action === 'analyze') {
        var fileInput = document.querySelector('input[type="file"]');
        if (!fileInput.files.length) {
            alert("Please select a file.");
            event.preventDefault();
            return false;
        }
        fetchStatus();  // Start polling for status updates
        showLoader('analyze');   // Show loader when the form is submitted
    }
    return true;
}




function selectAnalysisType(type) {
    document.getElementById('analysis_type_hidden').value = type; // Update the hidden input field with the selected type
    document.getElementById('analysis_type_hidden').value = type;
    var buttons = document.querySelectorAll('.analysis-button');
    buttons.forEach(function(button) {
        button.classList.remove('active-button');  // Remove active state from all buttons
    });
    document.getElementById(type + '-button').classList.add('active-button');  // Add active state to the selected button
    document.getElementById('selected-analysis-type').innerText = 'Selected analysis type: ' + type.charAt(0).toUpperCase() + type.slice(1) + ' Analysis';  // Update the display with the selected type
    console.log("[DEBUG] selectAnalysisType called with type:", type);
}


function selectAnalysisType(type) {
    document.getElementById('analysis_type_hidden').value = type; // Update this line to ensure the correct ID
    var buttons = document.querySelectorAll('.analysis-button');
    buttons.forEach(function(button) {
        button.classList.remove('active-button');
    });
    document.getElementById(type + '-button').classList.add('active-button');
    document.getElementById('selected-analysis-type').innerText = 'Selected analysis type: ' + type.charAt(0).toUpperCase() + type.slice(1) + ' Analysis';
    console.log("[DEBUG] selectAnalysisType called with type:", type);
}






function clearSessionData() {

    // Fetch the CSRF token from the hidden input in the form
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/clear-session/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            window.location.href = "/"; // Redirect to the dashboard (root URL)
        } else {
            console.error("[DEBUG] Failed to clear session data");
        }
    }).catch(error => {
        console.error("[DEBUG] clearSessionData error:", error);
    });
}

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
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);
        })
        .catch(error => console.error('Error downloading Excel:', error));
}


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

function hideInfo(infoId) {
    var infoBox = document.getElementById(infoId);
    infoBox.style.display = "none";
}



function validateForm() {
    console.log("[DEBUG] validateForm called.");
    const fileInput = document.querySelector('input[type="file"]').files.length > 0;
    const analysisType = document.getElementById('analysis_type_hidden').value !== "";
    const promptInput = document.querySelector('textarea[name="user_prompt"]').value.trim() !== "";

    const isValid = fileInput && analysisType && promptInput;
    const analyzeButton = document.getElementById('analyze-button');

    analyzeButton.disabled = !isValid;
    console.log("Analyze button disabled state:", analyzeButton.disabled);

}




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

    // Prevent entire row from being clickable
    document.querySelectorAll('.form-section').forEach(section => {
        section.addEventListener('click', function(event) {
            if (event.target.tagName !== 'INPUT' && event.target.tagName !== 'TEXTAREA' && event.target.tagName !== 'BUTTON' && event.target.tagName !== 'LABEL' && event.target.className !== 'file-name') {
                event.stopPropagation();
            }
        });
    });

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



// Establish WebSocket connection to the specified path
const socket = new WebSocket('ws://127.0.0.1:8000/ws/analysis/');

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
        }
    }
};

socket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};


function updateResults(promptTablePairs) {
    const resultContainer = document.getElementById('websocket-data');
    resultContainer.innerHTML = ''; // Clear previous results

    promptTablePairs.forEach(pair => {
        const promptDiv = document.createElement('div');
        promptDiv.innerHTML = `<strong>User Prompt:</strong> ${pair.prompt}`;
        resultContainer.appendChild(promptDiv);

        pair.tables.forEach(table => {
            const tableDiv = document.createElement('div');
            tableDiv.innerHTML = `<strong>${table.table_name}</strong>`;
            const tableElement = document.createElement('table');
            tableElement.classList.add('generated-table');

            const headerRow = document.createElement('tr');
            table.columns.forEach(column => {
                const th = document.createElement('th');
                th.textContent = column;
                headerRow.appendChild(th);
            });
            tableElement.appendChild(headerRow);

            table.data.forEach(row => {
                const rowElement = document.createElement('tr');
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    rowElement.appendChild(td);
                });
                tableElement.appendChild(rowElement);
            });

            resultContainer.appendChild(tableDiv);
            resultContainer.appendChild(tableElement);
        });
    });
}


function updateFlowchart(flowchartPath) {
    const flowchartContainer = document.getElementById('websocket-data');
    const imgElement = document.createElement('img');
    imgElement.src = flowchartPath;
    imgElement.alt = 'Generated Flowchart';
    imgElement.style.marginTop = '6px';
    imgElement.style.marginBottom = '12px';
    flowchartContainer.appendChild(imgElement);
}


function updateAnalysisStatus(status) {
    const statusContainer = document.getElementById('analysis-status');
    if (statusContainer) {
        statusContainer.innerText = status || "No status available";
        console.log('[DEBUG] Updated status:', status);
    } else {
        console.error("[DEBUG] Element with ID 'analysis-status' not found.");
    }
}







