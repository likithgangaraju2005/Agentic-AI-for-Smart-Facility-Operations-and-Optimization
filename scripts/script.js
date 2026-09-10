/* =========================================================
   SMART FACILITY INTELLIGENCE
   JAVASCRIPT ENGINE
   ---------------------------------------------------------
   ENERGY AGENT
   PREDICTIVE MAINTENANCE AGENT
   OCCUPANCY AGENT
   LOGIN + ROLE BASED ACCESS
========================================================= */


/* =========================================================
   1. GLOBAL SETTINGS
========================================================= */

const REFRESH_SECONDS = 15 * 60;

let remainingSeconds = REFRESH_SECONDS;

let autoRefresh = true;

let selectedBuilding = "ALL";

let currentUser = null;

let currentRole = null;

let dashboardInitialized = false;


/* =========================================================
   2. DEMO LOGIN USERS
========================================================= */

const users = {

    EMP001: {
        password: "emp123",
        role: "Employee",
        name: "Employee User"
    },

    TECH001: {
        password: "tech123",
        role: "Technician",
        name: "Maintenance Technician"
    },

    ENERGY001: {
        password: "energy123",
        role: "Energy Manager",
        name: "Energy Manager"
    },

    MANAGER001: {
        password: "manager123",
        role: "Facility Manager",
        name: "Facility Manager"
    },

    ADMIN001: {
        password: "admin123",
        role: "Administrator",
        name: "System Administrator"
    }

};


/* =========================================================
   3. BUILDING DATA
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


/* =========================================================
   4. OCCUPANCY DATA
========================================================= */

const occupancyData = {

    ALL: {
        averageOccupancy: 3.97,
        utilization: 20.01,
        maxOccupancy: 43,
        overcrowded: 12,
        availableSpaces: 84.16,
        peakHour: "11:00",
        peakOccupancy: 9.45,
        forecastPeak: 53.72,
        forecastUtilization: 62.08
    },

    A: {
        averageOccupancy: 3.79,
        utilization: 19.99,
        maxOccupancy: 36,
        overcrowded: 4,
        availableSpaces: 78.04,
        peakHour: "11:00",
        peakOccupancy: 9.45,
        forecastPeak: 13.50,
        forecastUtilization: 59.09
    },

    B: {
        averageOccupancy: 3.78,
        utilization: 19.78,
        maxOccupancy: 42,
        overcrowded: 5,
        availableSpaces: 82.12,
        peakHour: "11:00",
        peakOccupancy: 9.45,
        forecastPeak: 13.25,
        forecastUtilization: 62.50
    },

    C: {
        averageOccupancy: 4.34,
        utilization: 20.25,
        maxOccupancy: 43,
        overcrowded: 3,
        availableSpaces: 92.32,
        peakHour: "11:00",
        peakOccupancy: 9.45,
        forecastPeak: 39.00,
        forecastUtilization: 97.50
    }

};


/* =========================================================
   5. OCCUPANCY HOURLY DATA
========================================================= */

const occupancyHours = [
    "00:00",
    "01:00",
    "02:00",
    "03:00",
    "04:00",
    "05:00",
    "06:00",
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00"
];

const occupancyHourlyValues = [
    0.63,
    1.40,
    1.28,
    1.43,
    1.10,
    1.55,
    1.10,
    1.33,
    4.48,
    8.77,
    9.11,
    9.45,
    6.23,
    8.43,
    7.95,
    8.66,
    8.30,
    3.66,
    0.90,
    0.93,
    1.45,
    1.30,
    1.03,
    1.20
];


/* =========================================================
   6. DAY-WISE OCCUPANCY
========================================================= */

const occupancyDays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];

const occupancyDayValues = [
    4.78,
    4.57,
    4.45,
    5.02,
    4.49,
    1.11,
    0.92
];


/* =========================================================
   7. FORECAST DATA
========================================================= */

const forecastLabels = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00"
];

const forecastValues = [
    5.2,
    8.4,
    10.7,
    12.9,
    18.6,
    53.72,
    21.4,
    18.9,
    14.7,
    8.3,
    4.2,
    2.7
];


/* =========================================================
   8. CHART VARIABLES
========================================================= */

let energyChart = null;

let sourceChart = null;

let demandChart = null;

let sectorChart = null;

let healthChart = null;

let occupancyChart = null;

let occupancyDayChart = null;

let occupancyForecastChart = null;


/* =========================================================
   9. DOM HELPER
========================================================= */

function getElement(id) {

    return document.getElementById(id);

}


/* =========================================================
   10. SAFE TEXT UPDATE
========================================================= */

function setText(id, value) {

    const element = getElement(id);

    if (element) {

        element.textContent = value;

    }

}


/* =========================================================
   11. LOGIN INITIALIZATION
========================================================= */

