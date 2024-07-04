document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('signup-form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting traditionally
            
            // Create a FormData object to hold the form data
            const formData = new FormData(this);
            
            // Extract individual form values
            const firstName = formData.get('first_name');
            const lastName = formData.get('last_name');
            const username = formData.get('username');
            const email = formData.get('email');
            const password = formData.get('password');
            
            // Prepare the data for the AJAX request
            const requestData = {
                'first_name': firstName,
                'last_name': lastName,
                'username': username,
                'email': email,
                'password': password
            };
            
            // Send the data to the server using AJAX
            fetch('http://127.0.0.1:8000/api/user/', { // Adjust the URL to match your Django backend endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                alert('User created successfully!');
                window.location.href = 'index.html'; // Redirect to index.html
            })
            .catch((error) => {
                console.error('There has been a problem with your fetch operation:', error);
                alert('An error occurred while creating the user.');
            });
        });
    } else {
        console.error('Form element not found');
    }
});
