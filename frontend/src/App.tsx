import { useEffect, useState } from "react";
import { getRandomCountry } from "./Util/randomBirth";
import { getRandomWealth } from "./Util/randomWealth";
import { parsePercentile } from "./Util/parse";

const GENDERS = [
  "Acault",
  "AFAB",
  "Agender",
  "Aliagender",
  "Alyha And Hwame",
  "AMAB",
  "Androgynous",
  "Aporagender",
  "Aravani",
  "Ashtime",
  "Burrnesha",
  "Bakla",
  "Bigender",
  "Calabai",
  "Chuckchi Ne’uchika Shamans",
  "Demiboy",
  "Demigender",
  "Demigirl",
  "Fa’afafine",
  "Fakaleiti",
  "Femme",
  "Femminiello",
  "Guevedoche",
  "Femminiello",
  "FTM",
  "Gender Apathetic",
  "Gender Fluid",
  "Gender Neutral",
  "Gender Nonconforming",
  "Gender Questioning",
  "Gender Variant",
  "Genderqueer",
  "Hermaphrodite",
  "Hijra",
  "Intergender",
  "Intersex",
  "Kathoey",
  "Lhamana",
  "Mahu",
  "Maverique",
  "Metis",
  "MTF",
  "Muxe",
  "Neither",
  "Neutrois",
  "Ninauposkitzipxpe",
  "Nadleehi And Dilbaa",
  "Non-Binary",
  "Novigender",
  "Paṇḍaka",
  "Pangender",
  "Polygender",
  "Quariwarmi",
  "Sekrata",
  "Sistergirl And Brotherboy",
  "Third Gender",
  "Tom And Dee Identities",
  "Transmasculine",
  "Transfeminine",
  "Trigender",
  "Two-Spirit",
  "Two-Spirit Female",
  "Two-Spirit Male",
  "Waria",
  "Whakawahine",
  "Winkte",
  "Xanith",
];
function App() {
  const [gender, _] = useState<string>(() => {
    const random = Math.random();

    if (random < 0.475) {
      return "Male";
    } else if (random < 0.95) {
      return "Female";
    } else if (random < 0.99) {
      return ["Trans Man", "Trans Woman"][Math.floor(Math.random() * 2)];
    } else {
      return GENDERS[Math.floor(Math.random() * GENDERS.length)];
    }
  });
  const [country, setCountry] = useState<string>();
  const [rate, setRate] = useState<string>();
  const [rarity, setRarity] = useState<string>();
  const [wealth, setWealth] = useState<string>();
  const [wealthPerc, setWealthPerc] = useState<string>();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getRandomCountry().then(({ country, rate, rarity }) => {
      getRandomWealth(country).then(({ wealth, perc }) => {
        setWealth("$" + Math.round(wealth).toLocaleString());
        setWealthPerc(parsePercentile(perc));
        setIsLoading(false);
      });

      setCountry(country);
      setRarity(rarity);
      setRate((rate * 100).toPrecision(2) + "%");
    });
  }, []);

  return (
    <div className="h-full p-6">
      <div className="h-full flex items-center justify-center flex-col">
        <div className="text-3xl mb-2 text-center">You will be reborn in</div>
        {isLoading && <div className="h-[176px]"></div>}
        {!isLoading && (
          <>
            <div className="text-2xl text-[#ed143d] min-h-[32px] font-bold text-center">
              {country}
            </div>
            <div className="min-h-[24px] text-center mt-2">
              You had a {rate} chance (Rarity: {rarity})
            </div>
            <div className="mt-6 w-full bg-[#ffffff20] py-4 px-4 max-w-[500px]">
              <div className="min-h-[24px]">
                <span className="font-bold">Wealth:</span> {wealth} ({wealthPerc})
              </div>
              <div className="min-h-[24px] mt-2">
                <span className="font-bold">Gender:</span> {gender}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
