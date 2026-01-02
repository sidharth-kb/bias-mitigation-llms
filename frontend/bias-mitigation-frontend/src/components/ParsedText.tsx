import type { ParsedTextProps } from "./interfaces";
import { BiasType } from "./interfaces";
import { BiasSection } from "./BiasSection"

export const ParsedText: React.FC<ParsedTextProps> = ({ text, metadata}) => {
  const regex = /<id:(\d+) (gender|age|race)>(.*?)<\/\2>/g;

  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {

    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }

    const id = parseInt(match[1])
    let type: BiasType;

    switch (match[2]) {
      case "age":
        type = BiasType.Age
        break
      case "gender":
        type = BiasType.Gender
        break
      case "race":
        type = BiasType.Race
        break;
      default:
        type = BiasType.Error;
        console.error("Invalid bias type!!")
    }

    const content = match[3];

    const meta = metadata.find((m) => m.section_id === id)

    if (!meta) {
      throw new Error(`No metadata found for section ID ${id}`); // enforce required context
    }

    parts.push(<BiasSection key={id} type={type} context={meta.context}>{content}</BiasSection>);

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return <p>{parts}</p>;
};

