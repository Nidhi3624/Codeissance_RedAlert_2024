const experts = {
    tech: [
        { name: "Alice Johnson", photo: "alice.jpg", qualifications: "PhD in Computer Science" },
        { name: "Bob Smith", photo: "bob.jpg", qualifications: "20 years experience in Software Engineering" },
        { name: "Michael Brown", photo: "michael.jpg", qualifications: "MSc in AI, Data Scientist" },
        { name: "Jessica Taylor", photo: "jessica.jpg", qualifications: "Expert in Cybersecurity" },
        { name: "Ethan Harris", photo: "ethan.jpg", qualifications: "Software Architect, 15 years in Cloud Computing" }
    ],
    law: [
        { name: "Carol Williams", photo: "carol.jpg", qualifications: "JD, Corporate Law Specialist" },
        { name: "David Brown", photo: "david.jpg", qualifications: "LLM, Intellectual Property Expert" },
        { name: "Sophia Martinez", photo: "sophia.jpg", qualifications: "Family Law Attorney, 10 years experience" },
        { name: "Lucas Thompson", photo: "lucas.jpg", qualifications: "Criminal Law Specialist" },
        { name: "Emma Johnson", photo: "emma.jpg", qualifications: "Environmental Law Expert" }
    ],
    design: [
        { name: "Eve Davis", photo: "eve.jpg", qualifications: "MFA in Graphic Design" },
        { name: "Frank Miller", photo: "frank.jpg", qualifications: "UX Design Lead, 15 years experience" },
        { name: "Olivia Lee", photo: "olivia.jpg", qualifications: "Branding Specialist" },
        { name: "Liam Wilson", photo: "liam.jpg", qualifications: "Product Designer, 10 years in Tech" },
        { name: "Isabella Clark", photo: "isabella.jpg", qualifications: "UI/UX Designer, Adobe Certified" }
    ],
    architecture: [
        { name: "Grace Lee", photo: "grace.jpg", qualifications: "M.Arch, Sustainable Design Specialist" },
        { name: "Henry Wilson", photo: "henry.jpg", qualifications: "AIA, 25 years in Urban Planning" },
        { name: "Charlotte Young", photo: "charlotte.jpg", qualifications: "Landscape Architect" },
        { name: "James Hall", photo: "james.jpg", qualifications: "Architectural Designer, 15 years experience" },
        { name: "Amelia King", photo: "amelia.jpg", qualifications: "Historic Preservation Specialist" }
    ]
};

const categorySelect = document.getElementById('categorySelect');
const expertCardsContainer = document.getElementById('expertCards');
const appointmentForm = document.getElementById('appointmentForm');
const expertNameSpan = document.getElementById('expertName');
const confirmAppointmentButton = document.getElementById('confirmAppointment');
const confirmationDiv = document.getElementById('confirmation');
const cancelAppointmentButton = document.getElementById('cancelAppointment');

categorySelect.addEventListener('change', (e) => {
    const selectedCategory = e.target.value;
    expertCardsContainer.innerHTML = '';

    if (selectedCategory) {
        experts[selectedCategory].forEach(expert => {
            const card = document.createElement('div');
            card.className = 'expert-card';
            card.innerHTML = `
                <h4>${expert.name}</h4>
                <p>${expert.qualifications}</p>
                <button onclick="bookAppointment('${expert.name}')">Book Appointment</button>
            `;
            expertCardsContainer.appendChild(card);
        });
    }
});

function bookAppointment(expertName) {
    expertNameSpan.textContent = expertName;
    appointmentForm.classList.remove('hidden');
}

confirmAppointmentButton.onclick = function() {
    const appointmentDate = document.getElementById('appointmentDate').value;
    const appointmentTime = document.getElementById('appointmentTime').value;

    if (appointmentDate && appointmentTime) {
        const appointment = {
            expertName: expertNameSpan.textContent,
            date: appointmentDate,
            time: appointmentTime
        };

        // Store appointment in localStorage
        let appointments = JSON.parse(localStorage.getItem('appointments')) || [];
        appointments.push(appointment);
        localStorage.setItem('appointments', JSON.stringify(appointments));

        appointmentForm.classList.add('hidden');
        confirmationDiv.classList.remove('hidden');
    } else {
        alert('Please select a date and time.');
    }
};

cancelAppointmentButton.onclick = function() {
    confirmationDiv.classList.add('hidden');
    appointmentForm.classList.remove('hidden');
};

// Profile button to redirect to user profile page
document.getElementById('profileButton').onclick = function() {
    window.location.href ="{% url 'mentor_userProfile' %}";
};