function initializeLogin() {

    const loginForm = getElement("loginForm");

    const loginPage = getElement("loginPage");

    const dashboard = getElement("dashboardPage");

    const loginError = getElement("loginError");

    const userId = getElement("userId");

    const password = getElement("password");


    if (!loginForm) {

        showDashboard();

        return;

    }


    /* -----------------------------------------------------
       Initial screen
    ----------------------------------------------------- */

    if (loginPage) {

        loginPage.classList.remove("hidden");

        loginPage.style.display = "flex";

    }


    if (dashboard) {

        dashboard.classList.add("hidden");

        dashboard.style.display = "none";

    }


    /* -----------------------------------------------------
       Login form
    ----------------------------------------------------- */

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();


        const id = userId
            ? userId.value.trim().toUpperCase()
            : "";

        const pass = password
            ? password.value
            : "";


        const user = users[id];


        if (user && user.password === pass) {

            currentUser = id;

            currentRole = user.role;


            sessionStorage.setItem(
                "facilityUser",
                id
            );

            sessionStorage.setItem(
                "facilityRole",
                user.role
            );


            showLoginSuccess(user);

        }

        else {

            showLoginError();

        }

    });


    /* -----------------------------------------------------
       Input focus animation
    ----------------------------------------------------- */

    [userId, password].forEach(input => {

        if (!input) return;


        input.addEventListener("focus", function () {

            this.parentElement?.classList.add(
                "input-focused"
            );

        });


        input.addEventListener("blur", function () {

            this.parentElement?.classList.remove(
                "input-focused"
            );

        });

    });


    /* -----------------------------------------------------
       Previous session
    ----------------------------------------------------- */

    const savedUser =
        sessionStorage.getItem("facilityUser");

    const savedRole =
        sessionStorage.getItem("facilityRole");


    if (
        savedUser &&
        savedRole &&
        users[savedUser]
    ) {

        currentUser = savedUser;

        currentRole = savedRole;


        setTimeout(() => {

            showDashboard();

        }, 300);

    }

}


/* =========================================================
   12. LOGIN SUCCESS
========================================================= */

function showLoginSuccess(user) {

    const loginPage = getElement("loginPage");

    const dashboard = getElement("dashboardPage");

    const loginCard =
        document.querySelector(".login-card");

    const loginMessage =
        getElement("loginMessage");


    if (loginMessage) {

        loginMessage.textContent =
            "Welcome, " + user.name;

    }


    if (loginCard) {

        loginCard.classList.add("login-success");

    }


    if (loginPage) {

        loginPage.classList.add("login-exit");

    }


    setTimeout(() => {

        if (loginPage) {

            loginPage.classList.add("hidden");

            loginPage.style.display = "none";

        }


        if (dashboard) {

            dashboard.classList.remove("hidden");

            dashboard.style.display = "block";

            dashboard.classList.remove(
                "dashboard-enter"
            );


            void dashboard.offsetWidth;


            dashboard.classList.add(
                "dashboard-enter"
            );

        }


        initializeDashboard();

        applyRoleAccess();

        updateUserInterface();

    }, 700);

}


/* =========================================================
   13. LOGIN ERROR
========================================================= */

function showLoginError() {

    const loginCard =
        document.querySelector(".login-card");

    const loginError =
        getElement("loginError");


    if (loginError) {

        loginError.textContent =
            "Invalid ID or password.";

        loginError.style.display =
            "block";

    }


    if (loginCard) {

        loginCard.classList.remove(
            "login-shake"
        );


        void loginCard.offsetWidth;


        loginCard.classList.add(
            "login-shake"
        );

    }


    setTimeout(() => {

        if (loginError) {

            loginError.style.display =
                "none";

        }

    }, 3000);

}


/* =========================================================
   14. SHOW DASHBOARD
========================================================= */

function showDashboard() {

    const loginPage =
        getElement("loginPage");

    const dashboard =
        getElement("dashboardPage");


    if (loginPage) {

        loginPage.classList.add("hidden");

        loginPage.style.display = "none";

    }


    if (dashboard) {

        dashboard.classList.remove("hidden");

        dashboard.style.display = "block";

        dashboard.classList.add(
            "dashboard-enter"
        );

    }


    initializeDashboard();

    applyRoleAccess();

    updateUserInterface();

}


/* =========================================================
   15. ROLE BASED ACCESS
========================================================= */

