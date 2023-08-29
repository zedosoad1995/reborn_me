export const parsePercentile = (perc: number) => {
  let newPerc = perc * 100;
  let prefix = "Bottom";

  if (newPerc >= 50) {
    newPerc = 100 - newPerc;
    prefix = "Top";
  }

  const fixed = Math.max(Math.ceil(-Math.log10(newPerc)), 1);

  return `${prefix} ${newPerc.toFixed(fixed)}%`;
};
