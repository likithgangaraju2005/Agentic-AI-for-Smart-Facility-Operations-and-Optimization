/* ================================================================
   SMART FACILITY INTELLIGENCE
   COMPLETE DASHBOARD JAVASCRIPT ENGINE
   ================================================================
   AGENTS
   01 - ENERGY AGENT
   02 - PREDICTIVE MAINTENANCE AGENT
   03 - OCCUPANCY AGENT
   04 - SECURITY AGENT
   05 - COST OPTIMIZATION AGENT

   FEATURES
   - Login
   - Role based access
   - Building selection
   - 50+ dashboard parameters
   - Chart.js dashboards
   - Cost optimization
   - Auto refresh
   - Smooth scrolling
   - Scroll reveal
   - Card animations
   - Parallax
   - Glow effects
   - Animated counters
   - Heatmap
   - Navigation
   - Responsive sidebar
   - Live clock
   - Dashboard transitions
================================================================ */


/* ================================================================
   01. GLOBAL SETTINGS
================================================================ */

const REFRESH_SECONDS = 15 * 60;

let remainingSeconds = REFRESH_SECONDS;

let autoRefresh = true;

let selectedBuilding = "ALL";

let currentUser = null;

let currentRole = null;

let dashboardInitialized = false;

let chartsInitialized = false;


/* ================================================================
   02. CHART REFERENCES
================================================================ */

let energyChart = null;

let sourceChart = null;

let demandChart = null;

let sectorChart = null;

let healthChart = null;

let occupancyChart = null;

let occupancyDayChart = null;

let occupancyForecastChart = null;

let costDistributionChart = null;

let costBuildingChart = null;

let costROIChart = null;

let costHealthChart = null;


/* ================================================================
   03. DEMO LOGIN USERS
================================================================ */

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


/* ================================================================
   04. BUILDING DATA
================================================================ */

const buildingData = {

    ALL: {

        name: "All Buildings",

        energy: 12.22,

        power: 8.64,

        alerts: 7,

        efficiency: 82.6,

        temperature: 24.8,

        humidity: 58.4,

        hvac: 42.8,

        lighting: 24.6,

        water: 31.5,

        anomaly: 3

    },


    A: {

        name: "Building A",

        energy: 9.99,

        power: 7.42,

        alerts: 3,

        efficiency: 83.2,

        temperature: 24.5,

        humidity: 57.8,

        hvac: 41.2,

        lighting: 23.8,

        water: 30.7,

        anomaly: 1

    },


    B: {

        name: "Building B",

        energy: 9.86,

        power: 6.91,

        alerts: 2,

        efficiency: 82.1,

        temperature: 25.1,

        humidity: 59.1,

        hvac: 43.5,

        lighting: 25.2,

        water: 32.4,

        anomaly: 1

    },


    C: {

        name: "Building C",

        energy: 9.61,

        power: 6.48,

        alerts: 2,

        efficiency: 82.5,

        temperature: 24.7,

        humidity: 58.2,

        hvac: 43.7,

        lighting: 24.9,

        water: 31.4,

        anomaly: 1

    }

};


/* ================================================================
   05. OCCUPANCY DATA
================================================================ */

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

        forecastUtilization: 62.08,

        totalCapacity: 1020,

        occupiedMembers: 742,

        availableCapacity: 278,

        meetingRooms: 15,

        underutilizedRooms: 5,

        workspaceAvailability: 84.16

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

        forecastUtilization: 59.09,

        totalCapacity: 340,

        occupiedMembers: 248,

        availableCapacity: 92,

        meetingRooms: 5,

        underutilizedRooms: 2,

        workspaceAvailability: 78.04

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

        forecastUtilization: 62.50,

        totalCapacity: 340,

        occupiedMembers: 251,

        availableCapacity: 89,

        meetingRooms: 5,

        underutilizedRooms: 2,

        workspaceAvailability: 82.12

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

        forecastUtilization: 97.50,

        totalCapacity: 340,

        occupiedMembers: 243,

        availableCapacity: 97,

        meetingRooms: 5,

        underutilizedRooms: 1,

        workspaceAvailability: 92.32

    }

};


/* ================================================================
   06. OCCUPANCY CHART DATA
================================================================ */

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

    4.2,
    4.5,
    4.8,
    5.1,
    5.4,
    2.1,
    1.4

];


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
    "17:00"

];


const forecastValues = [

    18,
    25,
    31,
    38,
    42,
    39,
    44,
    41,
    36,
    28

];


/* ================================================================
   07. MAINTENANCE DATA
================================================================ */

const maintenanceData = {

    ALL: {

        immediate: 189,

        scheduled: 284,

        monitoring: 24,

        healthy: 317,

        decisions: 349,

        critical: 209,

        warning: 464,

        normal: 317,

        healthScore: 78.6,

        alerts: 849,

        anomalies: 73,

        predictionAccuracy: 91.4,

        preventiveActions: 286

    },

    A: {

        immediate: 64,

        scheduled: 96,

        monitoring: 8,

        healthy: 108,

        decisions: 117,

        critical: 67,

        warning: 154,

        normal: 108,

        healthScore: 78.5,

        alerts: 286,

        anomalies: 25,

        predictionAccuracy: 91.7,

        preventiveActions: 94

    },

    B: {

        immediate: 61,

        scheduled: 92,

        monitoring: 8,

        healthy: 105,

        decisions: 113,

        critical: 70,

        warning: 151,

        normal: 105,

        healthScore: 79.0,

        alerts: 281,

        anomalies: 24,

        predictionAccuracy: 91.2,

        preventiveActions: 91

    },

    C: {

        immediate: 64,

        scheduled: 96,

        monitoring: 8,

        healthy: 104,

        decisions: 119,

        critical: 72,

        warning: 159,

        normal: 104,

        healthScore: 79.0,

        alerts: 282,

        anomalies: 24,

        predictionAccuracy: 91.3,

        preventiveActions: 101

    }

};


/* ================================================================
   08. SECURITY DATA
================================================================ */

const securityData = {

    ALL: {

        totalEvents: 2000,

        authorized: 1770,

        unauthorized: 230,

        suspicious: 33,

        incidents: 21,

        cctvCameras: 48,

        cameraOnline: 46,

        cameraOffline: 2,

        avgRiskScore: 1.0,

        accessCompliance: 88.5,

        threatLevel: "LOW",

        securityHealth: 94.2

    },


    A: {

        totalEvents: 670,

        authorized: 594,

        unauthorized: 76,

        suspicious: 11,

        incidents: 7,

        cctvCameras: 16,

        cameraOnline: 15,

        cameraOffline: 1,

        avgRiskScore: 0.98,

        accessCompliance: 88.7,

        threatLevel: "LOW",

        securityHealth: 94.4

    },


    B: {

        totalEvents: 665,

        authorized: 590,

        unauthorized: 75,

        suspicious: 11,

        incidents: 7,

        cctvCameras: 16,

        cameraOnline: 16,

        cameraOffline: 0,

        avgRiskScore: 1.02,

        accessCompliance: 88.7,

        threatLevel: "LOW",

        securityHealth: 94.1

    },


    C: {

        totalEvents: 665,

        authorized: 586,

        unauthorized: 79,

        suspicious: 11,

        incidents: 7,

        cctvCameras: 16,

        cameraOnline: 15,

        cameraOffline: 1,

        avgRiskScore: 1.01,

        accessCompliance: 88.1,

        threatLevel: "LOW",

        securityHealth: 94.0

    }

};


/* ================================================================
   09. COST OPTIMIZATION DATA
================================================================ */

