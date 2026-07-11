import React from "react";

// counterexample: text element outside any <SafeArea>
export const Bad = ({ data }) => {
  return (
    <div>
      {data.texts.map((x) => (
        <div key={x.id} data-text-id={x.id}>
          {x.text}
        </div>
      ))}
    </div>
  );
};
