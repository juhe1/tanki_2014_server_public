class LightingEffect:
    def __init__(self):
        self.name = ""
        self.records = []


class LightingEffectRecord:
    attenuation_begin = 0.0
    attenuation_end = 0.0
    color = ""
    intensity = 0.0
    time = 0
