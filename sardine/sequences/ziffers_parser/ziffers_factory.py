import uuid

try:
    from ziffers import z
    from ziffers.classes import Sample, SampleList, Rest, Chord
except ImportError:
    print("Install the ziffers package for using Ziffers patterns")


def get_ziffers_params(orig: dict) -> dict:
    """Parses and pops ziffers parameters from kwargs"""
    params = ["key", "scale", "synth"]
    new_dict = {}
    for key in list(orig.keys()):
        if len(key) == 1 and key.isupper() or key in params:
            new_dict[key] = orig.pop(key)
    return new_dict


def _play_ziffers(D, N, sleep, ziffer: str, *args, **kwargs):
    """Parse ziffers notation and play using D OR N"""
    zparams = get_ziffers_params(kwargs)
    pat = z(ziffer, **zparams)
    instrument = zparams.get("synth", "superpiano")
    for cur in pat.evaluated_values:
        if isinstance(cur, Sample):
            D(cur.name, *args, **kwargs)
        elif isinstance(cur, SampleList):
            joined_samples = f"{{{' '.join([sample.name for sample in cur.values])}}}"
            D(joined_samples, *args, **kwargs)
        elif isinstance(cur, Chord):
            joined_chord = f"{{{' '.join([str(pitch.freq) for pitch in cur.pitch_classes])}}}"
            print(joined_chord)
            D(instrument, freq=joined_chord, *args, **kwargs)
        elif "channel" in kwargs:
            N(cur.note, *args, **kwargs)
        elif not isinstance(cur, Rest):
            D(instrument, midinote=cur.note, *args, **kwargs)
        sleep(cur.beat)


def create_zplay(D, N, sleep, swim, polyphonic=False):
    """Builder for zplay function"""

    def _zplay_creator(ziffer: str, *args, **kwargs):
        """Play ziffers in a swim"""

        def zplay():
            _play_ziffers(D, N, sleep, ziffer, *args, **kwargs)

        fun = zplay
        if polyphonic:
            fun.__name__ = f"ziffers_{uuid.uuid4().hex}"
        swim(fun)

    return _zplay_creator
