export const BiasType = {
  Age: "hsl(224deg, 96%, 95%)",
  Gender: "hsl(54deg, 96%, 90%)",
  Race: "hsl(283deg, 96%, 95%)",
  Error: "hsl(360deg, 96%, 90%)"
} as const;

export type BiasType = typeof BiasType[keyof typeof BiasType]

export interface BiasProps {
  context: string;
  children: string;
  type: BiasType;
}

export interface BiasMetadata {
  section_id: number,
  text: string,
  context: string
}

export interface ParsedTextProps {
  text: string;
  metadata: BiasMetadata[];
}
