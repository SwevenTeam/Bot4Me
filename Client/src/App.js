import './App.css';
import Home from './components/Home';
import {IconContext} from "react-icons"

function App() {
  return (
    <IconContext.Provider value={{color: "white",size:"2em",padding:"0.5em"}} >
      <div className="App">
        <header className="App-header">
          <Home/>
        </header>
      </div>
    </IconContext.Provider>
  );
}

export default App;