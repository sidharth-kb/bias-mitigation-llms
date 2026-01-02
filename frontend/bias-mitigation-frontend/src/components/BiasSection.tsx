import { useState } from "react"
import type { BiasProps } from "./interfaces";

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


export function BiasSection({ context, children, type }: BiasProps){

  const [section, setSection] = useState<string>(children)
  const [isRewritten, setRewritten] = useState<boolean>(false)

  return (
    <span
      onClick={
        !isRewritten ? () => {
          rewriteSection(context, children, setSection)
          setRewritten(true)
        } : undefined}
        style={{
          backgroundColor: isRewritten ? "transparent" : type, // original color for background
          lineHeight: "1.7",
          padding: "0 2px",
          paddingBlock: "1px 3px",
          borderRadius: "4px",
          cursor: isRewritten ? "default" : "pointer",
          textDecoration: !isRewritten ? "underline" : "none",
          textDecorationColor: type.replace(/(\d+)%\)$/, "70%)"), // lighten the underline to 70%
          textDecorationThickness: "3px",
          textUnderlineOffset: "4px",
          transition: "background-color 0.2s ease, text-decoration-color 0.2s ease"
        }}
    >
      {section}
    </span>
  )
}
