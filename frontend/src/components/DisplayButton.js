import "./DisplayButton.css";

export default function DisplayButton({ onClick }) {
    return (
      <button className = "displayButton" onClick={onClick}>
        Display
      </button>
    );
  }