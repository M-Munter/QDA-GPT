function showLoader(type) {
    console.log("[DEBUG] showLoader called with type:", type);
    if (type === 'analyze') {
        document.getElementById("analyze-loader").style.display = "block";
        document.getElementById("analysis-status").style.display = "none";
    }
    setTimeout(function(){
        if (type === 'analyze') {
            document.getElementById("analyze-loader").style.display = "none";
            document.getElementById("analysis-status").style.display = "block";
        }
    }, 5000);
}

function selectAnalysisType(type) {
    console.log("[DEBUG] selectAnalysisType called with type:", type);
    document.getElementById('analysis_type').value = type;
    document.getElementById('analysis_type_hidden').value = type;
    var buttons = document.querySelectorAll('.analysis-button');
    buttons.forEach(function(button) {
        button.classList.remove('active-button');
    });
    document.getElementById(type + '-button').classList.add('active-button');
    document.getElementById('selected-analysis-type').innerText = 'Selected analysis type: ' + type.charAt(0).toUpperCase() + type.slice(1) + ' Analysis';
}

function handleSubmit(event) {
    console.log("[DEBUG] handleSubmit called");
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
    console.log("[DEBUG] fetchStatus called");
    fetch('{% url "setup_status" %}', {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => response.json()).then(data => {
        if (data.setup_status) {
            document.getElementById('setup-status').innerText = data.setup_status;
            console.log("[DEBUG] Fetched setup_status:", data.setup_status);  // Debugging console log
        }
        if (data.setup_status !== "OpenAI Assistant initialized successfully. Sending messages to the Assistant.") {
            setTimeout(fetchStatus, 500); // Poll half a second
        }
    });
}

function clearSessionData() {
    console.log("[DEBUG] clearSessionData called");
    fetch('{% url "clear_session" %}', {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            console.log("[DEBUG] clearSessionData response received");
            window.location.href = "{% url 'dashboard' %}"; // Redirect to dashboard without reloading the current state
        } else {
            console.error("[DEBUG] Failed to clear session data");
        }
    }).catch(error => {
        console.error("[DEBUG] clearSessionData error:", error);
    });
}

function downloadCSV() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const fileName = `qda_${year}_${month}_${day}_${hours}${minutes}.csv`;

    const url = `/download_csv/?file_name=${fileName}`;
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
        .catch(error => console.error('Error downloading CSV:', error));
}



