import "./SortButton.css";

export default function SortButton({ onClick }) {
    return (
      <button className = "sortButton" onClick = { onClick }>
        Sort
      </button>
    );
  }