// Profile data
const profileData = {
    name: "Abinash Acharya",
    tagline: "Web Developer | Designer | Tech Enthusiast",
    profilePic: "https://via.placeholder.com/150",
    skills: ["JavaScript", "HTML & CSS", "React", "Node.js", "Python"],
    projects: [
        { name: "Interactive Web App", url: "https://example.com/project1" },
        { name: "Mobile Application", url: "https://example.com/project2" },
        { name: "E-Commerce Site", url: "https://example.com/project3" }
    ],
    contact: {
        email: "pupunsteave880@gmail.com",
        linkedin: "https://linkedin.com/in/yourprofile",
        github: "https://github.com/yourusername"
    }
};

// Function to populate the profile page with data
function populateProfile(data) {
    document.getElementById('profile-pic').src = data.profilePic;
    document.getElementById('profile-name').textContent = data.name;
    document.getElementById('profile-tagline').textContent = data.tagline;

    const skillsList = document.getElementById('skills-list');
    data.skills.forEach(skill => {
        const li = document.createElement('li');
        li.textContent = skill;
        skillsList.appendChild(li);
    });

    const projectsList = document.getElementById('projects-list');
    data.projects.forEach(project => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = project.url;
        a.target = '_blank';
        a.textContent = project.name;
        li.appendChild(a);
        projectsList.appendChild(li);
    });

    document.getElementById('contact-email').href = `mailto:${data.contact.email}`;
    document.getElementById('contact-email').textContent = `Email me (${data.contact.email})`;
    document.getElementById('linkedin-profile').href = data.contact.linkedin;
    document.getElementById('github-profile').href = data.contact.github;
}

// Populate profile with sample data
populateProfile(profileData);
// Function to toggle the SMS form popup
function toggleSmsForm() {
const popup = document.getElementById('sms-popup');
popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';
}

// Function to toggle the Mail form popup
function toggleMailForm() {
const popup = document.getElementById('mail-popup');
popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';
}

// Function to close any popup
function closePopup(popupId) {
const popup = document.getElementById(popupId);
popup.style.display = 'none';
}

// Example function for scrapping Google Search (you need to implement this)
function scrapGoogleSearch() {
const popup = document.getElementById('google-search-popup');
popup.style.display = 'flex';
}

// Example function for getting current location (you need to implement this)
function getCurrentLocation() {
const popup = document.getElementById('location-popup');
popup.style.display = 'flex';
}

// Example function for text to speech (you need to implement this)
function textToSpeech() {
const popup = document.getElementById('text-to-speech-popup');
popup.style.display = 'flex';
}

// Example function for sending SMS via phone (you need to implement this)
function sendSMSviaPhone() {
const popup = document.getElementById('send-sms-popup');
popup.style.display = 'flex';
}

// Example function for sending bulk mail (you need to implement this)
function sendBulkMail() {
const popup = document.getElementById('bulk-mail-popup');
popup.style.display = 'flex';
}

function openUploadCropPopup() {
    document.getElementById('upload-crop-popup').style.display = 'block';
}

function openApplyFilterPopup() {
    document.getElementById('apply-filter-popup').style.display = 'block';
}

function openCreateCustomImagePopup() {
    document.getElementById('create-custom-image-popup').style.display = 'block';
}

function openApplyCoolFiltersPopup() {
    document.getElementById('apply-cool-filters-popup').style.display = 'block';
}

function openPredictPopup() {
    document.getElementById('predict-popup').style.display = 'block';
}

// Function to send SMS via Twilio API
function sendTextSMS() {
    const accountSid = document.getElementById('account-sid').value;
    const authToken = document.getElementById('auth-token').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const fromPhoneNumber = document.getElementById('from-phone-number').value; // Add this line
    const message = document.getElementById('sms-message').value;

    if (accountSid && authToken && phoneNumber && fromPhoneNumber && message) { // Include new field in validation
        fetch('http://localhost:5000/send_text_sms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                account_sid: accountSid,
                auth_token: authToken,
                to: phoneNumber,
                from: fromPhoneNumber, // Include this in the request body
                body: message
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('SMS sent successfully!');
                document.getElementById('sms-form-content').reset();
                toggleSmsForm();
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    } else {
        alert('Please fill out all fields.');
    }
}

// Send Mail
function sendEmail() {
    const senderEmail = document.getElementById('sender-email').value;
    const senderPassword = document.getElementById('sender-password').value;
    const recipientEmail = document.getElementById('recipient-email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('mail-message').value;

    if (senderEmail && senderPassword && recipientEmail && subject && message) {
        fetch('http://localhost:5000/send_mail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender_email: senderEmail,
                sender_password: senderPassword,
                recipient_email: recipientEmail,
                subject: subject,
                message: message
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Email sent successfully!');
                document.getElementById('mail-form-content').reset();
                toggleMailForm();
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    } else {
        alert('Please fill out all fields.');
    }
}
// Function to open the popup
function openPopup(popupId) {
    document.getElementById(popupId).style.display = 'flex';
}

// Function to close the popup
function closePopup(popupId) {
    document.getElementById(popupId).style.display = 'none';
}

function googleQuery(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    const query = document.getElementById('google-query').value.trim();
    const numResults = parseInt(document.getElementById('num-results').value) || 5;
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsContainer = document.getElementById('google-results');

    if (query) {
        // Show the loading indicator
        loadingIndicator.style.display = 'block';
        resultsContainer.innerHTML = ''; // Clear any previous results

        fetch('http://localhost:5000/google_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query, num_results: numResults }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.message || `HTTP error! Status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.results && data.results.length > 0) {
                resultsContainer.innerHTML = data.results.map(result => 
                    `<p><a href="${result}" target="_blank">${result}</a></p>`
                ).join('');
            } else {
                resultsContainer.innerHTML = '<p>No results found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            // Hide the loading indicator after the request completes
            loadingIndicator.style.display = 'none';
        });
    } else {
        alert('Please enter a search query.');
    }
}

function getCurrentLocation() {
    const popup = document.getElementById('location-popup');
    popup.style.display = 'flex'; // Show the popup

    fetch('http://localhost:5000/get_location')
        .then(response => {
            if (!response.ok) {
                // Handle HTTP errors
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Parse JSON if response is OK
        })
        .then(data => {
            // Update the result element with location data
            document.getElementById('location-result').innerHTML = `
                <strong>Location Info:</strong><br>
                <strong>City:</strong> ${data.location}<br>
                <strong>Latitude:</strong> ${data.latitude}<br>
                <strong>Longitude:</strong> ${data.longitude}<br>
                <strong>Formatted Location:</strong> ${data.formatted_location}
            `;
        })
        .catch(error => {
            // Handle errors from fetch or parsing
            console.error('Error fetching location data:', error);
            alert('Error fetching location data: ' + error.message);
            document.getElementById('location-result').innerText = 'Error fetching location data.';
        });
}

function closePopup(popupId) {
    const popup = document.getElementById(popupId);
    popup.style.display = 'none';
}
// Handle the Text-to-Speech form submission
function handleTextToSpeech(event) {
    event.preventDefault(); // Prevent the default form submission

    const text = document.getElementById('text-to-speech-input').value;

    if (text) {
        // Show loading indicator (optional)
        document.getElementById('loading-indicator').style.display = 'block';

        fetch('http://localhost:5000/text_to_speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.blob(); // Get the response as a Blob
        })
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.play();

            // Hide loading indicator (optional)
            document.getElementById('loading-indicator').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);

            // Hide loading indicator in case of error (optional)
            document.getElementById('loading-indicator').style.display = 'none';
        });
    } else {
        alert('Please enter text to convert to speech.');
    }
}


