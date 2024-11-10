"use client";
import React, { useState } from "react";
import AsyncSelect from "react-select/async";
import { getAllFighters } from "./data";
//import Select from "./Select";
import PredictButton from "./PredictButton";
import FightForm from "./FightForm";
import { bebas, lato, oswald, quicksand, inter } from "./fonts";

export default function Prediction() {
  return (
    <div>
      <h1
        className={`${bebas.className} antialiased text-center pt-10 text-8xl`}
      >
        MMA Fight Predictor
      </h1>
      <div className={`${lato.className} antialiased flex flex-col `}>
        <div className="justify-center">
          <FightForm />
        </div>
      </div>
    </div>
  );
}
