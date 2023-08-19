import React from "react";


type Props = {
    handleNext: any;
  };

  function Next({ handleNext }: Props) {
    return (
        <button className = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
        onClick = {handleNext}>Next Level</button>
    );
  }

export default Next;