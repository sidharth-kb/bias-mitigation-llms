import type React from "react"

type InputBoxProps = {
  setText: React.Dispatch<React.SetStateAction<string>>
}

export function InputBox( { setText } : InputBoxProps) {

  const handleForm = (formData: FormData) => {
    const userText = formData.get("user_text")
    if (typeof userText == "string") {
      setText(userText)
    }
  }

  return (
    <section id="inputSection">
      <form action={handleForm}>
        <textarea name="user_text" placeholder="Write your input here"/>
        <button type="submit">Submit</button>
      </form>
    </section>
  )
}