// Handle the Send SMS form submission
// Handle the Send Bulk Mail form submission
document.getElementById('bulk-mail-form').onsubmit = function(e) {
    e.preventDefault();
    
    const senderEmail = document.getElementById('bulk-mail-sender-email').value;
    const senderPassword = document.getElementById('bulk-mail-sender-password').value;
    const recipientList = document.getElementById('bulk-mail-recipient-emails').value.split(',').map(email => email.trim());
    const subject = document.getElementById('bulk-mail-subject').value;
    const message = document.getElementById('bulk-mail-message').value;

    if (!senderEmail || !senderPassword || recipientList.length === 0 || !subject || !message) {
        alert("Please fill in all fields.");
        return;
    }

    // Disable the submit button to prevent multiple submissions
    const submitButton = document.querySelector('#bulk-mail-form button[type="submit"]');
    submitButton.disabled = true;

    fetch('http://localhost:5000/send_bulk_mail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sender_email: senderEmail,
            sender_password: senderPassword,
            recipient_list: recipientList,  // Change to recipient_list
            subject: subject,
            body: message  // Ensure key names match Flask
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Bulk mail status:', data.status);
        alert('Bulk emails sent successfully!');
        closePopup('bulk-mail-popup');  // Close the popup only after successful response
    })
    .catch(error => {
        console.error('Error sending bulk mail:', error);
        alert('Error sending bulk mail: ' + error.message);
    })
    .finally(() => {
        // Re-enable the submit button after request completion
        submitButton.disabled = false;
    });
};


// Function to close any popup
function closePopup(popupId) {
    const popup = document.getElementById(popupId);
    popup.style.display = 'none';
}


function openVolumeControlPopup() {
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}


// Function to handle image upload and crop face
function handleImageUpload() {
    const file = document.getElementById('imageInput').files[0];  // Assuming an input element with id="imageInput"
    
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('http://localhost:5000/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Image uploaded and face cropped:', data);
            alert('Image uploaded and face cropped successfully');
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            alert('Error uploading image');
        });
    }
}

// Function to handle applying filter to an image
function handleApplyFilter() {
    const file = document.getElementById('filterImageInput').files[0];  // Assuming an input element with id="filterImageInput"
    
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('http://localhost:5000/apply_filter', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Filter applied:', data);
            alert('Filter applied successfully');
        })
        .catch(error => {
            console.error('Error applying filter:', error);
            alert('Error applying filter');
        });
    }
}

// Function to handle creating a custom image
function handleCreateCustomImage() {
    fetch('http://localhost:5000/create_custom_image', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Custom image created:', data);
        alert('Custom image created successfully');
    })
    .catch(error => {
        console.error('Error creating custom image:', error);
        alert('Error creating custom image');
    });
}

// Function to handle applying cool filters to an image
function handleApplyCoolFilters() {
    const file = document.getElementById('coolFilterImageInput').files[0];  // Assuming an input element with id="coolFilterImageInput"
    
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('http://localhost:5000/apply_cool_filters', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Cool filters applied:', data);
            alert('Cool filters applied successfully');
        })
        .catch(error => {
            console.error('Error applying cool filters:', error);
            alert('Error applying cool filters');
        });
    }
}

// Function to handle prediction
function handlePrediction() {
    const inputData = document.getElementById('predictInputData').value.split(',').map(Number);  // Assuming a textarea with id="inputData"
    
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: inputData })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Prediction:', data);
        alert(`Prediction result: ${data.prediction}`);
    })
    .catch(error => {
        console.error('Error making prediction:', error);
        alert('Error making prediction');
    });
}

