import uuid

try:
    from ziffers import z
    from ziffers.classes import Sample
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
        elif "channel" in kwargs:
            N(cur.note, *args, **kwargs)
        else:
            D(instrument, midinote=cur.note, *args, **kwargs)
        sleep(cur.beat)


def create_zplay(D, N, sleep, swim, polyphonic=False):
    """Builder for zplay function"""

    def _zplay(ziffer: str, *args, **kwargs):
        """Play ziffers in a swim"""

        def dynamic_function():
            _play_ziffers(D, N, sleep, ziffer, *args, **kwargs)

        fun = dynamic_function
        if polyphonic:
            fun.__name__ = f"ziffers_{uuid.uuid4().hex}"
        swim(fun)

    return _zplay
