/* =========================================================
   FACILITY AI
   JAVASCRIPT ENGINE
========================================================= */


/* =========================================================
   CHART DEFAULTS
========================================================= */

Chart.defaults.font.family = "Inter";

Chart.defaults.font.size = 9;

Chart.defaults.color = "#637b90";

Chart.defaults.borderColor =
    "rgba(120,160,190,.07)";


/* =========================================================
   BUILDING DATA
========================================================= */

const buildingData = {

    ALL: {
        name: "All Buildings",
        energy: 12.22,
        power: 8.64,
        alerts: 7
    },

    A: {
        name: "Building A",
        energy: 9.99,
        power: 7.42,
        alerts: 3
    },

    B: {
        name: "Building B",
        energy: 9.86,
        power: 6.91,
        alerts: 2
    },

    C: {
        name: "Building C",
        energy: 9.61,
        power: 6.48,
        alerts: 2
    }

};


let selectedBuilding = "ALL";


/* =========================================================
   BUILDING SELECTOR
========================================================= */

const buildingSelector =
    document.getElementById(
        "buildingSelector"
    );


const buildingCards =
    document.querySelectorAll(
        ".building-card"
    );


const selectedBuildingText =
    document.getElementById(
        "selectedBuilding"
    );


function updateBuilding(building) {

    selectedBuilding =
        building;

    const data =
        buildingData[building];


    if (!data) return;


    /* Update selector */

    buildingSelector.value =
        building;


    /* Update header */

    selectedBuildingText.textContent =
        data.name;


    /* Update KPI */

    document.getElementById(
        "energyValue"
    ).textContent =
        data.energy.toFixed(2);


    document.getElementById(
        "powerValue"
    ).textContent =
        data.power.toFixed(2);


    document.getElementById(
        "alertValue"
    ).textContent =
        data.alerts;


    /* Active building */

    buildingCards.forEach(card => {

        card.classList.remove(
            "active"
        );


        if (
            card.dataset.building ===
            building
        ) {

            card.classList.add(
                "active"
            );

        }

    });

}


buildingSelector.addEventListener(
    "change",
    function () {

        updateBuilding(
            this.value
        );

    }
);


buildingCards.forEach(card => {

    card.addEventListener(
        "click",
        function () {

            updateBuilding(
                this.dataset.building
            );

        }
    );

});


/* =========================================================
   ENERGY DATA
========================================================= */

const labels = [
    "00:00",
    "02:00",
    "04:00",
    "06:00",
    "08:00",
    "10:00",
    "12:00",
    "14:00",
    "16:00",
    "18:00",
    "20:00",
    "22:00"
];


let energyValues = [
    7.8,
    7.2,
    6.9,
    8.4,
    11.3,
    13.1,
    14.2,
    13.6,
    12.8,
    14.9,
    13.4,
    11.8
];


const averageValues = [
    8.1,
    8.0,
    7.9,
    8.4,
    9.7,
    11.2,
    12.4,
    12.8,
    12.5,
    12.3,
    11.8,
    10.9
];


/* =========================================================
   ENERGY CHART
========================================================= */

const energyChart =
    new Chart(
        document.getElementById(
            "energyChart"
        ),
        {

            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Current",

                        data: energyValues,

                        borderColor:
                            "#4197ff",

                        backgroundColor:
                            "rgba(65,151,255,.08)",

                        fill: true,

                        tension: .4,

                        borderWidth: 2,

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#4197ff"
                    },

                    {
                        label: "Average",

                        data: averageValues,

                        borderColor:
                            "#00d6cb",

                        borderDash:
                            [5,5],

                        borderWidth: 1.5,

                        pointRadius: 0,

                        tension: .4
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {

                    mode: "index",

                    intersect: false

                },

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        }

                    },

                    y: {

                        grid: {

                            color:
                                "rgba(100,150,190,.06)"

                        },

                        ticks: {

                            callback:
                                value =>
                                    value +
                                    " kWh"

                        }

                    }

                }

            }

        }
    );


/* =========================================================
   SOURCE DONUT
========================================================= */