function applyRoleAccess() {

    const navLinks =
        document.querySelectorAll(".nav-link");


    if (!navLinks.length) {

        return;

    }


    let allowedSections = [];


    /* -----------------------------------------------------
       Employee
    ----------------------------------------------------- */

    if (currentRole === "Employee") {

        allowedSections = [

            "energy-overview"

        ];

    }


    /* -----------------------------------------------------
       Technician
    ----------------------------------------------------- */

    else if (currentRole === "Technician") {

        allowedSections = [

            "maintenance-decisions",
            "equipment-health",
            "health-distribution",
            "equipment-alerts",
            "maintenance-recommendations"

        ];

    }


    /* -----------------------------------------------------
       Energy Manager
    ----------------------------------------------------- */

    else if (currentRole === "Energy Manager") {

        allowedSections = [

            "energy-overview",
            "energy-distribution",
            "advanced-analytics",
            "energy-anomaly",
            "energy-recommendations"

        ];

    }


    /* -----------------------------------------------------
       Facility Manager
    ----------------------------------------------------- */

    else if (currentRole === "Facility Manager") {

        allowedSections = [

            "energy-overview",
            "energy-distribution",
            "advanced-analytics",
            "energy-anomaly",
            "energy-recommendations",

            "maintenance-decisions",
            "equipment-health",
            "health-distribution",
            "equipment-alerts",
            "maintenance-recommendations",

            "occupancy-overview",
            "space-utilization",
            "overcrowding-detection",
            "workspace-allocation",
            "occupancy-heatmap",
            "occupancy-forecast"

        ];

    }


    /* -----------------------------------------------------
       Administrator
    ----------------------------------------------------- */

    else if (currentRole === "Administrator") {

        allowedSections = [

            "energy-overview",
            "energy-distribution",
            "advanced-analytics",
            "energy-anomaly",
            "energy-recommendations",

            "maintenance-decisions",
            "equipment-health",
            "health-distribution",
            "equipment-alerts",
            "maintenance-recommendations",

            "occupancy-overview",
            "space-utilization",
            "overcrowding-detection",
            "workspace-allocation",
            "occupancy-heatmap",
            "occupancy-forecast"

        ];

    }


    /* -----------------------------------------------------
       Hide all navigation links first
    ----------------------------------------------------- */

    navLinks.forEach(link => {

        link.style.display = "none";

    });


    /* -----------------------------------------------------
       Show permitted navigation links
    ----------------------------------------------------- */

    navLinks.forEach(link => {

        const href =
            link.getAttribute("href");


        if (!href) return;


        const sectionId =
            href.replace("#", "");


        if (
            allowedSections.includes(sectionId)
        ) {

            link.style.display = "";

        }

    });


    /* -----------------------------------------------------
       Dashboard sections
    ----------------------------------------------------- */

    const allSections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    allSections.forEach(section => {

        const id = section.id;


        if (!id) return;


        const isAgentSection =
            id.startsWith("energy-") ||
            id.startsWith("maintenance-") ||
            id.startsWith("occupancy-") ||
            id === "advanced-analytics" ||
            id === "equipment-health" ||
            id === "health-distribution" ||
            id === "equipment-alerts" ||
            id === "space-utilization" ||
            id === "overcrowding-detection" ||
            id === "workspace-allocation";


        if (!isAgentSection) return;


        if (
            allowedSections.includes(id)
        ) {

            section.style.display = "";

        }

        else {

            section.style.display = "none";

        }

    });


    /* -----------------------------------------------------
       Agent headings
    ----------------------------------------------------- */

    const agentTitles =
        document.querySelectorAll(
            ".agent-title"
        );


    agentTitles.forEach(title => {

        const text =
            title.textContent.toLowerCase();


        if (text.includes("energy")) {

            title.style.display =
                (
                    currentRole === "Employee" ||
                    currentRole === "Energy Manager" ||
                    currentRole === "Facility Manager" ||
                    currentRole === "Administrator"
                )
                ? ""
                : "none";

        }


        if (text.includes("maintenance")) {

            title.style.display =
                (
                    currentRole === "Technician" ||
                    currentRole === "Facility Manager" ||
                    currentRole === "Administrator"
                )
                ? ""
                : "none";

        }


        if (text.includes("occupancy")) {

            title.style.display =
                (
                    currentRole === "Facility Manager" ||
                    currentRole === "Administrator"
                )
                ? ""
                : "none";

        }

    });


    /* -----------------------------------------------------
       Activate first visible navigation link
    ----------------------------------------------------- */

    const visibleLinks =
        Array.from(navLinks).filter(link => {

            return link.style.display !== "none";

        });


    navLinks.forEach(link => {

        link.classList.remove("active");

    });


    if (visibleLinks.length) {

        visibleLinks[0].classList.add("active");

    }

}


/* =========================================================
   16. USER INTERFACE
========================================================= */

function updateUserInterface() {

    const user =
        users[currentUser];


    document
        .querySelectorAll("[data-user-role]")
        .forEach(element => {

            element.textContent =
                currentRole || "Guest";

        });


    document
        .querySelectorAll("[data-user-name]")
        .forEach(element => {

            element.textContent =
                user
                    ? user.name
                    : "User";

        });


    setText(
        "currentRole",
        currentRole || "Guest"
    );


    setText(
        "currentUser",
        user
            ? user.name
            : "User"
    );

}


/* =========================================================
   17. LOGOUT
========================================================= */

function initializeLogout() {

    const logoutButtons =
        document.querySelectorAll(
            "#logoutButton, .logout-button"
        );


    logoutButtons.forEach(button => {

        button.addEventListener(
            "click",
            function () {

                sessionStorage.removeItem(
                    "facilityUser"
                );

                sessionStorage.removeItem(
                    "facilityRole"
                );


                currentUser = null;

                currentRole = null;


                const dashboard =
                    getElement("dashboardPage");

                const loginPage =
                    getElement("loginPage");


                if (dashboard) {

                    dashboard.classList.add(
                        "dashboard-exit"
                    );

                }


                setTimeout(() => {

                    if (dashboard) {

                        dashboard.classList.add(
                            "hidden"
                        );

                        dashboard.style.display =
                            "none";

                    }


                    if (loginPage) {

                        loginPage.classList.remove(
                            "hidden"
                        );

                        loginPage.classList.remove(
                            "login-exit"
                        );

                        loginPage.style.display =
                            "flex";

                    }


                    const form =
                        getElement("loginForm");


                    if (form) {

                        form.reset();

                    }

                }, 500);

            }
        );

    });

}


/* =========================================================
   18. DASHBOARD INITIALIZATION
========================================================= */

