import React from "react";
import { Composition } from "remotion";
import { DropFixture } from "./DropFixture.jsx";

// Top-level fields: `--props=props.json` overrides input props at the TOP level,
// so the component contract must match gen_props.py's output shape exactly —
// a nested wrapper silently falls back to defaults (defect caught at step 9
// by frame inspection: exit-0 render of the empty fallback).
const FALLBACK = { spec: { fps: 30, durationS: 10 }, texts: [], captions: [], scenes: [] };

export const Root = () => {
  return (
    <Composition
      id="DropFixture"
      component={DropFixture}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={FALLBACK}
    />
  );
};
