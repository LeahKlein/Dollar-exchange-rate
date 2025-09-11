import React from 'react';
import "./SortButton.css";

export default function DisplayMatButton({ onClick, resultMatrix }) {
    return (
        <div>
            <button className="displayMatButton" onClick={onClick}>
                Display Matrix
            </button>
            {resultMatrix.length > 0 && (
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Product</th>
                        </tr>
                    </thead>
                    <tbody>
                        {resultMatrix.map((item, index) => (
                            <tr key={index}>
                                <td>{item.date}</td>
                                <td>{item.product}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}