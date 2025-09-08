import "./Board.css";
import DataGraph from "./DataGraph"; // ודא שהנתיב נכון
import DataTable from "./DataTable"; // ודא שהנתיב נכון

export default function Board({data , isGraph}) {
    return (
      <div className="Board">
          {isGraph ? <DataGraph data={data} /> : <DataTable data={data} />}
      </div>
    );
  }
