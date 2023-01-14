

export async function executeCode(code) {
    const data = {
        code: code,
    }
    const response = await fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    return result;



}