const costOptimizationData = {

    ALL: {

        operationalCost: 18104149.82,

        budget: 19885215.48,

        budgetCompliance: 91.04,

        costReduction: 13.07,

        roi: 36.37,

        facilityHealth: 78.85,

        optimizations: 16078,

        resourceUtilization: 69.98,

        savingsOpportunity: 1909601.91,

        executivePriority: "HIGH",

        energyCost: 8315200,

        maintenanceCost: 4172000,

        securityCost: 2586000,

        administrativeCost: 3030949.82,

        investment: 12309925.21,

        vendorUtilization: 68.74,

        costEfficiency: 86.93,

        recommendations: [

            "Reduce energy consumption",

            "Optimize workspace and resource allocation",

            "Optimize security resource allocation",

            "Implement identified savings opportunities"

        ]

    },


    A: {

        operationalCost: 6178297.67,

        budget: 6795870.15,

        budgetCompliance: 90.91,

        costReduction: 13.19,

        roi: 36.92,

        facilityHealth: 78.51,

        optimizations: 5689,

        resourceUtilization: 70.94,

        savingsOpportunity: 646852.32,

        executivePriority: "HIGH",

        energyCost: 2836000,

        maintenanceCost: 1424000,

        securityCost: 883000,

        administrativeCost: 1035297.67,

        investment: 4200000,

        vendorUtilization: 69.12,

        costEfficiency: 86.81,

        recommendations: [

            "Reduce energy consumption",

            "Optimize workspace and resource allocation",

            "Optimize security resource allocation",

            "Implement identified savings opportunities"

        ]

    },


    B: {

        operationalCost: 5995310.14,

        budget: 6588450.22,

        budgetCompliance: 91.00,

        costReduction: 13.07,

        roi: 36.03,

        facilityHealth: 79.04,

        optimizations: 5262,

        resourceUtilization: 69.52,

        savingsOpportunity: 638946.22,

        executivePriority: "HIGH",

        energyCost: 2754000,

        maintenanceCost: 1383000,

        securityCost: 857000,

        administrativeCost: 1001310.14,

        investment: 4070000,

        vendorUtilization: 68.41,

        costEfficiency: 86.93,

        recommendations: [

            "Reduce energy consumption",

            "Optimize workspace and resource allocation",

            "Optimize security resource allocation",

            "Implement identified savings opportunities"

        ]

    },


    C: {

        operationalCost: 5930542.01,

        budget: 6590895.11,

        budgetCompliance: 89.98,

        costReduction: 12.95,

        roi: 36.13,

        facilityHealth: 79.00,

        optimizations: 5127,

        resourceUtilization: 69.44,

        savingsOpportunity: 623803.37,

        executivePriority: "MEDIUM",

        energyCost: 2725200,

        maintenanceCost: 1365000,

        securityCost: 846000,

        administrativeCost: 994342.01,

        investment: 4040000,

        vendorUtilization: 68.69,

        costEfficiency: 87.05,

        recommendations: [

            "Optimize workspace and resource allocation",

            "Optimize security resource allocation",

            "Implement identified savings opportunities"

        ]

    }

};


/* ================================================================
   10. HELPER FUNCTIONS
================================================================ */

function getElement(id) {

    return document.getElementById(id);

}


function setText(id, value) {

    const element = getElement(id);

    if (element) {

        element.textContent = value;

    }

}


function setHTML(id, value) {

    const element = getElement(id);

    if (element) {

        element.innerHTML = value;

    }

}


function number(value, decimals = 2) {

    const n = Number(value);

    if (Number.isNaN(n)) {

        return "0";

    }

    return n.toFixed(decimals);

}


function money(value) {

    const n = Number(value);

    if (Number.isNaN(n)) {

        return "₹0";

    }

    return "₹" + n.toLocaleString("en-IN", {

        maximumFractionDigits: 0

    });

}


function safePercent(value) {

    return number(value, 2) + "%";

}


/* ================================================================
   11. LOGIN SYSTEM
================================================================ */

function initializeLogin() {

    const loginForm =
        getElement("loginForm");

    const loginPage =
        getElement("loginPage");

    const dashboardPage =
        getElement("dashboardPage");

    if (!loginForm) {

        showDashboardWithoutLogin();

        return;

    }


    loginForm.addEventListener(

        "submit",

        function(event) {

            event.preventDefault();

            const userInput =
                getElement("userId");

            const passwordInput =
                getElement("password");

            const loginError =
                getElement("loginError");


            const userId =
                userInput
                    ? userInput.value.trim().toUpperCase()
                    : "";

            const password =
                passwordInput
                    ? passwordInput.value
                    : "";


            if (!userId || !password) {

                showLoginError(
                    "Please enter User ID and Password."
                );

                return;

            }


            const user =
                users[userId];


            if (
                !user ||
                user.password !== password
            ) {

                showLoginError(
                    "Invalid User ID or Password."
                );

                shakeElement(loginForm);

                return;

            }


            currentUser = userId;

            currentRole = user.role;


            sessionStorage.setItem(
                "facilityUser",
                userId
            );

            sessionStorage.setItem(
                "facilityRole",
                user.role
            );


            if (loginError) {

                loginError.textContent = "";

            }


            updateUserDetails(
                userId,
                user
            );


            if (loginPage) {

                loginPage.classList.add(
                    "login-exit"
                );

            }


            setTimeout(

                function() {

                    if (loginPage) {

                        loginPage.classList.add(
                            "hidden"
                        );

                        loginPage.style.display =
                            "none";

                    }


                    if (dashboardPage) {

                        dashboardPage.classList.remove(
                            "hidden"
                        );

                        dashboardPage.style.display =
                            "flex";

                        dashboardPage.classList.add(
                            "dashboard-enter"
                        );

                    }


                    initializeDashboard();

                },

                600

            );

        }

    );


    restoreSession();

}


function showLoginError(message) {

    const error =
        getElement("loginError");

    if (error) {

        error.textContent =
            message;

        error.classList.add(
            "error-visible"
        );

    }

}


function shakeElement(element) {

    if (!element) return;

    element.classList.remove(
        "shake"
    );

    void element.offsetWidth;

    element.classList.add(
        "shake"
    );

}


function updateUserDetails(userId, user) {

    setText(
        "userInitial",
        userId.substring(0, 1)
    );

    setText(
        "loggedUserId",
        userId
    );

    setText(
        "loggedUserRole",
        user.role
    );

    setText(
        "userName",
        user.name
    );

}


function restoreSession() {

    const savedUser =
        sessionStorage.getItem(
            "facilityUser"
        );

    const savedRole =
        sessionStorage.getItem(
            "facilityRole"
        );


    if (
        savedUser &&
        users[savedUser]
    ) {

        currentUser =
            savedUser;

        currentRole =
            savedRole ||
            users[savedUser].role;


        updateUserDetails(
            savedUser,
            users[savedUser]
        );


        const loginPage =
            getElement("loginPage");

        const dashboardPage =
            getElement("dashboardPage");


        if (loginPage) {

            loginPage.style.display =
                "none";

            loginPage.classList.add(
                "hidden"
            );

        }


        if (dashboardPage) {

            dashboardPage.classList.remove(
                "hidden"
            );

            dashboardPage.style.display =
                "flex";

        }


        initializeDashboard();

    }

}


function showDashboardWithoutLogin() {

    const dashboardPage =
        getElement("dashboardPage");

    if (!dashboardPage) {

        return;

    }

    dashboardPage.classList.remove(
        "hidden"
    );

    dashboardPage.style.display =
        "flex";

    initializeDashboard();

}


/* ================================================================
   12. LOGOUT
================================================================ */

