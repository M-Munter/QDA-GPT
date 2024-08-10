// Function to get the CSRF token from the meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function showLoader(type) {
    const loader = document.getElementById("analyze-loader");
    if (loader && type === 'analyze') {
        loader.style.display = "block";
        const analysisStatus = document.getElementById("analysis-status");
        if (analysisStatus) {
            analysisStatus.style.display = "none";
        }
    }
}


function selectAnalysisType(type) {
    document.getElementById('analysis_type').value = type;
    document.getElementById('analysis_type_hidden').value = type;
    var buttons = document.querySelectorAll('.analysis-button');
    buttons.forEach(function(button) {
        button.classList.remove('active-button');
    });
    document.getElementById(type + '-button').classList.add('active-button');
    document.getElementById('selected-analysis-type').innerText = 'Selected analysis type: ' + type.charAt(0).toUpperCase() + type.slice(1) + ' Analysis';
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


function handleSubmit(event) {
    var action = event.submitter.value;
    if (action === 'analyze') {
        var fileInput = document.querySelector('input[type="file"]');
        if (!fileInput.files.length) {
            alert("Please select a file.");
            event.preventDefault();
            return false;
        }
        fetchStatus();  // Start polling when the form is submitted
        showLoader('analyze');
    }
    return true;
}

function fetchStatus() {
    fetch('/setup-status/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    }).then(response => response.json()).then(data => {
        if (data.setup_status) {
            document.getElementById('setup-status').innerText = data.setup_status;
        }
        if (data.setup_status !== "OpenAI Assistant initialized successfully. Running analysis. This will take a while.") {
            setTimeout(fetchStatus, 500); // Poll half a second
        }
    });
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

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data.message);
};

socket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
};

function sendMessage(message) {
    socket.send(JSON.stringify({
        'message': message
    }));
}

