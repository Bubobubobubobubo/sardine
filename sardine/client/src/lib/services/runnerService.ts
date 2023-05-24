import debounce from 'lodash.debounce';

class RunnerService{

    host: string;

    constructor() {
        this.host = "http://localhost:8000";
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


    watchLogs(onLogs: (data: string[]) => void): () => void {
      const eventSource = new EventSource(this.host + "/log");
      const debounceDelay = 100;
      let logBuffer: string[] = [];

      const debouncedOnLogs = debounce(() => {
          onLogs(logBuffer.join('\n'));
          logBuffer = [];
      }, debounceDelay);

      const onMessage = (event: MessageEvent) => {
        logBuffer.push(event.data);
        debouncedOnLogs();
      };

      eventSource.onmessage = onMessage;

      return () => {
        eventSource.close();
        eventSource.onmessage = null;
      };
    }
}

const runnerService = new RunnerService();
export default runnerService;
