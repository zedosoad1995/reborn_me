import Papa from "papaparse";

async function parseBirthData(): Promise<[string, number][]> {
  return new Promise((resolve, reject) => {
    fetch("/country_birth_rates.csv")
      .then((response) => response.text())
      .then((data) => {
        Papa.parse(data, {
          complete: function (results) {
            if (!Array.isArray(results.data)) {
              return reject();
            }

            if (!Array.isArray(results.data[0])) {
              return reject();
            }

            const retData = (results.data as [string, string])
              .slice(1)
              .map(([country, num]) => [country, Number(num)]) as [string, number][];

            resolve(retData);
          },
        });
      });
  });
}

function rateToHumanReadable(rate: number) {
  let base = 100;
  while (Math.round(rate * base) < 10 && base <= 1e15) {
    base *= 10;
  }

  if (Math.round(rate * base) % 10 === 0) {
    return `${Math.round(rate * base) / 10} in ${base / 10}`;
  }

  return `${Math.round(rate * base)} in ${base}`;
}

export const getRandomCountry = async () => {
  const data = await parseBirthData();
  const totalBirths = data.reduce((acc, [_, num]) => {
    return acc + num;
  }, 0);

  let rate: number = 0;
  let randomCountry = "";
  let random = Math.random() * totalBirths;
  for (let i = 0; i < data.length; i++) {
    random -= data[i][1];
    if (random < 0) {
      rate = data[i][1] / totalBirths;
      randomCountry = data[i][0];
      break;
    }
  }

  return {
    country: randomCountry,
    rateHuman: rateToHumanReadable(rate),
    rate,
    rarity: getRarity(randomCountry, data),
  };
};

export const getRarity = (targetCountry: string, data: [string, number][]) => {
  const RARITIES = [
    "Common",
    "Uncommon",
    "Rare",
    "Very Rate",
    "Legendary",
    "Mystic",
    "Impossible",
    "God",
    "Gige God",
    "𓂝𓅓𓏏𓆑 𓏏𓋴 𓇌 𓅱𓏏𓅭",
  ];

  const totalBirths = data.reduce((acc, [_, num]) => {
    return acc + num;
  }, 0);
  let cnt = totalBirths;

  const lossRate = 0.2;
  let level = 1;
  for (const [country, num] of data) {
    cnt -= num;

    if (country === targetCountry) {
      return RARITIES[level - 1];
    }

    if (cnt / totalBirths < Math.pow(1 / lossRate, -level)) {
      level += 1;
    }
  }

  return RARITIES.at(-1);
};