function initializeLogout() {

    const buttons =
        document.querySelectorAll(
            "#logoutButton, .logout-button"
        );


    buttons.forEach(

        function(button) {

            button.addEventListener(

                "click",

                function() {

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


                    setTimeout(

                        function() {

                            if (dashboard) {

                                dashboard.classList.add(
                                    "hidden"
                                );

                                dashboard.style.display =
                                    "none";

                                dashboard.classList.remove(
                                    "dashboard-exit"
                                );

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

                        },

                        500

                    );

                }

            );

        }

    );

}


/* ================================================================
   13. BUILDING SELECTOR
================================================================ */

function initializeBuildingSelector() {

    const selector =
        getElement("buildingSelector");


    if (selector) {

        selector.addEventListener(

            "change",

            function() {

                updateBuilding(
                    this.value
                );

            }

        );

    }


    document
        .querySelectorAll(
            ".building-card, .building-btn"
        )
        .forEach(

            function(card) {

                card.addEventListener(

                    "click",

                    function() {

                        const building =
                            this.dataset.building;

                        if (building) {

                            updateBuilding(
                                building
                            );

                        }

                    }

                );

            }

        );


    updateBuilding("ALL");

}


/* ================================================================
   14. UPDATE BUILDING
================================================================ */

function updateBuilding(building) {

    if (!buildingData[building]) {

        building = "ALL";

    }


    selectedBuilding =
        building;


    const data =
        buildingData[building];

    const occupancy =
        occupancyData[building];

    const maintenance =
        maintenanceData[building];

    const security =
        securityData[building];

    const cost =
        costOptimizationData[building];


    setText(
        "selectedBuilding",
        data.name
    );


    const selector =
        getElement("buildingSelector");

    if (selector) {

        selector.value =
            building;

    }


    document
        .querySelectorAll(
            ".building-card, .building-btn"
        )
        .forEach(

            function(card) {

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

            }

        );


    updateEnergyParameters(data);

    updateMaintenanceParameters(
        maintenance
    );

    updateOccupancyParameters(
        occupancy
    );

    updateSecurityParameters(
        security
    );

    updateCostParameters(
        cost
    );

    updateCostBuildingCards();

    updateAllCharts();

    refreshOccupancyModule();

    animateVisibleCounters();

    flashDashboard();

}


/* ================================================================
   15. ENERGY PARAMETERS
================================================================ */

function updateEnergyParameters(data) {

    setText(
        "energyConsumption",
        number(data.energy)
    );

    setText(
        "energyValue",
        number(data.energy)
    );

    setText(
        "powerDemand",
        number(data.power)
    );

    setText(
        "powerValue",
        number(data.power)
    );

    setText(
        "alertValue",
        data.alerts
    );

    setText(
        "energyEfficiency",
        safePercent(data.efficiency)
    );

    setText(
        "efficiencyValue",
        safePercent(data.efficiency)
    );

    setText(
        "temperatureValue",
        number(data.temperature) + " °C"
    );

    setText(
        "humidityValue",
        safePercent(data.humidity)
    );

    setText(
        "hvacValue",
        number(data.hvac) + " kWh"
    );

    setText(
        "lightingValue",
        number(data.lighting) + " kWh"
    );

    setText(
        "waterValue",
        number(data.water) + " L"
    );

    setText(
        "energyAnomalyValue",
        data.anomaly
    );

}


/* ================================================================
   16. MAINTENANCE PARAMETERS
================================================================ */

function updateMaintenanceParameters(data) {

    if (!data) return;


    setText(
        "immediateMaintenance",
        data.immediate
    );

    setText(
        "scheduledMaintenance",
        data.scheduled
    );

    setText(
        "monitoringAssets",
        data.monitoring
    );

    setText(
        "healthyAssets",
        data.healthy
    );

    setText(
        "aiDecisions",
        data.decisions
    );

    setText(
        "criticalEquipment",
        data.critical
    );

    setText(
        "warningEquipment",
        data.warning
    );

    setText(
        "normalEquipment",
        data.normal
    );

    setText(
        "equipmentHealthScore",
        safePercent(data.healthScore)
    );

    setText(
        "maintenanceHealthScore",
        number(data.healthScore)
    );

    setText(
        "maintenanceAlerts",
        data.alerts
    );

    setText(
        "maintenanceAnomalies",
        data.anomalies
    );

    setText(
        "predictionAccuracy",
        safePercent(data.predictionAccuracy)
    );

    setText(
        "preventiveActions",
        data.preventiveActions
    );

}


/* ================================================================
   17. OCCUPANCY PARAMETERS
================================================================ */

function updateOccupancyParameters(data) {

    if (!data) return;


    setText(
        "occupancyValue",
        number(data.averageOccupancy)
    );

    setText(
        "utilizationValue",
        safePercent(data.utilization)
    );

    setText(
        "overcrowdingValue",
        data.overcrowded
    );

    setText(
        "maxOccupancyValue",
        data.maxOccupancy
    );

    setText(
        "availableSpaceValue",
        safePercent(data.availableSpaces)
    );

    setText(
        "totalOccupiedMembers",
        data.occupiedMembers
    );

    setText(
        "totalCapacity",
        data.totalCapacity
    );

    setText(
        "availableCapacity",
        data.availableCapacity
    );

    setText(
        "occupancyRate",
        safePercent(
            (
                data.occupiedMembers /
                data.totalCapacity
            ) * 100
        )
    );

    setText(
        "peakOccupancyHour",
        data.peakHour
    );

    setText(
        "peakOccupancy",
        number(data.peakOccupancy)
    );

    setText(
        "forecastPeakOccupancy",
        number(data.forecastPeak)
    );

    setText(
        "forecastUtilization",
        safePercent(data.forecastUtilization)
    );

    setText(
        "meetingRooms",
        data.meetingRooms
    );

    setText(
        "underutilizedRooms",
        data.underutilizedRooms
    );

    setText(
        "workspaceAvailability",
        safePercent(data.workspaceAvailability)
    );

}


/* ================================================================
   18. SECURITY PARAMETERS
================================================================ */

function updateSecurityParameters(data) {

    if (!data) return;


    setText(
        "securityTotalEvents",
        data.totalEvents
    );

    setText(
        "totalSecurityEvents",
        data.totalEvents
    );

    setText(
        "authorizedAccess",
        data.authorized
    );

    setText(
        "unauthorizedAccess",
        data.unauthorized
    );

    setText(
        "suspiciousActivity",
        data.suspicious
    );

    setText(
        "securityIncidents",
        data.incidents
    );

    setText(
        "cctvCameras",
        data.cctvCameras
    );

    setText(
        "cameraOnline",
        data.cameraOnline
    );

    setText(
        "cameraOffline",
        data.cameraOffline
    );

    setText(
        "avgRiskScore",
        number(data.avgRiskScore)
    );

    setText(
        "accessCompliance",
        safePercent(data.accessCompliance)
    );

    setText(
        "threatLevel",
        data.threatLevel
    );

    setText(
        "securityHealth",
        safePercent(data.securityHealth)
    );

}


/* ================================================================
   19. COST PARAMETERS
================================================================ */

function updateCostParameters(data) {

    if (!data) return;


    /* 01 */

    setText(
        "costOperationalCost",
        money(data.operationalCost)
    );

    setText(
        "operationalCost",
        money(data.operationalCost)
    );


    /* 02 */

    setText(
        "costBudget",
        money(data.budget)
    );

    setText(
        "budget",
        money(data.budget)
    );


    /* 03 */

    setText(
        "costBudgetCompliance",
        safePercent(data.budgetCompliance)
    );

    setText(
        "budgetCompliance",
        safePercent(data.budgetCompliance)
    );


    /* 04 */

    setText(
        "costReduction",
        safePercent(data.costReduction)
    );

    setText(
        "costReductionValue",
        safePercent(data.costReduction)
    );


    /* 05 */

    setText(
        "costROI",
        safePercent(data.roi)
    );

    setText(
        "roi",
        safePercent(data.roi)
    );


    /* 06 */

    setText(
        "costFacilityHealth",
        number(data.facilityHealth)
    );

    setText(
        "facilityHealth",
        number(data.facilityHealth)
    );


    /* 07 */

    setText(
        "costOptimizations",
        data.optimizations.toLocaleString()
    );

    setText(
        "optimizations",
        data.optimizations.toLocaleString()
    );


    /* 08 */

    setText(
        "costResourceUtilization",
        safePercent(data.resourceUtilization)
    );

    setText(
        "resourceUtilization",
        safePercent(data.resourceUtilization)
    );


    /* 09 */

    setText(
        "costSavingsOpportunity",
        money(data.savingsOpportunity)
    );

    setText(
        "savingsOpportunity",
        money(data.savingsOpportunity)
    );


    /* 10 */

    setText(
        "costExecutivePriority",
        data.executivePriority
    );

    setText(
        "executivePriority",
        data.executivePriority
    );


    /* 11 */

    setText(
        "costInvestment",
        money(data.investment)
    );

    setText(
        "investmentAmount",
        money(data.investment)
    );


    /* 12 */

    setText(
        "vendorUtilization",
        safePercent(data.vendorUtilization)
    );


    /* 13 */

    setText(
        "costEfficiency",
        safePercent(data.costEfficiency)
    );


    updateCostRecommendations(
        data.recommendations
    );

}


/* ================================================================
   20. COST RECOMMENDATIONS
================================================================ */

function updateCostRecommendations(
    recommendations
) {

    const container =
        getElement(
            "costRecommendations"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    recommendations.forEach(

        function(item, index) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "cost-recommendation-item reveal";


            card.innerHTML =

                "<span class='cost-rec-number'>" +
                String(index + 1).padStart(2, "0") +
                "</span>" +

                "<div>" +

                "<strong>" +
                item +
                "</strong>" +

                "<small>" +
                "Cross-agent optimization recommendation" +
                "</small>" +

                "</div>";


            container.appendChild(
                card
            );


            setTimeout(

                function() {

                    card.classList.add(
                        "visible"
                    );

                },

                index * 100

            );

        }

    );

}


/* ================================================================
   21. COST BUILDING CARDS
================================================================ */

function updateCostBuildingCards() {

    const cards =
        document.querySelectorAll(
            "[data-cost-building]"
        );


    cards.forEach(

        function(card) {

            const key =
                card.dataset.costBuilding;

            const data =
                costOptimizationData[key];


            if (!data) return;


            const operational =
                card.querySelector(
                    ".cost-operational"
                );

            const reduction =
                card.querySelector(
                    ".cost-reduction"
                );

            const roi =
                card.querySelector(
                    ".cost-roi"
                );

            const health =
                card.querySelector(
                    ".cost-health"
                );

            const savings =
                card.querySelector(
                    ".cost-savings"
                );


            if (operational) {

                operational.textContent =
                    money(data.operationalCost);

            }


            if (reduction) {

                reduction.textContent =
                    safePercent(data.costReduction);

            }


            if (roi) {

                roi.textContent =
                    safePercent(data.roi);

            }


            if (health) {

                health.textContent =
                    number(data.facilityHealth);

            }


            if (savings) {

                savings.textContent =
                    money(data.savingsOpportunity);

            }

        }

    );

}


/* ================================================================
   22. CHART CHECK
================================================================ */

function chartExists(id) {

    return (

        getElement(id) &&
        typeof Chart !== "undefined"

    );

}


/* ================================================================
   23. GLOBAL CHART DEFAULTS
================================================================ */

function setupChartDefaults() {

    if (
        typeof Chart ===
        "undefined"
    ) {

        return;

    }


    Chart.defaults.font.family =
        "Inter, Arial, sans-serif";

    Chart.defaults.font.size =
        10;

    Chart.defaults.color =
        "#7890a5";

    Chart.defaults.animation.duration =
        1100;

}


/* ================================================================
   24. COMMON CHART OPTIONS
================================================================ */

function getChartOptions() {

    return {

        responsive: true,

        maintainAspectRatio: false,

        animation: {

            duration: 1200,

            easing: "easeOutQuart"

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

                },

                ticks: {

                    color: "#527084"

                }

            },

            y: {

                beginAtZero: true,

                ticks: {

                    color: "#527084"

                },

                grid: {

                    color:
                        "rgba(100,160,190,.07)"

                }

            }

        }

    };

}


