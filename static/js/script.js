// 🔍 SEARCH FUNCTION (FIXED)
function searchItems(inputId, cardClass) {
    let inputEl = document.getElementById(inputId);
    if (!inputEl) return;

    let input = inputEl.value.toLowerCase();
    let cards = document.getElementsByClassName(cardClass);

    for (let i = 0; i < cards.length; i++) {
        let text = cards[i].innerText.toLowerCase();

        if (text.includes(input)) {
            cards[i].style.display = "";   // ✅ FIX (not "block")
        } else {
            cards[i].style.display = "none";
        }
    }
}

// 📊 LOAD CHARTS (SAFE)
function loadCharts() {
    let bar = document.getElementById("barChart");
    let pie = document.getElementById("pieChart");

    if (!bar && !pie) return;

    fetch('/stats')
    .then(res => res.json())
    .then(data => {

        if (bar) {
            new Chart(bar, {
                type: 'bar',
                data: {
                    labels: ['Tasks','Jobs','Materials','Electricians'],
                    datasets: [{
                        label: 'System Data',
                        data: [data.tasks, data.jobs, data.materials, data.electricians]
                    }]
                }
            });
        }

        if (pie) {
            new Chart(pie, {
                type: 'pie',
                data: {
                    labels: ['Tasks','Jobs','Materials','Electricians'],
                    datasets: [{
                        data: [data.tasks, data.jobs, data.materials, data.electricians]
                    }]
                }
            });
        }

    });
}

// 🎯 FILTER TASKS BY STATUS (FIXED FOR GRID)
function filterTasks() {
    let status = document.getElementById("statusFilter").value;
    let cards = document.getElementsByClassName("task-card");

    for (let i = 0; i < cards.length; i++) {
        let cardStatus = cards[i].getAttribute("data-status");

        if (status === "All" || cardStatus === status) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}

// 👷 FILTER ELECTRICIANS (FIXED)
function filterElectricians() {
    let input = document.getElementById("searchElectrician").value.toLowerCase();
    let cards = document.getElementsByClassName("electrician-card");

    for (let i = 0; i < cards.length; i++) {
        let text = cards[i].innerText.toLowerCase();
        cards[i].style.display = text.includes(input) ? "" : "none";
    }
}

// 🚀 RUN AFTER LOAD
window.onload = function () {
    loadCharts();
};