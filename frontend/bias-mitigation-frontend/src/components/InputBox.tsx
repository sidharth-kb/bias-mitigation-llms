import type React from "react"

type InputBoxProps = {
  setText: React.Dispatch<React.SetStateAction<string>>
  setContextSize: React.Dispatch<React.SetStateAction<number>>
}

export function InputBox( { setText, setContextSize } : InputBoxProps) {

  const handleForm = (formData: FormData) => {
    const userText = formData.get("user_text")
    if (typeof userText == "string") {
      setText(userText)
    }
    const contextSize = formData.get("context_size")

    if (typeof contextSize == "number")
      setContextSize(contextSize)
  }

  return (
    <section id="inputSection">
      <form action={handleForm}>
        <textarea name="user_text" placeholder="Write your input here"/>
        <input type="range" min="3" max="20" name="context_size" defaultValue={3}/>
        <button type="submit">Submit</button>
      </form>
    </section>
  )
}
