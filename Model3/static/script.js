let selectedModel = '';

function loadContent(page) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', page, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('contentArea').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

function selectModel(model) {
    selectedModel = model;
    document.getElementById('model-title').innerText = `Predict using ${model.toUpperCase()}`;
    document.getElementById('prediction-form').style.display = 'block';
    document.getElementById('result').innerHTML = '';

    // Debugging line
    console.log(`Model selected: ${model}`);
}

document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    if (!selectedModel) {
        alert('Please select a model first.');
        return;
    }

    const emissions = document.getElementById('emissions').value;
    const cost = document.getElementById('cost').value;

    if (!emissions || !cost || isNaN(emissions) || isNaN(cost)) {
        document.getElementById('result').innerText = 'Please provide valid emissions and cost values.';
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: selectedModel,
            emissions: parseFloat(emissions),
            cost: parseFloat(cost)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        } else {
            document.getElementById('result').innerText = `The best strategy to follow is ${data.best_strategy}. Predicted Effectiveness: ${data.best_effectiveness.toFixed(2)} tonnes neutralized.`;
        }
    })
    .catch(error => {
        console.error('Error during prediction request:', error);
        document.getElementById('result').innerText = 'An error occurred while fetching prediction data. Please try again.';
    });
});
