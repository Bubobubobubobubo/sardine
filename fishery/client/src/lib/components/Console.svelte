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
    }
</style>