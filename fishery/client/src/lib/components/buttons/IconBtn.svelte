<script>
    import Fa from 'svelte-fa'
    import { faPlay, faStop, faFloppyDisk, faUserGroup  } from '@fortawesome/free-solid-svg-icons'

    export let icon = "";

    // map icon names to FontAwesome icons
    const icons = {
        play: faPlay,
        stop: faStop,
        save: faFloppyDisk,
        users: faUserGroup
    }

</script>
<section>
    <button>
        <Fa class="" icon={icons[icon]} />
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