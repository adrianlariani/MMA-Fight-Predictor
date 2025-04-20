import { getFighterByID } from "@/app/data";

export async function POST(req: Request) {
  const data = await req.json();
  const fighter1 = data.fighter1;
  const fighter2 = data.fighter2;

  console.log(fighter1);
  console.log(fighter2);

  const fighters = [fighter1, fighter2];

  const response = await fetch(
    "https://mma-fight-predictor.onrender.com/predict",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ fighters: fighters }),
    }
  );

  const jsonResponse = await response.json();
  console.log(jsonResponse);
  console.log("Prediction: " + jsonResponse.prediction);

  const obj = {
    prediction: jsonResponse.prediction,
    fighterOneName: fighter1.label,
    fighterTwoName: fighter2.label,
  };

  const blob = new Blob([JSON.stringify(obj, null, 2)], {
    type: "application/json",
  });

  return new Response(blob, {
    status: 200,
  });
}