new Chart(

    document.getElementById(
        "sourceChart"
    ),

    {

        type: "doughnut",

        data: {

            labels: [
                "Renewable",
                "Grid",
                "Backup"
            ],

            datasets: [

                {
                    data: [
                        48,
                        32,
                        20
                    ],

                    backgroundColor: [
                        "#42dda0",
                        "#4896ff",
                        "#987fff"
                    ],

                    borderWidth: 0,

                    hoverOffset: 6

                }

            ]

        },

        options: {

            cutout: "72%",

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    }

);


/* =========================================================
   DEMAND CHART
========================================================= */

new Chart(

    document.getElementById(
        "demandChart"
    ),

    {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Power Demand",

                    data: [
                        5.1,
                        4.8,
                        5.2,
                        7.4,
                        10.8,
                        14.3,
                        16.2,
                        15.1,
                        13.7,
                        17.8,
                        15.3,
                        10.2
                    ],

                    borderColor:
                        "#ff5870",

                    backgroundColor:
                        "rgba(255,88,112,.07)",

                    fill: true,

                    tension: .4,

                    borderWidth: 2,

                    pointRadius: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }

            },

            scales: {

                x: {
                    grid: {
                        display: false
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback:
                            value =>
                                value +
                                " kW"

                    }

                }

            }

        }

    }

);


/* =========================================================
   SECTOR CHART
========================================================= */

new Chart(

    document.getElementById(
        "sectorChart"
    ),

    {

        type: "bar",

        data: {

            labels: [
                "HVAC",
                "Industry",
                "Private",
                "Traffic"
            ],

            datasets: [

                {

                    data: [
                        35,
                        30,
                        20,
                        15
                    ],

                    backgroundColor: [
                        "#00cfff",
                        "#4c96ff",
                        "#8876ff",
                        "#40dda0"
                    ],

                    borderRadius: 6,

                    borderSkipped: false

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }

            },

            scales: {

                x: {

                    grid: {
                        display: false
                    }

                },

                y: {

                    beginAtZero: true,

                    max: 40,

                    ticks: {

                        callback:
                            value =>
                                value +
                                "%"

                    }

                }

            }

        }

    }

);


/* =========================================================
   HEALTH DONUT
========================================================= */

new Chart(

    document.getElementById(
        "healthChart"
    ),

    {

        type: "doughnut",

        data: {

            labels: [
                "Critical",
                "Warning",
                "Normal",
                "Healthy"
            ],

            datasets: [

                {

                    data: [
                        209,
                        464,
                        317,
                        10
                    ],

                    backgroundColor: [
                        "#ff526d",
                        "#ffb44d",
                        "#4b96ff",
                        "#40dfa0"
                    ],

                    borderWidth: 0,

                    hoverOffset: 7

                }

            ]

        },

        options: {

            cutout: "68%",

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    }

);


/* =========================================================
   SCROLL REVEAL
========================================================= */

const revealElements =
    document.querySelectorAll(
        ".reveal"
    );


const revealObserver =
    new IntersectionObserver(

        entries => {

            entries.forEach(
                entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "visible"
                        );

                    }

                }
            );

        },

        {

            threshold: .12

        }

    );


revealElements.forEach(
    element => {

        revealObserver.observe(
            element
        );

    }
);


/* =========================================================
   NAVIGATION ACTIVE STATE
========================================================= */

const navLinks =
    document.querySelectorAll(
        ".nav-link"
    );


const sections =
    document.querySelectorAll(
        ".dashboard-section"
    );


window.addEventListener(
    "scroll",
    function () {

        let current = "";


        sections.forEach(
            section => {

                const top =
                    section.offsetTop -
                    220;


                if (
                    window.scrollY >=
                    top
                ) {

                    current =
                        section.id;

                }

            }
        );


        navLinks.forEach(
            link => {

                link.classList.remove(
                    "active"
                );


                if (
                    link.getAttribute(
                        "href"
                    ) ===
                    "#" + current
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            }
        );

    }
);


/* =========================================================
   SMOOTH NAVIGATION
========================================================= */

navLinks.forEach(
    link => {

        link.addEventListener(
            "click",
            function () {

                navLinks.forEach(
                    item =>
                        item.classList.remove(
                            "active"
                        )
                );


                this.classList.add(
                    "active"
                );

            }
        );

    }
);


/* =========================================================
   LIVE TIME
========================================================= */

function updateClock() {

    const now =
        new Date();


    const time =
        now.toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            }
        );


    const updateTime =
        document.getElementById(
            "updateTime"
        );


    const footerTime =
        document.getElementById(
            "footerTime"
        );


    if (updateTime) {

        updateTime.textContent =
            time;

    }


    if (footerTime) {

        footerTime.textContent =
            time;

    }

}


updateClock();

setInterval(
    updateClock,
    1000
);


/* =========================================================
   15 MINUTE AUTO REFRESH
========================================================= */

const REFRESH_SECONDS =
    15 * 60;


let remainingSeconds =
    REFRESH_SECONDS;


let autoRefresh =
    true;


const countdownElement =
    document.getElementById(
        "countdown"
    );


