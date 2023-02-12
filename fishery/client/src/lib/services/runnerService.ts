class RunnerService{

    host: string;

    constructor() {
        this.host = "";
    }

    async executeCode(code:string) {
        const data = {
            code: code,
        }
        const response = await fetch( this.host + '/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        return result;
    }

    watchLogs(onLogs: (data: string) => void): () => void {
        // Create a new EventSource to receive server
        // sent events from the server.
        const eventSource = new EventSource(this.host + '/log');

        // The event listener that will be called when a message is received.
        const onMessage = (event: MessageEvent) => {
            onLogs(event.data);
        };

        // Register the handler for the message event.
        eventSource.onmessage = onMessage;

        // Return a function that will be called when
        // the client no longer wants to receive events.
        return () => {
            // Close the connection.
            eventSource.close();
            // Remove the event listener.
            eventSource.onmessage = null;
        };
    }

}

const runnerService = new RunnerService();
export default runnerService;
