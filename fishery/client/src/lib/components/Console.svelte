<script lang="ts">
    export let logs: Array<string> = [];
</script>
<section>
    <div class="console">
        <div class="console-header">
            <h3>Console</h3>
        </div>
        <div class="console-content">
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
    padding-left: 15px;
    }

    .console-content{
    height: 100%;
    overflow-y: scroll;
    }

    .console-content ul{
    list-style: none;
    padding: 0;
    margin: 0;
    height: 10vh;
    }

    .console-content li{
    padding: 5px 15px;
    }

    .console-content li:nth-child(odd){
    background-color: #333;
    }

</style>