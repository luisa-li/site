document.addEventListener('DOMContentLoaded', function() {
    fetch('portfolio.json')
        .then(response => response.json())
        .then(data => {
            populateSummary(data.summary);
            populateWorkExperience(data.workExperience);
            populateEducation(data.education)
        })
        .catch(error => {
            console.error('Error fetching or parsing JSON:', error);
        });
});

function populateSummary(summary) {
    const summaryContent = document.getElementById('summary');
    summaryContent.textContent = summary;
}

function populateWorkExperience(workExperience) {
    const workExperienceSection = document.getElementById('experience-body');
    const jobsContainer = workExperience.map(job => `
        <div>
            <div class="left-right">
                <h3> ${job.companyName} </h4>
                <p><i> ${job.dates} </i></p>
            </div>
            <div class="left-right">
                <h4> ${job.title} </h4>
                <p><i> ${job.location} </i></p>
            </div>
            <nav class="assets_nav">
                ${parseAssets(job.assets)}
            </nav>
            <ul class="job-description">
                ${job.description.map(desc => `<li>${desc}</li>`).join('')}
            </ul>
        </div>
    `).join('');

    workExperienceSection.innerHTML = jobsContainer;
}

function populateEducation(education) {
    const educationSection = document.getElementById('education-body');
    const educationContainer = education.map(edu => `
        <div>
            <h3>${edu.institution}</h3>
            <h4>${edu.degree}</h4>
            <p><b>Grade: ${edu.grade}</b>, <i>${edu.dates}</i></p>
            ${edu.honors ? `<p><strong>Honors:</strong> ${edu.honors.join(', ')}</p>` : ''}
            ${edu.courses && edu.courses.length > 0 ? `
                <p><strong>Courses:</strong> ${edu.courses.join(', ')}</p>` : ''}
            ${edu.description ? `<p>${edu.description}</p>` : ''}
        </div>
    `).join('');
    educationSection.innerHTML = educationContainer;
}

function parseAssets(assets) {
    let html = '';
    Object.keys(assets).forEach(key => {
        html += `<a href="${assets[key]}" class="asset-link" target="_blank">${key}</a>`;
    });
    return html;
}