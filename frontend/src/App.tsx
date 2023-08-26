import { useEffect, useState } from "react";
import { getRandomCountry } from "./Util/randomBirth";

function App() {
  const [country, setCountry] = useState<string>();
  const [rate, setRate] = useState<string>();
  const [rarity, setRarity] = useState<string>();

  useEffect(() => {
    getRandomCountry().then(({ country, rate, rarity }) => {
      setCountry(country);
      setRarity(rarity);
      setRate((rate * 100).toPrecision(2) + "%");
    });
  }, []);

  return (
    <div className="h-full p-6">
      <div className="h-full flex items-center justify-center flex-col">
        <div className="text-3xl mb-6">You will be reborn in</div>
        <div className="text-2xl text-[#1D75F3] min-h-[32px] font-bold">{country}</div>
        <div className="min-h-[24px]">You had a {rate} chance</div>
        <div className="min-h-[24px]">
          Rarity: <span className="font-bold">{rarity}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
