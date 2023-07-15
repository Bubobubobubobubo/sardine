import debounce from 'lodash.debounce';

export class RunnerService{

    port: number;
    host: string;
    // eventSource: EventSource;

    constructor(port: number) {
        this.port = port;
        this.host = `http://localhost:${this.port}`;
        // this.eventSource = new EventSource(`${this.host}/logs`);
        // this.eventSource.onerror = () => {
        //     this.eventSource.close();
        // };
    }

    async executeCode(code:string) {
        const data = {
            code: code + "\n\r",
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


    // watchLogs(onLogs: (data: string) => void): (data: string) => void {

    //   const debounceDelay = 100;
    //   let logBuffer: string[] = [];

    //   const debouncedOnLogs = debounce(() => {
    //       onLogs(logBuffer.join('\n\r'));
    //       logBuffer = [];
    //   }, debounceDelay);

    //   const onMessage = (event: MessageEvent) => {
    //     logBuffer.push(event.data);
    //     debouncedOnLogs();
    //   };

    //   this.eventSource.onmessage = onMessage;
    //   this.eventSource.onerror = (err) => {
    //     console.error(err);
    //   };

    //   return () => {
    //     this.eventSource.close();
    //     this.eventSource.onmessage = null;
    //   };
    // }
}