import { useEffect, useState } from "react"
import type { BiasMetadata } from "./interfaces"
import { ParsedText } from "./ParsedText"

export function OutputBox({ text, contextSize }: {text: string, contextSize: number}) {

  const [result, setResult] = useState<string>("")
  const [metaData, setMetaData] = useState<BiasMetadata[]>([])

  useEffect(() => {
    if (text !== "") {
      fetch(`/api/tag-text?context_size=${contextSize}`, {
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
