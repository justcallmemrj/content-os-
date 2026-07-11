import React from "react";
import { SAFE } from "./tokens.js";

export const SafeArea = ({ children }) => {
  return (
    <div
      style={{
        position: "absolute",
        top: SAFE.safeTop,
        bottom: SAFE.safeBottom,
        left: SAFE.safeX,
        right: SAFE.safeX,
      }}
    >
      {children}
    </div>
  );
};
