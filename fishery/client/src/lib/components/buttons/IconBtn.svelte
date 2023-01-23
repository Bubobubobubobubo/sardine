<script lang='ts'>
    import Fa from 'svelte-fa';
    import { 
        faPlay, faStop, faFloppyDisk, 
        faUserGroup, type IconDefinition  
    } from '@fortawesome/free-solid-svg-icons';
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    // Initialisation of props and events
    export let icon: string = "";

    function sendEvent(): void {
        dispatch('pressed', {
            text: 'event!'
        });
    };

    interface Dictionary<T> {
        [Key: string]: T;
    }

    // Map icon names to FontAwesome glyphs
    const icons: Dictionary<IconDefinition> = {
        play: faPlay, stop: faStop,
        save: faFloppyDisk, users: faUserGroup
    };

</script>

<section>
    <button>
        <Fa 
        class="" icon={icons[icon]} 
        on:click={sendEvent} />
    </button>
</section>
<style>
    button {
        background: none;
        color: white;
        font-size: 1.5rem;
        border: none;
    }
    button:hover {
        transform: scale(1.1);
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
</style>