document.addEventListener("DOMContentLoaded", function() {
    fetchDisasterUpdates();

    document.getElementById("update-form").addEventListener("submit", function(e) {
        e.preventDefault();

        const type = document.getElementById("type").value;
        const location = document.getElementById("location").value;
        const details = document.getElementById("details").value;
        const contact = document.getElementById("contact").value;

        const data = { type, location, details, contact };

        fetch('http://127.0.0.1:5000/api/updates', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Update added successfully!");
            fetchDisasterUpdates();  // Refresh the updates list
        })
        .catch(error => console.error('Error:', error));
    });

    function fetchDisasterUpdates() {
        fetch('http://127.0.0.1:5000/api/updates')
            .then(response => response.json())
            .then(data => {
                const updatesList = document.getElementById("updates-list");
                updatesList.innerHTML = "";  // Clear the list first
                
                data.forEach(update => {
                    const li = document.createElement("li");
                    li.innerHTML = `<strong>${update.type}</strong> in ${update.location}: ${update.details} (Contact: ${update.contact})`;
                    updatesList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching updates:', error));
    }

    document.getElementById("contact-form").addEventListener("submit", function(e) {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        const contactData = { name, email, message };

        fetch('http://127.0.0.1:5000/api/contact', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(contactData)
        })
        .then(response => response.json())
        .then(data => alert(data.message || "Message sent successfully!"))
        .catch(error => console.error('Error:', error));
    });
});

function scrollToUpdates() {
    document.getElementById("disaster-updates").scrollIntoView({ behavior: "smooth" });
}