const autoRefreshButton =
    document.getElementById(
        "autoRefreshButton"
    );


const refreshStatus =
    document.getElementById(
        "refreshStatus"
    );


function updateCountdown() {

    if (!countdownElement) {
        return;
    }


    const minutes =
        Math.floor(
            remainingSeconds / 60
        );


    const seconds =
        remainingSeconds % 60;


    countdownElement.textContent =

        String(minutes).padStart(
            2,
            "0"
        )

        +

        ":"

        +

        String(seconds).padStart(
            2,
            "0"
        );

}


function nextReading() {

    /* Generate small realistic variation */

    const variation =
        (Math.random() - .5) * .9;


    const powerVariation =
        (Math.random() - .5) * .5;


    const currentEnergy =
        Math.max(
            5,
            buildingData[
                selectedBuilding
            ].energy + variation
        );


    const currentPower =
        Math.max(
            3,
            buildingData[
                selectedBuilding
            ].power + powerVariation
        );


    document.getElementById(
        "energyValue"
    ).textContent =
        currentEnergy.toFixed(2);


    document.getElementById(
        "powerValue"
    ).textContent =
        currentPower.toFixed(2);


    /* Add new chart point */

    const newValue =
        currentEnergy;


    energyValues.push(
        newValue
    );


    energyValues.shift();


    energyChart.data.datasets[0].data =
        energyValues;


    energyChart.update(
        "none"
    );


    /* Update timestamp */

    updateClock();


    /* Restart countdown */

    remainingSeconds =
        REFRESH_SECONDS;


    updateCountdown();


    /* Visual flash */

    flashDashboard();

}


function flashDashboard() {

    document.body.classList.add(
        "data-refresh"
    );


    setTimeout(
        () => {

            document.body.classList.remove(
                "data-refresh"
            );

        },
        600
    );

}


/* =========================================================
   COUNTDOWN TIMER
========================================================= */

setInterval(
    () => {

        if (!autoRefresh) {
            return;
        }


        remainingSeconds--;


        if (
            remainingSeconds <= 0
        ) {

            nextReading();

        }


        updateCountdown();

    },
    1000
);


/* =========================================================
   NEXT READING BUTTON
========================================================= */

document
    .getElementById(
        "nextReading"
    )
    .addEventListener(
        "click",
        () => {

            nextReading();

        }
    );


/* =========================================================
   RESET MONITORING
========================================================= */

document
    .getElementById(
        "resetMonitoring"
    )
    .addEventListener(
        "click",
        () => {

            remainingSeconds =
                REFRESH_SECONDS;


            updateBuilding(
                selectedBuilding
            );


            energyValues = [
                7.8,
                7.2,
                6.9,
                8.4,
                11.3,
                13.1,
                14.2,
                13.6,
                12.8,
                14.9,
                13.4,
                11.8
            ];


            energyChart.data.datasets[0].data =
                energyValues;


            energyChart.update();


            updateCountdown();


            flashDashboard();

        }
    );


/* =========================================================
   AUTO REFRESH TOGGLE
========================================================= */

autoRefreshButton.addEventListener(
    "click",
    () => {

        autoRefresh =
            !autoRefresh;


        if (autoRefresh) {

            autoRefreshButton.textContent =
                "⏱ Auto Refresh: ON";


            autoRefreshButton.classList.remove(
                "auto-off"
            );


            refreshStatus.textContent =
                "Auto Refresh ON";

        }

        else {

            autoRefreshButton.textContent =
                "⏸ Auto Refresh: OFF";


            autoRefreshButton.classList.add(
                "auto-off"
            );


            refreshStatus.textContent =
                "Auto Refresh OFF";

        }

    }
);


/* =========================================================
   BUTTON RIPPLE EFFECT
========================================================= */

document
    .querySelectorAll(
        "button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                function () {

                    this.classList.add(
                        "clicked"
                    );


                    setTimeout(
                        () => {

                            this.classList.remove(
                                "clicked"
                            );

                        },
                        250
                    );

                }
            );

        }
    );


/* =========================================================
   INITIALIZATION
========================================================= */

updateBuilding(
    "ALL"
);

updateCountdown();


/* =========================================================
   CONSOLE
========================================================= */

console.log(
    "%c Facility AI ",
    "background:#061d2d;color:#00d9ff;padding:8px;font-weight:bold"
);

console.log(
    "Energy Agent: ONLINE"
);

console.log(
    "Predictive Maintenance Agent: ONLINE"
);

console.log(
    "Live Monitoring: ACTIVE"
);

console.log(
    "15-Minute Auto Refresh: ENABLED"
);