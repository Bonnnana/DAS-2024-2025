const FIREBASE_DOMAIN = "http://127.0.0.1:5000/";

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

export async function getCertainIssuer(Issuer) {
  const response = await fetch(`${FIREBASE_DOMAIN}/issuers_data/${Issuer}`);
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



