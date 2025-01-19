const FIREBASE_DOMAIN = process.env.REACT_APP_API_URL || "http://localhost:5000";

export async function getAllIssuers() {
    const response = await fetch(`${FIREBASE_DOMAIN}/issuers_data`,
    );
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch Issuers.");
    }
    const transformedData = [];
    for (const key in data) {
        transformedData.push({
            value: data[key],
            label: data[key],
        });
    }
    return transformedData;
}

export async function getMostLiquid() {
    const response = await fetch(`${FIREBASE_DOMAIN}/mostLiquid`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch Issuers.");
    }
    const transformedData = [];
    for (const key in data) {
        transformedData.push(data[key]);
    }
    return transformedData;
}

export async function getCertainIssuer(requestData) {
    var params = null;
    var response = null;
    const {selectedStock, startDate, endDate} = requestData;

    // Check if startDate and endDate are not empty strings or undefined
    if (startDate && endDate && startDate !== "" && endDate !== "") {
        params = `?startDate=${startDate}&endDate=${endDate}`;
        response = await fetch(
            `${FIREBASE_DOMAIN}/issuers_data/${selectedStock}${params}`
        );
    } else {
        response = await fetch(`${FIREBASE_DOMAIN}/issuers_data/${selectedStock}`);
    }

    // Log to verify startDate and endDate
    // console.log("Start Date:", startDate);
    // console.log("End Date:", endDate);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch.");
    }

    const transformedData = [];
    for (const key in data) {
        transformedData.push(data[key]);
    }

    return transformedData;
}

export async function getTechnical(requestData) {
    var response = null;
    const {selectedStock, days} = requestData;

    // Check if startDate and endDate are not empty strings or undefined
    response = await fetch(
        `${FIREBASE_DOMAIN}/issuers_data/${selectedStock}/technical?days=${days}`)

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch.");
    }


    return data;
}

export async function getPrediction(selectedStock) {
    var response = null;

    // Check if startDate and endDate are not empty strings or undefined
    response = await fetch(
        `${FIREBASE_DOMAIN}/issuers_data/${selectedStock}/predict`
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch.");
    }

    return data;
}

export async function getFundamental(selectedStock) {
    var response = null;

    // Check if startDate and endDate are not empty strings or undefined
    response = await fetch(
        `${FIREBASE_DOMAIN}/issuers_data/${selectedStock}/fundamental`
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Could not fetch.");
    }

    return data;
}
