import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { BRAND, FONTS } from "./tokens.js";
import { SafeArea } from "./SafeArea.jsx";

export const DropFixture = ({ texts, captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const activeCaptions = captions.filter((c) => t >= c.startS && t < c.endS);
  const persistent = texts.filter((x) => x.persistent);
  const nonPersistent = texts.filter((x) => !x.persistent);

  return (
    <AbsoluteFill style={{ backgroundColor: BRAND.navy }}>
      <SafeArea>
        <div style={{ position: "absolute", top: 80, left: 0, right: 0 }}>
          {nonPersistent.map((x) => (
            <div
              key={x.id}
              data-text-id={x.id}
              style={{
                color: BRAND.paper,
                fontFamily: FONTS.display,
                fontSize: 56,
                textAlign: "center",
                opacity: t < 5 ? 1 : 0.35,
              }}
            >
              {x.text}
            </div>
          ))}
          {activeCaptions.map((c) => (
            <div
              key={c.id}
              data-text-id={c.id}
              style={{
                color: BRAND.cream,
                fontFamily: FONTS.ui,
                fontSize: 44,
                textAlign: "center",
                marginTop: 40,
              }}
            >
              {c.text}
            </div>
          ))}
        </div>
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0 }}>
          {persistent.map((x) => (
            <div
              key={x.id}
              data-text-id={x.id}
              style={{
                color: BRAND.cream,
                fontFamily: FONTS.ui,
                fontSize: 27,
                textAlign: "center",
                backgroundColor: "rgba(8,26,45,0.72)",
                padding: "12px 16px",
                opacity: t >= 0.0 ? 1 : 0,
              }}
            >
              {x.text}
            </div>
          ))}
        </div>
      </SafeArea>
    </AbsoluteFill>
  );
};
