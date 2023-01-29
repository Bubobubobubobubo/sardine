<script lang="ts">

	import { tick } from "svelte";

    export let logs: Array<string> = [];
    export let autoScroll: boolean = true;
    let consoleView: HTMLDivElement;


    const scrollToTheBottomOfTheConsole = () => {
        if(!autoScroll) return;
        if(!consoleView) return;
        // console.log("scrolling to the bottom of the console")
        consoleView.scrollTop = consoleView.scrollHeight;
    }

    // watch for changes in the logs array and scroll to the bottom of the console
    $:{logs; tick().then(() => {scrollToTheBottomOfTheConsole();})}

</script>
<section>
    <div class="console">
        <div class="console-header">
            <h3>Logs</h3>
        </div>
        <div class="console-content" bind:this={consoleView}>
            <ul>
                {#each logs as log }
                    <li>{log}</li>
                {/each}
            </ul>
        </div>
    </div>
</section>
<style>
    
    .console{
        color: white;
        border-top: dashed white 1px;
    }

    .console-header{
        display: flex;
        align-items: center;
    }

    h3 {
        font-size: 14px;
        padding-left: 15px;
    }

    .console-content{
        font-size: 12px;
        height: 100%;
        overflow-y: scroll;
    }

    .console-content ul{
        font-size: 12px;
        list-style: none;
        padding: 0;
        margin: 0;
        height: 10vh;
    }

    .console-content li{
        font-size: 12px;
        padding: 0px 15px;
    }

    /*.console-content li:nth-child(odd){
        background-color: #333;
    }
    */


</style>