function initializeDashboard() {

    if (dashboardInitialized) {

        return;

    }


    dashboardInitialized = true;


    initializeBuildingSelector();

    initializeCharts();

    initializeRevealAnimation();

    initializeNavigation();

    initializeClock();

    initializeMonitoring();

    initializeButtons();

    initializeLogout();

    initializeOccupancyControls();

    initializeButtonAnimations();

    initializeCardAnimations();

    initializeParallax();

    initializeSectionGlow();

    generateOccupancyHeatmap();

    updateSystemStatus();

    initializeAIActivity();

    initializeKeyboardShortcuts();

    initializeResponsiveNavigation();

}


/* =========================================================
   19. BUILDING SELECTOR
========================================================= */

function initializeBuildingSelector() {

    const buildingSelector =
        getElement("buildingSelector");


    const buildingCards =
        document.querySelectorAll(
            ".building-card"
        );


    if (buildingSelector) {

        buildingSelector.addEventListener(
            "change",
            function () {

                updateBuilding(
                    this.value
                );

            }
        );

    }


    buildingCards.forEach(card => {

        card.addEventListener(
            "click",
            function () {

                const building =
                    this.dataset.building;


                updateBuilding(
                    building
                );

            }
        );

    });


    updateBuilding("ALL");

}


/* =========================================================
   20. UPDATE BUILDING
========================================================= */

function updateBuilding(building) {

    if (!buildingData[building]) {

        building = "ALL";

    }


    selectedBuilding = building;


    const data =
        buildingData[building];


    const occupancy =
        occupancyData[building];


    const buildingSelector =
        getElement("buildingSelector");


    const selectedBuildingText =
        getElement("selectedBuilding");


    if (buildingSelector) {

        buildingSelector.value =
            building;

    }


    if (selectedBuildingText) {

        selectedBuildingText.textContent =
            data.name;

    }


    /* -----------------------------------------------------
       ENERGY
    ----------------------------------------------------- */

    setText(
        "energyConsumption",
        data.energy.toFixed(2)
    );


    setText(
        "powerDemand",
        data.power.toFixed(2)
    );


    setText(
        "alertValue",
        data.alerts
    );


    /* -----------------------------------------------------
       Occupancy
    ----------------------------------------------------- */

    if (occupancy) {

        setText(
            "occupancyValue",
            occupancy.averageOccupancy.toFixed(2)
        );


        setText(
            "utilizationValue",
            occupancy.utilization.toFixed(2) + "%"
        );


        setText(
            "overcrowdingValue",
            occupancy.overcrowded
        );


        setText(
            "maxOccupancyValue",
            occupancy.maxOccupancy
        );


        setText(
            "availableSpaceValue",
            occupancy.availableSpaces.toFixed(2) + "%"
        );

    }


    /* -----------------------------------------------------
       Active building card
    ----------------------------------------------------- */

    document
        .querySelectorAll(".building-card")
        .forEach(card => {

            card.classList.remove("active");


            if (
                card.dataset.building === building
            ) {

                card.classList.add("active");

            }

        });


    refreshOccupancyModule();

}


/* =========================================================
   21. CHART CHECK
========================================================= */

function chartExists(id) {

    const canvas = getElement(id);


    return (
        canvas &&
        typeof Chart !== "undefined"
    );

}


/* =========================================================
   22. CHART INITIALIZATION
========================================================= */

function initializeCharts() {

    if (typeof Chart === "undefined") {

        console.warn(
            "Chart.js is not loaded."
        );

        return;

    }


    Chart.defaults.font.family = "Inter";

    Chart.defaults.font.size = 9;

    Chart.defaults.color = "#7890a5";


    initializeEnergyChart();

    initializeSourceChart();

    initializeDemandChart();

    initializeSectorChart();

    initializeHealthChart();

    initializeOccupancyChart();

    initializeOccupancyDayChart();

    initializeOccupancyForecastChart();

}


/* =========================================================
   23. ENERGY CHART
========================================================= */

