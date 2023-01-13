

export async function executeCode(code) {
    const data = {
        code: code,
    }
    const response = await fetch('http://localhost:5000/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    return result;



}
