import { getFighterByID } from "@/app/data";

export async function POST(req: Request) {
  const data = await req.json();
  const fighter1 = data.fighter1;
  const fighter2 = data.fighter2;

  console.log(fighter1);
  console.log(fighter2);

  const fighterOneStats = await getFighterByID(fighter1.value);
  const fighterTwoStats = await getFighterByID(fighter2.value);

  const stance_to_id: { [key: string]: number } = {
    Orthodox: 0,
    Southpaw: 1,
    Switch: 2,
    "Open Stance": 3,
  };
  console.log(fighterOneStats);
  console.log(fighterTwoStats);

  const weight_diff = fighterOneStats!.weight?.sub(fighterTwoStats!.weight!);
  const height_diff = fighterOneStats!.height?.sub(fighterTwoStats!.height!);
  const reach_diff = fighterOneStats!.reach?.sub(fighterTwoStats!.reach!);
  const r_stance = stance_to_id[fighterOneStats?.stance!];
  const b_stance = stance_to_id[fighterTwoStats?.stance!];
  const slpm_total_diff = fighterOneStats!.slpm?.sub(fighterTwoStats!.slpm!);
  const sig_str_acc_total_diff = fighterOneStats!.str_acc?.sub(
    fighterTwoStats!.str_acc!
  );
  const sapm_total_diff = fighterOneStats!.sapm?.sub(fighterTwoStats!.sapm!);
  const str_def_total_diff = fighterOneStats!.str_def?.sub(
    fighterTwoStats!.str_def!
  );
  const td_avg_total_diff = fighterOneStats!.td_avg?.sub(
    fighterTwoStats!.td_avg!
  );
  const td_acc_total_diff = fighterOneStats!.td_acc?.sub(
    fighterTwoStats!.td_acc!
  );
  const td_def_total_diff = fighterOneStats!.td_def?.sub(
    fighterTwoStats!.td_def!
  );
  const sub_avg_diff = fighterOneStats!.sub_avg?.sub(fighterTwoStats!.sub_avg!);

  const features = [
    weight_diff,
    height_diff,
    reach_diff,
    r_stance,
    b_stance,
    slpm_total_diff,
    sig_str_acc_total_diff,
    sapm_total_diff,
    str_def_total_diff,
    td_avg_total_diff,
    td_acc_total_diff,
    td_def_total_diff,
    sub_avg_diff,
  ];

  const response = await fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ features: features }),
  });

  const jsonResponse = await response.json();
  console.log(jsonResponse);
  console.log("Prediction: " + jsonResponse.prediction);
  const obj = {
    prediction: jsonResponse.prediction,
    fighterOneName: fighterOneStats?.name,
    fighterTwoName: fighterTwoStats?.name,
  };

  const blob = new Blob([JSON.stringify(obj, null, 2)], {
    type: "application/json",
  });

  return new Response(blob, {
    status: 200,
  });
}
