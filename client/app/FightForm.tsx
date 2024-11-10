import React, { useState } from "react";
import PredictButton from "./PredictButton";
import Select from "./Select";

export default function FightForm() {
  const [firstFighter, setFirstFighter] = useState<any>();
  const [secondFighter, setSecondFighter] = useState<any>();
  const [prediction, setPrediction] = useState(null);
  const [firstFighterName, setFirstFighterName] = useState<any>();
  const [secondFighterName, setSecondFighterName] = useState<any>();

  const handlePredict = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    //console.log(firstFighter);
    //console.log(secondFighter);

    if (!firstFighter || !secondFighter) return;

    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fighter1: firstFighter,
        fighter2: secondFighter,
      }),
    });

    const data = await response.json();
    setFirstFighterName(data.fighterOneName);
    setSecondFighterName(data.fighterTwoName);
    setPrediction(data.prediction);
  };

  return (
    <>
      <form onSubmit={handlePredict}>
        <div className="flex  w-[100%]">
          <Select onChange={setFirstFighter} className="w-[100%]" />
          <Select onChange={setSecondFighter} />
        </div>
        <PredictButton />
      </form>
      <div className="text-xl text-center p-3">
        {prediction !== null && prediction == "1" && (
          <h2>
            Prediction: <b>{firstFighterName} </b>has a better chance of winning
            than <b>{secondFighterName}</b>.
          </h2>
        )}
        {prediction !== null && prediction == "0" && (
          <h2>
            Prediction: <b>{secondFighterName}</b> has a better chance of
            winning than <b>{firstFighterName}</b>.
          </h2>
        )}
      </div>
    </>
  );
}
