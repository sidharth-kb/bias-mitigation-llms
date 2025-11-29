import { useEffect, useState } from "react"

export function OutputBox({ text }: {text: string}) {

  const [result, setResult] = useState<string | boolean>(false)

  useEffect(() => {
    if (text !== "") {
      fetch("http://127.0.0.1:8080/remove-bias", {
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
        if (data.result) {
          setResult(data.result)
        } else {
          setResult("something went wrong!")
        }
      })
      .catch(err => console.error(err))
    }
  }, [text])

  return (
    <section id="outputSection">
    <h2>Output:</h2>
    {result && <p>{result}</p>}
    </section>
  )
}
