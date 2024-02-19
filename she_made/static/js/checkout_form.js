function serializeForm(form) {
    var formData = {};
    // Loop through each form element
    for (var i = 0; i < form.elements.length; i++) {
      var element = form.elements[i];
      // Skip elements without a name
      if (!element.name) continue;
      // Check if element is a select field
      if (element.tagName === 'SELECT') {
        // Get selected option value
        formData[element.name] = element.options[element.selectedIndex].value;
      } else {
        // Otherwise, get input value
        formData[element.name] = element.value;
      }
    }
    return formData;
  }

  // Function to handle form submission
  function submitForm(event) {
    event.preventDefault(); // Prevent default form submission
    var form = event.target; // Get the form element
    var formData = serializeForm(form); // Serialize form data

    // Log the serialized form data
    console.log(formData);

    // Send the form data to Django REST Framework endpoint
    // Replace 'your-api-endpoint-url' with the actual URL of your API endpoint
    fetch('your-api-endpoint-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any additional headers if required
      },
      body: JSON.stringify(formData), // Convert form data to JSON
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      // Handle success response here if needed
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error response here if needed
    });
  }

  // Get the form element
  var form = document.querySelector('form');

  // Add submit event listener to the form
  form.addEventListener('submit', submitForm);