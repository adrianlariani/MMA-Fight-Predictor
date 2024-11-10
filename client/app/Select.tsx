import AsyncSelect from "react-select/async";
import { getFighterByID, getFighterImageByID, mapFightersNames } from "./data";
import Image from "next/image";
import { useState } from "react";
const SelectFighter = ({ onChange }: any) => {
  const [selectedFighter, setSelectedFighter] = useState<string>();

  const promiseOptions = async (input: string) => {
    return await mapFightersNames(input);
  };

  const handleChange = async (selectedOption: any) => {
    const fighter = await getFighterImageByID(selectedOption.value);
    setSelectedFighter(fighter!);
    onChange(selectedOption);
  };

  return (
    <div className="w-[100%] flex flex-col flex-wrap justify-center items-center  p-[2%]">
      <AsyncSelect
        id={Date.now().toString()}
        cacheOptions
        defaultOptions
        loadOptions={promiseOptions}
        onChange={handleChange}
        className="w-[100%]"
      />
      <div className="p-1 w-[100%] flex flex-col flex-wrap justify-center items-center ">
        {!selectedFighter && (
          <div className="border-4 border-black relative md:w-[70%] w-[100%] md:h-[600px] h-[320px]">
            <Image
              fill
              src={
                "https://answers-embed-client.ufc.com.pagescdn.com/static/assets/images/UFC-Male-Fallback-Image.jpg"
              }
              alt={
                "https://answers-embed-client.ufc.com.pagescdn.com/static/assets/images/UFC-Male-Fallback-Image.jpg"
              }
              style={{ objectFit: "cover", objectPosition: "top" }}
            />
          </div>
        )}
        {selectedFighter && (
          <div className="border-4 border-black relative md:w-[70%] w-[100%] md:h-[600px] h-[320px]">
            <Image
              fill
              src={selectedFighter}
              alt={selectedFighter}
              style={{ objectFit: "cover", objectPosition: "top" }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default SelectFighter;