/* ================================================================
   25. INITIALIZE ALL CHARTS
================================================================ */

function initializeCharts() {

    if (
        chartsInitialized
    ) {

        return;

    }


    if (
        typeof Chart ===
        "undefined"
    ) {

        console.warn(
            "Chart.js is not loaded."
        );

        return;

    }


    chartsInitialized =
        true;


    setupChartDefaults();


    initializeEnergyChart();

    initializeSourceChart();

    initializeDemandChart();

    initializeSectorChart();

    initializeHealthChart();

    initializeOccupancyChart();

    initializeOccupancyDayChart();

    initializeOccupancyForecastChart();

    initializeCostDistributionChart();

    initializeCostBuildingChart();

    initializeCostROIChart();

    initializeCostHealthChart();

}


/* ================================================================
   26. ENERGY LINE CHART
================================================================ */

function initializeEnergyChart() {

    if (
        !chartExists(
            "energyChart"
        )
    ) {

        return;

    }


    energyChart =
        new Chart(

            getElement(
                "energyChart"
            ),

            {

                type: "line",

                data: {

                    labels: [

                        "00",
                        "02",
                        "04",
                        "06",
                        "08",
                        "10",
                        "12",
                        "14",
                        "16",
                        "18",
                        "20",
                        "22"

                    ],

                    datasets: [

                        {

                            label:
                                "Energy Consumption",

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

                            borderColor:
                                "#00d9ff",

                            backgroundColor:
                                "rgba(0,217,255,.10)",

                            fill: true,

                            tension: .42,

                            borderWidth: 2.5,

                            pointRadius: 2,

                            pointBackgroundColor:
                                "#00d9ff"

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   27. ENERGY SOURCE DONUT
================================================================ */

function initializeSourceChart() {

    if (
        !chartExists(
            "sourceChart"
        )
    ) {

        return;

    }


    sourceChart =
        new Chart(

            getElement(
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

                                "#40dda0",
                                "#4197ff",
                                "#9b7cff"

                            ],

                            borderWidth: 0,

                            hoverOffset: 8

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

                    cutout: "70%",

                    animation: {

                        animateRotate: true,

                        duration: 1400

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


/* ================================================================
   28. POWER DEMAND CHART
================================================================ */

function initializeDemandChart() {

    if (
        !chartExists(
            "demandChart"
        )
    ) {

        return;

    }


    demandChart =
        new Chart(

            getElement(
                "demandChart"
            ),

            {

                type: "line",

                data: {

                    labels: [

                        "00",
                        "02",
                        "04",
                        "06",
                        "08",
                        "10",
                        "12",
                        "14",
                        "16",
                        "18",
                        "20",
                        "22"

                    ],

                    datasets: [

                        {

                            label:
                                "Power Demand",

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
                                "rgba(255,88,112,.08)",

                            fill: true,

                            tension: .4,

                            borderWidth: 2.5,

                            pointRadius: 2

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   29. SECTOR BAR CHART
================================================================ */

function initializeSectorChart() {

    if (
        !chartExists(
            "sectorChart"
        )
    ) {

        return;

    }


    sectorChart =
        new Chart(

            getElement(
                "sectorChart"
            ),

            {

                type: "bar",

                data: {

                    labels: [

                        "HVAC",
                        "Lighting",
                        "Equipment",
                        "Water"

                    ],

                    datasets: [

                        {

                            data: [

                                35,
                                25,
                                25,
                                15

                            ],

                            backgroundColor: [

                                "#00d9ff",
                                "#4197ff",
                                "#9b7cff",
                                "#40dda0"

                            ],

                            borderRadius: 8,

                            borderSkipped: false

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   30. MAINTENANCE HEALTH DONUT
================================================================ */

function initializeHealthChart() {

    if (
        !chartExists(
            "healthChart"
        )
    ) {

        return;

    }


    healthChart =
        new Chart(

            getElement(
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
                                "#4197ff",
                                "#40dfa0"

                            ],

                            borderWidth: 0,

                            hoverOffset: 7

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

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


/* ================================================================
   31. OCCUPANCY HOURLY CHART
================================================================ */

function initializeOccupancyChart() {

    if (
        !chartExists(
            "occupancyChart"
        )
    ) {

        return;

    }


    occupancyChart =
        new Chart(

            getElement(
                "occupancyChart"
            ),

            {

                type: "line",

                data: {

                    labels:
                        occupancyHours,

                    datasets: [

                        {

                            label:
                                "Average Occupancy",

                            data:
                                occupancyHourlyValues,

                            borderColor:
                                "#40dda0",

                            backgroundColor:
                                "rgba(64,221,160,.10)",

                            fill: true,

                            tension: .42,

                            borderWidth: 2.5,

                            pointRadius: 2

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   32. OCCUPANCY DAY CHART
================================================================ */

function initializeOccupancyDayChart() {

    if (
        !chartExists(
            "occupancyDayChart"
        )
    ) {

        return;

    }


    occupancyDayChart =
        new Chart(

            getElement(
                "occupancyDayChart"
            ),

            {

                type: "bar",

                data: {

                    labels:
                        occupancyDays,

                    datasets: [

                        {

                            label:
                                "Average Occupancy",

                            data:
                                occupancyDayValues,

                            backgroundColor: [

                                "#00d9ff",
                                "#4197ff",
                                "#6d7cff",
                                "#9b7cff",
                                "#a855f7",
                                "#40dda0",
                                "#00bcd4"

                            ],

                            borderRadius: 8,

                            borderSkipped: false

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   33. OCCUPANCY FORECAST CHART
================================================================ */

function initializeOccupancyForecastChart() {

    if (
        !chartExists(
            "occupancyForecastChart"
        )
    ) {

        return;

    }


    occupancyForecastChart =
        new Chart(

            getElement(
                "occupancyForecastChart"
            ),

            {

                type: "line",

                data: {

                    labels:
                        forecastLabels,

                    datasets: [

                        {

                            label:
                                "Predicted Occupancy",

                            data:
                                forecastValues,

                            borderColor:
                                "#9b7cff",

                            backgroundColor:
                                "rgba(155,124,255,.10)",

                            fill: true,

                            tension: .4,

                            borderWidth: 2.5,

                            pointRadius: 3,

                            pointBackgroundColor:
                                "#00d9ff"

                        }

                    ]

                },

                options:
                    getChartOptions()

            }

        );

}


/* ================================================================
   34. COST DISTRIBUTION CHART
================================================================ */

function initializeCostDistributionChart() {

    if (
        !chartExists(
            "costDistributionChart"
        )
    ) {

        return;

    }


    costDistributionChart =
        new Chart(

            getElement(
                "costDistributionChart"
            ),

            {

                type: "doughnut",

                data: {

                    labels: [

                        "Energy",
                        "Maintenance",
                        "Security",
                        "Administrative"

                    ],

                    datasets: [

                        {

                            data: [

                                45.93,
                                23.05,
                                14.28,
                                16.74

                            ],

                            backgroundColor: [

                                "#00d9ff",
                                "#9b7cff",
                                "#40dda0",
                                "#ffb44d"

                            ],

                            borderWidth: 0,

                            hoverOffset: 10

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

                    cutout: "65%",

                    animation: {

                        animateRotate: true,

                        duration: 1500

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


/* ================================================================
   35. COST BUILDING CHART
================================================================ */

function initializeCostBuildingChart() {

    if (
        !chartExists(
            "costBuildingChart"
        )
    ) {

        return;

    }


    costBuildingChart =
        new Chart(

            getElement(
                "costBuildingChart"
            ),

            {

                type: "bar",

                data: {

                    labels: [

                        "Building A",
                        "Building B",
                        "Building C"

                    ],

                    datasets: [

                        {

                            label:
                                "Operational Cost",

                            data: [

                                6178297.67,
                                5995310.14,
                                5930542.01

                            ],

                            backgroundColor: [

                                "#00d9ff",
                                "#9b7cff",
                                "#40dda0"

                            ],

                            borderRadius: 10,

                            borderSkipped: false

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

                    animation: {

                        duration: 1400,

                        easing: "easeOutQuart"

                    },

                    plugins: {

                        legend: {

                            display: false

                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    function(context) {

                                        return money(
                                            context.raw
                                        );

                                    }

                            }

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
                                    function(value) {

                                        return "₹" +
                                            (
                                                value /
                                                1000000
                                            ).toFixed(1) +
                                            "M";

                                    }

                            }

                        }

                    }

                }

            }

        );

}


/* ================================================================
   36. COST ROI CHART
================================================================ */

function initializeCostROIChart() {

    if (
        !chartExists(
            "costROIChart"
        )
    ) {

        return;

    }


    costROIChart =
        new Chart(

            getElement(
                "costROIChart"
            ),

            {

                type: "bar",

                data: {

                    labels: [

                        "A",
                        "B",
                        "C"

                    ],

                    datasets: [

                        {

                            label:
                                "ROI Generated",

                            data: [

                                36.92,
                                36.03,
                                36.13

                            ],

                            backgroundColor: [

                                "#00d9ff",
                                "#9b7cff",
                                "#40dfa0"

                            ],

                            borderRadius: 10

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

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

                            ticks: {

                                callback:
                                    function(value) {

                                        return value +
                                            "%";

                                    }

                            }

                        }

                    }

                }

            }

        );

}


/* ================================================================
   37. COST FACILITY HEALTH CHART
================================================================ */

function initializeCostHealthChart() {

    if (
        !chartExists(
            "costHealthChart"
        )
    ) {

        return;

    }


    costHealthChart =
        new Chart(

            getElement(
                "costHealthChart"
            ),

            {

                type: "line",

                data: {

                    labels: [

                        "Building A",
                        "Building B",
                        "Building C"

                    ],

                    datasets: [

                        {

                            label:
                                "Facility Health",

                            data: [

                                78.51,
                                79.04,
                                79.00

                            ],

                            borderColor:
                                "#40dda0",

                            backgroundColor:
                                "rgba(64,221,160,.10)",

                            fill: true,

                            tension: .35,

                            borderWidth: 3,

                            pointRadius: 5,

                            pointBackgroundColor:
                                "#40dda0"

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,

                    animation: {

                        duration: 1400

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

                            min: 70,

                            max: 100

                        }

                    }

                }

            }

        );

}


/* ================================================================
   38. UPDATE OCCUPANCY CHARTS
================================================================ */

function updateOccupancyCharts() {

    let multiplier = 1;


    if (
        selectedBuilding === "A"
    ) {

        multiplier = .93;

    }

    else if (
        selectedBuilding === "B"
    ) {

        multiplier = .95;

    }

    else if (
        selectedBuilding === "C"
    ) {

        multiplier = 1.08;

    }


    if (occupancyChart) {

        occupancyChart
            .data
            .datasets[0]
            .data =
            occupancyHourlyValues.map(

                function(value) {

                    return Number(
                        (
                            value *
                            multiplier
                        ).toFixed(2)
                    );

                }

            );


        occupancyChart.update();

    }


    if (occupancyDayChart) {

        occupancyDayChart
            .data
            .datasets[0]
            .data =
            occupancyDayValues.map(

                function(value) {

                    return Number(
                        (
                            value *
                            multiplier
                        ).toFixed(2)
                    );

                }

            );


        occupancyDayChart.update();

    }


    if (occupancyForecastChart) {

        let forecastMultiplier =
            1;


        if (
            selectedBuilding === "A"
        ) {

            forecastMultiplier =
                .75;

        }

        else if (
            selectedBuilding === "B"
        ) {

            forecastMultiplier =
                .72;

        }

        else if (
            selectedBuilding === "C"
        ) {

            forecastMultiplier =
                1.05;

        }


        occupancyForecastChart
            .data
            .datasets[0]
            .data =
            forecastValues.map(

                function(value) {

                    return Number(
                        (
                            value *
                            forecastMultiplier
                        ).toFixed(2)
                    );

                }

            );


        occupancyForecastChart.update();

    }

}


/* ================================================================
   39. UPDATE COST CHARTS
================================================================ */

function updateCostCharts() {

    const data =
        costOptimizationData;


    if (costBuildingChart) {

        costBuildingChart
            .data
            .datasets[0]
            .data = [

                data.A.operationalCost,

                data.B.operationalCost,

                data.C.operationalCost

            ];

        costBuildingChart.update();

    }


    if (costROIChart) {

        costROIChart
            .data
            .datasets[0]
            .data = [

                data.A.roi,

                data.B.roi,

                data.C.roi

            ];

        costROIChart.update();

    }


    if (costHealthChart) {

        costHealthChart
            .data
            .datasets[0]
            .data = [

                data.A.facilityHealth,

                data.B.facilityHealth,

                data.C.facilityHealth

            ];

        costHealthChart.update();

    }

}


/* ================================================================
   40. UPDATE ALL CHARTS
================================================================ */

function updateAllCharts() {

    updateOccupancyCharts();

    updateCostCharts();

}


/* ================================================================
   41. REVEAL ON SCROLL
================================================================ */

function initializeRevealAnimation() {

    const elements =
        document.querySelectorAll(
            ".reveal, " +
            ".dashboard-section, " +
            ".metric-card, " +
            ".panel, " +
            ".decision-card, " +
            ".security-card, " +
            ".cost-card, " +
            ".agent-title"
        );


    if (
        !("IntersectionObserver" in window)
    ) {

        elements.forEach(

            function(element) {

                element.classList.add(
                    "visible"
                );

            }

        );

        return;

    }


    const observer =
        new IntersectionObserver(

            function(entries) {

                entries.forEach(

                    function(entry) {

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

                threshold: .10

            }

        );


    elements.forEach(

        function(element) {

            observer.observe(
                element
            );

        }

    );

}


/* ================================================================
   42. SMOOTH NAVIGATION
================================================================ */

function initializeNavigation() {

    const links =
        document.querySelectorAll(
            ".nav-link"
        );


    links.forEach(

        function(link) {

            link.addEventListener(

                "click",

                function(event) {

                    const href =
                        this.getAttribute(
                            "href"
                        );


                    if (
                        !href ||
                        href === "#"
                    ) {

                        return;

                    }


                    const target =
                        document.querySelector(
                            href
                        );


                    if (!target) {

                        return;

                    }


                    event.preventDefault();


                    links.forEach(

                        function(item) {

                            item.classList.remove(
                                "active"
                            );

                        }

                    );


                    this.classList.add(
                        "active"
                    );


                    target.scrollIntoView({

                        behavior:
                            "smooth",

                        block:
                            "start"

                    });


                    target.classList.add(
                        "section-highlight"
                    );


                    setTimeout(

                        function() {

                            target.classList.remove(
                                "section-highlight"
                            );

                        },

                        1200

                    );

                }

            );

        }

    );


    window.addEventListener(

        "scroll",

        function() {

            updateActiveNavigation();

        },

        {

            passive: true

        }

    );

}


function updateActiveNavigation() {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );

    const links =
        document.querySelectorAll(
            ".nav-link"
        );


    let current = "";


    sections.forEach(

        function(section) {

            const rect =
                section.getBoundingClientRect();


            if (
                rect.top <= 250 &&
                rect.bottom >= 180
            ) {

                current =
                    section.id;

            }

        }

    );


    if (!current) {

        return;

    }


    links.forEach(

        function(link) {

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


/* ================================================================
   43. LIVE CLOCK
================================================================ */

function initializeClock() {

    updateClock();

    setInterval(

        updateClock,

        1000

    );

}


function updateClock() {

    const now =
        new Date();


    const time =
        now.toLocaleTimeString(

            [],

            {

                hour:
                    "2-digit",

                minute:
                    "2-digit",

                second:
                    "2-digit"

            }

        );


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


/* ================================================================
   44. COUNTDOWN
================================================================ */

function updateCountdown() {

    const countdown =
        getElement(
            "countdown"
        );


    if (!countdown) {

        return;

    }


    const minutes =
        Math.floor(
            remainingSeconds /
            60
        );


    const seconds =
        remainingSeconds %
        60;


    countdown.textContent =

        String(minutes)
            .padStart(2, "0")

        +

        ":" +

        String(seconds)
            .padStart(2, "0");

}


/* ================================================================
   45. LIVE READING
================================================================ */

function nextReading() {

    const data =
        buildingData[
            selectedBuilding
        ];


    if (!data) {

        return;

    }


    const energyVariation =
        (
            Math.random() -
            .5
        ) * .9;


    const powerVariation =
        (
            Math.random() -
            .5
        ) * .5;


    const currentEnergy =
        Math.max(

            5,

            data.energy +
            energyVariation

        );


    const currentPower =
        Math.max(

            3,

            data.power +
            powerVariation

        );


    setText(

        "energyConsumption",

        currentEnergy.toFixed(2)

    );


    setText(

        "energyValue",

        currentEnergy.toFixed(2)

    );


    setText(

        "powerDemand",

        currentPower.toFixed(2)

    );


    setText(

        "powerValue",

        currentPower.toFixed(2)

    );


    setText(

        "flowEnergyValue",

        currentEnergy.toFixed(2) +
        " kWh"

    );


    setText(

        "flowPowerValue",

        currentPower.toFixed(2) +
        " kW"

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


        energyChart.update();

    }


    remainingSeconds =
        REFRESH_SECONDS;


    updateCountdown();

    animateNumberElements();

    flashDashboard();

}


/* ================================================================
   46. MONITORING
================================================================ */

function initializeMonitoring() {

    updateCountdown();


    setInterval(

        function() {

            if (!autoRefresh) {

                return;

            }


            remainingSeconds--;


            if (
                remainingSeconds <=
                0
            ) {

                nextReading();

            }


            updateCountdown();

        },

        1000

    );

}


/* ================================================================
   47. MONITORING BUTTONS
================================================================ */

function initializeButtons() {

    const nextButton =
        getElement(
            "nextReading"
        );


    const resetButton =
        getElement(
            "resetMonitoring"
        );


    const autoButton =
        getElement(
            "autoRefreshButton"
        );


    const refreshStatus =
        getElement(
            "refreshStatus"
        );


    if (nextButton) {

        nextButton.addEventListener(

            "click",

            function() {

                nextReading();

            }

        );

    }


    if (resetButton) {

        resetButton.addEventListener(

            "click",

            function() {

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

            function() {

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


/* ================================================================
   48. FLASH DASHBOARD
================================================================ */

function flashDashboard() {

    document.body.classList.remove(
        "data-refresh"
    );


    void document.body.offsetWidth;


    document.body.classList.add(
        "data-refresh"
    );


    setTimeout(

        function() {

            document.body.classList.remove(
                "data-refresh"
            );

        },

        700

    );

}


/* ================================================================
   49. OCCUPANCY CONTROLS
================================================================ */

function initializeOccupancyControls() {

    document
        .querySelectorAll(
            "[data-occupancy-building]"
        )
        .forEach(

            function(button) {

                button.addEventListener(

                    "click",

                    function() {

                        const building =
                            this.dataset
                                .occupancyBuilding;


                        if (
                            buildingData[
                                building
                            ]
                        ) {

                            updateBuilding(
                                building
                            );

                        }

                    }

                );

            }

        );

}


/* ================================================================
   50. HEATMAP
================================================================ */

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

        [18,25,31,38,26,35,29,32,27,19],

        [16,24,30,36,28,33,31,34,26,18],

        [15,22,29,34,27,31,30,32,25,17],

        [19,27,34,40,31,37,36,38,30,21],

        [17,26,33,41,35,58,39,43,34,23],

        [6,8,11,13,12,14,13,10,8,6],

        [4,6,8,10,8,9,8,7,5,4]

    ];


    const empty =
        document.createElement(
            "div"
        );


    empty.className =
        "heatmap-label";


    container.appendChild(
        empty
    );


    hours.forEach(

        function(hour) {

            const label =
                document.createElement(
                    "div"
                );


            label.className =
                "heatmap-label";


            label.textContent =
                hour + ":00";


            container.appendChild(
                label
            );

        }

    );


    days.forEach(

        function(day, dayIndex) {

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

                function(hour, hourIndex) {

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
                        .35 +
                        (
                            value /
                            100
                        ) * .65;


                    cell.addEventListener(

                        "mouseenter",

                        function() {

                            this.style.opacity =
                                "1";

                            this.classList.add(
                                "heatmap-active"
                            );

                        }

                    );


                    cell.addEventListener(

                        "mouseleave",

                        function() {

                            this.style.opacity =
                                .35 +
                                (
                                    value /
                                    100
                                ) * .65;

                            this.classList.remove(
                                "heatmap-active"
                            );

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


/* ================================================================
   51. OCCUPANCY SUMMARY
================================================================ */

function updateOccupancyAgentSummary() {

    const data =
        occupancyData[
            selectedBuilding
        ];


    if (!data) {

        return;

    }


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
        number(
            data.peakOccupancy
        )
    );


    setText(
        "forecastPeakOccupancy",
        number(
            data.forecastPeak
        )
    );


    setText(
        "forecastUtilization",
        safePercent(
            data.forecastUtilization
        )
    );

}


/* ================================================================
   52. OCCUPANCY STATUS
================================================================ */

function getOccupancyStatus(
    utilization
) {

    if (
        utilization > 120
    ) {

        return {

            label: "Critical",

            priority: "HIGH",

            alert:
                "CRITICAL OCCUPANCY ALERT"

        };

    }


    if (
        utilization > 100
    ) {

        return {

            label: "Overcrowded",

            priority: "HIGH",

            alert:
                "OVERCROWDING ALERT"

        };

    }


    if (
        utilization >= 80
    ) {

        return {

            label: "High Usage",

            priority: "MEDIUM",

            alert:
                "HIGH USAGE WARNING"

        };

    }


    if (
        utilization >= 40
    ) {

        return {

            label: "Normal",

            priority: "LOW",

            alert:
                "NORMAL OCCUPANCY"

        };

    }


    return {

        label: "Low",

        priority: "LOW",

        alert:
            "LOW USAGE"

    };

}


/* ================================================================
   53. WORKSPACE ALLOCATION
================================================================ */

function updateWorkspaceAllocation() {

    const allocation = {

        A: {

            recommended:
                "A102 Office",

            available:
                78.04

        },

        B: {

            recommended:
                "B202 Conference",

            available:
                82.12

        },

        C: {

            recommended:
                "C201 Lab",

            available:
                92.32

        },

        ALL: {

            recommended:
                "C201 Lab",

            available:
                84.16

        }

    };


    const data =
        allocation[
            selectedBuilding
        ];


    if (!data) {

        return;

    }


    setText(
        "recommendedWorkspace",
        data.recommended
    );


    setText(
        "workspaceAvailability",
        safePercent(
            data.available
        )
    );

}


/* ================================================================
   54. REFRESH OCCUPANCY MODULE
================================================================ */

function refreshOccupancyModule() {

    updateOccupancyCharts();

    updateOccupancyAgentSummary();

    updateWorkspaceAllocation();

}


/* ================================================================
   55. BUTTON ANIMATIONS
================================================================ */

function initializeButtonAnimations() {

    document
        .querySelectorAll(
            "button, .nav-link, .building-btn, .building-card"
        )
        .forEach(

            function(button) {

                button.addEventListener(

                    "click",

                    function() {

                        this.classList.add(
                            "clicked"
                        );


                        setTimeout(

                            function() {

                                button.classList.remove(
                                    "clicked"
                                );

                            },

                            350

                        );

                    }

                );

            }

        );

}


/* ================================================================
   56. CARD HOVER ANIMATIONS
================================================================ */

function initializeCardAnimations() {

    const cards =
        document.querySelectorAll(

            ".metric-card, " +

            ".panel, " +

            ".decision-card, " +

            ".recommendation-card, " +

            ".maintenance-recommendation, " +

            ".equipment-alert, " +

            ".health-category, " +

            ".security-card, " +

            ".cost-card, " +

            ".cost-building-card, " +

            ".insight"

        );


    cards.forEach(

        function(card) {

            card.addEventListener(

                "mouseenter",

                function() {

                    this.classList.add(
                        "card-hover"
                    );

                }

            );


            card.addEventListener(

                "mouseleave",

                function() {

                    this.classList.remove(
                        "card-hover"
                    );

                }

            );

        }

    );

}


/* ================================================================
   57. PARALLAX ANIMATION
================================================================ */

function initializeParallax() {

    const ambient =
        document.querySelectorAll(
            ".ambient"
        );


    if (!ambient.length) {

        return;

    }


    let ticking =
        false;


    window.addEventListener(

        "scroll",

        function() {

            if (ticking) {

                return;

            }


            window.requestAnimationFrame(

                function() {

                    const scrollY =
                        window.scrollY;


                    ambient.forEach(

                        function(element, index) {

                            const speed =
                                (
                                    index +
                                    1
                                ) * .015;


                            element.style.transform =

                                "translate3d(0," +

                                (
                                    scrollY *
                                    speed
                                ) +

                                "px,0)";

                        }

                    );


                    ticking =
                        false;

                }

            );


            ticking =
                true;

        },

        {

            passive: true

        }

    );

}


/* ================================================================
   58. SECTION GLOW
================================================================ */

function initializeSectionGlow() {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    if (
        !(
            "IntersectionObserver"
            in window
        )
    ) {

        return;

    }


    const observer =
        new IntersectionObserver(

            function(entries) {

                entries.forEach(

                    function(entry) {

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

                    }

                );

            },

            {

                threshold: .18

            }

        );


    sections.forEach(

        function(section) {

            observer.observe(
                section
            );

        }

    );

}


/* ================================================================
   59. SYSTEM STATUS
================================================================ */

function updateSystemStatus() {

    const elements =
        document.querySelectorAll(

            ".system-online, " +

            ".engine-status, " +

            ".live-indicator, " +

            ".section-live, " +

            ".status-dot"

        );


    elements.forEach(

        function(element) {

            element.classList.add(
                "status-pulse"
            );

        }

    );

}


/* ================================================================
   60. AI ACTIVITY
================================================================ */

function initializeAIActivity() {

    const elements =
        document.querySelectorAll(

            ".ai-core, " +

            ".ai-rings, " +

            ".final-ai-glow, " +

            ".hero-core, " +

            ".hero-visual"

        );


    elements.forEach(

        function(element) {

            element.classList.add(
                "ai-active"
            );

        }

    );

}


/* ================================================================
   61. ANIMATED COUNTERS
================================================================ */

function animateCounter(
    element,
    target,
    duration = 1000
) {

    if (!element) {

        return;

    }


    const numericTarget =
        Number(
            String(target)
                .replace(/[^0-9.-]/g, "")
        );


    if (
        Number.isNaN(
            numericTarget
        )
    ) {

        return;

    }


    const start =
        0;


    const startTime =
        performance.now();


    function update(
        currentTime
    ) {

        const progress =
            Math.min(

                (
                    currentTime -
                    startTime
                ) /
                duration,

                1

            );


        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );


        const value =
            start +
            (
                numericTarget -
                start
            ) *
            eased;


        element.textContent =
            Number(
                value
            ).toLocaleString(
                "en-IN",
                {
                    maximumFractionDigits: 2
                }
            );


        if (
            progress < 1
        ) {

            requestAnimationFrame(
                update
            );

        }

    }


    requestAnimationFrame(
        update
    );

}


function animateNumberElements() {

    document
        .querySelectorAll(
            "[data-counter]"
        )
        .forEach(

            function(element) {

                animateCounter(

                    element,

                    element.dataset.counter

                );

            }

        );

}


function animateVisibleCounters() {

    document
        .querySelectorAll(
            ".metric-number, " +
            ".decision-card strong, " +
            ".security-card strong, " +
            ".insight strong"
        )
        .forEach(

            function(element) {

                element.classList.add(
                    "number-pop"
                );


                setTimeout(

                    function() {

                        element.classList.remove(
                            "number-pop"
                        );

                    },

                    800

                );

            }

        );

}


/* ================================================================
   62. RIPPLE EFFECT
================================================================ */

function initializeRippleEffect() {

    document
        .querySelectorAll(
            "button, .nav-link, .metric-card, .panel"
        )
        .forEach(

            function(element) {

                element.addEventListener(

                    "click",

                    function(event) {

                        const rect =
                            this.getBoundingClientRect();


                        const ripple =
                            document.createElement(
                                "span"
                            );


                        ripple.className =
                            "js-ripple";


                        ripple.style.left =
                            (
                                event.clientX -
                                rect.left
                            ) + "px";


                        ripple.style.top =
                            (
                                event.clientY -
                                rect.top
                            ) + "px";


                        this.appendChild(
                            ripple
                        );


                        setTimeout(

                            function() {

                                ripple.remove();

                            },

                            700

                        );

                    }

                );

            }

        );

}


/* ================================================================
   63. MOUSE GLOW EFFECT
================================================================ */

function initializeMouseGlow() {

    const cards =
        document.querySelectorAll(
            ".metric-card, .panel, .cost-card, .security-card"
        );


    cards.forEach(

        function(card) {

            card.addEventListener(

                "mousemove",

                function(event) {

                    const rect =
                        this.getBoundingClientRect();


                    const x =
                        event.clientX -
                        rect.left;


                    const y =
                        event.clientY -
                        rect.top;


                    this.style.setProperty(
                        "--mouse-x",
                        x + "px"
                    );


                    this.style.setProperty(
                        "--mouse-y",
                        y + "px"
                    );

                }

            );


            card.addEventListener(

                "mouseleave",

                function() {

                    this.style.removeProperty(
                        "--mouse-x"
                    );

                    this.style.removeProperty(
                        "--mouse-y"
                    );

                }

            );

        }

    );

}


/* ================================================================
   64. SCROLL PROGRESS
================================================================ */

function initializeScrollProgress() {

    let progress =
        document.querySelector(
            ".js-scroll-progress"
        );


    if (!progress) {

        progress =
            document.createElement(
                "div"
            );


        progress.className =
            "js-scroll-progress";


        document.body.appendChild(
            progress
        );

    }


    window.addEventListener(

        "scroll",

        function() {

            const scrollTop =
                window.scrollY;


            const height =
                document.documentElement
                    .scrollHeight -
                window.innerHeight;


            const percentage =
                height > 0
                    ? (
                        scrollTop /
                        height
                    ) * 100
                    : 0;


            progress.style.width =
                percentage + "%";

        },

        {

            passive: true

        }

    );

}


/* ================================================================
   65. MOBILE NAVIGATION
================================================================ */

function initializeResponsiveNavigation() {

    const sidebar =
        document.querySelector(
            ".sidebar"
        );


    if (!sidebar) {

        return;

    }


    const menuButton =
        document.querySelector(

            ".mobile-menu-button, " +

            "#mobileMenuButton"

        );


    if (!menuButton) {

        return;

    }


    menuButton.addEventListener(

        "click",

        function() {

            sidebar.classList.toggle(
                "sidebar-open"
            );

        }

    );


    document
        .querySelectorAll(
            ".nav-link"
        )
        .forEach(

            function(link) {

                link.addEventListener(

                    "click",

                    function() {

                        sidebar.classList.remove(
                            "sidebar-open"
                        );

                    }

                );

            }

        );

}


/* ================================================================
   66. KEYBOARD SHORTCUTS
================================================================ */

function initializeKeyboardShortcuts() {

    document.addEventListener(

        "keydown",

        function(event) {

            if (
                event.key ===
                "Escape"
            ) {

                document
                    .activeElement
                    ?.blur();

            }


            if (
                event.key ===
                "1"
            ) {

                scrollToSection(
                    "energy-overview"
                );

            }


            if (
                event.key ===
                "2"
            ) {

                scrollToSection(
                    "maintenance-decisions"
                );

            }


            if (
                event.key ===
                "3"
            ) {

                scrollToSection(
                    "occupancy-overview"
                );

            }


            if (
                event.key ===
                "4"
            ) {

                scrollToSection(
                    "security-overview"
                );

            }


            if (
                event.key ===
                "5"
            ) {

                scrollToSection(
                    "cost-overview"
                );

            }

        }

    );

}


function scrollToSection(id) {

    const element =
        getElement(id);


    if (!element) {

        return;

    }


    element.scrollIntoView({

        behavior:
            "smooth",

        block:
            "start"

    });

}


/* ================================================================
   67. FLOATING PARTICLES
================================================================ */

function initializeParticles() {

    const container =
        document.querySelector(
            ".particles"
        );


    if (!container) {

        return;

    }


    for (
        let i = 0;
        i < 35;
        i++
    ) {

        const particle =
            document.createElement(
                "span"
            );


        particle.className =
            "js-particle";


        particle.style.left =
            (
                Math.random() *
                100
            ) + "%";


        particle.style.top =
            (
                Math.random() *
                100
            ) + "%";


        particle.style.animationDelay =
            (
                Math.random() *
                8
            ) + "s";


        particle.style.animationDuration =
            (
                5 +
                Math.random() *
                8
            ) + "s";


        container.appendChild(
            particle
        );

    }

}


/* ================================================================
   68. TILT EFFECT
================================================================ */

function initializeTiltEffect() {

    const cards =
        document.querySelectorAll(
            ".tilt-card"
        );


    cards.forEach(

        function(card) {

            card.addEventListener(

                "mousemove",

                function(event) {

                    const rect =
                        this.getBoundingClientRect();


                    const x =
                        event.clientX -
                        rect.left;


                    const y =
                        event.clientY -
                        rect.top;


                    const centerX =
                        rect.width /
                        2;


                    const centerY =
                        rect.height /
                        2;


                    const rotateX =
                        (
                            y -
                            centerY
                        ) /
                        18;


                    const rotateY =
                        (
                            centerX -
                            x
                        ) /
                        18;


                    this.style.transform =

                        "perspective(900px) " +

                        "rotateX(" +
                        rotateX +
                        "deg) " +

                        "rotateY(" +
                        rotateY +
                        "deg) " +

                        "translateY(-4px)";

                }

            );


            card.addEventListener(

                "mouseleave",

                function() {

                    this.style.transform =
                        "";

                }

            );

        }

    );

}


/* ================================================================
   69. SECTION LOADING ANIMATION
================================================================ */

function initializeSectionLoading() {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    sections.forEach(

        function(section, index) {

            section.style.setProperty(
                "--section-delay",
                (
                    index *
                    60
                ) + "ms"
            );

        }

    );

}


/* ================================================================
   70. DASHBOARD INITIALIZATION
================================================================ */

function initializeDashboard() {

    if (
        dashboardInitialized
    ) {

        return;

    }


    dashboardInitialized =
        true;


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

    initializeRippleEffect();

    initializeMouseGlow();

    initializeScrollProgress();

    initializeParticles();

    initializeTiltEffect();

    initializeSectionLoading();

    updateCostBuildingCards();

    updateCostCharts();

    animateVisibleCounters();


    console.log(
        "Dashboard initialized successfully."
    );

}


/* ================================================================
   71. DOM READY
================================================================ */

document.addEventListener(

    "DOMContentLoaded",

    function() {

        console.log(
            "Smart Facility Intelligence loading..."
        );


        initializeLogin();

    }

);


/* ================================================================
   72. CONSOLE SYSTEM STATUS
================================================================ */

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
    "%c Security Agent: ONLINE ",
    "color:#ff5870;font-weight:bold"
);


console.log(
    "%c Cost Optimization Agent: ONLINE ",
    "color:#ffb44d;font-weight:bold"
);


console.log(
    "%c Facility Intelligence Engine: ACTIVE ",
    "color:#4197ff;font-weight:bold"
);


/* ================================================================
   END OF SMART FACILITY INTELLIGENCE JAVASCRIPT
================================================================ */