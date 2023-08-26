import { useEffect, useState } from "react";
import { getRandomCountry } from "./Util/randomBirth";

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

    if (random < 0.47) {
      return "Male";
    } else if (random < 0.94) {
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
        <div className="text-3xl mb-2">You will be reborn in</div>
        <div className="text-2xl text-[#ed143d] min-h-[32px] font-bold">{country}</div>
        <div className="min-h-[24px]">
          You had a {rate} chance (Rarity: {rarity})
        </div>
        <div className="min-h-[24px] mt-2">
          Gender: <span className="font-bold">{gender}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
