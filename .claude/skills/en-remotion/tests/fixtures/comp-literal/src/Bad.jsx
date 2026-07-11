import React from "react";
import { SafeArea } from "./SafeArea.jsx";

// counterexample: retyped words in JSX — the "props are populated from the
// storyboard file, not retyped" rule violated
export const Bad = ({ data }) => {
  return (
    <SafeArea>
      <div data-text-id="CAP-01">Your DROP payout comes as one check.</div>
    </SafeArea>
  );
};
