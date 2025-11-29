import { useState } from 'react'
import { InputBox } from './components/InputBox'
import { OutputBox } from './components/OutputBox'
import './App.css'

function App() {
  const [text, setText] = useState<string>("")

  return (
    <section id="main">
      <InputBox setText={setText} />
      <OutputBox text={text} />
    </section>
  )
}

export default App
