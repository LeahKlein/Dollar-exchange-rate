export const calculateForecastAverage = (data) => {
    const forecast = [];
    const length = data.length;

    for (let i = 0; i < length; i++) {
        if (i < 3) {
            // 3 התאים הראשונים יהיו כמו במטריצה המקורית
            forecast.push({ date: data[i].date, rate: data[i].rate });
        } else {
            // חישוב ממוצע של 3 התאים הקודמים
            const averageRate = (data[i - 1].rate + data[i - 2].rate + data[i - 3].rate) / 3;
            forecast.push({ date: data[i].date, rate: averageRate });
        }
    }

    return forecast;
};

export const calculateDifferences = (actualRates, forecastRates) => {
    const differences = [];

    // בדוק אם יש מספיק נתונים בשתי המטריצות
    const length = Math.min(actualRates.length, forecastRates.length);

    for (let i = 0; i < length; i++) {
        const actualRate = actualRates[i].rate;
        const forecastRate = forecastRates[i].rate;
        const difference = actualRate - forecastRate; // חישוב ההפרש
        differences.push({ date: actualRates[i].date, difference });
    }

    return differences;
};

export const calculateAverageDifferences = (differences) => {
    const averageDifferences = [];

    for (let i = 0; i < differences.length; i++) {
        // הוסף את ההפרשים המקוריים
        averageDifferences.push(differences[i]);

        // בכל שלושה חודשים, חשב ממוצע והוסף שורה חדשה
        if (i > 1 && (i + 1) % 3 === 0) {
            const avgDifference = (differences[i].difference + differences[i - 1].difference + differences[i - 2].difference) / 3;
            averageDifferences.push({ date: `Average ${differences[i].date}`, difference: avgDifference });
        }
    }
    
    return averageDifferences;
};

export const multiplyMatrices = (matrixB, matrixC) => {
    const result = [];
  
    // בדוק אם אפשר להכפיל את המטריצות
    if (matrixB[0].length !== matrixC.length) {
        throw new Error('Number of columns in the first matrix must equal the number of rows in the second matrix.');
    }
  
    for (let i = 0; i < matrixB.length; i++) {
        result[i] = [];
        for (let j = 0; j < matrixC[0].length; j++) {
            result[i][j] = 0; // אתחול של תא תוצאה
            for (let k = 0; k < matrixB[0].length; k++) {
                result[i][j] += matrixB[i][k] * matrixC[k][j];
            }
        }
    }
  
    return result;
};
