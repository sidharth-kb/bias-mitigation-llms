import { useState } from 'react'
import { InputBox } from './components/InputBox'
import { OutputBox } from './components/OutputBox'
import './App.css'

function App() {
  const [text, setText] = useState<string>("")
  const [contextSize, setContextSize] = useState<number>(2)

  return (
    <section id="main">
      <InputBox setText={setText} setContextSize={setContextSize}/>
      <OutputBox text={text} contextSize={contextSize}/>
    </section>
  )
}

export default App
