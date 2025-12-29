import { useEffect, useState } from "react"

async function rewriteSection(context: string, text: string, setSection: React.Dispatch<React.SetStateAction<string>>) {
  try{
    const res = await fetch("http://127.0.0.1:8080/remove-section-bias",{
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        section: {
          context: context,
          text: text
        },
        mode: true
      })
    })
    const data = await res.json();
    setSection(data.neutralised_text);
  } catch(err) {
    console.error(err)
  }
}

interface BiasProps {
  context: string;
  children: string;
}

export const Gender: React.FC<BiasProps> = ({ context , children }) => (
  <span
    style={{ backgroundColor: "pink", padding: "0 2px", borderRadius: "2px" }}
    title="Gender Bias"
  >
    {children}
  </span>
);

export const Age: React.FC<BiasProps> = ({ context, children }) => (
  <span
    style={{ backgroundColor: "lightblue", padding: "0 2px", borderRadius: "2px" }}
    title="Age Bias"
  >
    {children}
  </span>
);

function Race({ context, children }: BiasProps){

  const [section, setSection] = useState<string>(children)

  return (
    <span
      onClick={() => rewriteSection(context, children, setSection)}
      style={{ backgroundColor: "lightgreen", padding: "0 2px", borderRadius: "2px" }}
      title="Race Bias"
    >
      {section}
    </span>
  )
}

interface BiasMetadata {
  section_id: number,
  text: string,
  context: string
}

interface ParsedTextProps {
  text: string;
  metadata: BiasMetadata[];
}


const ParsedText: React.FC<ParsedTextProps> = ({ text, metadata}) => {
  const regex = /<id:(\d+) (gender|age|race)>(.*?)<\/\2>/g;

  const componentsMap: Record<string, React.FC<BiasProps>> = {
    gender: Gender,
    age: Age,
    race: Race,
  };

  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    // Text before the biased section
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }

    const id = parseInt(match[1])
    const type = match[2]; // gender, age, race
    const content = match[3]; // text content

    const meta = metadata.find((m) => m.section_id === id)

    if (!meta) {
      throw new Error(`No metadata found for section ID ${id}`); // enforce required context
    }

    const Component = componentsMap[type];
    parts.push(<Component key={id} context={meta.context}>{content}</Component>);

    lastIndex = regex.lastIndex;
  }

  // Remaining text
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return <p>{parts}</p>;
};

export function OutputBox({ text, contextSize }: {text: string, contextSize: number}) {

  const [result, setResult] = useState<string>("")
  const [metaData, setMetaData] = useState<BiasMetadata[]>([])

  useEffect(() => {
    if (text !== "") {
      fetch(`http://127.0.0.1:8080/tag-text?context_size=${contextSize}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: text
        })
      })
      .then(res => res.json())
      .then(data => {
        setMetaData(data.parsed_text)
        setResult(data.tagged_text)
      })
      .catch(err => console.error(err))
    }
  }, [text])

  return (
    <section id="outputSection">
    <h2>Output:</h2>
    {result != "" && <ParsedText text={result} metadata={metaData}/>}
    </section>
  )
}