function initializeEnergyChart() {

    if (!chartExists("energyChart")) {

        return;

    }


    energyChart = new Chart(
        getElement("energyChart"),
        {

            type: "line",

            data: {

                labels: [
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
                ],

                datasets: [

                    {

                        label: "Current",

                        data: [
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
                        ],

                        borderColor: "#4197ff",

                        backgroundColor:
                            "rgba(65,151,255,.10)",

                        fill: true,

                        tension: 0.4,

                        borderWidth: 2,

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#41c9ff"

                    },

                    {

                        label: "Average",

                        data: [
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
                        ],

                        borderColor: "#00d6cb",

                        borderDash: [5, 5],

                        borderWidth: 1.5,

                        pointRadius: 0,

                        tension: 0.4

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 900

                },

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

                        beginAtZero: true,

                        grid: {

                            color:
                                "rgba(100,150,190,.06)"

                        },

                        ticks: {

                            callback: value =>
                                value + " kWh"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   24. SOURCE DONUT
========================================================= */

function initializeSourceChart() {

    if (!chartExists("sourceChart")) {

        return;

    }


    sourceChart = new Chart(
        getElement("sourceChart"),
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

                        hoverOffset: 7

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "72%",

                animation: {

                    animateRotate: true,

                    duration: 1200

                },

                plugins: {

                    legend: {

                        display: false

                    }

                }

            }

        }
    );

}


/* =========================================================
   25. POWER DEMAND CHART
========================================================= */

function initializeDemandChart() {

    if (!chartExists("demandChart")) {

        return;

    }


    demandChart = new Chart(
        getElement("demandChart"),
        {

            type: "line",

            data: {

                labels: [
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
                ],

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

                        borderColor: "#ff5870",

                        backgroundColor:
                            "rgba(255,88,112,.07)",

                        fill: true,

                        tension: 0.4,

                        borderWidth: 2,

                        pointRadius: 2

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 900

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

                        beginAtZero: true,

                        ticks: {

                            callback: value =>
                                value + " kW"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   26. ANALYTICS BAR CHART
========================================================= */

function initializeSectorChart() {

    if (!chartExists("sectorChart")) {

        return;

    }


    sectorChart = new Chart(
        getElement("sectorChart"),
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

                animation: {

                    duration: 1100

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

                        beginAtZero: true,

                        max: 40,

                        ticks: {

                            callback: value =>
                                value + "%"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   27. MAINTENANCE HEALTH CHART
========================================================= */

function initializeHealthChart() {

    if (!chartExists("healthChart")) {

        return;

    }


    healthChart = new Chart(
        getElement("healthChart"),
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

                responsive: true,

                maintainAspectRatio: false,

                cutout: "68%",

                animation: {

                    animateRotate: true,

                    duration: 1300

                },

                plugins: {

                    legend: {

                        display: false

                    }

                }

            }

        }
    );

}


/* =========================================================
   28. OCCUPANCY HOURLY CHART
========================================================= */

function initializeOccupancyChart() {

    if (!chartExists("occupancyChart")) {

        return;

    }


    occupancyChart = new Chart(
        getElement("occupancyChart"),
        {

            type: "line",

            data: {

                labels: occupancyHours,

                datasets: [

                    {

                        label: "Average Occupancy",

                        data: occupancyHourlyValues,

                        borderColor: "#00d9ff",

                        backgroundColor:
                            "rgba(0,217,255,.10)",

                        fill: true,

                        tension: 0.42,

                        borderWidth: 2.5,

                        pointRadius: 2,

                        pointBackgroundColor:
                            "#7b61ff"

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 1200

                },

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

                        beginAtZero: true,

                        title: {

                            display: true,

                            text: "People"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   29. OCCUPANCY DAY CHART
========================================================= */

function initializeOccupancyDayChart() {

    if (!chartExists("occupancyDayChart")) {

        return;

    }


    occupancyDayChart = new Chart(
        getElement("occupancyDayChart"),
        {

            type: "bar",

            data: {

                labels: occupancyDays,

                datasets: [

                    {

                        label: "Average Occupancy",

                        data: occupancyDayValues,

                        backgroundColor: [
                            "#00d9ff",
                            "#4197ff",
                            "#6d7cff",
                            "#8b5cf6",
                            "#a855f7",
                            "#4c96ff",
                            "#00bcd4"
                        ],

                        borderRadius: 8,

                        borderSkipped: false

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 1000

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

                        beginAtZero: true,

                        title: {

                            display: true,

                            text: "People"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   30. OCCUPANCY FORECAST CHART
========================================================= */

function initializeOccupancyForecastChart() {

    if (!chartExists("occupancyForecastChart")) {

        return;

    }


    occupancyForecastChart = new Chart(
        getElement("occupancyForecastChart"),
        {

            type: "line",

            data: {

                labels: forecastLabels,

                datasets: [

                    {

                        label: "Predicted Occupancy",

                        data: forecastValues,

                        borderColor: "#9b7cff",

                        backgroundColor:
                            "rgba(155,124,255,.10)",

                        fill: true,

                        tension: 0.4,

                        borderWidth: 2.5,

                        pointRadius: 3,

                        pointBackgroundColor:
                            "#00d9ff"

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 1300

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

                        beginAtZero: true,

                        title: {

                            display: true,

                            text: "Predicted people"

                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   31. UPDATE OCCUPANCY CHARTS
========================================================= */

function updateOccupancyCharts() {

    let multiplier = 1;


    if (selectedBuilding === "A") {

        multiplier = 0.93;

    }

    else if (selectedBuilding === "B") {

        multiplier = 0.95;

    }

    else if (selectedBuilding === "C") {

        multiplier = 1.08;

    }


    if (occupancyChart) {

        occupancyChart.data.datasets[0].data =
            occupancyHourlyValues.map(value => {

                return Number(
                    (value * multiplier).toFixed(2)
                );

            });


        occupancyChart.update("none");

    }


    if (occupancyDayChart) {

        occupancyDayChart.data.datasets[0].data =
            occupancyDayValues.map(value => {

                return Number(
                    (value * multiplier).toFixed(2)
                );

            });


        occupancyDayChart.update("none");

    }


    if (occupancyForecastChart) {

        let forecastMultiplier = 1;


        if (selectedBuilding === "A") {

            forecastMultiplier = 0.75;

        }

        else if (selectedBuilding === "B") {

            forecastMultiplier = 0.72;

        }

        else if (selectedBuilding === "C") {

            forecastMultiplier = 1.05;

        }


        occupancyForecastChart
            .data
            .datasets[0]
            .data =
            forecastValues.map(value => {

                return Number(
                    (
                        value *
                        forecastMultiplier
                    ).toFixed(2)
                );

            });


        occupancyForecastChart.update("none");

    }

}


/* =========================================================
   32. REVEAL ANIMATION
========================================================= */

function initializeRevealAnimation() {

    const elements =
        document.querySelectorAll(".reveal");


    if (
        !("IntersectionObserver" in window)
    ) {

        elements.forEach(element => {

            element.classList.add("visible");

        });

        return;

    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "visible"
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    elements.forEach(element => {

        observer.observe(element);

    });

}


/* =========================================================
   33. NAVIGATION
========================================================= */

function initializeNavigation() {

    const navLinks =
        document.querySelectorAll(".nav-link");


    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    navLinks.forEach(link => {

        link.addEventListener(
            "click",
            function (event) {

                const href =
                    this.getAttribute("href");


                if (
                    !href ||
                    href === "#"
                ) {

                    return;

                }


                const target =
                    document.querySelector(href);


                if (!target) {

                    return;

                }


                event.preventDefault();


                navLinks.forEach(item => {

                    item.classList.remove(
                        "active"
                    );

                });


                this.classList.add("active");


                target.scrollIntoView({

                    behavior: "smooth",

                    block: "start"

                });

            }
        );

    });


    window.addEventListener(
        "scroll",
        function () {

            let current = "";


            sections.forEach(section => {

                if (
                    section.style.display ===
                    "none"
                ) {

                    return;

                }


                const top =
                    section.offsetTop - 230;


                if (
                    window.scrollY >= top
                ) {

                    current =
                        section.id;

                }

            });


            if (!current) return;


            navLinks.forEach(link => {

                link.classList.remove(
                    "active"
                );


                if (
                    link.getAttribute("href") ===
                    "#" + current
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            });

        }
    );

}


/* =========================================================
   34. CLOCK
========================================================= */

function initializeClock() {

    updateClock();


    setInterval(
        updateClock,
        1000
    );

}


function updateClock() {

    const now = new Date();


    const time =
        now.toLocaleTimeString([], {

            hour: "2-digit",

            minute: "2-digit",

            second: "2-digit"

        });


    setText(
        "updateTime",
        time
    );


    setText(
        "footerTime",
        time
    );


    setText(
        "currentTime",
        time
    );

}


/* =========================================================
   35. COUNTDOWN
========================================================= */

function updateCountdown() {

    const countdown =
        getElement("countdown");


    if (!countdown) return;


    const minutes =
        Math.floor(
            remainingSeconds / 60
        );


    const seconds =
        remainingSeconds % 60;


    countdown.textContent =
        String(minutes).padStart(2, "0") +
        ":" +
        String(seconds).padStart(2, "0");

}


/* =========================================================
   36. NEXT READING
========================================================= */

function nextReading() {

    const data =
        buildingData[selectedBuilding];


    if (!data) return;


    const energyVariation =
        (Math.random() - 0.5) * 0.9;


    const powerVariation =
        (Math.random() - 0.5) * 0.5;


    const currentEnergy =
        Math.max(
            5,
            data.energy + energyVariation
        );


    const currentPower =
        Math.max(
            3,
            data.power + powerVariation
        );


    setText(
        "energyConsumption",
        currentEnergy.toFixed(2)
    );


    setText(
        "powerDemand",
        currentPower.toFixed(2)
    );


    setText(
        "flowEnergyValue",
        currentEnergy.toFixed(2) + " kWh"
    );


    setText(
        "flowPowerValue",
        currentPower.toFixed(2) + " kW"
    );


    if (energyChart) {

        const values =
            energyChart
                .data
                .datasets[0]
                .data;


        values.push(
            Number(
                currentEnergy.toFixed(2)
            )
        );


        values.shift();


        energyChart.update("none");

    }


    remainingSeconds =
        REFRESH_SECONDS;


    updateCountdown();

    flashDashboard();

}


/* =========================================================
   37. MONITORING
========================================================= */

function initializeMonitoring() {

    updateCountdown();


    setInterval(() => {

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

    }, 1000);

}


/* =========================================================
   38. MONITORING BUTTONS
========================================================= */

function initializeButtons() {

    const nextButton =
        getElement("nextReading");


    const resetButton =
        getElement("resetMonitoring");


    const autoButton =
        getElement("autoRefreshButton");


    const refreshStatus =
        getElement("refreshStatus");


    if (nextButton) {

        nextButton.addEventListener(
            "click",
            () => {

                nextReading();

            }
        );

    }


    if (resetButton) {

        resetButton.addEventListener(
            "click",
            () => {

                remainingSeconds =
                    REFRESH_SECONDS;


                updateBuilding(
                    selectedBuilding
                );


                updateCountdown();


                flashDashboard();

            }
        );

    }


    if (autoButton) {

        autoButton.addEventListener(
            "click",
            () => {

                autoRefresh =
                    !autoRefresh;


                if (autoRefresh) {

                    autoButton.textContent =
                        "⏱ Auto Refresh: ON";


                    autoButton.classList.remove(
                        "auto-off"
                    );


                    if (refreshStatus) {

                        refreshStatus.textContent =
                            "Auto Refresh ON";

                    }

                }

                else {

                    autoButton.textContent =
                        "⏸ Auto Refresh: OFF";


                    autoButton.classList.add(
                        "auto-off"
                    );


                    if (refreshStatus) {

                        refreshStatus.textContent =
                            "Auto Refresh OFF";

                    }

                }

            }
        );

    }

}


/* =========================================================
   39. FLASH EFFECT
========================================================= */

function flashDashboard() {

    document.body.classList.add(
        "data-refresh"
    );


    setTimeout(() => {

        document.body.classList.remove(
            "data-refresh"
        );

    }, 600);

}


/* =========================================================
   40. OCCUPANCY CONTROLS
========================================================= */

function initializeOccupancyControls() {

    const buttons =
        document.querySelectorAll(
            "[data-occupancy-building]"
        );


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            function () {

                const building =
                    this.dataset
                        .occupancyBuilding;


                if (
                    buildingData[building]
                ) {

                    updateBuilding(
                        building
                    );

                }

            }
        );

    });


    document
        .querySelectorAll(".heatmap-cell")
        .forEach(cell => {

            cell.addEventListener(
                "mouseenter",
                function () {

                    this.classList.add(
                        "heatmap-active"
                    );

                }
            );


            cell.addEventListener(
                "mouseleave",
                function () {

                    this.classList.remove(
                        "heatmap-active"
                    );

                }
            );

        });

}


/* =========================================================
   41. BUTTON ANIMATIONS
========================================================= */

function initializeButtonAnimations() {

    document
        .querySelectorAll("button")
        .forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    this.classList.add(
                        "clicked"
                    );


                    setTimeout(() => {

                        this.classList.remove(
                            "clicked"
                        );

                    }, 300);

                }
            );

        });

}


/* =========================================================
   42. CARD ANIMATIONS
========================================================= */

function initializeCardAnimations() {

    const cards =
        document.querySelectorAll(
            ".metric-card, " +
            ".panel, " +
            ".decision-card, " +
            ".recommendation-card, " +
            ".maintenance-recommendation, " +
            ".equipment-alert, " +
            ".health-category"
        );


    cards.forEach(card => {

        card.addEventListener(
            "mouseenter",
            function () {

                this.classList.add(
                    "card-hover"
                );

            }
        );


        card.addEventListener(
            "mouseleave",
            function () {

                this.classList.remove(
                    "card-hover"
                );

            }
        );

    });

}


/* =========================================================
   43. PARALLAX
========================================================= */

function initializeParallax() {

    const ambient =
        document.querySelectorAll(
            ".ambient"
        );


    if (!ambient.length) {

        return;

    }


    window.addEventListener(
        "scroll",
        () => {

            const scrollY =
                window.scrollY;


            ambient.forEach(
                (element, index) => {

                    const speed =
                        (index + 1) * 0.015;


                    element.style.transform =
                        "translate3d(0," +
                        (scrollY * speed) +
                        "px,0)";

                }
            );

        }
    );

}


/* =========================================================
   44. SECTION GLOW
========================================================= */

function initializeSectionGlow() {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    if (
        !("IntersectionObserver" in window)
    ) {

        return;

    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "section-active"
                        );

                    }

                    else {

                        entry.target.classList.remove(
                            "section-active"
                        );

                    }

                });

            },
            {
                threshold: 0.2
            }
        );


    sections.forEach(section => {

        observer.observe(section);

    });

}


/* =========================================================
   45. OCCUPANCY HEATMAP
========================================================= */

function generateOccupancyHeatmap() {

    const container =
        getElement(
            "occupancyHeatmapGrid"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const days = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ];


    const hours = [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17
    ];


    const values = [

        [18, 25, 31, 38, 26, 35, 29, 32, 27, 19],

        [16, 24, 30, 36, 28, 33, 31, 34, 26, 18],

        [15, 22, 29, 34, 27, 31, 30, 32, 25, 17],

        [19, 27, 34, 40, 31, 37, 36, 38, 30, 21],

        [17, 26, 33, 41, 35, 58, 39, 43, 34, 23],

        [6, 8, 11, 13, 12, 14, 13, 10, 8, 6],

        [4, 6, 8, 10, 8, 9, 8, 7, 5, 4]

    ];


    const empty =
        document.createElement("div");


    empty.className =
        "heatmap-label";


    container.appendChild(
        empty
    );


    hours.forEach(hour => {

        const label =
            document.createElement("div");


        label.className =
            "heatmap-label";


        label.textContent =
            hour + ":00";


        container.appendChild(
            label
        );

    });


    days.forEach(
        (day, dayIndex) => {

            const dayLabel =
                document.createElement(
                    "div"
                );


            dayLabel.className =
                "heatmap-label";


            dayLabel.textContent =
                day;


            container.appendChild(
                dayLabel
            );


            hours.forEach(
                (hour, hourIndex) => {

                    const value =
                        values[
                            dayIndex
                        ][
                            hourIndex
                        ];


                    const cell =
                        document.createElement(
                            "div"
                        );


                    cell.className =
                        "heatmap-cell";


                    cell.dataset.value =
                        value;


                    cell.title =
                        day +
                        " " +
                        hour +
                        ":00 — " +
                        value +
                        "% utilization";


                    cell.style.setProperty(
                        "--heat-value",
                        value
                    );


                    cell.style.opacity =
                        0.35 +
                        (value / 100) * 0.65;


                    cell.addEventListener(
                        "mouseenter",
                        function () {

                            this.style.opacity =
                                "1";

                        }
                    );


                    cell.addEventListener(
                        "mouseleave",
                        function () {

                            this.style.opacity =
                                0.35 +
                                (value / 100) * 0.65;

                        }
                    );


                    container.appendChild(
                        cell
                    );

                }
            );

        }
    );

}


/* =========================================================
   46. OCCUPANCY STATUS
========================================================= */

function getOccupancyStatus(utilization) {

    if (utilization > 120) {

        return {

            label: "Critical",

            priority: "HIGH",

            alert: "CRITICAL OCCUPANCY ALERT"

        };

    }


    if (utilization > 100) {

        return {

            label: "Overcrowded",

            priority: "HIGH",

            alert: "OVERCROWDING ALERT"

        };

    }


    if (utilization >= 80) {

        return {

            label: "High Usage",

            priority: "MEDIUM",

            alert: "HIGH USAGE WARNING"

        };

    }


    if (utilization >= 40) {

        return {

            label: "Normal",

            priority: "LOW",

            alert: "NORMAL OCCUPANCY"

        };

    }


    return {

        label: "Low",

        priority: "LOW",

        alert: "LOW USAGE"

    };

}


/* =========================================================
   47. OCCUPANCY AGENT SUMMARY
========================================================= */

function updateOccupancyAgentSummary() {

    const data =
        occupancyData[selectedBuilding];


    if (!data) return;


    const status =
        getOccupancyStatus(
            data.utilization
        );


    setText(
        "occupancyStatus",
        status.label
    );


    setText(
        "occupancyPriority",
        status.priority
    );


    setText(
        "occupancyAlert",
        status.alert
    );


    setText(
        "peakOccupancyHour",
        data.peakHour
    );


    setText(
        "peakOccupancy",
        data.peakOccupancy.toFixed(2)
    );


    setText(
        "forecastPeakOccupancy",
        data.forecastPeak.toFixed(2)
    );


    setText(
        "forecastUtilization",
        data.forecastUtilization.toFixed(2) +
        "%"
    );

}


/* =========================================================
   48. WORKSPACE ALLOCATION
========================================================= */

function updateWorkspaceAllocation() {

    const allocation = {

        A: {

            recommended: "A102 Office",

            available: 78.04

        },

        B: {

            recommended: "B202 Conference",

            available: 82.12

        },

        C: {

            recommended: "C201 Lab",

            available: 92.32

        },

        ALL: {

            recommended: "C201 Lab",

            available: 84.16

        }

    };


    const data =
        allocation[selectedBuilding];


    if (!data) return;


    setText(
        "recommendedWorkspace",
        data.recommended
    );


    setText(
        "workspaceAvailability",
        data.available.toFixed(2) +
        "%"
    );

}


/* =========================================================
   49. OCCUPANCY MODULE REFRESH
========================================================= */

function refreshOccupancyModule() {

    updateOccupancyCharts();

    updateOccupancyAgentSummary();

    updateWorkspaceAllocation();

}


/* =========================================================
   50. SYSTEM STATUS
========================================================= */

function updateSystemStatus() {

    const elements =
        document.querySelectorAll(
            ".system-online, " +
            ".engine-status, " +
            ".live-indicator"
        );


    elements.forEach(element => {

        element.classList.add(
            "status-pulse"
        );

    });

}


/* =========================================================
   51. AI ACTIVITY
========================================================= */

function initializeAIActivity() {

    const elements =
        document.querySelectorAll(
            ".ai-core, " +
            ".ai-rings, " +
            ".final-ai-glow"
        );


    elements.forEach(element => {

        element.classList.add(
            "ai-active"
        );

    });

}


/* =========================================================
   52. KEYBOARD SHORTCUTS
========================================================= */

function initializeKeyboardShortcuts() {

    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Escape"
            ) {

                document
                    .activeElement
                    ?.blur();

            }

        }
    );

}


/* =========================================================
   53. RESPONSIVE SIDEBAR
========================================================= */

function initializeResponsiveNavigation() {

    const sidebar =
        document.querySelector(
            ".sidebar"
        );


    if (!sidebar) return;


    const menuButton =
        document.querySelector(
            ".mobile-menu-button, " +
            "#mobileMenuButton"
        );


    if (!menuButton) return;


    menuButton.addEventListener(
        "click",
        () => {

            sidebar.classList.toggle(
                "sidebar-open"
            );

        }
    );


    document
        .querySelectorAll(".nav-link")
        .forEach(link => {

            link.addEventListener(
                "click",
                () => {

                    sidebar.classList.remove(
                        "sidebar-open"
                    );

                }
            );

        });

}


/* =========================================================
   54. INITIAL APPLICATION START
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Smart Facility Intelligence loading..."
        );


        initializeLogin();

    }
);


/* =========================================================
   55. CONSOLE STATUS
========================================================= */

console.log(
    "%c SMART FACILITY INTELLIGENCE ",
    "background:#071b3d;color:#00d9ff;padding:10px;font-weight:bold;border-radius:5px"
);

console.log(
    "%c Energy Agent: ONLINE ",
    "color:#00d9ff;font-weight:bold"
);

console.log(
    "%c Predictive Maintenance Agent: ONLINE ",
    "color:#9b7cff;font-weight:bold"
);

console.log(
    "%c Occupancy Agent: ONLINE ",
    "color:#40dda0;font-weight:bold"
);

console.log(
    "%c Facility Intelligence Engine: ACTIVE ",
    "color:#4197ff;font-weight:bold"
);


/* =========================================================
   END OF JAVASCRIPT ENGINE
========================================================= */