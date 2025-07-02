import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [rectangles, setRectangles] = useState([])
  const [newWidth, setNewWidth] = useState('')
  const [newHeight, setNewHeight] = useState('')
  const [newQuantity, setNewQuantity] = useState('')

  const handleAddRectangle = () => {
    const width = parseFloat(newWidth);
    const height = parseFloat(newHeight);
    const quantity = parseInt(newQuantity);

    if (!width || !height || !quantity || quantity <= 0 || width <= 0 || height <= 0) {
      alert("Please enter valid dimensions and quantity.");
      return;
    }

    const newRectangle = {
      id: Date.now(),
      width: width,
      height: height,
      quantity: quantity
    };

    setRectangles([...rectangles, newRectangle]);
    setNewWidth('');
    setNewHeight('');
    setNewQuantity('');
  };

  const handleDeleteRectangle = (id) => {
    setRectangles(rectangles.filter(rect => rect.id !== id));
  };

  return (
    <div className="app">
      <div className="column layout-preview">
        <div className="card">
          <h2>Layout Preview</h2>
          {/* Placeholder for layout preview component */}
        </div>
      </div>

      <div className="column settings">
        <div className="card">
          <h2>Settings</h2>
          <label>
            Print Width (cm)
            <select>
              <option value="155">155 cm</option>
              <option value="185">185 cm</option>
              <option value="custom">Custom</option>
            </select>
          </label>

          <label>
            Price per square meter
            <input type="number" placeholder="5.00 €/m²" />
          </label>

          <button>Optimize Layout</button>
        </div>
      </div>

      <div className="column rectangles">
        <div className="card">
          <h2>Rectangles</h2>
          {/* Placeholder for rectangle list component */}
          <div className="rectangle-list">
            <input type="number" placeholder="Width" value={newWidth} onChange={(e) => setNewWidth(e.target.value)}/>
            <input type="number" placeholder="Height" value={newHeight} onChange={(e) => setNewHeight(e.target.value)}/>
            <input type="number" placeholder="Quantity" value={newQuantity} onChange={(e) => setNewQuantity(e.target.value)}/>
          </div>
          <button className="add-btn" onClick={handleAddRectangle}>+ Add Rectangle</button>
          <div className="rectangle-list-rendered">
            {rectangles.map((rect) => (
            <div key={rect.id} className="rectangle-card">
              <div className="rectangle-icon">
                <i className="fas fa-square-full"></i>
              </div>
              <div className="rectangle-info">
                <span>{rect.width} × {rect.height} cm</span>
                <span>Quantiy: {rect.quantity}</span>
              </div>
              <button className="remove-btn" onClick={() => handleDeleteRectangle(rect.id)}>
                <i className="fas fa-trash"></i>
              </button>
            </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
