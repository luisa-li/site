document.addEventListener('DOMContentLoaded', function() {
    fetch('portfolio/info.json')
        .then(response => response.json())
        .then(data => {
            populateSummary(data.summary);
            populateWorkExperience(data.workExperience);
            populateEducation(data.education)
            populateProjects(data.projects)
        })
        .catch(error => {
            console.error('Error fetching or parsing JSON:', error);
        });
});

function populateSummary(summary) {
    const summaryContent = document.getElementById('summary');
    summaryContent.textContent = summary;
}

function populateEducation(education) {
    const educationSection = document.getElementById('education-body');
    const educationContainer = education.map(edu => `
        <div class="portfolio-section">
            <div>
                <div class="left-right">
                    <h3> ${edu.institution} </h3>
                    <p><i> ${edu.location} </i></p>
                </div>
                <div class="left-right">
                    <h3> ${edu.degree} </h3>
                    <p><i> ${edu.dates} </i></p>
                </div>
                <p><b>Grade: ${edu.grade}</b></p>
            </div>
            <div>
                ${edu.honors ? `<p><strong>Honors:</strong> ${edu.honors.join(', ')}</p>` : ''}
                ${edu.courses && edu.courses.length > 0 ? `
                    <p><strong>Courses:</strong> ${edu.courses.join(', ')}</p>` : ''}
                ${edu.description ? `<p>${edu.description}</p>` : ''}
            </div>
        </div>
    `).join('');
    educationSection.innerHTML = educationContainer;
}

function populateWorkExperience(workExperience) {
    const workExperienceSection = document.getElementById('experience-body');
    const jobsContainer = workExperience.map(job => `
        <div class="portfolio-section">
            <div>
                <div class="left-right">
                    <h3> ${job.companyName} </h3>
                    <p><i> ${job.dates} </i></p>
                </div>
                <div class="left-right">
                    <h4> ${job.title} </h4>
                    <p><i> ${job.location} </i></p>
                </div>
                ${parseAssets(job.assets)}
            </div>
            <ul class="bullets">
                ${job.description.map(desc => `<li>${desc}</li>`).join('')}
            </ul>
        </div>
    `).join('');

    workExperienceSection.innerHTML = jobsContainer;
}

function populateProjects(projects) {
    const projectsSection = document.getElementById('projects-body')
    const educationContainer = projects.map(proj => `
        <div class="portfolio-section">
            <div>
                <div class="left-right">
                    <h3> ${proj.name} </h3>
                    <p><i> ${proj.date} </i></p>
                </div>
                ${parseAssets(proj.assets)}
            </div>
            <ul class="bullets">
                ${proj.description.map(desc => `<li>${desc}</li>`).join('')}
            </ul>
        </div>
    `).join('');
    projectsSection.innerHTML = educationContainer;
}

function parseAssets(assets) {
    let links = [];
    Object.keys(assets).forEach(key => {
        links.push(`<a href="${assets[key]}" target="_blank">${key}</a>`);
    });
    return links.join(', ');
}