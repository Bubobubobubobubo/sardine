<script lang="ts">
	import { tick } from "svelte";
    export let logs: Array<string> = [];
    export let autoScroll: boolean = true;
    let consoleView: HTMLDivElement;

    const scrollToTheBottomOfTheConsole = () => {
        if(!autoScroll) return;
        if(!consoleView) return;
        consoleView.scrollTop = consoleView.scrollHeight;
    }

    // watch for changes in the logs array and scroll to the bottom of the console
    $:{logs; tick().then(() => {scrollToTheBottomOfTheConsole();})}
</script>

<div class="console">
    <div class="console-content" bind:this={consoleView}>
        <ul>
            {#each logs as log }
                <li>{log}</li>
            {/each}
        </ul>
    </div>
</div>
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
        margin-left: 15px;
        padding: 4px;
        cursor: pointer;
    }
    h3:hover {
        color: black;
        background-color: white;
        transition: all 0.2s ease-in-out;
    }
    h3.active {
        color: black;
        background-color: white;
    }

    .console-content{
        font-size: 12px;
        height: 10vh;
        overflow-y: scroll;
    }

    .console-content ul{
        font-size: 12px;
        list-style: none;
        padding: 0;
        margin: 0;
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
