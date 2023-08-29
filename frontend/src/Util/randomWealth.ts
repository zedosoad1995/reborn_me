import Papa from "papaparse";
import quantile from "@stdlib/stats-base-dists-lognormal-quantile";

async function parseWealthParams(country: string): Promise<number[]> {
  return new Promise((resolve, reject) => {
    fetch("/wealth_params_simple.csv")
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

            const row = (results.data as string[][]).find((row) => row[0] === country);

            if (!row) {
              return reject();
            }

            resolve(row.slice(1).map(parseFloat));
          },
        });
      });
  });
}

async function parseParetoRatio(country: string): Promise<number> {
  return new Promise((resolve, reject) => {
    fetch("/1perc_ration.csv")
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

            const row = (results.data as string[][]).find((row) => row[0] === country);

            if (!row) {
              return reject();
            }

            resolve(parseFloat(row[1]));
          },
        });
      });
  });
}

function inversePareto(perc: number, a: number, b: number) {
  return a * (Math.pow(1 - perc, -1 / b) - 1);
}

export const getRandomWealth = async (country: string) => {
  const countryParams = await parseWealthParams(country);
  const ratio = await parseParetoRatio(country);

  const random = Math.random();

  if (random > 0.99) {
    return {
      wealth: inversePareto(random, 2.97457774e5, 1.45807092) * ratio,
      perc: random,
    };
  }

  return {
    wealth: quantile(random, countryParams[0], countryParams[1]),
    perc: random,
  };
};
